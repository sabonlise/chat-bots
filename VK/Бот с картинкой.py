import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from settings import GROUP_TOKEN, GROUP_ID, USER_TOKEN
import random


def main():
    vk_session = vk_api.VkApi(token=GROUP_TOKEN)
    vk_session_user = vk_api.VkApi(token=USER_TOKEN)
    longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
    vk_user = vk_session_user.get_api()

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user_id = event.obj.message['from_id']
            name = vk_user.users.get(users_id=user_id)[0]['first_name']
            photos = vk_user.photos.get(owner_id=-166527539, album_id=271509370, photo_sizes=1)
            pics = []
            for photo in photos['items']:
                pics.append(f'photo{photo["owner_id"]}_{photo["id"]}')
            vk.messages.send(user_id=user_id,
                             message=f"Привет, {name}!",
                             random_id=get_random_id(),
                             attachment=[random.choice(pics)])


if __name__ == '__main__':
    main()
