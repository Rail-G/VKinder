from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class Button:

    def __init__(self) -> None:
        pass

    def start(self) -> VkKeyboard:
        start_key = VkKeyboard(inline=False, one_time=True)
        start_key.add_button('Начать поиск', color=VkKeyboardColor.POSITIVE)
        start_key.add_button('Вернуться к поиску', color=VkKeyboardColor.POSITIVE)
        start_key.add_line()
        start_key.add_button('Показать понравившиеся фотографии', color=VkKeyboardColor.POSITIVE)
        start_key.add_line()
        start_key.add_button('Показать чёрный список', color=VkKeyboardColor.PRIMARY)
        start_key.add_line()
        start_key.add_button('Показать избранных пользователей', color=VkKeyboardColor.PRIMARY)
        return start_key.get_keyboard()
    
    def next(self) -> VkKeyboard:
        next_key = VkKeyboard(inline=False, one_time=True)
        next_key.add_button('Далее', color=VkKeyboardColor.PRIMARY)
        next_key.add_button('Начать все сначало', color=VkKeyboardColor.PRIMARY)
        next_key.add_line()
        next_key.add_button('Добавить в чёрный список', color=VkKeyboardColor.NEGATIVE)
        next_key.add_line()
        next_key.add_button('Добавить в избранные', color=VkKeyboardColor.PRIMARY)
        next_key.add_button('В главное меню', color=VkKeyboardColor.PRIMARY)
        return next_key.get_keyboard()
    
    def delete_black_list(self) -> VkKeyboard:
        delete_black_list = VkKeyboard(inline=False, one_time=True)
        delete_black_list.add_button('Удалить из чёрного списка', color=VkKeyboardColor.NEGATIVE)
        delete_black_list.add_button('В главное меню', color=VkKeyboardColor.PRIMARY)
        return delete_black_list.get_keyboard()
    
    def yes_or_no(self) -> VkKeyboard:
        yes_or_no = VkKeyboard(inline=False, one_time=True)
        yes_or_no.add_button('Удалить все данные!', color=VkKeyboardColor.NEGATIVE)
        yes_or_no.add_button('Нет, я передумал', color=VkKeyboardColor.PRIMARY)
        return yes_or_no.get_keyboard()
    
    def delete_photo(self):
        delete_photo = VkKeyboard(inline=False, one_time=True)
        delete_photo.add_button('Удалить фото из понравивщихся', color=VkKeyboardColor.PRIMARY)
        delete_photo.add_button('В главное меню', color=VkKeyboardColor.PRIMARY)
        return delete_photo.get_keyboard()
    
    def delete_favorite(self):
        delete_favorite = VkKeyboard(inline=False, one_time=True)
        delete_favorite.add_button('Удалить из избранных', color=VkKeyboardColor.NEGATIVE)
        delete_favorite.add_button('В главное меню', color=VkKeyboardColor.PRIMARY)
        return delete_favorite.get_keyboard()
    
    def back_to_menu(self):
        back = VkKeyboard(inline=False, one_time=True)
        back.add_button('В главное меню', color=VkKeyboardColor.PRIMARY)
        return back.get_keyboard()
        
    def like_dislike(self):
        keyboard = VkKeyboard(inline=True) 
        keyboard.add_button('Like', color=VkKeyboardColor.SECONDARY)
        keyboard.add_button('Dislike', color=VkKeyboardColor.SECONDARY)
        return keyboard.get_keyboard()