import sys

sys.path.insert(0, "repair_20260907")
from helper import save


DECK_15260210 = {
    10: ("нора", "burrow", "Нора в лесу.", "The burrow is in the forest."),
    25: ("прижимать", "to press", "Она прижимает книгу к себе.", "She presses the book to herself."),
    60: ("дрожь", "shiver", "Меня взяла дрожь.", "A shiver ran through me."),
    79: ("перенос", "postponement", "Перенос встречи назначен на пятницу.", "The postponement is set for Friday."),
    93: ("недаром", "not for nothing", "Недаром его любят.", "They love him not for nothing."),
    167: ("задыхаться", "to suffocate", "Я задыхаюсь.", "I am suffocating."),
    198: ("влезть", "to climb through", "Он влез в окно.", "He climbed through the window."),
    203: ("гудеть", "to hum", "Холодильник гудит.", "The refrigerator hums."),
    240: ("практиковать", "to practice", "Она практикует язык.", "She practices the language."),
    256: ("отказывать", "to refuse", "Он мне отказывает.", "He refuses my request."),
    312: ("передвигаться", "to move", "Он передвигается медленно.", "He moves slowly."),
    303: ("переть", "to lug", "Тяжело переть мешок.", "It is hard to lug the sack."),
    314: ("вцепиться", "to cling", "Он вцепился в меня.", "He clung to me."),
    338: ("рассыпаться", "to spill", "Сахар рассыпался.", "The sugar spilled."),
    362: ("направленность", "direction", "Его направленность ясна.", "Its direction is clear."),
    370: ("хитрость", "trick", "Это его хитрость.", "This is his trick."),
    390: ("сливаться", "to merge", "Реки сливаются.", "The rivers merge."),
    429: ("возложить", "to lay", "Возложи ответственность на него.", "Lay responsibility on him."),
    490: ("питерский", "from Petersburg", "Это питерский друг.", "This is a friend from Petersburg."),
}

DECK_15260213 = {
    12: ("просматривать", "to look through", "Я просматриваю почту.", "I look through the mail."),
    17: ("пират", "pirate", "Пират украл золото.", "The pirate stole gold."),
    19: ("востребовать", "to demand repayment", "Он востребовал свой долг.", "He demanded repayment of the debt."),
    37: ("общность", "common ground", "Между ними есть общность взглядов.", "They share common ground."),
    52: ("испуганно", "in fright", "Она испуганно оглянулась.", "She looked back in fright."),
    53: ("досада", "annoyance", "Какая досада!", "What an annoyance!"),
    72: ("супружеский", "married", "У них спокойная супружеская жизнь.", "They have a quiet married life."),
    77: ("живописный", "picturesque", "Какой живописный вид!", "What a picturesque view!"),
    79: ("нежелательный", "undesirable", "Это нежелательная привычка.", "This is an undesirable habit."),
    95: ("лопнуть", "burst", "Шарик внезапно лопнул.", "The ball burst suddenly."),
    105: ("зубной", "dental", "Зубная боль сильная.", "The dental pain is severe."),
    113: ("диагностика", "diagnostics", "Диагностика ещё идёт.", "The diagnostics continue."),
    126: ("архангельский", "Arkhangelsk", "Архангельский порт открыт.", "The Arkhangelsk port is open."),
    196: ("рывок", "lurch", "Рывок был неожиданным.", "The lurch was unexpected."),
    208: ("порадовать", "to please", "Надо порадовать их.", "We must please them."),
    241: ("уран", "uranium", "Уран — металл.", "Uranium is a metal."),
    254: ("загореться", "to catch fire", "Дом загорелся ночью.", "The house caught fire at night."),
    261: ("обучить", "to teach", "Он обучил сына.", "He taught his son."),
    271: ("заведомо", "obviously", "Это заведомо плохой план.", "This is an obviously bad plan."),
    274: ("старшина", "sergeant major", "Старшина дал приказ.", "The sergeant major gave an order."),
    284: ("сбрасывать", "to dump", "Не сбрасывай снег на дорогу.", "Don't dump snow on the road."),
    294: ("жать", "to squeeze", "Не жми мне руку.", "Don't squeeze my hand."),
    302: ("задаваться", "to wonder", "Он начал задаваться вопросом.", "He began to wonder."),
    314: ("проникновение", "break-in", "Проникновение было ночью.", "The break-in happened at night."),
    365: ("правота", "being right", "Я вижу его правоту.", "I see that he is right."),
    377: ("поздороваться", "to say hello", "Я хочу поздороваться.", "I want to say hello."),
    391: ("обмениваться", "to exchange", "Мы хотим обмениваться книгами.", "We want to exchange books."),
    400: ("ценовой", "pricing", "Это ценовой вопрос.", "This is a pricing issue."),
    404: ("досуг", "free time", "У меня есть досуг.", "I have free time."),
    412: ("отбирать", "to select", "Они хотят отбирать лучших.", "They want to select the best."),
    432: ("острота", "sharpness", "Острота ножа важна.", "The knife's sharpness is important."),
    453: ("пробыть", "to stay", "Я хочу пробыть неделю.", "I want to stay for a week."),
    484: ("заблудиться", "to get lost", "Здесь можно заблудиться.", "You can get lost here."),
    487: ("впасть", "to fall asleep", "Он может впасть в сон.", "He may fall asleep."),
    498: ("нравственность", "morality", "Нравственность важна.", "Morality is important."),
}


save(
    "russian_english",
    "15260210",
    DECK_15260210,
    reviewed=500,
    notes="Reviewed all 500 rows in 100-card batches; repaired vocabulary leakage, collocations, aspect/tense, and misleading examples.",
)
save(
    "russian_english",
    "15260213",
    DECK_15260213,
    reviewed=500,
    notes="Reviewed all 500 rows in 100-card batches; repaired vocabulary leakage, collocations, aspect/tense, and misleading examples.",
)
