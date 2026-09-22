import sys

sys.path.insert(0, 'repair_20260907')
from helper import save


PATCH_15260190 = {
    12: ('крыша', 'roof', 'Крыша дома.', 'The roof of the house.'),
    35: ('брак', 'marriage', 'Это долгий брак.', "It's a long marriage."),
    36: ('стекло', 'glass', 'Стекло чистое.', 'The glass is clean.'),
    32: ('привыкнуть', 'to get used to', 'Я хочу привыкнуть к этому.', 'I want to get used to this.'),
    44: ('гореть', 'to burn, to be on', 'Огонь горит.', 'The fire is burning.'),
    87: ('соответственно', 'accordingly, therefore', 'Он занят и, соответственно, не придёт.', 'He is busy and therefore will not come.'),
    101: ('удобный', 'convenient, comfortable', 'Здесь удобно.', "It's comfortable here."),
    105: ('шея', 'neck', 'Шея длинная.', 'The neck is long.'),
    119: ('собирать', 'to collect, to gather', 'Я собираю книги.', 'I am collecting books.'),
    146: ('ожидание', 'waiting, expectation', 'Долгое ожидание.', 'A long wait.'),
    147: ('господь', 'Lord, God', 'О Господи!', 'Lord!'),
    161: ('водитель', 'driver', 'Водитель здесь.', 'The driver is here.'),
    185: ('обращать', 'to turn, to direct', 'Обращай внимание на это.', 'Turn your attention to this.'),
    198: ('задать', 'to pose, to assign', 'Задай вопрос.', 'Pose a question.'),
    222: ('обратный', 'return, reverse', 'Обратная сторона?', 'The reverse side?'),
    228: ('передавать', 'to pass on', 'Я передаю это ему.', "I'm passing it on to him."),
    252: ('крыло', 'wing', 'У птицы есть крыло.', 'The bird has a wing.'),
    278: ('попадать', 'to get into, to hit', 'Я попадаю в цель.', 'I hit it.'),
    274: ('принятие', 'acceptance, adoption', 'Принятие закона важно.', 'Adoption of the law is important.'),
    281: ('следовательно', 'therefore', 'Следовательно, всё хорошо.', 'Therefore, everything is good.'),
    297: ('крепкий', 'strong', 'Крепкий чай.', 'The tea is strong.'),
    299: ('генеральный', 'general, chief', 'Генеральный план готов.', 'The general plan is ready.'),
    304: ('китайский', 'Chinese', 'Любишь китайский чай?', 'Do you like Chinese tea?'),
    318: ('символ', 'symbol', 'Это символ жизни.', "It's a symbol of life."),
    343: ('полтора', 'one and a half', 'Полтора часа прошло.', 'One and a half hours have passed.'),
    353: ('представляться', 'to introduce oneself', 'Он представляется.', 'He introduces himself.'),
    365: ('бок', 'side', 'Левый бок.', 'The left side.'),
    461: ('живот', 'stomach, belly', 'Живот полный.', 'The stomach is full.'),
    480: ('утверждение', 'statement, assertion', 'Это утверждение верно?', 'Is that statement right?'),
}

PATCH_15260191 = {
    32: ('строй', 'formation, order', 'Кто в строю?', "Who's in formation?"),
    86: ('вслед', 'after, following', 'Он идёт вслед за мной.', 'He walks after me.'),
    155: ('программный', 'software, program', 'Программный продукт.', 'A software product.'),
    180: ('ремонт', 'renovation, repairs', 'Идёт ремонт.', 'The repairs continue.'),
    309: ('спектакль', 'play, show', 'Идём на спектакль?', 'Shall we go to the play?'),
    229: ('сдать', 'to pass, to hand in', 'Я сдал это.', 'I passed it.'),
    233: ('удача', 'luck, fortune', 'Удачи тебе!', 'Good luck to you!'),
    414: ('судно', 'ship, vessel', 'Судно уже здесь.', 'The ship is here already.'),
    365: ('предназначить', 'to destine, to assign', 'Это ей предназначено.', 'This is destined for her.'),
    390: ('богатство', 'wealth', 'Какое богатство!', 'What wealth!'),
    419: ('впоследствии', 'afterwards, subsequently', 'Впоследствии всё стало ясно.', 'Afterwards everything became clear.'),
    422: ('пахнуть', 'to smell', 'Хлеб хорошо пахнет.', 'The bread smells good.'),
    445: ('особенный', 'special, particular', 'Это особенный день.', "It's a special day."),
    443: ('побежать', 'to run, to dash', 'Он побежал в магазин.', 'He ran to the store.'),
    446: ('предоставлять', 'to provide, to grant', 'Они предоставляют доступ.', 'They provide access.'),
    447: ('раздаться', 'to ring out', 'Раздался звонок.', 'The call rang out.'),
    451: ('пустить', 'to let, to release', 'Пусти меня!', 'Let me go!'),
    453: ('подавать', 'to pass, to serve', 'Она подаёт чай.', 'She serves tea.'),
    460: ('исчезать', 'to disappear, to vanish', 'Всё исчезает слишком быстро.', 'Everything disappears too fast.'),
    462: ('замуж', 'married, to marry', 'Она хочет замуж.', 'She wants to get married.'),
    480: ('нанести', 'to apply, to inflict', 'Нанеси удар.', 'Inflict a blow.'),
}

PATCH_15260192 = {
    1: ('дар', 'gift, talent', 'У неё дар.', 'She has a gift.'),
    14: ('ловить', 'to catch', 'Лови меня!', 'Catch me!'),
    250: ('пожать', 'to shake, to squeeze', 'Давай пожмём руки.', "Let's shake hands."),
    44: ('явный', 'obvious, clear', 'Это явная ошибка.', 'This is an obvious mistake.'),
    54: ('коммунист', 'communist', 'Мой дед коммунист.', 'My grandfather is a communist.'),
    56: ('двенадцать', 'twelve', 'Ровно двенадцать.', 'Exactly twelve.'),
    280: ('раскрыть', 'to reveal', 'Не раскрой секрет.', "Don't reveal the secret."),
    284: ('задержать', 'to delay, to detain', 'Они задержали его.', 'They detained him.'),
    286: ('мелочь', 'small change, trifle', 'Есть мелочь?', 'Do you have any small change?'),
    337: ('мотор', 'engine, motor', 'Мотор работает.', 'The engine is running.'),
    354: ('компонент', 'component', 'Компонент нужен.', 'The component is needed.'),
    382: ('законодательный', 'legislative', 'Законодательная власть.', 'Legislative power.'),
    390: ('слуга', 'servant', 'Слуга здесь.', 'The servant is here.'),
    273: ('нежели', 'than', 'Лучше сейчас, нежели потом.', 'Better now than later.'),
    282: ('временной', 'time (attributive), temporal', 'Это временной ряд.', "That's a time series."),
    283: ('надоесть', 'to get tired of', 'Мне это надоело.', 'I got tired of this.'),
}


if __name__ == '__main__':
    save('russian_english', '15260190', PATCH_15260190, reviewed=500,
         notes='Reviewed all 500 rows in 100-card batches; repaired vocabulary-sequence violations, awkward examples, and aspect mismatches.')
    save('russian_english', '15260191', PATCH_15260191, reviewed=500,
         notes='Reviewed all 500 rows in 100-card batches; repaired vocabulary-sequence violations, awkward examples, and aspect mismatches.')
    save('russian_english', '15260192', PATCH_15260192, reviewed=500,
         notes='Reviewed all 500 rows in 100-card batches; repaired vocabulary-sequence violations, awkward examples, and aspect mismatches.')
