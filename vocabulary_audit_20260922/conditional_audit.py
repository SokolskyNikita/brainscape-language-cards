"""Final rule: shared English timeline; scheduled forms win, otherwise inflect known words."""
from pathlib import Path
from collections import defaultdict,Counter
import sys,json,hashlib
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact_audit import ROOT,BASE,load,tokens,head_tokens,esc
from audit import forms,GRAMMAR,tokens as expanded_tokens
EXEMPT=set(json.loads((BASE/"exempt_forms.json").read_text()))

def main(*, sense_reviews=None, output_base=None, report_writer=None):
    output_base=output_base or BASE
    if sense_reviews is None:
        reviews_path=BASE/'meaning'/'sense_reviews.json'
        reviews=json.loads(reviews_path.read_text()) if reviews_path.exists() else []
        sense_reviews={(x['pack'],x['overall'],x['word']):x for x in reviews}
    semantic_review_count=len(sense_reviews)
    semantic_decisions=[]
    decks,manifest=load();exact={};morph=defaultdict(list);findings=[];deck_results=[];decisions=Counter();reference_by_position={}
    if sense_reviews:
        expected=json.loads((BASE/'meaning'/'reference_fingerprint.json').read_text())
        heads=[[c['qMdBody'],c['aMdBody']] for d in decks['english_russian'] for c in d['cards']]
        fingerprint=hashlib.sha256(json.dumps(heads,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()
        assert fingerprint==expected['headword_pairs_sha256'],'Reference vocabulary changed; refresh semantic review before rerunning'

    for di,d in enumerate(decks['english_russian']):
        for row,c in enumerate(d['cards'],1):
            ref=dict(deck=d['file'][5:-4],deck_index=di,band=d['band'],row=row,overall=di*500+row,head=c['qMdBody'])
            reference_by_position[ref['overall']]=dict(ref,russian=c['aMdBody'],example=c['qMdFootnote'])
            for t in sorted(set(head_tokens(c['qMdBody']))):
                exact.setdefault(t,ref)
                for f in forms(t):morph[f].append(dict(ref,head_token=t))
    for pack,ds in decks.items():
        key,ex=('qMdBody','qMdFootnote') if pack=='english_russian' else ('aMdBody','aMdFootnote')
        for di,d in enumerate(ds):
            subset=[];limit=max(0,di-1)
            for row,c in enumerate(d['cards'],1):
                target=set(head_tokens(c[key]));target_forms=set().union(*(forms(t) for t in target))
                def check(t):
                    if t in EXEMPT:return None,'explicit_exemption'
                    if t in target:return None,'current_target'
                    review=sense_reviews.get((pack,di*500+row,t))
                    if review and review['action']=='resolve_sense':
                        assert review['head']==c[key] and review['example']==c[ex],f'Stale semantic review: {pack} {di*500+row} {t}'
                        matching=[reference_by_position[n] for n in review['exact_reference_positions']]
                        assert all(t in head_tokens(r['head']) for r in matching)
                        if matching:
                            earliest=min(matching,key=lambda r:r['overall'])
                            allowed=earliest['deck_index']<=limit
                            outcome=None if allowed else dict(word=t,reason='same_deck' if earliest['deck_index']==di else 'later_deck',earliest=earliest,matched_forms=[],sense=review['sense'],semantic_reason=review['reason'])
                        elif target & set(review['current_target_lemmas']):
                            earliest=None;allowed=True;outcome=None
                        else:
                            bases=[reference_by_position[n] for n in review['base_reference_positions']]
                            earliest=min(bases,key=lambda r:r['overall']) if bases else None
                            allowed=bool(earliest and earliest['deck_index']<=limit)
                            outcome=None if allowed else dict(word=t,reason='base_not_yet_allowed' if earliest else 'sense_not_taught',earliest=earliest,matched_forms=review['current_target_lemmas'],sense=review['sense'],semantic_reason=review['reason'])
                        semantic_decisions.append(dict(pack=pack,overall=di*500+row,word=t,sense=review['sense'],allowed=allowed,earliest=earliest,reason=review['reason']))
                        return outcome,'sense_allowed' if allowed else 'sense_blocked'
                    e=exact.get(t)
                    if e:
                        if e['deck_index']<=limit:return None,'exact_prior'
                        return dict(word=t,reason='same_deck' if e['deck_index']==di else 'later_deck',earliest=e,matched_forms=[]),'blocked_scheduled_form'
                    # Grammar contractions/possessives are decomposed only when the
                    # entire spelling is never explicitly taught in the reference.
                    components=expanded_tokens(t)
                    if len(components)>1:
                        missing=[]
                        for part in components:
                            result,_=check(part)
                            if result:missing.append(result)
                        return (dict(word=t,reason='component_not_allowed',earliest=None,matched_forms=[],components=missing) if missing else None),'expanded_expression'
                    if len(components)==1 and components[0]!=t:
                        result,_=check(components[0])
                        return (dict(word=t,reason='component_not_allowed',earliest=None,matched_forms=[],components=[result]) if result else None),'expanded_expression'
                    fs=forms(t)
                    if fs&target_forms:return None,'never_taught_target_inflection'
                    refs=[r for f in fs for r in morph.get(f,[])]
                    allowed=[r for r in refs if r['deck_index']<=limit]
                    if allowed:return None,'never_taught_prior_inflection'
                    earliest=min(refs,key=lambda x:x['overall']) if refs else None
                    return dict(word=t,reason='base_not_yet_allowed' if earliest else 'absent',earliest=earliest,matched_forms=sorted(fs)),'blocked_unintroduced_base'
                for t,n in sorted(Counter(tokens(c.get(ex,''))).items()):
                    bad,decision=check(t);decisions[(pack,decision)]+=1
                    if not bad:continue
                    f=dict(pack=pack,deck=d['file'][5:-4],band=d['band'],row=row,overall=di*500+row,head=c[key],example=c.get(ex,''),occurrences=n,**bad)
                    subset.append(f);findings.append(f)
            deck_results.append(dict(pack=pack,deck=d['file'][5:-4],band=d['band'],total_cards=500,flagged_cards=len({x['overall'] for x in subset}),word_card_pairs=len(subset)))
    summary={}
    for pack in decks:
        xs=[x for x in findings if x['pack']==pack]
        summary[pack]=dict(total_cards=10000,flagged_cards=len({x['overall'] for x in xs}),word_card_pairs=len(xs),word_occurrences=sum(x['occurrences'] for x in xs),unique_word_forms=len({x['word'] for x in xs}),reasons=dict(Counter(x['reason'] for x in xs)),most_common=Counter(x['word'] for x in xs).most_common(30),decisions={k[1]:v for k,v in decisions.items() if k[0]==pack})
    for name,obj in [('summary',summary),('findings',findings),('decks',deck_results),('english_inventory',exact),('source_manifest',manifest)]:
        (output_base/f'final_{name}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    if report_writer is not None:report_writer(summary,deck_results,findings,manifest,semantic_decisions)
    elif output_base==BASE:report(summary,deck_results,findings,manifest)
    (output_base/'semantic_decisions.json').write_text(json.dumps(semantic_decisions,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({p:{k:v for k,v in s.items() if k not in ('most_common','decisions')} for p,s in summary.items()},indent=2))
    return summary,deck_results,findings,manifest,semantic_decisions

def report(summary,deck_results,findings,manifest):
    names={'english_russian':'English → Russian','russian_english':'Russian → English'}
    lines=['# English-example sequencing audit — 22 September 2026','',
        '**Final rule: use the English → Russian vocabulary timeline for both packs. Inflections may inherit an allowed base only if that exact form is never explicitly taught in the same sense.**','',
        '| Pack | Cards audited | Cards with violations | Percentage | Offending word/card pairs |','|---|---:|---:|---:|---:|']
    for p,s in summary.items():lines.append(f"| {names[p]} | 10,000 | {s['flagged_cards']:,} | {s['flagged_cards']/100:.2f}% | {s['word_card_pairs']:,} |")
    total=sum(s['flagged_cards'] for s in summary.values())
    lines+=['',f'**Total: {total:,} cards out of 20,000 ({total/200:.2f}%).**','',
        'A card is counted once regardless of how many words violate the rule. Word/card pairs count distinct offending surface words once per card. Repeated occurrences are separately recorded in JSON.',
        '', '## Method', '',
        '- Only English examples are checked. Russian examples are excluded.',
        '- Reference vocabulary comes only from English → Russian English targets/glosses. Both packs use this same reference. Example sentences do not add vocabulary to the allow-list.',
        '- Deck 1 may use all English → Russian cards 1–500. Deck 2 may also use only cards 1–500; deck 3 may use 1–1000; and so on. Same-deck supporting vocabulary is forbidden after deck 1, even if its card occurs earlier within that deck.',
        '- The current card’s exact English target and its explicitly listed alternatives are allowed.',
        '- If an exact supporting form is taught in the same sense, its scheduled deck takes precedence: a previously learned base does not unlock it early. This also applies to inflected forms of the current target. Different homonyms do not reserve each other’s schedule.',
        '- If an exact form is never taught in the relevant sense, it is allowed when an inflectionally related English target has been introduced in an allowed deck, or is the current card’s target. Example: `worked` is never taught, so it can follow `work`. `forbidden` is explicitly taught at #6,169 and must wait.',
        '- Inflection matching uses NLTK WordNet forms, English pronoun/reflexive paradigms, common modal pairs, and the `an/a`, `disc/disk`, `towards/toward` variants. Derivational relatives and synonyms are not generally equated.',
        '- Case and apostrophe/hyphen typography are normalized. A contraction or possessive never explicitly taught is checked through its expanded/base words. A scheduled contraction must wait for its own deck. Hyphenated expressions never taught are checked through their components.',
        '- Explicit alternatives and constituent words of multiword glosses count as introduced; parenthetical explanatory labels do not. This is a lexical sequencing audit, not a full assessment of word senses or whether an idiom teaches its constituents.',
        '- Explicit exempt forms, allowed in every deck: '+', '.join('`'+t+'`' for t in sorted(EXEMPT))+'. Exemptions also apply to expanded contraction components, so exempting `not` removes a `didn’t` flag caused solely by `not`. No other blanket grammar exemption is applied.',
        '- Meaning corrections use 421 reviewed example contexts across 19 ambiguous forms, with explicit compatible reference lessons and base-word evidence. See [sense review decisions](meaning/sense_reviews.json). Context changes invalidate the reviewed correction instead of silently reusing it. This is a reviewed disambiguation layer, not general automatic word-sense understanding; other ambiguous cases remain conservatively flagged.',
        '- Same lexical meaning in active/passive forms still counts as taught: bought in to be bought remains reserved. Reading as an activity and reading a book are not treated as unrelated homonyms. No blanket inflection exemption was added.',
        '- See [changes from the previous audit](meaning/COMPARISON.md), [regression checks](meaning/test_regressions.py), and the [proposed update inventory](meaning/update_plan.json). No card text or audio has been changed.',
        '', '## Your mom’s example', '',
        'Russian → English **#2,140**, deck 2000→2500, card 140: **strictly** — “It’s strictly forbidden.”', '',
        '**forbidden** is introduced at English → Russian **#6,169**, deck 6000→6500. Only English → Russian cards 1–2000 are available as supporting vocabulary on this card. **This is a violation.** The exact form becomes available for supporting examples from the 6500→7000 deck onward.',
        '', '## Most frequent offending forms', '', '| Form | English → Russian cards | Russian → English cards |','|---|---:|---:|']
    cs={p:Counter(x['word'] for x in findings if x['pack']==p) for p in names}
    for w,n in sum(cs.values(),Counter()).most_common(20):lines.append(f"| {esc(w)} | {cs['english_russian'][w]:,} | {cs['russian_english'][w]:,} |")
    lines+=['','## Per-deck counts','','| Card band | English → Russian | Russian → English |','|---|---:|---:|']
    for i in range(20):lines.append(f"| {i*500+1:,}–{(i+1)*500:,} | {deck_results[i]['flagged_cards']:,} | {deck_results[20+i]['flagged_cards']:,} |")
    live=sum('/live/' in x['source'] for x in manifest)
    lines+=['','## Files and verification','',f'{live}/40 decks were audited from saved live snapshots. See [live/local comparison](manifest.json) and [source fingerprints](final_source_manifest.json). No card was changed.', '',
        '- [All English → Russian flagged cards](english_russian_findings.md)', '- [All Russian → English flagged cards](russian_english_findings.md)',
        '- [Full structured findings](final_findings.json)', '- [Summary counts](final_summary.json)', '- [English reference inventory](final_english_inventory.json)',
        '', 'Reproduce with `python3 vocabulary_audit_20260922/conditional_audit.py` from the project directory. Files prefixed `exact_` and earlier exploratory outputs reflect superseded rules; the final result is this report and `final_*.json`.']
    (BASE/'REPORT.md').write_text('\n'.join(lines)+'\n')
    for p,name in names.items():
        grouped=defaultdict(list)
        for x in findings:
            if x['pack']==p:grouped[x['overall']].append(x)
        detail=[f'# {name} — final sequencing violations','', '[Rules and summary](REPORT.md)','', '| Overall # | Deck card # | Target | English example | Unallowed forms and reference positions |','|---:|---:|---|---|---|']
        def describe(f):
            e=f.get('earliest')
            if f['reason']=='component_not_allowed':return f"{f['word']} → "+'; '.join(describe(c) for c in f['components'])
            loc='no matching taught form/base' if not e else f"#{e['overall']:,} ({e['head']}; {f['reason'].replace('_',' ')})"
            return f"{f['word']} → {loc}"
        for overall,xs in grouped.items():
            x=xs[0];detail.append(f"| {overall:,} | {x['row']} | {esc(x['head'])} | {esc(x['example'])} | {esc('; '.join(describe(f) for f in xs))} |")
        (BASE/f'{p}_findings.md').write_text('\n'.join(detail)+'\n')
if __name__=='__main__':main()
