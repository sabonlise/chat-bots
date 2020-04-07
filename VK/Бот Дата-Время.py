import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from settings import GROUP_TOKEN, GROUP_ID, USER_TOKEN
import datetime


vk_session = vk_api.VkApi(token=GROUP_TOKEN)
vk_session_user = vk_api.VkApi(token=USER_TOKEN)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
vk_user = vk_session_user.get_api()
vk = vk_session.get_api()


def time_now():
    days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    offset = datetime.timezone(datetime.timedelta(hours=3))
    dt = datetime.datetime.now(offset)
    return f'По московскому времени сейчас: {dt.strftime("%d %B")}, {dt.strftime("%H:%M")}, {days[dt.weekday()]}.'


def main():

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            msg = event.obj.message['text'].lower()
            keywords = ['время', 'число', 'дата', 'день']
            is_date = False
            for word in keywords:
                if word in msg:
                    vk.messages.send(user_id=user_id,
                                     message=time_now(),
                                     random_id=get_random_id())
                    is_date = True
                    break
            if not is_date:
                vk.messages.send(user_id=user_id,
                                 message='Хотите узнать текущее время? Напишите "время".',
                                 random_id=get_random_id())


if __name__ == '__main__':
    main()
