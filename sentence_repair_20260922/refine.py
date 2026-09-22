from pathlib import Path
import json,re
B=Path(__file__).resolve().parent;p=B/'replacements.json';r=json.loads(p.read_text())
for v in r.values():
 v['en']=re.sub(r'\b([a-z]+ly) will\b',r'will \1',v['en'])
 v['en']=v['en'].replace(' .','.').replace('a abstraction','an abstraction')
 v['ru']=re.sub(r'\b(буду|будешь|будет|будем|будете|будут) быть\b',r'\1',v['ru'])
 v['ru']=v['ru'][0].upper()+v['ru'][1:]
fix={
'english_russian:1575':("Let's connect this to the computer.",'Давайте соединим это с компьютером.'),
'english_russian:2740':('A hostile army is near the city.','Вражеская армия находится рядом с городом.'),
'english_russian:1169':('She will feel this deeply.','Она будет глубоко это чувствовать.'),
'english_russian:1175':('Do not lose your key.','Не потеряй свой ключ.'),
'english_russian:1810':('Do not lose your glasses.','Не потеряй свои очки.'),
'english_russian:1844':('Do not lose your mobile.','Не потеряй свой мобильный телефон.'),
'english_russian:2634':('Do not lose your shoe.','Не потеряй свой ботинок.'),
'english_russian:3217':('Do not lose your pencil again.','Не потеряй свой карандаш снова.'),
'english_russian:3635':('Do not lose your left glove.','Не потеряй свою левую перчатку.'),
'english_russian:4159':('Do not lose the remote control again.','Не потеряй пульт снова.'),
'english_russian:4472':('Do not lose your handbag.','Не потеряй свою сумочку.'),
'english_russian:3472':('The actress will play well.','Актриса будет хорошо играть.'),
'english_russian:4103':('She will support him in every way.','Она будет всячески его поддерживать.'),
'english_russian:6919':('She will play brilliantly.','Она будет блестяще играть.'),
'english_russian:7456':('He will display his trophy proudly.','Он будет гордо показывать свой трофей.'),
'english_russian:1330':('I will hear noise in the street.','Я услышу шум на улице.'),
'english_russian:2080':('He will hear a shot.','Он услышит выстрел.'),
'english_russian:2510':('I will hear the call.','Я услышу призыв.'),
'english_russian:2626':('I will hear an echo.','Я услышу эхо.'),
'english_russian:2917':('I will hear the shooting.','Я услышу стрельбу.'),
'english_russian:3179':('I will feel a gust of wind.','Я почувствую порыв ветра.'),
'russian_english:520':('Politics is important.','Политика важна.'),
'russian_english:564':('The population is big.','Население большое.'),
'russian_english:910':('He will grow.','Он будет расти.'),
'russian_english:1040':('He wears this.','Он носит это.'),
'russian_english:1085':('I will try again.','Я попытаюсь снова.'),
'russian_english:1587':('He knows this and therefore will come.','Он знает это и, соответственно, придёт.'),
'russian_english:2173':('We can live on this.','Мы можем прожить на это.'),
'russian_english:2480':('He will inflict harm.','Он нанесёт вред.'),
'russian_english:4009':('They will take away your books.','Они отберут у тебя книги.'),
'russian_english:5285':('This is a border town.','Это пограничный город.'),
'russian_english:5713':('Stretch the string.','Натяни струну.'),
'russian_english:2365':('Assign this room to him.','Предназначьте эту комнату для него.'),
'russian_english:6621':('This is outside my competence.','Это вне моей компетенции.'),
'russian_english:7598':('We must reduce the time.','Надо сокращать время.'),
'russian_english:8360':('This is a wireless connection.','Это беспроводное соединение.'),
'russian_english:1669':('He will lose his mind.','Он потеряет разум.'),
'russian_english:2818':('They will elect him.','Его изберут.'),
'russian_english:728':('They will install it.','Они установят это.'),
'russian_english:1002':('They will build the house.','Они построят дом.'),
'russian_english:1021':('The minister will say so.','Министр так скажет.'),
'russian_english:2484':('They will release him.','Его освободят.'),
'russian_english:1391':('Do not lose your key.','Не потеряй свой ключ.'),
'russian_english:2226':('Do not lose your glasses.','Не потеряй свои очки.'),
'russian_english:4629':('Her charm is clear.','Её прелесть очевидна.'),
'russian_english:2606':('I will die of hunger.','Я умру от голода.'),
'russian_english:1043':('Who will speak?','Кто будет выступать?'),
'russian_english:53':("I will stay so that he can go.",'Я останусь, чтобы он мог пойти.'),
'russian_english:130':("Although he's here, I can go.",'Хотя он здесь, я могу идти.'),
'russian_english:434':("He speaks as if he knows.",'Он говорит, будто знает.'),
'russian_english:1398':('This is a miracle.','Это чудо.'),
'russian_english:2600':('This is a magnificent house.','Это великолепный дом.'),
}
for k,(en,ru) in fix.items():r[k].update(en=en,ru=ru,method='reviewed replacement')
p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
extra=[]
for s in json.loads((B/'stale_sense_reviews.json').read_text()):
 v=s['old'];v['example']=s['new_example'];extra.append(v)
(B/'new_sense_reviews.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2)+'\n')
