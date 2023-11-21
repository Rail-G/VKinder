import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import USER_TOKEN, GROUP_TOKEN, GROUP_ID

class VKinder():

    def __init__(self) -> None:
        self.vk_group = vk_api.VkApi(token=GROUP_TOKEN)
        self.vk_user = vk_api.VkApi(token=USER_TOKEN)
        self.bot_longpoll = VkBotLongPoll(self.vk_group, GROUP_ID)
        self.url = 'https://api.vk.com/method/'

    def bot_write(self, user_id: int, message: str, keyboard=None) -> None:
        self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'message': message, 'keyboard': keyboard})

    # user_id
    def user_name(self) -> int:
        user_name = self.vk_user.method('users.get')[0]['name']
        return user_name
    
    # user_bdate
    def user_bdate(self) -> str:
        user_bdate = self.vk_user.method('users.get', {'fields': 'bdate'})
        return user_bdate
    
    # user_city
    def user_city(self) -> str:
        user_city = self.vk_user.method('users.get', {'fields': 'city'})[0]
        if user_city.get('city') == None:
            return None
        user_city_id = user_city.get('id')
        user_city_title = user_city.get('title')
        return (user_city_id, user_city_title)
    
    # user_sex
    def user_sex(self) -> int:
        user_sex = self.vk_user.method('user.get', {'fields': 'sex'})[0]['sex']
        if user_sex == 1:
            return 2
        return 1
    
    # find_users
    def search_partner(self, city_id: tuple, user_sex: int, user_bdate: str) -> None:
        user_id_city = self.user_city()
        search_result = self.vk_user.method('users.search', {'city': user_id_city[0], 'sex': user_sex, 'age_from': self.user_bdate()-3, 'age_to': self.user_bdate()+3})
        if search_result.get('count') == 0:
            return 'Нам очень жаль, что вы не смогли найти вашего партнёра(-шу) в городе {}'.format(user_id_city[1])
        for i in search_result['items']:
            # BD INSERT users: id, vk_id, firstname, lastname, link
            pass

    # photo_id
    def photo_id(self) -> list:
        # BD SELECT users: vk_id
        photo_id = self.vk_user.method('photos.get', {'owner_id': BD, 'album_id': 'profile', 'extended': 1})['items']
        popular_photos = sorted(photo_id, key=lambda x: x['likes']['count'], reverse=True)
        photo_id = [i['id'] for i in popular_photos]
        return photo_id[:3]

    # send_users_photo
    def send_photos(self, user_id: int, photo_id: list) -> str:
        keyboard = VkKeyboard(inline=True) 
        keyboard.add_button('Like', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Пропустить', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Dislike', color=VkKeyboardColor.SECONDARY)
        for i in photo_id:
            self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'attachment': f'photo348914127_{i}', 'keyboard': keyboard.get_keyboard()})
            for event in self.bot_longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.object.message['text'] == 'Like':
                        self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'message': "Фотография добавлена в понравившиеся."})
                        #DB Update photo like to 1
                    elif event.object.message['text'] == 'Dislike':
                        self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'message': "Мы постараемся вам больше не показывать эту фотографию."})
                        #DB Update photo like to 0
                    break
    
    # DB_users
    # DB_
    # DB_
    # DB_
