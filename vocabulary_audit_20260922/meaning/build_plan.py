from pathlib import Path
from collections import defaultdict,Counter
import json,sys
B=Path(__file__).resolve().parent;P=B.parent
sys.path.insert(0,str(P))
from exact_audit import load,esc

def main():
 old=json.loads((B/'baseline_findings.json').read_text());new=json.loads((P/'final_findings.json').read_text())
 key=lambda x:(x['pack'],x['overall'],x['word'])
 before={key(x):x for x in old};after={key(x):x for x in new}
 removed=[before[k] for k in sorted(before.keys()-after.keys())];added=[after[k] for k in sorted(after.keys()-before.keys())]
 grouped=defaultdict(list)
 for x in new:grouped[(x['pack'],x['overall'])].append(x)
 decks,_=load();plans=[]
 for (pack,overall),xs in sorted(grouped.items()):
  di,row=divmod(overall-1,500);d=decks[pack][di];c=d['cards'][row]
  en,ru=('qMdFootnote','aMdFootnote') if pack=='english_russian' else ('aMdFootnote','qMdFootnote')
  plans.append(dict(pack=pack,packId=21917816 if pack=='english_russian' else 21919521,deckId=int(d['file'][5:-4]),cardId=c['cardId'],overall=overall,row=row+1,english_target=c['qMdBody' if pack=='english_russian' else 'aMdBody'],russian_target=c['aMdBody' if pack=='english_russian' else 'qMdBody'],current_english_example=c[en],current_russian_example=c[ru],findings=xs,proposed_actions=['Replace the English example with an allowed, natural sentence preserving the target sense.','Update the Russian example to match the replacement English sentence.','Regenerate the English target + 500 ms pause + full replacement sentence recording.'],audio_side='question' if pack=='english_russian' else 'answer',status='identified_only_no_replacement_written'))
 (B/'update_plan.json').write_text(json.dumps(plans,ensure_ascii=False,indent=2)+'\n')
 (B/'resolved_findings.json').write_text(json.dumps(removed,ensure_ascii=False,indent=2)+'\n')
 (B/'new_findings.json').write_text(json.dumps(added,ensure_ascii=False,indent=2)+'\n')
 lines=['# Meaning-aware re-audit','', 'The English → Russian timeline remains the shared source. All 16 approved exemptions are active. No card text or audio has been changed.', '', '| Pack | Before meaning corrections | Remaining | Cards cleared | Newly flagged cards |','|---|---:|---:|---:|---:|']
 for p in ['english_russian','russian_english']:
  a={x['overall'] for x in old if x['pack']==p};z={x['overall'] for x in new if x['pack']==p}
  lines.append(f"| {p} | {len(a)} | {len(z)} | {len(a-z)} | {len(z-a)} |")
 lines+=['',f'{len(removed)} word/card flags were removed and {len(added)} added. Cards with another remaining issue still count as needing attention.', '', '## Reviewed changes', '',
 '- 421 occurrences across 19 ambiguous forms were reviewed against English and Russian reference targets and example sentences. 361 received explicit sense resolutions; the others keep the conservative original check.',
 '- saw = past of see is not reserved by saw = пила/пилить; fell = past of fall is not reserved by fell = валить; possessive mine is not reserved by mine = мина.',
 '- managed = succeeded is distinct from being controlled; entered a room is distinct from entering data; brought/delivered is distinct from brought up/raised; calling for help is distinct from a vocation.',
 '- found = discovered still has its own later entry at #1,650. The earlier #1,363 found = основать cannot unlock it. This reveals five more English → Russian cards in 1501–2000.',
 '- A moving sermon is emotionally touching, not physical motion or a driving force. English → Russian #9,971 is newly flagged for this sense.',
 '- bought remains reserved by to be bought. Active/passive grammar alone is not a separate lexical meaning. Forbidden remains reserved at #6,169.',
 '- Remaining cases are conservative candidates, not a claim of complete automatic semantic understanding. For example, played brilliantly is underspecified, so the acting/music distinction is not silently guessed.',
 '', '## Work inventory','',f'{len(plans)} existing cards are listed in [update_plan.json](update_plan.json), with IDs, current English/Russian sentences, offending forms, and audio side. Each needs a replacement English example, its matching Russian translation, and an English recording if the sentence changes. Targets and card order are to be preserved.',
 '', '[Current full report](../REPORT.md) · [Cleared flags](resolved_findings.json) · [New flags](new_findings.json) · [Reviewed contexts](sense_reviews.json)', '', '## Why flags were cleared', '', '| Word | Removed word/card flags |','|---|---:|']
 for w,n in Counter(x['word'] for x in removed).most_common():lines.append(f'| {w} | {n} |')
 (B/'COMPARISON.md').write_text('\n'.join(lines)+'\n')
 print('Plan cards:',len(plans),'removed flags:',len(removed),'new flags:',len(added))
if __name__=='__main__':main()
