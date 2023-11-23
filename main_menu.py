from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType
from bot import VKinder
from buttons import Button

for event in VKinder().bot_longpoll.listen():
    bot = VKinder()
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.object.message['text']
        user_id = event.object.message['from_id']
        peer_id = event.object.message['peer_id']
        if text == '/start':
            bot.bot_write(user_id, f'Добро пожаловать {bot.user_name()}', Button().start())
        if peer_id == user_id:
            if text in ['Начать поиск', 'Да, хочу начать сначала']:
                bot.bot_write(user_id, 'Отлично. Изучим ваши данные и найдем вам партнера(-шу)')
                # bot.search_partner()
                bot.bot_write(user_id, 'Мы закончили поиск! Пожалуйста, нажмите \'Далее\' чтобы ознакомиться результатом! Остальные кнопки надеюсь не нуждаются в объяснении.', Button().next())
            elif text == 'Начать все сначало':
                bot.bot_write(user_id, 'Это приведет к удалению текущих данных!', Button().yes_or_no())
            elif text == 'Далее':
                bot.bot_write(user_id, 'cool', Button().next())
                # BD SELECT USERS with get()
                # bot.send_photos()
                pass
            elif text in ['Назад', 'Нет, я передумал']:
                bot.bot_write(user_id, 'Я вас понял.', Button().next())
            elif text == 'Добавить в чёрный список':
                # BD INSERT INTO BLOCKED
                bot.bot_write(user_id, f'Пользователь {None} добавлен в черный список', Button().next())
                pass
            elif text == 'Показать понравившиеся фотографии':
                bot.bot_write(user_id, 'Пользователи находящиеся в списке:', Button().back())
                # BD SELECT LikedDisliked where reaction == 1 OR BD photos where photo_likes == 1
                pass
            elif text == 'Показать чёрный список':
                bot.bot_write(user_id, 'Пользователи находящиеся в списке:', Button().delete_black_list())
                # BD SELECT BLOCKED
                pass
            elif text == 'Удалить из чёрного списка':
                # BD SELECT and DELETE this user in BLOCKED
                bot.bot_write(user_id, 'Пользователь удален из чёрного списка', Button().next())
                pass
