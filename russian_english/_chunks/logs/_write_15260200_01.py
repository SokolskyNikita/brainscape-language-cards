import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from russian_english._chunk_io import rewrite_chunk

print(
    rewrite_chunk(
        Path("russian_english/_chunks/deck_15260200_01.csv"),
        {
            "преступный": (
                "criminal, felonious",
                "Это преступный план.",
                "This is a criminal plan.",
            ),
            "крыльцо": (
                "porch, stoop",
                "Мы сидели на крыльце.",
                "We sat on the porch.",
            ),
            "издавать": (
                "to publish, to issue",
                "Она издаёт книгу.",
                "She publishes a book.",
            ),
            "рубрика": (
                "column, section",
                "Я читаю эту рубрику.",
                "I read this column.",
            ),
            "поражать": (
                "strike, amaze",
                "Молния поразила дом.",
                "Lightning struck the house.",
            ),
            "укрепить": (
                "strengthen, reinforce",
                "Мы укрепили стену.",
                "We strengthened the wall.",
            ),
            "драма": (
                "drama, play",
                "Это сильная драма.",
                "This is a strong drama.",
            ),
            "концентрация": (
                "concentration, focus",
                "Концентрация соли высока.",
                "The salt concentration is high.",
            ),
            "заблуждение": (
                "delusion, misconception",
                "Это простое заблуждение.",
                "This is a simple delusion.",
            ),
            "налево": (
                "to the left, left",
                "Иди налево.",
                "Go to the left.",
            ),
            "дева": (
                "virgin, maiden",
                "Она ещё дева.",
                "She is still a virgin.",
            ),
            "перемещение": (
                "displacement, movement",
                "Это большое перемещение.",
                "This is a big movement.",
            ),
            "спектр": (
                "spectrum, range",
                "Спектр света широкий.",
                "The spectrum of light is wide.",
            ),
            "командировка": (
                "business trip, assignment",
                "Он сейчас в командировке.",
                "He is on a business trip now.",
            ),
            "махать": (
                "wave, flap",
                "Она машет рукой.",
                "She is waving her hand.",
            ),
            "комплексный": (
                "comprehensive, integrated",
                "Нужен комплексный подход.",
                "We need a comprehensive approach.",
            ),
            "удачно": (
                "successfully, fortunately",
                "Всё прошло удачно.",
                "Everything went successfully.",
            ),
            "щель": (
                "crack, slit",
                "Свет идёт через щель.",
                "Light comes through the crack.",
            ),
            "стальной": (
                "steel",
                "Это стальной мост.",
                "This is a steel bridge.",
            ),
            "звуковой": (
                "sound, acoustic",
                "Это звуковой сигнал.",
                "This is a sound signal.",
            ),
            "простота": (
                "simplicity, easiness",
                "Мне нравится простота.",
                "I like the simplicity.",
            ),
            "актриса": (
                "actress, female actor",
                "Актриса вышла на сцену.",
                "The actress came on stage.",
            ),
            "ограничивать": (
                "to limit, to restrict",
                "Мы ограничиваем расходы.",
                "We limit expenses.",
            ),
            "чудовищный": (
                "monstrous, hideous",
                "Это чудовищный сон.",
                "This is a monstrous dream.",
            ),
            "рог": (
                "horn, antler",
                "Рог был очень большой.",
                "The horn was very large.",
            ),
            "грек": (
                "Greek, Hellene",
                "Мой друг — грек.",
                "My friend is Greek.",
            ),
            "выезжать": (
                "to leave, to depart",
                "Мы выезжаем утром.",
                "We leave in the morning.",
            ),
            "совершение": (
                "commitment, perpetration",
                "Совершение преступления ясно.",
                "The perpetration of the crime is clear.",
            ),
            "прелесть": (
                "charm, delight",
                "Её улыбка — чистая прелесть.",
                "Her smile is pure charm.",
            ),
            "заключать": (
                "conclude, contain",
                "Они заключают договор.",
                "They conclude a contract.",
            ),
            "помолчать": (
                "to be silent, to keep quiet",
                "Я решил помолчать.",
                "I decided to be silent.",
            ),
            "поработать": (
                "to work, to labor",
                "Мне нужно поработать завтра.",
                "I need to work tomorrow.",
            ),
            "чуждый": (
                "alien, foreign",
                "Его идеи мне чужды.",
                "His ideas are alien to me.",
            ),
            "осознание": (
                "realization, awareness",
                "Пришло важное осознание.",
                "An important realization came.",
            ),
            "потянуть": (
                "pull, stretch",
                "Потяни дверь.",
                "Pull the door.",
            ),
            "возврат": (
                "return, refund",
                "Я хочу возврат.",
                "I want a refund.",
            ),
            "коричневый": (
                "brown, chestnut",
                "Коричневый стол стоит тут.",
                "The brown table stands here.",
            ),
            "напрямую": (
                "directly, straight",
                "Он говорил со мной напрямую.",
                "He spoke to me directly.",
            ),
            "силовой": (
                "power, forceful",
                "Это силовой удар.",
                "This is a power blow.",
            ),
            "недоумение": (
                "bewilderment, perplexity",
                "Я в полном недоумении.",
                "I am in complete bewilderment.",
            ),
            "шкура": (
                "hide, skin",
                "Шкура медведя даёт тепло.",
                "The bear's hide gives heat.",
            ),
            "армейский": (
                "army, military",
                "Он носит армейскую одежду.",
                "He wears army clothing.",
            ),
            "ислам": (
                "Islam",
                "Ислам — его религия.",
                "Islam is his religion.",
            ),
            "залить": (
                "pour, flood",
                "Залейте воду в стакан.",
                "Pour water into the glass.",
            ),
            "предварительно": (
                "preliminarily, in advance",
                "Скажи мне предварительно.",
                "Tell me in advance.",
            ),
            "упаковка": (
                "packaging, package",
                "Упаковка товара крепкая.",
                "The packaging of the goods is strong.",
            ),
            "неизменный": (
                "unchanging, constant",
                "Её верность неизменна.",
                "Her loyalty is unchanging.",
            ),
            "ликвидация": (
                "liquidation, elimination",
                "Компания начала ликвидацию.",
                "The company started liquidation.",
            ),
            "царить": (
                "reign, rule",
                "В доме царит тишина.",
                "Silence reigns in the house.",
            ),
            "винтовка": (
                "rifle, gun",
                "Он взял свою винтовку.",
                "He took his rifle.",
            ),
            "перевозка": (
                "transportation, carriage",
                "Перевозка груза идёт.",
                "The transportation of the load is going.",
            ),
            "долгосрочный": (
                "long-term, long-range",
                "Это долгосрочный план.",
                "This is a long-term plan.",
            ),
            "отклик": (
                "response, feedback",
                "Её отклик был быстрым.",
                "Her response was quick.",
            ),
            "абстрактный": (
                "abstract, conceptual",
                "Его искусство абстрактно.",
                "His art is abstract.",
            ),
            "неудачный": (
                "unsuccessful, failed",
                "Попытка была неудачной.",
                "The attempt was unsuccessful.",
            ),
            "сюрприз": (
                "surprise, shock",
                "Вечеринка была сюрпризом.",
                "The party was a surprise.",
            ),
            "вырвать": (
                "to pull out, to tear out",
                "Он вырвал зуб.",
                "He pulled out the tooth.",
            ),
            "наследник": (
                "heir, successor",
                "Принц — наследник короля.",
                "The prince is the king's heir.",
            ),
            "похороны": (
                "funeral, burial",
                "Они были на похоронах.",
                "They were at the funeral.",
            ),
            "довод": (
                "argument, reason",
                "Ваш довод очень сильный.",
                "Your argument is very strong.",
            ),
            "мусульманин": (
                "Muslim, Moslem",
                "Он мусульманин.",
                "He is a Muslim.",
            ),
            "набить": (
                "stuff, pad",
                "Я набью сумку.",
                "I will stuff the bag.",
            ),
            "убирать": (
                "to clean, to remove",
                "Я убираю комнату.",
                "I am cleaning my room.",
            ),
            "менеджмент": (
                "management, administration",
                "Менеджмент знает своё дело.",
                "Management knows its work.",
            ),
            "огненный": (
                "fiery, flaming",
                "Дракон дал огненное дыхание.",
                "The dragon gave a fiery breath.",
            ),
            "окошко": (
                "window, little window",
                "Открой окошко.",
                "Open the window.",
            ),
            "аналитический": (
                "analytical, analytic",
                "У неё очень аналитический ум.",
                "She has a very analytical mind.",
            ),
            "благополучно": (
                "safely, successfully",
                "Мы благополучно пришли домой.",
                "We arrived home safely.",
            ),
            "стадо": (
                "herd, flock",
                "Стадо стоит у реки.",
                "The herd stands by the river.",
            ),
            "упоминаться": (
                "to be mentioned, to be referred to",
                "Его имя упоминается часто.",
                "His name is mentioned often.",
            ),
            "порция": (
                "portion, serving",
                "Она съела порцию супа.",
                "She ate a portion of soup.",
            ),
            "тротуар": (
                "sidewalk, pavement",
                "Иди по тротуару.",
                "Walk on the sidewalk.",
            ),
            "паника": (
                "panic, hysteria",
                "В зале началась паника.",
                "Panic started in the hall.",
            ),
            "рейс": (
                "flight, voyage",
                "Рейс уже готов.",
                "The flight is already ready.",
            ),
            "рождество": (
                "Christmas, Nativity",
                "Рождество уже близко.",
                "Christmas is already near.",
            ),
            "ручной": (
                "manual, hand-held",
                "Это ручной труд.",
                "This is manual labor.",
            ),
            "светский": (
                "secular, worldly",
                "Это светский вечер.",
                "This is a secular evening.",
            ),
            "обстоять": (
                "to stand, to be (the case)",
                "Как обстоят дела?",
                "How do things stand?",
            ),
            "характеризовать": (
                "characterize, describe",
                "Как ты характеризуешь его?",
                "How do you characterize him?",
            ),
            "мат": (
                "checkmate, foul language",
                "Не говори мат.",
                "Don't use foul language.",
            ),
            "академический": (
                "academic, scholarly",
                "Это академический год.",
                "This is an academic year.",
            ),
            "колебаться": (
                "hesitate, waver",
                "Он ещё колеблется.",
                "He still hesitates.",
            ),
            "запереть": (
                "lock up, lock",
                "Запри дом.",
                "Lock the house.",
            ),
            "наверху": (
                "upstairs, above",
                "Кот спит наверху.",
                "The cat is sleeping upstairs.",
            ),
            "пробить": (
                "pierce, break through",
                "Пуля пробила дверь.",
                "The bullet pierced the door.",
            ),
            "сходство": (
                "similarity, resemblance",
                "Сходство между ними сильное.",
                "The similarity between them is strong.",
            ),
            "вздрогнуть": (
                "startle, flinch",
                "Я вздрогнул от шума.",
                "I flinched from the noise.",
            ),
            "осмотр": (
                "inspection, examination",
                "Врач начал осмотр.",
                "The doctor started the examination.",
            ),
            "осторожный": (
                "cautious, careful",
                "Он очень осторожный.",
                "He is very cautious.",
            ),
            "терапия": (
                "therapy, treatment",
                "Ей нужна терапия.",
                "She needs therapy.",
            ),
            "этнический": (
                "ethnic, ethnical",
                "Это этнический праздник.",
                "This is an ethnic holiday.",
            ),
            "глазок": (
                "peephole, eyepiece",
                "Она смотрит в глазок.",
                "She looks through the peephole.",
            ),
            "становление": (
                "formation, establishment",
                "Его становление было долгим.",
                "His formation was long.",
            ),
            "плакат": (
                "poster, placard",
                "Я видел плакат на стене.",
                "I saw a poster on the wall.",
            ),
            "вечеринка": (
                "party, gathering",
                "Вечеринка уже началась.",
                "The party has already started.",
            ),
            "основываться": (
                "to be based, to rely",
                "Теория основывается на фактах.",
                "The theory is based on facts.",
            ),
            "наряд": (
                "outfit, dress",
                "Ей нравится новый наряд.",
                "She likes her new outfit.",
            ),
            "покойный": (
                "deceased, late",
                "Покойный отец любил нас.",
                "The late father loved us.",
            ),
            "обожать": (
                "adore, worship",
                "Я обожаю эту песню.",
                "I adore this song.",
            ),
            "блестеть": (
                "shine, sparkle",
                "Звёзды блестят ночью.",
                "Stars shine at night.",
            ),
        },
    )
)
