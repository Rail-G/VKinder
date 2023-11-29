from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotEventType
from bot import VKinder
from buttons import Button
from vkinder_data_base.db_connection import create_table, add_client, drop_users, delete_all, add_to_blocked, add_user_to_favorites


create_table()
pk_number = 0
for event in VKinder().bot_longpoll.listen():
    bot = VKinder()
    if event.type == VkBotEventType.MESSAGE_NEW:
        text = event.object.message['text']
        user_id = event.object.message['from_id']
        peer_id = event.object.message['peer_id']
        if text == '/start':
            bot.bot_write(user_id, f'Добро пожаловать {bot.user_name()}', Button().start())
            add_client(user_id)
        if peer_id == user_id:
            if text == 'Начать поиск':
                drop_users(user_id)
                bot.bot_write(user_id, 'Отлично. Изучим ваши данные и найдем вам партнера(-шу).')
                g = bot.search_partner(user_id)
                if g == False:
                    bot.bot_write(user_id, 'Вернитесь в меню, чтобы продолжить.', Button().back_to_menu())
                else:
                    bot.bot_write(user_id, 'Мы закончили поиск! Пожалуйста, нажмите \'Далее\' чтобы ознакомиться результатом! Остальные кнопки надеюсь не нуждаются в объяснении.', Button().next())
            elif text == 'Начать все сначало':
                bot.bot_write(user_id, 'Это приведет к полному удалению всех данных!', Button().yes_or_no())
            elif text == 'Удалить все данные!':
                pk_number = 0
                delete_all(user_id)
                bot.bot_write(user_id, 'Все данные удалены!', Button().start())
            elif text == 'Далее':
                pk_number += 1
                data = bot.get_user(pk_number)
                bot.bot_write(user_id, f"vk.com/id{data['user_vk_id']} {data['user_first_name']} {data['user_last_name']}")
                bot.send_photos(user_id, pk_number)
                bot.bot_write(user_id, 'Идем дальше?', Button().next())
            elif text == 'Нет, я передумал':
                bot.bot_write(user_id, 'Я вас понял.', Button().next())
            elif text == 'Добавить в чёрный список':
                data = bot.get_user(pk_number)
                add_to_blocked(data, user_id)
                bot.bot_write(user_id, f'Пользователь {data["user_first_name"]} {data["user_last_name"]} добавлен в черный список.', Button().next())
            elif text == 'Добавить в избранные':
                data = bot.get_user(pk_number)
                add_user_to_favorites(data, user_id)
                bot.bot_write(user_id, f'Пользователь {data["user_first_name"]} {data["user_last_name"]} добавлен в список избранных.', Button().next())
            elif text == 'Показать понравившиеся фотографии':
                bot.bot_write(user_id, 'Фотографии находящиеся в списке:', Button().delete_photo())
                bot.show_liked_photo(user_id, pk_number)
            elif text == 'Показать избранных пользователей':
                bot.bot_write(user_id, 'Список избранных:', Button().delete_favorite())
                bot.show_favorite(user_id)
            elif text == 'Показать чёрный список':
                bot.bot_write(user_id, 'Пользователи находящиеся в списке:', Button().delete_black_list())
                bot.show_blocked(user_id)
            elif text == 'Удалить из чёрного списка':
                bot.bot_write(user_id, 'Нажмите на соответствующую кнопку, рядом с пользователем, чтобы удалить его/её.', Button().back_to_menu())
                bot.delete_black_list(user_id)
                bot.bot_write(user_id, 'Вернитесь в меню, чтобы продолжить.', Button().back_to_menu())
            elif text == 'Удалить фото из понравивщихся':
                bot.bot_write(user_id, 'Нажмите на соответствующую кнопку, рядом с фотографией, чтобы удалить его.', Button().back_to_menu())
                bot.delete_photo(user_id, pk_number)
                bot.bot_write(user_id, 'Вернитесь в меню, чтобы продолжить.', Button().back_to_menu())
            elif text == 'Удалить из избранных':
                bot.bot_write(user_id, 'Нажмите на соответствующую кнопку, рядом с избранным, чтобы удалить его/её.', Button().back_to_menu())
                bot.delete_favorites(user_id)
                bot.bot_write(user_id, 'Вернитесь в меню, чтобы продолжить', Button().back_to_menu())
            elif text == 'В главное меню':
                bot.bot_write(user_id, 'Возвращаемся.', Button().start())
            elif text == 'Вернуться к поиску' and pk_number > 0:
                bot.bot_write(user_id, 'Возвращаемся к списку.', Button().next())
            elif text == 'Вернуться к поиску' and pk_number == 0:
                bot.bot_write(user_id, 'Вы еще не начали поиск или не выполнили условия поиска!', Button().start())
