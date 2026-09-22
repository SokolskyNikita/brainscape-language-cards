"""Exact-form audit. Reads saved cards only; never modifies or uploads decks."""
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime, timezone
import sys, json, re, hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from brainscape import cards_from_path
BASE=Path(__file__).resolve().parent

def tokens(s):
    s=s.lower().replace('’', "'").replace('‘', "'").replace('‐','-').replace('‑','-')
    return re.findall(r"[a-zà-öø-ÿ]+(?:['-][a-zà-öø-ÿ]+)*",s)

def head_tokens(s):
    # Parentheses contain explanatory labels, not target vocabulary.
    return tokens(re.sub(r'\([^)]*\)','',s))

def load():
    out={};manifest=[]
    for pack in ['english_russian','russian_english']:
        out[pack]=[]
        mapping=re.findall(r'\| `(deck_\d+\.csv)` \| ([^|]+) \|',(ROOT/pack/'file_to_deck.md').read_text())
        assert len(mapping)==20
        for di,(filename,band) in enumerate(mapping):
            assert int(band.strip().split('->')[0])==(1 if di==0 else di*500)
            local=ROOT/pack/filename;live=BASE/'live'/pack/(local.stem[5:]+'.json')
            source=live if live.exists() else local
            cards=json.loads(live.read_text()) if live.exists() else cards_from_path(local)
            assert len(cards)==500
            out[pack].append(dict(file=filename,band=band.strip(),cards=cards,source=str(source.relative_to(ROOT))))
            manifest.append(dict(pack=pack,deck=filename[5:-4],cards=len(cards),source=str(source.relative_to(ROOT)),sha256=hashlib.sha256(source.read_bytes()).hexdigest()))
    return out,manifest

