import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from settings import GROUP_TOKEN, GROUP_ID, USER_TOKEN
import wikipedia


vk_session = vk_api.VkApi(token=GROUP_TOKEN)
vk_session_user = vk_api.VkApi(token=USER_TOKEN)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
vk_user = vk_session_user.get_api()
vk = vk_session.get_api()


def main():

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.obj.message['from_id']
            msg = event.obj.message['text'].lower()
            if msg.split()[0] == '/wiki':
                try:
                    vk.messages.send(user_id=user_id,
                                     message='Статья из википедии:\n' + str(wikipedia.summary(msg.split()[1:])),
                                     random_id=get_random_id())
                except Exception:
                    vk.messages.send(user_id=user_id,
                                     message='Статья не найдена!',
                                     random_id=get_random_id())
            else:
                vk.messages.send(user_id=user_id,
                                 message='Что Вы хотите узнать? Воспользуйтесь командой "/wiki <текст>"',
                                 random_id=get_random_id())


if __name__ == '__main__':
    main()
