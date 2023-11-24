import vk_api
from datetime import datetime
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import USER_TOKEN, GROUP_TOKEN, GROUP_ID
# from vkinder_data_base.db_connection import add_user, add_to_blocked, add_photo, add_user_to_favorites, all_favorites, get_user

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
        user_name = self.vk_user.method('users.get')[0]['first_name']
        return user_name

    # user_bdate
    def user_bdate(self, user_id: int) -> int:
        user_info = self.vk_user.method('users.get', {'fields': 'bdate'})
        user_bdate = user_info[0].get('bdate')
        if user_bdate == None:
            self.bot_write(user_id, 'Пожалуйста напишите, сколько вам лет?')
            for event in self.bot_longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    peer_id = event.object.message['peer_id']
                    if peer_id == user_id:
                        age = event.object.message['text']
                        if int(age) < 100:
                            return age
                        else:
                            self.bot_write(user_id, 'А вы точно человек? Введите реальный возраст.')
        else:
            age = self.calculate_age(user_bdate)
            return age
    
    # user_city
    def user_city(self, user_id: int) -> str:
        user_city = self.vk_user.method('users.get', {'fields': 'city'})[0]
        if user_city.get('city') == None:
            self.bot_write(user_id, 'Пожалуйста введите ваш город: ')
            for event in self.bot_longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    peer_id = event.object.message['peer_id']
                    if peer_id == user_id:
                        city = event.object.message['text']
                        citys_db = self.vk_user.method('database.getCities', {'q': city})
                        user_city_title = citys_db['items'][0].get('title')
                        if user_city_title.lowe() == city.lower():
                            user_city_id = citys_db['items'][0].get('id')
                            return (user_city_id, user_city_title)
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
    def search_partner(self, user_id: int) -> None:
        user_tuple_city = self.user_city()
        self.bot_write(user_id, 'На сколько младше и старше должен(-на) быть партнер(-ша)?\n(Укажите два числа через пробел)')
        for event in self.bot_longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                peer_id = event.object.message['peer_id']
                if peer_id == user_id:
                    age_from, age_to = list(map(int, event.object.message['text'].split()))
        search_result = self.vk_user.method('users.search', {'city': user_tuple_city[0], 'sex': self.user_sex(), 'age_from': self.user_bdate()-age_from, 'age_to': self.user_bdate()+age_to})
        if search_result.get('count') == 0:
            return self.bot_write(user_id, 'Нам очень жаль, что вы не смогли найти вашего партнёра(-шу) в городе {}'.format(user_tuple_city[1]))
        for i in search_result['items']:
            items = {'user_vk_id': i['id'], 'user_first_name': i['first_name'], 'user_last_name': i['last_name'], 'user_link': f"vk.com/id{i['id']}"}
            # add_user(items)

    # photo_id
    def photo_id(self, owner_id: int) -> list:
        photo_id = self.vk_user.method('photos.get', {'owner_id': owner_id, 'album_id': 'profile', 'extended': 1})['items']
        popular_photos = sorted(photo_id, key=lambda x: x['likes']['count'], reverse=True)
        photo_id = [i['id'] for i in popular_photos]
        return photo_id[:3]

    # send_users_photo
    def send_photos(self, user_id: int, number: int) -> str:
        keyboard = VkKeyboard(inline=True) 
        keyboard.add_button('Like', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Dislike', color=VkKeyboardColor.SECONDARY)
        # owner_id = get_user(number)
        photo_id = self.photo_id(owner_id)
        for i in photo_id:
            self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'attachment': f'photo{owner_id}_{i}', 'keyboard': keyboard.get_keyboard()})
            for event in self.bot_longpoll.listen():
                peer_id = event.object.message['peer_id']
                if event.type == VkBotEventType.MESSAGE_NEW:
                    if event.object.message['text'] == 'Like' and user_id == peer_id:
                        self.bot_write(user_id, "Фотография добавлена в понравившиеся.")
                        #DB Update photo_likes to 1 ОДНУ ФУНКЦИЮ В КОТОРЫЙ ПАРАМЕТРОМ ДОАБВИТЬ 1 ИЛИ 0
                    break
    
    # calculate age
    def calculate_age(self, date: str) -> int:
        bdate = date.split('.')
        if len(bdate) == 3:
            date_now = datetime.now()
            age = date_now.year -  int(bdate[2])
            if int(bdate[1]) > date_now.month:
                return age - 1
            elif int(bdate[1]) == date_now.month and int(bdate[0]) > date_now.day:
                return age - 1
            else:
                return age
        # DB_users
    # DB_
    # DB_
    # DB_