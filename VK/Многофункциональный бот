from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from settings import GROUP_TOKEN, USER_TOKEN, SERVICE_TOKEN
import vk_api
import wikipedia

vk_session = vk_api.VkApi(token=GROUP_TOKEN)
vk = vk_session.get_api()
vk_session_serice = vk_api.VkApi(token=SERVICE_TOKEN)
vk_service = vk_session_serice.get_api()
vk_session_user = vk_api.VkApi(token=USER_TOKEN)
vk_user = vk_session_user.get_api()
longpoll = VkLongPoll(vk_session)


help_ = ['/help', 'ПОМОЩЬ', 'НАЧАТЬ', 'СТАРТ']
hello = ['привет', 'ку', 'здарова', 'прив', 'ку-ку']


def layout(msg):
    eng = [i for i in "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"]
    ru = [_ for _ in "йцукенгшщзхъфывапролджэячсмитьбю.ё"]
    layout = {}
    for i in msg:
        if i.lower() in eng:
            layout = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                                "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
        elif i.lower() in ru:
            layout = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                                "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))
    return msg.translate(layout)


def transliterate(name):
    slovar = {
        'А': 'A',
        'а': 'a',
        'Б': 'B',
        'б': 'b',
        'В': 'V',
        'в': 'v',
        'Г': 'G',
        'г': 'g',
        'Д': 'D',
        'д': 'd',
        'Е': 'E',
        'е': 'e',
        'Ё': 'E',
        'ё': 'e',
        'Ж': 'Zh',
        'ж': 'zh',
        'З': 'Z',
        'з': 'z',
        'И': 'I',
        'и': 'i',
        'Й': 'I',
        'й': 'i',
        'К': 'K',
        'к': 'k',
        'Л': 'L',
        'л': 'l',
        'М': 'M',
        'м': 'm',
        'Н': 'N',
        'н': 'n',
        'О': 'O',
        'о': 'o',
        'П': 'P',
        'п': 'p',
        'Р': 'R',
        'р': 'r',
        'С': 'S',
        'с': 's',
        'Т': 'T',
        'т': 't',
        'У': 'U',
        'у': 'u',
        'Ф': 'F',
        'ф': 'f',
        'Х': 'Kh',
        'х': 'kh',
        'Ц': 'Tc',
        'ц': 'tc',
        'Ч': 'Ch',
        'ч': 'ch',
        'Ш': 'Sh',
        'ш': 'sh',
        'Щ': 'Shch',
        'щ': 'shch',
        'Ы': 'Y',
        'ы': 'y',
        'Э': 'E',
        'э': 'e',
        'Ю': 'Iu',
        'ю': 'iu',
        'Я': 'Ia',
        'я': 'ia',
    }

    for key in slovar:
        name = name.replace(key, slovar[key])
    return name


def message_send(msg):
    if event.from_user:
        vk.messages.send(
            user_id=event.user_id,
            message=msg,
            random_id=get_random_id())
    elif event.from_chat:
        vk.messages.send(
            chat_id=event.chat_id,
            message=msg,
            random_id=get_random_id())


def get_keywords(sticker_id):

    words_ = []
    words_mas = []
    for words in vk_user.store.getStickersKeywords(stickers_ids=sticker_id, v=5.67)['dictionary']:
        words_.append(list(words.values())[0])
    for word in words_:
        for w in word:
            words_mas.append(w)

    return ', '.join(words_mas)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        try:
            if event.text:
                response = str(event.text)
                if response in hello:
                    message_send('Приветствую.')
                elif response.lower() == '/users':
                    members_testers = vk_service.groups.getMembers(group_id='testers')['count']
                    members_testpool = vk_service.groups.getMembers(group_id='testpool')['count']
                    old_testers = 95483
                    old_testpool = 23693
                    message_send(f'В сообществе [club84585194|VK Testers] '
                                 f'{"{0:,}".format(members_testers).replace(",", " ")} участников '
                                 f'(+{"{0:,}".format(members_testers-old_testers).replace(",", " ")} '
                                 f'с начала раздачи стикеров) \
                                 \nВ сообществе [club134304772|/testpool] '
                                 f'{"{0:,}".format(members_testpool).replace(",", " ")} \
                                 участников (+{"{0:,}".format(members_testpool - old_testpool).replace(",", " ")} '
                                 f'с начала раздачи стикеров)')
                elif response.split()[0].lower() == '/wiki':
                    try:
                        message_send('Статья из википедии:\n' + str(wikipedia.summary(response.split()[1:])))
                    except wikipedia.exceptions.DisambiguationError as w:
                        message_send('Статья не найдена!')
                elif response.split()[0].lower() == '/translit':
                    message_send(f"Транслитерированная строка:\n{transliterate(' '.join(response.split()[1:]))}")
                elif response in [el.lower() for el in help_]:
                    message_send('1) Отправьте любой стикер - бот выдаст его ключевые слова. \
                        \n\n2) /users: Выводит количество новыприбывших людей в VK Testers и /testpool '
                                 'после введения тестерских стикеров. \
                        \n\n3) /wiki <текст>: Выводит статью из Wikipedia на английском языке. \
                        \n\n4) /translit <текст>: Транслитерация русского текста латиницей. \
                        \n\n5) /layout <текст>: Перевод из одной раскладки в другую. \
                        \n\n6) /ссылка <ссылка вида vk.cc/*>: Выводит несокращённую ссылку и забанена ли она на сайте ВКонтакте.')
                elif response.split()[0].lower() == '/layout':
                    message_send(f"Перевод в другую раскладку:\n{layout(' '.join(response.split()[1:]))}")
                elif response.lower() == '/secret':
                    message_send('Нет.')
                elif len(response.split()) > 0 and response.split()[0] == '/secret':
                    message_send(''.join(response.split()[1:]))
                elif response.split()[0].lower() == '/ссылка':
                    try:
                        link = vk_service.utils.checkLink(url=response.split()[1])
                        if link['status'] == 'banned':
                            message_send(f'Исходная ссылка: {link["link"]}\nСостояние ссылки: заблокирована.')
                        elif link['status'] == 'not_banned':
                            message_send(f'Исходная ссылка: {link["link"]}\nСостояние ссылки: не заблокирована.')
                        else:
                            message_send(f'Исходная ссылка: {link["link"]}\nСостояние ссылки: проверяется.')
                    except vk_api.exceptions.ApiError:
                        message_send(f'Некорректная ссылка.')
            else:
                response = vk.messages.getById(message_ids=event.message_id)
                if response['items'][0]['attachments'][0]['sticker']:
                    sticker_id = response['items'][0]['attachments'][0]['sticker']['sticker_id']
                    message_send(f'Ключевые слова стикера: \
                        {get_keywords(sticker_id)}')
        except Exception as e:
            print(e)