def main():
    decks,manifest=load();index={};findings=[];deck_results=[]
    for di,d in enumerate(decks['english_russian']):
        for row,c in enumerate(d['cards'],1):
            ref=dict(deck=d['file'][5:-4],deck_index=di,band=d['band'],row=row,overall=di*500+row,head=c['qMdBody'])
            for t in sorted(set(head_tokens(c['qMdBody']))):index.setdefault(t,ref)
    for pack,ds in decks.items():
        key,ex=('qMdBody','qMdFootnote') if pack=='english_russian' else ('aMdBody','aMdFootnote')
        for di,d in enumerate(ds):
            subset=[]
            for row,c in enumerate(d['cards'],1):
                target=set(head_tokens(c[key]));example_tokens=Counter(tokens(c.get(ex,'')))
                for t,count in sorted(example_tokens.items()):
                    if t in target:continue
                    earliest=index.get(t)
                    if earliest and earliest['deck_index']<=max(0,di-1):continue
                    f=dict(pack=pack,deck=d['file'][5:-4],band=d['band'],row=row,overall=di*500+row,head=c[key],example=c.get(ex,''),word=t,occurrences=count,reason='absent' if not earliest else ('same_deck' if earliest['deck_index']==di else 'later_deck'),earliest=earliest)
                    subset.append(f);findings.append(f)
            deck_results.append(dict(pack=pack,deck=d['file'][5:-4],band=d['band'],total_cards=500,flagged_cards=len({x['overall'] for x in subset}),word_card_pairs=len(subset),word_occurrences=sum(x['occurrences'] for x in subset)))
    summary={}
    for pack in decks:
        xs=[x for x in findings if x['pack']==pack]
        summary[pack]=dict(total_cards=10000,flagged_cards=len({x['overall'] for x in xs}),word_card_pairs=len(xs),word_occurrences=sum(x['occurrences'] for x in xs),unique_word_forms=len({x['word'] for x in xs}),reasons=dict(Counter(x['reason'] for x in xs)),most_common=Counter(x['word'] for x in xs).most_common(25))
    assert any(x['pack']=='russian_english' and x['overall']==2140 and x['word']=='forbidden' and x['earliest']['overall']==6169 for x in findings)
    for name,obj in [('exact_summary',summary),('exact_findings',findings),('exact_decks',deck_results),('english_inventory',index),('source_manifest',dict(audited_at=datetime.now(timezone.utc).isoformat(),decks=manifest))]:
        (BASE/f'{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    write_report(summary,deck_results,findings,manifest)
    print(json.dumps(summary,indent=2))

def esc(s):return str(s).replace('|','\\|').replace('\n',' ')

def write_report(summary,decks,findings,manifest):
    names={'english_russian':'English → Russian','russian_english':'Russian → English'}
    lines=['# English-example vocabulary audit — 22 September 2026','',
           '**Final rule: the English → Russian pack supplies the vocabulary timeline for both packs; exact forms everywhere, including the current target.**','',
           '| Pack | Cards audited | Cards with violations | Percentage | Offending word/card pairs |',
           '|---|---:|---:|---:|---:|']
    for pack,s in summary.items():lines.append(f"| {names[pack]} | 10,000 | {s['flagged_cards']:,} | {s['flagged_cards']/100:.2f}% | {s['word_card_pairs']:,} |")
    total=sum(x['flagged_cards'] for x in summary.values())
    lines.extend(['',f'**Total: {total:,} of 20,000 cards ({total/200:.2f}%) contain at least one unallowed English word form.**',
        '', 'A card is counted once even if it has several offending words. Word/card pairs count each distinct offending spelling once per card; `occurrences` in the JSON also records repetitions.',
        '', '## Rule and scope', '',
        '- Only English example text is audited: the question example in English → Russian and the answer example in Russian → English.',
        '- For deck 1, supporting words may appear anywhere in English → Russian cards 1–500. For deck 2, only those same 500 cards are allowed; for deck 3, cards 1–1000; and so on.',
        '- The current card’s English target is allowed in its exact form, including explicitly listed English alternatives. Russian words never supply an English vocabulary allowance.',
        '- No stemming, lemmatization, inflection, synonym, function-word, or basic-grammar exemptions. `work` does not permit `works` or `worked`; `be` does not permit `is`; `forbid` does not permit `forbidden`.',
        '- Case and curly/straight apostrophe or hyphen typography are normalized. Contractions, internal possessives, and hyphenated compounds remain whole surface tokens: `I’m` → `i\'m`, not `i` + `am`. Numbers and punctuation are not vocabulary tokens.',
        '- The reference inventory comes from English target/gloss text only, not examples. English tokens in multiword targets and explicitly listed alternatives count as introduced; parenthetical explanations are excluded. A token in a phrase is credited regardless of sense, so this checks word-form sequencing, not all idiomatic or semantic prerequisites.',
        '- “Absent” means the exact form is absent from the entire English → Russian target inventory. Many ordinary inflections fall into this category and therefore never become allowed under this rule unless taught explicitly.',
        '', '## Your mom’s example', '',
        'Russian → English **#2,140**, deck 2000→2500, card 140: **strictly** — “It’s strictly forbidden.”',
        '', '**forbidden** is not introduced until English → Russian **#6,169**, deck 6000→6500. At #2,140, only the first 2,000 English → Russian cards are available as supporting vocabulary. This is a violation. Under exact surface-form matching, `it’s` is separately flagged because it is absent as an English → Russian target token.',
        '', '## Common offending forms', '', '| Form | English → Russian cards | Russian → English cards |', '|---|---:|---:|'])
    counts={p:Counter(x['word'] for x in findings if x['pack']==p) for p in names}
    common=sum(counts.values(),Counter()).most_common(15)
    for word,n in common:lines.append(f"| {esc(word)} | {counts['english_russian'][word]:,} | {counts['russian_english'][word]:,} |")
    lines.extend(['','## Per-deck counts','','| Card band | English → Russian | Russian → English |','|---|---:|---:|'])
    for i in range(20):lines.append(f"| {i*500+1:,}–{(i+1)*500:,} | {decks[i]['flagged_cards']:,} | {decks[20+i]['flagged_cards']:,} |")
    live=sum('/live/' in x['source'] for x in manifest)
    lines.extend(['','## Evidence and reproduction','',f'Sources: {live}/40 decks read from saved live API snapshots; {40-live}/40 from local CSVs. See [source fingerprints](source_manifest.json) and [live/local comparison](manifest.json). No deck content was changed.',
        '', '- [Every English → Russian flagged card](english_russian_findings.md)', '- [Every Russian → English flagged card](russian_english_findings.md)',
        '- [Full structured findings](exact_findings.json)', '- [Summary counts](exact_summary.json)', '- [English reference inventory with first positions](english_inventory.json)',
        '', 'Reproduce from the project directory: `python3 vocabulary_audit_20260922/exact_audit.py`. Earlier exploratory audit files reflect superseded interpretations and are not the final result.'])
    (BASE/'REPORT.md').write_text('\n'.join(lines)+'\n')
    for pack in names:
        grouped=defaultdict(list)
        for x in findings:
            if x['pack']==pack:grouped[x['overall']].append(x)
        detail=[f'# {names[pack]} — exact-form violations','', '[Audit rules and summary](REPORT.md)','', '| Overall # | Deck card # | Target | English example | Unallowed forms → first English → Russian target position |','|---:|---:|---|---|---|']
        for overall,xs in grouped.items():
            x=xs[0];bad=[]
            for f in xs:
                e=f['earliest'];loc='absent' if not e else f"#{e['overall']:,} ({e['head']}; {f['reason'].replace('_',' ')})"
                bad.append(f"{f['word']} → {loc}")
            detail.append(f"| {overall:,} | {x['row']} | {esc(x['head'])} | {esc(x['example'])} | {esc('; '.join(bad))} |")
        (BASE/f'{pack}_findings.md').write_text('\n'.join(detail)+'\n')
if __name__=='__main__':main()
