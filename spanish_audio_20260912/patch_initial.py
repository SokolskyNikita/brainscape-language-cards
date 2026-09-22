from spanish_audio_20260912.review import patch
patch(15350686,{
19:({'qMdFootnote':"Rodrigo is the doctor's brother."},'Align brother with hermano.'),
28:({'qMdBody':'like this, this way','qMdFootnote':'Do it like this.','aMdFootnote':'Hazlo así.'},'Teach así itself rather than the conjunction así que.'),
30:({'qMdFootnote':'Call me when you arrive.','aMdFootnote':'Llámame cuando llegues.'},'Use unaccented relative cuando, matching the headword.'),
38:({'qMdFootnote':'Thank you for your help.'},'Remove stray quotation marks.'),
65:({'aMdFootnote':'Ni la lluvia ni la nieve los detienen.'},'Plural subject agreement.'),
103:({'qMdFootnote':'This is part of the plan.','aMdFootnote':'Esto es parte del plan.'},'Replace misleading theatrical role translation.'),
111:({'qMdFootnote':'This is a serious problem.','aMdFootnote':'Este es un problema serio.'},'Replace unidiomatic estar serio en aprender.'),
115:({'qMdFootnote':'She is the person who called.','aMdFootnote':'Ella es la persona quien llamó.'},'Use relative quien instead of interrogative quién.'),
190:({'qMdFootnote':'I ordered a big coffee.'},'Use the English target.'),
194:({'qMdFootnote':"He seems completely crazy today!",'aMdFootnote':'¡Parece completamente loco hoy!'},'Natural matched example.'),
202:({'qMdFootnote':'His return home made me happy.','aMdFootnote':'Su vuelta a casa me alegró.'},'Natural use of vuelta.'),
204:({'aMdFootnote':'Pienso que tienes razón.'},'Use pensar, the target verb.'),
207:({'aMdFootnote':'Todos morimos tarde o temprano.'},'Avoid the false-friend use of eventualmente.'),
214:({'aMdFootnote':'Óscar e Ignacio trabajan juntos.'},'Remove English and from the Spanish example; use target e.'),
234:({'qMdBody':'neither, not either','qMdFootnote':"I don't like coffee either.",'aMdFootnote':'A mí tampoco me gusta el café.'},'Use tampoco naturally and match the meaning.'),
236:({'qMdFootnote':'I bought a pair of shoes.','aMdFootnote':'Compré un par de zapatos.'},'Use target pair in a matched example.'),
258:({'qMdFootnote':'The fire kept us warm.','aMdFootnote':'El fuego nos mantuvo calientes.'},'Use fuego rather than fogata.'),
287:({'qMdFootnote':"I'll take the remainder home.",'aMdFootnote':'Me llevaré el resto a casa.'},'Remove awkward repeated llevar construction.'),
297:({'qMdFootnote':'I need to put the book on the table.','aMdFootnote':'Necesito poner el libro en la mesa.'},'Natural concrete location for poner.'),
304:({'qMdFootnote':'Where to now?','aMdFootnote':'¿Adónde vamos ahora?'},'Remove stray quotes and match the question.'),
306:({'aMdFootnote':'El asesino escapó sin que nadie lo notara.'},'Natural translation of unnoticed.'),
307:({'aMdFootnote':'Nos vemos frente a la tienda.'},'Meet me is an arrangement, not find me.'),
311:({'aMdFootnote':'Tenemos derecho a estar aquí.'},'Correct derecho a construction.'),
321:({'qMdFootnote':'I made an error yesterday.'},'Use the English target.'),
323:({'qMdFootnote':'She has good taste in music.','aMdFootnote':'Ella tiene buen gusto para la música.'},'Natural matched taste example.'),
324:({'qMdFootnote':'I need to change the plan.','aMdFootnote':'Necesito cambiar el plan.'},'Avoid literal change my clothes construction.'),
340:({'qMdBody':'both'},'Ambos does not mean either.'),
354:({'qMdFootnote':'He returned after the war.','aMdFootnote':'Regresó tras la guerra.'},'Natural example using tras.'),
377:({'qMdFootnote':'We crossed the lake by boat.','aMdFootnote':'Cruzamos el lago en barco.'},'Natural matched navigation example.'),
384:({'aMdFootnote':'Nos vemos en el centro de la ciudad.'},'Translate the meeting arrangement naturally.'),
387:({'aMdFootnote':'Vamos a comer pasta para la cena de esta noche.'},'Avoid calque tener pasta para la cena.'),
397:({'aMdFootnote':'Él infringió la ley.'},'Use natural infringir la ley rather than romper la ley.'),
418:({'qMdFootnote':'We are in danger.','aMdFootnote':'Estamos en peligro.'},'Remove unnatural danger ahead calque.'),
422:({'qMdFootnote':"Sorry, what's your name?"},'Remove period after question mark.'),
434:({'qMdBody':'still, yet'},'Correct English typo.'),
442:({'qMdFootnote':'I will have more time tomorrow.','aMdFootnote':'Tendré más tiempo mañana.'},'Have dinner is cenar, not tener cena; preserve target tendré.'),
462:({'qMdFootnote':'He hurt his backside.','aMdFootnote':'Se lastimó el trasero.'},'Natural matched use of trasero.')})
# Improve the relative-clause example without the nonstandard noun + quien pattern.
patch(15350686,{115:({'qMdFootnote':'She is the one who called.','aMdFootnote':'Ella es quien llamó.'},'Correct relative quien example.')})
patch(15350703,{160:({'qMdBody':'accept (subjunctive)','aMdBody':'acepte','qMdFootnote':'I hope she accepts the invitation.','aMdFootnote':'Espero que acepte la invitación.'},'Restore original Spanish lemma acepte from the source export; corrupted Spanish fields contained unrelated English.')})
patch(15350708,{380:({'qMdBody':'you break','aMdBody':'rompes','qMdFootnote':'You break the glass.'},'Remove stray English from Spanish headword; clarify person.')})
patch(15350724,{159:({'qMdBody':'relax (subjunctive)','qMdFootnote':'He wants me to relax.','aMdFootnote':'Quiere que me relaje.'},'Put English and Spanish examples on the correct sides.')})
# These four shared language-placement errors must also be fixed before Spanish-only audio.
patch(15350594,{214:({'qMdFootnote':'Óscar e Ignacio trabajan juntos.'},'Remove English contamination before Spanish audio.')})
patch(15350628,{160:({'qMdBody':'acepte','aMdBody':'accept (subjunctive)','qMdFootnote':'Espero que acepte la invitación.','aMdFootnote':'I hope she accepts the invitation.'},'Restore corrupted Spanish card before Spanish-only audio.')})
patch(15350631,{380:({'qMdBody':'rompes','aMdBody':'you break','aMdFootnote':'You break the glass.'},'Remove stray English from Spanish headword before audio.')})
patch(15350649,{159:({'aMdBody':'relax (subjunctive)','qMdFootnote':'Quiere que me relaje.','aMdFootnote':'He wants me to relax.'},'Correct swapped example languages before Spanish-only audio.')})
patch(15350728,{270:({'aMdBody':'crío'},'Restore accent for child, distinguishing crio (bred).')})
patch(15350729,{
20:({'qMdBody':'uproar, loud noise','qMdFootnote':'The concert ended with a loud noise.'},'Correct load/loud typo and align example.'),
142:({'qMdBody':'I improvise','qMdFootnote':'I improvise the song.'},'Improviso is a conjugated verb, not the noun improvisation.'),
179:({'qMdBody':'medically','qMdFootnote':'The treatment is medically necessary.','aMdFootnote':'El tratamiento es médicamente necesario.'},'Distinguish medically from medicinally.'),
197:({'qMdBody':'you shoot (subjunctive, vosotros)'},'Disparéis is subjunctive, used in negative commands, not affirmative imperative.'),
203:({'aMdBody':'me atreví'},'Include the reflexive pronoun required by dare.'),
224:({'qMdBody':'charitable','qMdFootnote':'The charitable event starts now.'},'Correct part of speech and English spelling.'),
359:({'aMdBody':'elige','aMdFootnote':'Por favor, elige tu color favorito.'},'Correct the spelling of the elegir imperative.'),
398:({'qMdBody':'I made an effort','aMdBody':'me esforcé','qMdFootnote':'I made an effort to learn Spanish.'},'Use reflexive esforzarse and accurate gloss.'),
424:({'aMdBody':'me emborraché'},'Reflexive pronoun required for got drunk.'),
447:({'qMdBody':'I force','qMdFootnote':'I force no one to help.','aMdFootnote':'No obligo a nadie a ayudar.'},'Obligo is a conjugated verb, not the noun obligation.')})
