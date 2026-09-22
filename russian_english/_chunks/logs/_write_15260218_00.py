import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260218_00.csv"),
        {
            "непреодолимый": (
                "insurmountable",
                "Задача казалась непреодолимой.",
                "The task seemed insurmountable.",
            ),
            "канадский": (
                "Canadian",
                "Это канадский флаг.",
                "This is a Canadian flag.",
            ),
            "кошачий": (
                "feline, cat's",
                "У неё кошачьи глаза.",
                "She has feline eyes.",
            ),
            "наркомания": (
                "drug addiction",
                "Наркомания разрушает жизни.",
                "Drug addiction destroys lives.",
            ),
            "сладость": (
                "sweetness",
                "Сладость торта мне нравится.",
                "I like the sweetness of the cake.",
            ),
            "сжаться": (
                "to shrink",
                "Ткань сжалась в воде.",
                "The fabric shrank in water.",
            ),
            "вдохнуть": (
                "to inhale, to breathe in",
                "Он глубоко вдохнул.",
                "He inhaled deeply.",
            ),
            "урегулирование": (
                "settlement",
                "Урегулирование спора близко.",
                "The settlement of the dispute is near.",
            ),
            "смертность": (
                "mortality",
                "Смертность выросла в этом году.",
                "Mortality grew this year.",
            ),
            "воспитанник": (
                "pupil, ward",
                "Он мой воспитанник.",
                "He is my pupil.",
            ),
            "трапеза": (
                "meal, feast",
                "Семья собралась за трапезой.",
                "The family gathered for the meal.",
            ),
            "отважный": (
                "brave",
                "Он отважный солдат.",
                "He is a brave soldier.",
            ),
            "тщетно": (
                "in vain",
                "Он тщетно ждал ответа.",
                "He waited in vain for an answer.",
            ),
            "кузнец": (
                "blacksmith",
                "Кузнец работает с железом.",
                "The blacksmith works with iron.",
            ),
            "наглость": (
                "impudence, audacity",
                "Его наглость меня удивила.",
                "His impudence surprised me.",
            ),
            "браслет": (
                "bracelet",
                "У неё золотой браслет.",
                "She has a gold bracelet.",
            ),
            "посоветоваться": (
                "consult",
                "Я посоветовался с врачом.",
                "I consulted a doctor.",
            ),
            "странность": (
                "oddity",
                "Я заметил странность.",
                "I noticed an oddity.",
            ),
            "мнимый": (
                "imaginary",
                "Это мнимый друг.",
                "This is an imaginary friend.",
            ),
            "мобилизация": (
                "mobilization",
                "Мобилизация началась утром.",
                "Mobilization started in the morning.",
            ),
            "разрывать": (
                "to tear",
                "Не разрывай письмо.",
                "Don't tear the letter.",
            ),
            "ворон": (
                "raven",
                "Ворон сел на забор.",
                "A raven sat on the fence.",
            ),
            "обострение": (
                "exacerbation",
                "Началось обострение болезни.",
                "The exacerbation of the illness started.",
            ),
            "лихо": (
                "trouble",
                "Лихо пришло в дом.",
                "Trouble came to the house.",
            ),
            "пролив": (
                "strait",
                "Корабль вошёл в пролив.",
                "The ship entered the strait.",
            ),
            "багажник": (
                "trunk",
                "Положи сумку в багажник.",
                "Put the bag in the trunk.",
            ),
            "адский": (
                "hellish",
                "Сегодня адская жара.",
                "Today the heat is hellish.",
            ),
            "лингвистический": (
                "linguistic",
                "Это лингвистический вопрос.",
                "This is a linguistic question.",
            ),
            "прикрепить": (
                "attach",
                "Прикрепи фото к письму.",
                "Attach the photo to the letter.",
            ),
            "вскинуть": (
                "to throw up, to fling up",
                "Он вскинул голову.",
                "He flung up his head.",
            ),
            "шашка": (
                "checker, sabre",
                "Я взял шашку.",
                "I took a checker.",
            ),
            "пружина": (
                "spring",
                "Пружина сломалась.",
                "The spring broke.",
            ),
            "фронтовой": (
                "front-line",
                "Это фронтовой госпиталь.",
                "This is a front-line hospital.",
            ),
            "эквивалент": (
                "equivalent",
                "Это русский эквивалент.",
                "This is the Russian equivalent.",
            ),
            "косточка": (
                "pit, seed",
                "Не ешь косточку.",
                "Don't eat the pit.",
            ),
            "умолкнуть": (
                "to fall silent",
                "Толпа умолкла.",
                "The crowd fell silent.",
            ),
            "зарядить": (
                "charge",
                "Заряди телефон.",
                "Charge the phone.",
            ),
            "пригород": (
                "suburb",
                "Они живут в пригороде.",
                "They live in a suburb.",
            ),
            "устремить": (
                "to direct",
                "Она устремила взгляд на него.",
                "She directed her gaze at him.",
            ),
            "свисать": (
                "hang down",
                "Провода свисают с крыши.",
                "Wires hang down from the roof.",
            ),
            "таиться": (
                "to lurk, to hide",
                "В траве таится змея.",
                "A snake lurks in the grass.",
            ),
            "оконный": (
                "window",
                "Это оконное стекло.",
                "This is window glass.",
            ),
            "русско": (
                "Russian",
                "Это русско-английский словарь.",
                "This is a Russian-English dictionary.",
            ),
            "путаться": (
                "get confused, get tangled",
                "Я путаюсь в словах.",
                "I get confused in the words.",
            ),
            "невежество": (
                "ignorance",
                "Это просто невежество.",
                "This is simply ignorance.",
            ),
            "табуретка": (
                "stool",
                "Сядь на табуретку.",
                "Sit on the stool.",
            ),
            "развязать": (
                "untie",
                "Развяжи узел.",
                "Untie the knot.",
            ),
            "нетерпеливо": (
                "impatiently",
                "Она нетерпеливо ждала ответа.",
                "She waited impatiently for an answer.",
            ),
            "ревновать": (
                "to be jealous",
                "Он ревнует жену.",
                "He is jealous of his wife.",
            ),
            "удел": (
                "lot, fate",
                "Это мой удел.",
                "This is my lot.",
            ),
            "приверженец": (
                "adherent",
                "Он приверженец демократии.",
                "He is an adherent of democracy.",
            ),
            "суетиться": (
                "fuss",
                "Не суетись.",
                "Don't fuss.",
            ),
            "потереть": (
                "to rub",
                "Потри глаза.",
                "Rub your eyes.",
            ),
            "записываться": (
                "to enroll, to sign up",
                "Я записываюсь на курс.",
                "I am enrolling in the course.",
            ),
            "отсрочка": (
                "deferment",
                "Он получил отсрочку.",
                "He got a deferment.",
            ),
            "подкрепление": (
                "reinforcement",
                "Нам нужно подкрепление.",
                "We need reinforcement.",
            ),
            "аналогично": (
                "similarly",
                "Он сделал это аналогично.",
                "He did it similarly.",
            ),
            "оклад": (
                "salary",
                "Его оклад вырос.",
                "His salary grew.",
            ),
            "бармен": (
                "bartender",
                "Бармен налил вино.",
                "The bartender poured wine.",
            ),
            "вытеснить": (
                "displace",
                "Они вытеснили конкурента.",
                "They displaced the competitor.",
            ),
            "брюхо": (
                "belly",
                "У него большое брюхо.",
                "He has a big belly.",
            ),
            "прибавлять": (
                "to add",
                "Она прибавляет соль.",
                "She adds salt.",
            ),
            "джаз": (
                "jazz",
                "Я люблю джаз.",
                "I love jazz.",
            ),
            "факел": (
                "torch",
                "Он нёс факел.",
                "He carried the torch.",
            ),
            "наличный": (
                "cash",
                "Это наличная оплата.",
                "This is a cash payment.",
            ),
            "темперамент": (
                "temperament",
                "У неё живой темперамент.",
                "She has a lively temperament.",
            ),
            "смещение": (
                "shift, displacement",
                "Это смещение власти.",
                "This is a shift of power.",
            ),
            "участница": (
                "participant",
                "Она участница конкурса.",
                "She is a participant in the contest.",
            ),
            "байка": (
                "tall tale",
                "Он рассказал старую байку.",
                "He told an old tall tale.",
            ),
            "сводный": (
                "step, consolidated",
                "Он мой сводный брат.",
                "He is my step brother.",
            ),
            "заимствовать": (
                "borrow",
                "Он заимствует слова из английского.",
                "He borrows words from English.",
            ),
            "капать": (
                "drip",
                "Вода капает из крана.",
                "Water drips from the tap.",
            ),
            "подножие": (
                "foot",
                "Мы стоим у подножия горы.",
                "We stand at the foot of the mountain.",
            ),
            "вынуждать": (
                "to force",
                "Он вынуждает меня лгать.",
                "He is forcing me to lie.",
            ),
            "листочек": (
                "small leaf",
                "На земле лежит листочек.",
                "A small leaf lies on the ground.",
            ),
            "забиться": (
                "to hide",
                "Она забилась в угол.",
                "She hid in the corner.",
            ),
            "удостоить": (
                "to honor",
                "Его удостоили награды.",
                "They honored him with an award.",
            ),
            "очищать": (
                "to cleanse",
                "Она очищает рану.",
                "She is cleansing the wound.",
            ),
            "патология": (
                "pathology",
                "Он изучает патологию.",
                "He studies pathology.",
            ),
            "синоним": (
                "synonym",
                "Это синоним слова дом.",
                "This is a synonym of the word house.",
            ),
            "принуждение": (
                "coercion",
                "Это было принуждение.",
                "This was coercion.",
            ),
            "зонтик": (
                "umbrella",
                "Она забыла зонтик дома.",
                "She forgot her umbrella at home.",
            ),
            "подошва": (
                "sole",
                "У ботинка толстая подошва.",
                "The boot has a thick sole.",
            ),
            "сирена": (
                "siren",
                "Сирена громко кричит.",
                "The siren screams loudly.",
            ),
            "гнилой": (
                "rotten",
                "Это гнилое яблоко.",
                "This is a rotten apple.",
            ),
            "локомотив": (
                "locomotive",
                "Старый локомотив ещё работает.",
                "The old locomotive still works.",
            ),
            "понестись": (
                "to rush",
                "Он понесся домой.",
                "He rushed home.",
            ),
            "растерять": (
                "lose",
                "Он растерял всех друзей.",
                "He lost all his friends.",
            ),
            "хирургический": (
                "surgical",
                "Ему нужна хирургическая помощь.",
                "He needs surgical help.",
            ),
            "потащить": (
                "to drag",
                "Он потащил чемодан.",
                "He dragged the suitcase.",
            ),
            "льготный": (
                "preferential",
                "У него льготный билет.",
                "He has a preferential ticket.",
            ),
            "воронежский": (
                "Voronezh",
                "Это воронежский поезд.",
                "This is a Voronezh train.",
            ),
            "делегат": (
                "delegate",
                "Делегат говорил первым.",
                "The delegate spoke first.",
            ),
            "параграф": (
                "paragraph",
                "Прочитай этот параграф.",
                "Read this paragraph.",
            ),
            "унижать": (
                "humiliate",
                "Не унижай его.",
                "Don't humiliate him.",
            ),
            "доступность": (
                "availability",
                "Доступность воды важна.",
                "The availability of water is important.",
            ),
            "изумительный": (
                "amazing",
                "Вид просто изумительный.",
                "The view is simply amazing.",
            ),
            "уделяться": (
                "to be given, to be devoted",
                "Много внимания уделяется спорту.",
                "Much attention is given to sport.",
            ),
            "расхождение": (
                "discrepancy",
                "Есть расхождение в цифрах.",
                "There is a discrepancy in the figures.",
            ),
            "сокол": (
                "falcon",
                "Сокол летит высоко.",
                "The falcon flies high.",
            ),
        },
    )
)
