# ПАМЯТКА


# -ЧТОБЫ ИСПОЛЬЗОВАТЬ ЦВЕТ, НУЖНО ИСПОЛЬЗОВАТЬ {color:int, int, int} ... {/color}, ГДЕ ВМЕСТО ... ДОЛЖНЫ БЫТЬ СЛОВА, А int ПРИНАДЛЕЖИТ ОТ 0 ДО 255


# -ЧТОБЫ СДЕЛАТЬ ПАУЗУ, НУЖНО ПОСТАВИТЬ СИМВОЛ |, А УЖЕ В DialogPhrase ЗАДАТЬ ПАРАМЕТР pause=float, ГДЕ float - ПРОДОЛЖИТЕЛЬНОСТЬ ЗАДЕРЖКИ В СЕКУНДАХ
# ЛИБО МОЖНО ПОНАТЫКАТЬ | сколь угодно раз, по дефолту одна пауза равна 0.15 с. И вообще пауза идёт автоматом после знаков препинания
# так что не обязательно тыкать | везде
LANGUAGES = {
    'play_button': ['Играть', 'Play', 'Luaj'],
    'settings_button': ['Настройки', 'Settings', 'Cilësimet'],
    'change_language': ['Язык:', 'Language:', 'Gjuha:'],
    'language': ['Русский', 'English', 'Shqiptare'],
    'music': ['Музыка', 'Music', 'Muzikë'],
    'creators': ['Создатели', 'Creators', 'Krijuesit'],
    'full_screen_mode': ['Полный экран', 'Full screen', 'Ekran të plotë'],
    'press_for_cont': ['Нажмите для продолжения', 'Click to continue', 'Klikoni për të vazhduar'],
    'Esc_to_return': ['Нажмите ECS для возвращения', 'Press ESC to return', 'shtypni ESC për t\'u kthyer'],
    # 'Alexey Jid': ['Лёха Жидковский', 'Lech Zhidkovsky', 'Lech Zhidkovsky'],
    'Glossary': ['Глоссарий', 'Glossary', 'Fjalori'],
    'episodes': ['Эпизод', 'Episode', 'Episodi'],
    'monologues': {
        '1': ['Какие к чёрту аномалии? Почему я должен расхлебывать всё это за других?', 'What the hell kind of anomalies are these? Why do I have to clean up this mess for everyone else?', 'Ç\'dreqin janë këto anomalira? Pse më qëlloi mua të pastroj gjëmën e të tjerëve?'],
        '2': ['Агх, ладно, ничего не поделаешь, зная наше правительство, лучше сделать всё так, как они сказали, иначе...', 'Ugh, fine. Nothing we can do – knowing our government, better do everything how they said, or else...', 'Uff, në rregull, s\'ka ç\'të bësh – duke e ditur qeverinë tonë, më mirë bëje gjithçka ashtu si thanë ata, përndryshe...'],
        '3': ['Кто в здравом уме пойдет к дому отшельника?', 'Who in their right mind would go to a hermit\'s house?', 'Kush me mendje të shëndoshë do të shkonte në shtëpinë e një ermolit?'],
        '4': ['Ладно, открою.', 'Fine, I\'ll open it.', 'Në rregull, do ta hap.'],
        '5': ['Никогда не любил этого почтальона, от него несёт какой-то напыщенностью что ли.', 'Never liked that mailman. He reeks of arrogance or something.', 'Asnjëherë s\'më ka pëlqyer ai postieri. Vjen nga ai me diçka të fryrë, apo çfarë.'],
        '6': ['', '', ''],
        '7': ['', '', ''],
        '8': ['', '', ''],
        '9': ['', '', ''],
        '10': ['', '', ''],
        '11': ['', '', ''],
        '12': ['', '', ''],
        '13': ['', '', ''],
        '14': ['', '', ''],
        '15': ['', '', '']

    },
    'dialogues': {
        'ui_sound_desc': {
            'knocking': ['Стук в дверь. . .', 'A knock at the door. . .', 'Trokitje në derë. . .']
        },
        'postman_talkings': {
            '1': ['Доброго здоровья-с.| Осмелюсь побеспокоить. Не изволите ли вы быть господином Н.?', 'Good day to you, sir. | I beg your pardon for the disturbance. Might you be Mr. N.?', 'Tungjatjeta, zotëri. | Më falni që ju shqetësoj. A do të ishit ju, ndoshta, z. N.?'],

            '2': ['Да, так и есть.', 'Yes, indeed I am.', 'Po, pikërisht ashtu.'],

            '3': ['Чрезвычайно рад-с. Имею честь вручить вам корреспонденцию казённой почты.', 'Most delighted, sir. I have the honour of delivering to you official state correspondence.', 'Gëzim i madh, zotëri. Kam nderin t\'ju dorëzoj korrespondencë zyrtare të postës së shtetit.'],
            '4': ['Потрудитесь соблаговолить принять оную и удостоверить факт получения вашей собственноручной росписью в сём формуляре.', 'Kindly deign to accept it and confirm the fact of receipt with your personal signature on this form.', 'Ju lutem të pranoni dhe të vërtetoni marrjen me nënshkrimin tuaj personal në këtë formular.'],
            '5': ['Здесь, под строкой, означенной «получатель»-с.', 'Here, under the line marked «recipient», sir.', 'Këtu, nën vijën e shënuar «marrësi», zotëri.'],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],
            '': ['', '', ''],

        },
        'phone_talkings': {
            'calling': ['Звонок. . .', 'The phone rings. . .', 'Bërtet telefoni. . .'],
            'hanging_up': ['Конец звонка. . .', 'The call ends. . .', 'Telefonia mbaron. . .'],
            '1episode': {
                '1': ['Здравствуй, есть минутка?', 'Hey, got a minute?', 'Ç\'kemi, ke një minutë?'],

                '2': ['Кто это говорит?', 'Who is this speaking?', 'Kush foli atje?'],

                '3': ['Неважно, пока неважно.|| Кстати, этот разговор записывается.', 'Doesn\'t matter, not yet anyway. || By the way, this call is being recorded.', 'S\'ka rëndësi, ende jo. || Me që ra fjala, ky bisedë po regjistrohet.'],

                '4': ['К чему всё это?| Я вроде бы нигде не косячил, чтобы заслуживать такого...', 'What\'s all this about? | I haven\'t screwed up anywhere to deserve this, have I...', 'Për ç\'është fjala? | S\'kam gabuar askund që ta meritoja këtë, s\'kam...'],

                '5': ['Дело не в тебе, ну, почти.| По нашей информации, ты - лесничий, живущий подальше от деревни, так?', 'It\'s not about you, well, almost. | According to our information, you\'re the forest warden living away from the village, correct?', 'Bëhet fjalë për ty, mirë, pothuajse. | Sipas informacionit tonë, ti je pylltari që jeton larg nga fshati, apo jo?'],

                '6': ['Да, но кто-нибудь объяснит, что происходит?!', 'Yes, but is anyone going to explain what\'s going on?!', 'Po, por a do më shpjegon dikush ç\'po ndodh?!'],

                '7': ['Слушай, если кратко, то в твоих окрестностях происходят| {color:51,110,25}странные вещи{/color}.', 'Listen, in short, there are | {color:51,110,25}strange things{/color} happening around your area.', 'Dëgjo, shkurt, në zonën tënde po ndodhin | {color:51,110,25}gjëra të çuditshme{/color}.'],
                '8': ['Некоторые люди пропадают,|| некоторые сходят с ума.', 'Some people are disappearing, || others are losing their minds.', 'Disa njerëz po zhduken, || disa po çmenden.'],
                '9': ['Мы отправляли группу исследователей к вам, но она не доехала.', 'We sent a team of researchers your way, but they never made it.', 'Dërguam një grup kërkuesish te ju, por ata s\'arritën kurrë atje.'],
                '10': ['Остальные силы направлены на Южный фронт, мы не можем перенести их.', 'The remaining forces are deployed to the Southern Front; we can\'t redeploy them.', 'Forcat e mbetura janë dërguar në Frontin Jugor; nuk mund t\'i zhvendosim.'],

                '11': ['Но почему я?|| Я могу отказаться? Неужели не нашлось кого-то из деревни, кто смог бы?', 'But why me? || Can I refuse? Surely there\'s someone from the village who could do it?', 'Por përse unë? || Mund të refuzoj? Me siguri ka dikë nga fshati që mund ta bëjë?'],

                '12': ['{color:99,11,15}Это не просьба.{/color}', '{color:99,11,15}This is not a request.{/color}', '{color:99,11,15}Kjo nuk është një kërkesë.{/color}'],
                '13': ['По нашим данным, частое социальное взаимодействие как раз приводит к этим |{color:51,110,25}неизвестным последствиям{/color}.', 'According to our data, frequent social interaction is precisely what leads to these | {color:51,110,25}unknown consequences{/color}.', 'Sipas të dhënave tona, bashkëveprimi i shpeshtë shoqëror është pikërisht ajo që çon në këto | {color:51,110,25}pasojat e panjohura{/color}.'],
                '14': ['Ты единственный отшельник в этой деревушке.', 'You\'re the only hermit in this hamlet.', 'Ti je i vetmi ermit në këtë fshatëz.'],

                '15': ['Понял...| А что мне собственно нужно делать?', 'Understood... | So what exactly do I need to do?', 'E kuptova... | Pra çfarë saktësisht duhet të bëj?'],

                '16': ['Всё очень просто. Сегодня вечером {color:51,110,25}почтальон{/color} доставит тебе нашу последнюю техническую разработку - {color:51,110,25}особую камеру{/color}.', 'It\'s very simple. This evening, the {color:51,110,25}mailman{/color} will deliver our latest technical development — a {color:51,110,25}special camera{/color} — to you.', 'Është shumë e thjeshtë. Sot në mbrëmje, {color:51,110,25}postieri{/color} do të të dorëzojë zhvillimin tonë të fundit teknik — një {color:51,110,25}kamerë speciale{/color}.'],
                '17': ['Твоя задача - {color:51,110,25}фотографировать аномальные объекты и отправлять снимки нам{/color}.', 'Your task is to {color:51,110,25}photograph anomalous objects and send the pictures to us{/color}.', 'Detyra jote është të {color:51,110,25}fotografosh objekte anomale dhe të na dërgosh fotot{/color}.'],
                '18': ['А мы в свою очередь будем их изучать.', 'And we, in turn, will study them.', 'Ne, nga ana jonë, do t\'i studiojmë ato.'],

                '19': ['Но учти, что если ты будешь присылать рядовые снимки предметов,|||| то у тебя будут {color:99,11,15}неприятности{/color}.', 'But keep in mind, if you send us ordinary photos of objects, |||| you will face {color:99,11,15}trouble{/color}.', 'Por ki parasysh, nëse na dërgon foto të zakonshme të objekteve, |||| do të përballeh me {color:99,11,15}vështirësi{/color}.'],



                '20': ['А как я смогу отличить обычный предмет от аномального?', 'And how am I supposed to tell an ordinary object from an anomalous one?', 'Dhe si mund ta dalloj një objekt të zakonshëm nga një anormal?'],
                '21': ['', '', ''],
                '22': ['', '', ''],
                '23': ['', '', ''],
                '24': ['', '', ''],
                '25': ['', '', ''],
                '26': ['', '', ''],
                '27': ['', '', ''],
                '28': ['', '', ''],
                '29': ['', '', ''],
                '30': ['', '', ''],
                '31': ['', '', ''],
                '32': ['', '', ''],
                '33': ['', '', ''],
                '34': ['', '', ''],
                '35': ['', '', ''],
                '36': ['', '', ''],
                '37': ['', '', ''],
                '38': ['', '', ''],
                '39': ['', '', ''],
                '40': ['', '', ''],
                '41': ['', '', ''],
                '42': ['', '', ''],
                '43': ['', '', ''],
                '44': ['', '', ''],
                '45': ['', '', ''],
                '46': ['', '', ''],
                '47': ['', '', ''],
                '48': ['', '', ''],
                '49': ['', '', ''],
                '50': ['', '', ''],
                '51': ['', '', ''],
                '52': ['', '', ''],
                '53': ['', '', ''],
                '54': ['', '', ''],
                '55': ['', '', ''],
                '56': ['', '', ''],
                '57': ['', '', ''],
                '58': ['', '', ''],
                '59': ['', '', ''],
                '60': ['', '', ''],
                '61': ['', '', ''],
                '62': ['', '', ''],
                '63': ['', '', ''],
                '64': ['', '', ''],
                '65': ['', '', ''],
                '66': ['', '', ''],
                '67': ['', '', ''],
                '68': ['', '', ''],
                '69': ['', '', ''],
                '70': ['', '', ''],
                '71': ['', '', ''],
                '72': ['', '', ''],
                '73': ['', '', ''],
                '74': ['', '', ''],
                '75': ['', '', ''],
                '76': ['', '', ''],
                '77': ['', '', ''],
                '78': ['', '', ''],
                '79': ['', '', ''],

            }
        }
    }
}
