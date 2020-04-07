import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from settings import GROUP_TOKEN, GROUP_ID
from datetime import date


def main():
    vk_session = vk_api.VkApi(token=GROUP_TOKEN)
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user_id = event.obj.message['from_id']
            msg = event.obj.message['text'].lower()
            if msg in ['/help', 'помощь', 'help', 'команды']:
                vk.messages.send(user_id=user_id,
                                 message='Я могу сказать, в какой день недели была какая-нибудь дата!'
                                         'Отправь сообщение в формате YYYY-MM-DD.',
                                 random_id=get_random_id())
            else:
                try:
                    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
                    year, month, day = map(int, msg.strip().split('-'))
                    assert len(str(year)) == 4 and 1 <= len(str(month)) <= 2 and 1 <= len(str(day)) <= 2
                    dt = date(year, month, day)
                    vk.messages.send(user_id=user_id,
                                     message=f'В дату {msg} был день недели {days[dt.weekday()]}',
                                     random_id=get_random_id())
                except Exception:
                    vk.messages.send(user_id=user_id,
                                     message='Неверный формат сообщения. '
                                             'Напишите /help для более подробной информации',
                                     random_id=get_random_id())


if __name__ == '__main__':
    main()
