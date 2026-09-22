"""Persist reviewed context labels; no automatic WSD on unseen sentences.
Every context in contexts.json was inspected alongside both-language reference
headwords and examples. Exception IDs below distinguish remaining senses.
"""
from pathlib import Path
import json
B=Path(__file__).resolve().parent
contexts=json.loads((B/'contexts.json').read_text())
# word, sense -> exact-form lessons in that sense; eligible base lessons;
# current-target lemmas; rationale. Empty exact means never taught in this sense.
specs={
 'saw':('see',[ ],[93],['see'],'Past of see, not the cutting tool or cutting verb.'),
 'fell':('fall',[],[307,904],['fall'],'Past of fall, not fell = cut/knock down.'),
 'left':('leave',[],[351,492],['leave'],'Past of leave, not left-hand direction.'),
 'mine':('possessive',[],[5],['i','my','mine'],'Possessive pronoun, not an explosive device or excavation.'),
 'found':('find',[1650],[143,939],['find'],'Past/participle of find; ignore found = establish, but retain to be found at #1650.'),
 'managed':('succeed',[],[530,1732],['manage'],'Manage to accomplish something, not control/operate machinery.'),
 'entered':('go_in',[],[503,609],['enter'],'Go into a place/group, not enter a name/data in a record.'),
 'held':('hold_physical',[],[511],['hold'],'Hold/grasp, not hold/conduct an event.'),
 'holding':('hold_physical',[],[511],['hold'],'Holding hands, not a holding company.'),
 'calling':('call_for',[],[2510],['call'],'Calling/appealing for help or peace, not a vocation.'),
 'setting':('set_in',[],[],['set'],'Winter setting in is not a configuration setting; only current-target support accepted here.'),
 'realized':('understand',[],[2176,3889],['realize'],'Realize = understand, not realize/implement a plan.'),
 'finishing':('complete',[],[979,2551],['finish'],'Complete work, not a surface finish/trim.'),
 'recognized':('identify',[],[1060,9601,9630],['recognize'],'Identify a person, not acknowledge/acclaim someone.'),
 'living':('alive_or_residing',[],[112,1948],['live'],'Living/alive/residing, not the room-name compound living room.'),
 'moving':('physical_motion',[],[3970,4099,9631],['move'],'Physical movement, not moving = driving/causal force or emotionally touching.'),
 'names':('identifiers',[],[174,476],['name'],'Personal names or naming, not insults in call names.'),
 'played':('recreation',[],[317,1619],['play'],'Recreational or musical play, not play out/enact a scene.'),
 'brought':('transport',[],[395,717],['bring'],'Bring/deliver, not bring up = raise a child.'),
}
# Reviewed exceptions where the default sense does not apply. Those retain the
# existing conservative check unless a specific alternate specification is given.
skip={
 'saw':{'english_russian:7554','english_russian:7844'},
 'fell':{'english_russian:4687','english_russian:9995','russian_english:6436'},
 'left':{'english_russian:841','english_russian:3463','english_russian:3635','english_russian:5794','russian_english:977','russian_english:1865','russian_english:2758','russian_english:4610','russian_english:5672','russian_english:5806','russian_english:5864','russian_english:6405'},
 'mine':{'russian_english:2589','russian_english:5641'},
 'found':{'english_russian:1363','english_russian:7481'},
 'managed':{'english_russian:5886'},
 'entered':{'english_russian:8681'},
 'held':{'english_russian:1419','english_russian:5157','english_russian:9985','russian_english:1712','russian_english:7158','russian_english:9639'},
 'holding':{'english_russian:5620','russian_english:1133','russian_english:7912'},
 'calling':{'english_russian:5798','russian_english:8183'},
 'setting':{'english_russian:2721','russian_english:3524','russian_english:4716','russian_english:7038'},
 'realized':{'english_russian:4437','russian_english:6043'},
 'finishing':{'english_russian:6674','russian_english:9571'},
 'recognized':{'english_russian:7034'},
 'living':{'english_russian:2848','russian_english:3714'},
 'moving':{'english_russian:8862'},
 'names':{'english_russian:8074'},
 # Acting is compatible with the play-out reference. Without more context,
 # "played brilliantly" and "played with excitement" are left conservative.
 'played':{'english_russian:3472','english_russian:6919','english_russian:9251','english_russian:9383','russian_english:8935'},
 # Result/cause senses require more than transport vocabulary; do not clear them.
 'brought':{'english_russian:2756','english_russian:6185','english_russian:6702','english_russian:7418','english_russian:7692','english_russian:9325','russian_english:8368','russian_english:9683'},
}
reviews=[]
for w,spec in specs.items():
 sense,exact,bases,lemmas,why=spec
 for c in contexts[w]:
  key=f"{c['pack']}:{c['overall']}"
  reviewed=dict(**c,word=w)
  if key in skip.get(w,set()):reviewed.update(action='retain_default',reason='Different/uncertain contextual sense; do not apply the general resolution for this word.')
  elif w=='moving' and key=='english_russian:9971':reviewed.update(action='resolve_sense',sense='emotionally_touching',exact_reference_positions=[],base_reference_positions=[],current_target_lemmas=[],reason='Moving sermon means emotionally touching; physical movement and a moving/driving force do not teach this sense.')
  else:reviewed.update(action='resolve_sense',sense=sense,exact_reference_positions=exact,base_reference_positions=bases,current_target_lemmas=lemmas,reason=why)
  reviews.append(reviewed)
(B/'sense_reviews.json').write_text(json.dumps(reviews,ensure_ascii=False,indent=2)+'\n')
print('Reviewed contextual occurrences:',len(reviews),'resolved:',sum(x['action']=='resolve_sense' for x in reviews))
