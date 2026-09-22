from pathlib import Path
import json,re,sys
import pymorphy3
B=Path(__file__).resolve().parent
M=pymorphy3.MorphAnalyzer()
verbmap=dict(x.split(':') for x in '''bought:buy felt:feel opened:open lost:lose found:find asked:ask accepted:accept checked:check heard:hear told:tell said:say published:publish released:release understood:understand led:lead covered:cover played:play added:add displayed:display offered:offer brought:bring expressed:express named:name believed:believe dedicated:dedicate discussed:discuss built:build issued:issue studied:study killed:kill achieved:achieve disappointed:disappoint illuminated:illuminate attracted:attract lay:lie increased:increase mentioned:mention dressed:dress noted:note confirmed:confirm supported:support authorized:authorize welcomed:welcome exhausted:exhaust crumpled:crumple guarded:guard created:create installed:install forced:force decided:decide produced:produce placed:place allowed:allow intended:intend amazed:amaze caught:catch elected:elect spent:spend earned:earn paid:pay interrupted:interrupt opposed:oppose strengthened:strengthen saved:save carried:carry honored:honor'''.split())
plan=json.loads((B/'plan.json').read_text());out={}
for x in plan:
 ws=[f['word'] for f in x['findings']]
 if len(ws)!=1 or ws[0] not in verbmap:continue
 w=ws[0];en=x['current_english_example'];ru=x['current_russian_example']
 if re.search(r'\b(is|was|are|were|been|be|has|have|had|did|since)\b',en,re.I):continue
 if w=='felt' and not re.search('чувств|ощущ|был',ru,re.I):continue
 # Select exactly one past finite verb; leave passives/participles for manual edits.
 matches=[]
 for mm in re.finditer(r'[А-Яа-яЁё]+',ru):
  ps=[p for p in M.parse(mm.group()) if p.tag.POS=='VERB' and p.tag.tense=='past']
  if ps:matches.append((mm,max(ps,key=lambda p:p.score)))
 if len(matches)!=1:continue
 mm,p=matches[0];plural=p.tag.number=='plur'
 pre=en[:re.search(r'\b'+w+r'\b',en,re.I).start()]
 prs=re.findall(r'\b(I|we|you|he|she|it|they)\b',pre,re.I)
 subject=prs[-1].lower() if prs else ''
 person='1per' if subject in {'i','we'} else '2per' if subject=='you' else '3per'
 if p.tag.aspect=='perf':
  inf=p.inflect({'futr',person,'plur' if plural else 'sing'})
  if not inf:continue
  replacement=inf.word
 else:
  aux={('1per',False):'буду',('1per',True):'будем',('2per',False):'будешь',('2per',True):'будете',('3per',False):'будет',('3per',True):'будут'}[(person,plural)]
  replacement=aux+' '+p.normal_form
 if mm.group()[0].isupper():replacement=replacement.capitalize()
 newru=ru[:mm.start()]+replacement+ru[mm.end():]
 newen=re.sub(r'\b'+w+r'\b','will '+verbmap[w],en,flags=re.I)
 newen=re.sub(r'\byesterday\b','tomorrow',newen,flags=re.I);newru=re.sub(r'\bвчера\b','завтра',newru,flags=re.I)
 out[f"{x['pack']}:{x['overall']}"]={'en':newen,'ru':newru,'method':'future_tense_draft'}
(B/'auto_drafts.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Auto drafts:',len(out),'manual remaining:',len(plan)-len(out))
