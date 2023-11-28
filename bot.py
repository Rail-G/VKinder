import vk_api
from datetime import datetime
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from config import USER_TOKEN, GROUP_TOKEN, GROUP_ID, COUNT
from vkinder_data_base.db_connection import all_favorites, delete_from_favorites, delete_from_blocked, all_blocked, show_liked_photos, get_user, add_liked_photos, add_user
from buttons import Button

class VKinder():

    def __init__(self) -> None:
        self.vk_group = vk_api.VkApi(token=GROUP_TOKEN)
        self.vk_user = vk_api.VkApi(token=USER_TOKEN)
        self.bot_longpoll = VkBotLongPoll(self.vk_group, GROUP_ID)
        self.url = 'https://api.vk.com/method/'

    def bot_write(self, user_id: int, message: str, keyboard=None) -> None:
        self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'message': message, 'keyboard': keyboard})

    def user_name(self) -> str:
        user_name = self.vk_user.method('users.get')[0]['first_name']
        return user_name

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
        age = self.calculate_age(user_bdate)
        return age
    
    def user_city(self, user_id: int) -> tuple:
        user_city = self.vk_user.method('users.get', {'fields': 'city'})[0]
        if user_city.get('city') == None:
            self.bot_write(user_id, 'Пожалуйста введите ваш город: ')
            for event in self.bot_longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    peer_id = event.object.message['peer_id']
                    if peer_id == user_id:
                        city = event.object.message['text']
                        citys_db = self.vk_user.method('database.getCities', {'q': city})
                        if len(citys_db['items']) == 0:
                            self.bot_write(user_id, 'Такого города нету!')
                        else:
                            user_city_title = citys_db['items'][0].get('title')
                            if user_city_title.lower() == city.lower():
                                user_city_id = citys_db['items'][0].get('id')
                                return (user_city_id, user_city_title)
        user_city_id = user_city.get('id')
        user_city_title = user_city.get('title')
        return (user_city_id, user_city_title)
    
    def user_sex(self) -> int:
        user_sex = self.vk_user.method('users.get', {'fields': 'sex'})[0]['sex']
        if user_sex == 1:
            return 2
        return 1
    
    def search_partner(self, user_id: int) -> None:
        user_tuple_city = self.user_city(user_id)
        self.bot_write(user_id, 'На сколько младше и старше должен(-на) быть партнер(-ша)?\n(Укажите два числа через пробел)')
        for event in self.bot_longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                peer_id = event.object.message['peer_id']
                if peer_id == user_id:
                    age_from, age_to = list(map(int, event.object.message['text'].split()))
                break
        search_result = self.vk_user.method('users.search', {'city': user_tuple_city[0], 'count': int(COUNT), 'sex': self.user_sex(), 'age_from': self.user_bdate(user_id)-age_from, 'age_to': self.user_bdate(user_id)+age_to})
        if search_result.get('count') == 0:
            self.bot_write(user_id, 'Нам очень жаль, что вы не смогли найти вашего партнёра(-шу) в городе {}. Пожалуйста, начните поиск заного.'.format(user_tuple_city[1]))
            return False
        for i in search_result['items']:
            items = {'user_vk_id': i['id'], 'user_first_name': i['first_name'], 'user_last_name': i['last_name']}
            add_user(items, user_id)

    def photo_id(self, owner_id: int) -> list:
        photo_id = self.vk_user.method('photos.get', {'owner_id': owner_id, 'album_id': 'profile', 'extended': 1})['items']
        popular_photos = sorted(photo_id, key=lambda x: x['likes']['count'], reverse=True)
        photo_id = [i['id'] for i in popular_photos]
        return photo_id[:3]

    def send_photos(self, user_id: int, pk_number: int) -> None:
        func = self.get_user(pk_number)
        photo_id = self.photo_id(func['user_vk_id'])
        for i in photo_id:
            self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'attachment': f'photo{func["user_vk_id"]}_{i}', 'keyboard': Button().like_dislike()})
            for event in self.bot_longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    peer_id = event.object.message['peer_id']
                    if event.object.message['text'] == 'Like' and user_id == peer_id:
                        self.bot_write(user_id, "Фотография добавлена в понравившиеся.")
                        add_liked_photos(i, user_id)
                    break
    
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
            
    def delete_favorites(self, user_id: int) -> None:
        id = all_favorites(user_id)
        if id == []:
            self.bot_write(user_id, 'А тут пусто')
        else:
            for i in id:
                favorite = VkKeyboard(inline=True)
                favorite.add_button(f"{i[0]}", color=VkKeyboardColor.NEGATIVE)
                self.bot_write(user_id, f'{i[1]} {i[2]}', favorite.get_keyboard())
            for event in self.bot_longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    favorit = event.object.message['text']
                    if favorit.isdigit():
                        favorite_id = int(favorit)
                        self.bot_write(user_id, f'Пользователь {i[1]} {i[2]} удален из избранных')
                        delete_from_favorites(favorite_id)
                        break

    def delete_black_list(self, user_id: int) -> None:
        id = all_blocked(user_id)
        if id == []:
            self.bot_write(user_id, 'А тут пусто')
        else:
            for i in id:
                favorite = VkKeyboard(inline=True)
                favorite.add_button(f"{i[0]}", color=VkKeyboardColor.NEGATIVE)
                self.bot_write(user_id, f'{i[1]} {i[2]}', favorite.get_keyboard())
            for event in self.bot_longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    black_id = event.object.message['text']
                    if black_id.isdigit():
                        black_list_id = int(black_id)
                        self.bot_write(user_id, f'Пользователь {i[1]} {i[2]} удален из черного списка')
                        delete_from_blocked(black_list_id)
                        break

    def delete_photo(self, user_id: int, pk_number: int) -> None:
        id = show_liked_photos(user_id)
        if id == []:
            self.bot_write(user_id, 'А тут пусто')
        else:
            owner_id = self.get_user(pk_number)['user_vk_id']
            for i in id:
                favorite = VkKeyboard(inline=True)
                favorite.add_button(f"{i[0]}", color=VkKeyboardColor.NEGATIVE)
                self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'attachment': f'photo{owner_id}_{i[0]}', 'keyboard': favorite.get_keyboard()})
            for event in self.bot_longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:
                    ph_id = event.object.message['text']
                    if ph_id.isdigit():
                        photo_id = int(ph_id)
                        self.bot_write(user_id, f'Фото удален из понравившихся')
                        delete_from_favorites(photo_id)
                        break
                    
    def get_user(self, pk_number: int) -> dict:
        data = get_user(pk_number)
        user_data = {'user_vk_id': data[0], 'user_first_name': data[1], 'user_last_name': data[2]}
        return user_data
    
    def show_favorite(self, user_id: int) -> None:
        data = all_favorites(user_id)
        if data == []:
            self.bot_write(user_id, 'Тут никого нет (╥﹏╥)')
        else:
            for i in data:
                self.bot_write(user_id, f"vk.com/id{i[0]} {i[1]} {i[2]}")

    def show_blocked(self, user_id: int) -> None:
        data = all_blocked(user_id)
        if data == []:
            self.bot_write(user_id, 'Тут никого нет (╥﹏╥)')
        else:
            for i in data:
                self.bot_write(user_id, f"vk.com/id{i[0]} {i[1]} {i[2]}")

    def show_liked_photo(self, user_id: int, pk_number: int) -> None:
        data = show_liked_photos(user_id)
        if data == []:
            self.bot_write(user_id, 'Тут ничего нет (╥﹏╥)')
        else:
            owner_id = self.get_user(pk_number)['user_vk_id']
            for i in data:
                self.vk_group.method('messages.send', {'user_id': user_id, 'random_id': 0, 'attachment': f'photo{owner_id}_{i[0]}'})