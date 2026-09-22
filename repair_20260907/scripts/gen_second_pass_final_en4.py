import json
import sys
from pathlib import Path

sys.path.insert(0, ".")
from brainscape import cards_from_path


PATCHES = {
    "15260268": {
        25: (("hallway", "коридор", "The hallway is empty.", "Коридор пуст."), "Прихожая is an entryway, whereas hallway here is коридор."),
        95: (("intelligent", "умный", "He is an intelligent man.", "Он умный человек."), "Интеллектуальный человек is an unnatural false-friend rendering of intelligent."),
        102: (("psychiatrist", "психиатр", "The psychiatrist helps her.", "Психиатр помогает ей."), "Make the English present tense match the Russian example."),
        113: (("to rush by", "проноситься", "Trains rush by.", "Поезда проносятся мимо."), "Use a repeated/durative event on both faces rather than mismatching a single future event with a durative future."),
        203: (("qualitatively", "качественно", "They are qualitatively different.", "Они качественно разные."), "Works qualitatively is not idiomatic English; use the adverb in its genuine analytical sense."),
        215: (("decompose", "разложить", "Heat will decompose this substance.", "Тепло разложит это вещество."), "Fire does not naturally decompose a leaf; use a scientifically coherent example."),
        231: (("notorious", "пресловутый", "This is the notorious claim.", "Это пресловутое утверждение."), "Пресловутый naturally modifies a notorious, much-discussed claim rather than a person."),
        238: (("sociology", "социология", "He studies sociology.", "Он учится социологии."), "Use idiomatic study phrasing instead of the mismatched читаю sociology."),
        246: (("extremity", "крайность", "That is the other extremity.", "Это другая крайность."), "Pain reached an extremity is not a natural use of either noun."),
        249: (("worthily", "достойно", "He acts worthily.", "Он действует достойно."), "Replace an unsupported verb with a natural prior-deck verb."),
        250: (("heel", "каблук", "Her heel is high.", "У неё высокий каблук."), "Replace the incoherent claim that a shoe heel is old with a normal collocation."),
        278: (("blessed", "блаженный", "They lived in blessed peace.", "Они жили в блаженном покое."), "The original examples were ungrammatical and did not express the blissful sense of блаженный."),
        299: (("little by little", "понемногу", "Little by little, he learned to read.", "Понемногу он научился читать."), "Align learned with научился; учился only says that he studied."),
        301: (("toast", "тост", "This is a toast to friendship.", "Это тост за дружбу."), "Avoid the calque поднимать тост while keeping within prior-deck supporting vocabulary."),
        304: (("competence", "компетенция", "This issue is outside her competence.", "Этот вопрос вне её компетенции."), "High competence is an unnatural collocation and confuses компетенция with компетентность."),
        347: (("disagreement", "разногласие", "Their disagreement is clear.", "Их разногласие ясно."), "A disagreement can be clear, but is not naturally described as strong here."),
        363: (("correction", "коррекция", "This correction is important.", "Эта коррекция важна."), "Avoid the calqued сделать коррекцию while retaining the technical noun."),
        370: (("related", "родственный", "These are related languages.", "Это родственные языки."), "Родственный naturally describes related languages; родственный вопрос is a calque."),
        386: (("grace", "благодать", "She felt God's grace.", "Она чувствовала Божью благодать."), "Use the idiomatic Russian possessive adjective for God's grace."),
        406: (("oath", "клятва", "He swore an oath of loyalty.", "Он дал клятву верности."), "English idiom is swear an oath, not give an oath."),
        418: (("ambition", "амбиция", "She has great ambition.", "У неё большие амбиции."), "Russian normally uses амбиции in the plural in this sense."),
        426: (("dough", "тесто", "The dough is ready.", "Тесто готово."), "Use the natural Russian short-form predicate."),
        446: (("to look out", "выглянуть", "He went to look out of the window.", "Он пошёл выглянуть из окна."), "Both languages require looking out of, not into, the window in this sense."),
        458: (("mountain pass", "перевал", "The mountain pass is closed.", "Перевал закрыт."), "Use the idiomatic Russian short-form predicate."),
        483: (("curve", "кривая", "I draw a curve.", "Я рисую кривую."), "A road has a bend or turn; кривая is naturally something one draws."),
    },
    "15260269": {
        63: (("cent", "цент", "I found a cent outside.", "Я нашёл цент на улице."), "Replace the unnatural on the earth phrasing while preserving the location."),
        102: (("intestine", "кишка", "The intestine is part of the body.", "Кишка — часть тела."), "Replace the biologically vacuous and unnatural claim that an intestine works every day."),
        106: (("molecule", "молекула", "A water molecule is small.", "Молекула воды маленькая."), "Water is not a molecule; it consists of water molecules."),
        110: (("to incline", "склонить", "His words inclined me to agree.", "Его слова склонили меня согласиться."), "Replace the incomplete and calqued incline him to this construction."),
        114: (("slow down", "замедлить", "Please slow down the process.", "Пожалуйста, замедлите процесс."), "Slow down speech is awkward on both faces; process gives the transitive verb a natural object."),
        120: (("canon", "канон", "This book entered the canon.", "Эта книга вошла в канон."), "A single book is not itself the canon; it can enter the canon."),
        125: (("materially", "материально", "This helps materially.", "Это помогает материально."), "Materially better life is an unnatural predicate on both faces."),
        151: (("bliss", "блаженство", "Living here is bliss.", "Жить здесь — блаженство."), "Replace the unnatural statement that a day is bliss with a normal predicative use."),
        193: (("ambush", "засада", "They set an ambush at dawn.", "Они устроили засаду на рассвете."), "The idiom is set/устроить an ambush, not make/сделать one."),
        195: (("assist", "содействовать", "I will assist with this work.", "Я буду содействовать этой работе."), "Add the preposition required by idiomatic English assist with."),
        197: (("rotation", "вращение", "Earth's rotation creates day and night.", "Вращение Земли создаёт день и ночь."), "Rotation creates the day-night cycle; it does not simply give day and night."),
        204: (("to poke", "совать", "He pokes his finger into the cup.", "Он суёт палец в чашку."), "Совать requires a destination; the staged examples were incomplete."),
        205: (("neighborhood", "район", "I love our peaceful neighborhood.", "Я люблю наш тихий район."), "Соседство means proximity or neighbor relations, not a residential neighborhood."),
        206: (("moisture", "влага", "Moisture helps plants grow.", "Влага помогает растениям расти."), "Plants grow with moisture is an unnatural instrumental construction."),
        208: (("inconvenience", "неудобство", "I caused some inconvenience.", "Я причинил неудобство."), "Use idiomatic English number/determination with inconvenience."),
        218: (("sparrow", "воробей", "A sparrow sat by the window.", "Воробей сидел у окна."), "English sat on the window is not idiomatic for the intended location."),
        225: (("to lean", "упереться", "She leaned hard against the wall.", "Она сильно упёрлась в стену."), "Make the English express the braced-against sense of упереться."),
        233: (("intense", "пристальный", "He gave me an intense look.", "Он бросил на меня пристальный взгляд."), "Use a natural collocation for the gaze sense of пристальный/intense."),
        236: (("additive", "добавка", "Sugar is an additive.", "Сахар — добавка."), "Replace the unidiomatic in food / в еде construction."),
        246: (("to apply", "прилагать", "Do not apply force.", "Не прилагайте силу."), "Прилагать слабое давление is an unnatural rendering of apply gentle pressure."),
        248: (("clarification", "разъяснение", "I need clarification of the rule.", "Мне нужно разъяснение правила."), "Выяснение is investigation or finding out; requested clarification is разъяснение."),
        311: (("to alleviate", "облегчать", "Medicine alleviates pain.", "Лекарство облегчает боль."), "Remove the awkward помогает облегчать aspect construction while keeping the listed verb."),
        353: (("gamma", "гамма", "I wrote gamma.", "Я написал гамму."), "Rich gamma is a Russian-only color-range usage and is not idiomatic English."),
        363: (("notable", "знатный", "He came from a notable family.", "Он происходил из знатной семьи."), "Restore the original notable card overwritten by a first-pass row-identity error."),
        367: (("expiration", "истечение", "The contract's expiration is tomorrow.", "Истечение договора — завтра."), "Expiration/истечение cannot naturally be described as near in these nominal sentences."),
        370: (("silvery", "серебристый", "Her hair looked silvery.", "Её волосы казались серебристыми."), "Restore the original silvery card overwritten by a first-pass row-identity error."),
        379: (("Sunday", "воскресенье", "We rest on Sunday.", "Мы отдыхаем в воскресенье."), "Restore the original Sunday card overwritten by a first-pass row-identity error."),
        401: (("ford", "брод", "We cross the ford.", "Мы переходим брод."), "A river ford is брод; форд is the car brand."),
        419: (("variable", "переменный", "The machine has variable speed.", "У машины переменная скорость."), "Variable weather is naturally изменчивая погода; переменный fits variable speed."),
        437: (("to slip", "скользнуть", "The knife slipped on the table.", "Нож скользнул по столу."), "Replace the incorrect slip from my hand / скользнуть с руки pairing."),
        444: (("to be prohibited", "запрещаться", "Smoking is prohibited here.", "Курение здесь запрещается."), "Replace the unnatural prospective English construction with a present prohibition."),
        458: (("to write out", "выписывать", "She writes out the recipe.", "Она выписывает рецепт."), "Make the English and Russian present tense match."),
        479: (("grape", "виноград", "I love eating grapes.", "Я люблю есть виноград."), "English count noun needs the plural to match Russian mass-noun виноград."),
        481: (("starting", "стартовый", "This is the starting point.", "Это стартовая точка."), "Starting place / стартовое место is an unnatural collocation."),
        486: (("to peer out", "выглядывать", "She likes to peer out of the window.", "Она любит выглядывать из окна."), "Both verbs take out of/from the window, not into it, in this sense."),
    },
    "15260272": {
        28: (("identification", "идентификация", "Identification took an hour.", "Идентификация заняла час."), "I need identification normally means an ID document, not the process идентификация."),
        33: (("flying", "летучий", "This is a flying object.", "Это летучий объект."), "Flying mouse is a misleading literal rendering of летучая мышь, which means bat."),
        41: (("anti-aircraft", "зенитный", "They used an anti-aircraft weapon.", "Они использовали зенитное оружие."), "Use matching generic weapon terms on both faces."),
        52: (("newton", "ньютон", "This force is one newton.", "Эта сила — один ньютон."), "Lowercase the unit headword to match the staged measurement example."),
        106: (("Nobel", "нобелевский", "This is a Nobel award.", "Это Нобелевская награда."), "Use prior-deck vocabulary while retaining a natural adjectival use of Nobel/нобелевский."),
        67: (("kindly", "любезно", "She answered kindly.", "Она любезно ответила."), "Please kindly and любезно закройте are redundant, unnatural request formulas."),
        81: (("broadcasting", "вещание", "Broadcasting began today.", "Вещание началось сегодня."), "Keep broadcasting as a noun on both faces and remove the awkward вещание новостей construction."),
        86: (("legislator", "законодатель", "The legislator passed a new law.", "Законодатель принял новый закон."), "Laws are passed/приняты, not made/созданы."),
        91: (("to delay", "задерживать", "He delays me.", "Он задерживает меня."), "Задерживать поездку is an unnatural rendering of postpone a trip; use the hold-up sense."),
        110: (("productive", "производительный", "This machine is productive.", "Эта машина производительная."), "Производительный naturally describes a machine or labor, not a factory."),
        115: (("similar to", "наподобие", "She built a house similar to ours.", "Она построила дом наподобие нашего."), "Supply a complete comparison after наподобие instead of the calqued style construction."),
        136: (("glue", "клей", "I need glue for this project.", "Мне нужен клей для этого проекта."), "Remove the unsupported added action взять from the Russian example."),
        158: (("legality", "законность", "They asked about legality.", "Они спросили о законности."), "Avoid the tautological legality of the law / законность закона."),
        165: (("reservation", "сомнение", "I have one reservation.", "У меня есть одно сомнение."), "A reservation meaning a doubt is сомнение, not оговорка."),
        169: (("fit in", "вписываться", "He is slowly fitting in.", "Он медленно вписывается."), "Replace the unnatural вписываться в школе while retaining the listed imperfective verb."),
        174: (("perseverance", "упорство", "Perseverance will bring success.", "Упорство принесёт успех."), "Use a natural equivalent of leads to success."),
        200: (("enmity", "вражда", "Their enmity was long.", "Их вражда была долгой."), "Correct the unidiomatic Russian duration phrase шла годы."),
        201: (("lyrics", "слова песни", "She writes new lyrics.", "Она пишет новые слова песни."), "Song lyrics are слова песни or текст песни; лирика means lyric poetry or lyricism."),
        214: (("grumble", "ворчать", "He grumbles at work.", "Он ворчит на работе."), "Replace the unidiomatic ворчать о работе with a natural setting."),
        228: (("traffic", "дорожное движение", "Traffic is heavy today.", "Дорожное движение сегодня плотное."), "Road traffic is дорожное движение; трафик is chiefly data traffic and is a poor match here."),
        232: (("twirl", "вертеть", "She loves to twirl a pencil.", "Она любит вертеть карандаш."), "Вертеть волосами is unnatural; a pencil is a natural object of both verbs."),
        234: (("greed", "жадность", "His greed is obvious.", "Его жадность очевидна."), "Greed is evident or great, not strong, in this neutral context."),
        271: (("to eat up", "съедать", "She always eats up her vegetables.", "Она всегда съедает овощи."), "Use the normal eat-up construction instead of loves to eat up."),
        290: (("rhyme", "рифма", "This poem contains a rhyme.", "В этом стихотворении есть рифма."), "Make the singular poem and Russian example refer to the same work."),
        307: (("distinctive", "отличительный", "This is a distinctive sign.", "Это отличительный знак."), "Отличительный naturally modifies a sign, not a voice as a predicate."),
        323: (("noiselessly", "бесшумно", "She noiselessly entered the room.", "Она бесшумно вошла в комнату."), "Make the Russian past tense match the English example."),
        334: (("snort", "фыркнуть", "He snorted.", "Он фыркнул."), "Хмыкнуть is grunt or chuckle; snort is фыркнуть."),
        340: (("to be implied", "подразумеваться", "This is implied by his words.", "Это подразумевается его словами."), "Correct the English and Russian complement construction."),
        348: (("hurricane", "ураган", "The hurricane was strong.", "Ураган был сильным."), "Use instrumental case after был in the neutral predicate."),
        350: (("expediency", "целесообразность", "Expediency is important.", "Целесообразность важна."), "For expediency / для целесообразности is not idiomatic in either language."),
        354: (("ethereal", "неземной", "Her voice is ethereal.", "Её голос неземной."), "Эфирный is a false friend in this poetic sense; an ethereal voice is неземной."),
        363: (("to sew", "сшить", "She will sew the pieces together.", "Она сошьёт части вместе."), "Restore the original sew card overwritten by a first-pass row-identity error."),
        378: (("entail", "повлечь", "The delay will entail costs.", "Задержка повлечёт расходы."), "Success does not naturally entail work; delay and costs form a coherent causal example."),
        383: (("to leak", "потечь", "The roof began to leak.", "Крыша потекла."), "Water began to flow is not specifically a leak; a leaking roof matches потечь."),
        386: (("to be managed", "управляться", "This machine is easily managed.", "Эта машина легко управляется."), "Work is not naturally managed in the staged passive construction; a machine can be управляться."),
        391: (("bite", "кусать", "The dog bites strangers.", "Собака кусает незнакомцев."), "Make tense and aspect match while using the listed imperfective verb."),
        393: (("fever", "лихорадка", "She has a fever.", "У неё лихорадка."),
              "High fever is высокая температура in Russian; лихорадка names the condition."),
        394: (("set off", "пуститься", "They set off on their journey.", "Они пустились в путь."), "Supply the complement required by пуститься in the set-off sense."),
        409: (("comprehension", "осмысление", "Comprehension takes time.", "Осмысление требует времени."), "Good comprehension / хорошее осмысление is an unnatural process predicate."),
        410: (("layout", "расположение", "Check the room's layout.", "Проверьте расположение комнат."), "Расклад is a card spread or situation, not the physical layout intended here."),
        419: (("subway", "метрополитен", "I use the subway daily.", "Я ежедневно пользуюсь метрополитеном."), "Use the idiomatic Russian verb with formal метрополитен."),
        422: (("modesty", "скромность", "Her modesty is evident.", "Её скромность очевидна."), "Modesty cannot naturally be described as strong in either example."),
        424: (("weakening", "ослабление", "I noticed a weakening of the signal.", "Я заметил ослабление сигнала."), "Avoid the semantically redundant weakening of his power / ослабление его силы."),
        426: (("conceptual", "концептуальный", "This is a conceptual design.", "Это концептуальный проект."), "The staged Russian omits design and leaves an incomplete conceptual phase."),
        427: (("maid", "служанка", "The maid washed the floor quietly.", "Служанка тихо мыла пол."), "Make the English object match the Russian verb мыла."),
        434: (("led", "ведомый", "The group was led by a guide.", "Группа была ведома проводником."), "The led group is not grammatical English; use led as a passive participle on both faces."),
        435: (("overflow", "переполнить", "Joy overflowed his heart.", "Радость переполнила его сердце."), "Overflow is not naturally a command applied to a cup; use the transitive figurative sense of переполнить."),
        446: (("cord", "шнур", "I need a new cord.", "Мне нужен новый шнур."), "Remove the extra unsupported action взять from the Russian example."),
        458: (("occupation", "оккупация", "The occupation was long.", "Оккупация была долгой."), "Correct the unidiomatic duration phrase шла годы."),
        463: (("skilled", "умелый", "He is a skilled worker.", "Он умелый сотрудник."), "Make grammatical gender agree with the occupational noun."),
        468: (("suggestion", "внушение", "Hypnosis relies on suggestion.", "Гипноз основан на внушении."), "Teach suggestion in the psychological influence sense that matches внушение."),
        471: (("show off", "красоваться", "He likes to show off in his new suit.", "Он любит красоваться в новом костюме."), "Красоваться машиной is not idiomatic; the verb naturally describes displaying oneself."),
        472: (("coastal", "прибрежный", "This is a coastal city.", "Это прибрежный город."), "A coastal city is прибрежный; береговой is used for shore-based objects and functions."),
        485: (("to throw back", "отбрасывать", "The wall throws the ball back.", "Стена отбрасывает шар."), "Make the English phrasal verb explicit while retaining the generic spherical-object sense of шар."),
        486: (("trudge", "брести", "We trudge through deep snow.", "Мы бредём по глубокому снегу."), "Correct the Russian path construction and restore ё in бредём."),
        488: (("vibration", "вибрация", "The telephone's vibration startles me.", "Вибрация телефона пугает меня."), "Make the English present tense match Russian."),
        491: (("discontentedly", "недовольно", "She sighed discontentedly about the news.", "Она недовольно вздохнула из-за новостей."), "Correct the Russian causal preposition and align the English complement."),
    },
}


def current_tuple(card):
    return [card["qMdBody"], card["aMdBody"], card["qMdFootnote"], card["aMdFootnote"]]


out = []
reviewed = []
for deck, patches in PATCHES.items():
    cards = cards_from_path(f"repair_20260907/staged/english_russian/deck_{deck}.csv")
    assert len(cards) == 500
    for row, (after, reason) in sorted(patches.items()):
        out.append({
            "pack": "english_russian",
            "deck": deck,
            "row": row,
            "before": current_tuple(cards[row - 1]),
            "after": list(after),
            "reason": reason,
        })
    reviewed.append({
        "pack": "english_russian",
        "deck": deck,
        "reviewed": 500,
        "proposed_changes": len(patches),
    })

Path("repair_20260907/second_pass_final_en4.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
Path("repair_20260907/second_pass_final_en4_reviewed.json").write_text(
    json.dumps(reviewed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
