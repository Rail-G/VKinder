from vk_api.keyboard import VkKeyboard, VkKeyboardColor

class Button:

    def __init__(self) -> None:
        pass

    def start(self) -> VkKeyboard:
        start_key = VkKeyboard(inline=False, one_time=True)
        start_key.add_button('Начать поиск', color=VkKeyboardColor.SECONDARY)
        return start_key
    
    def next(self) -> VkKeyboard:
        next_key = VkKeyboard(inline=False, one_time=True)
        next_key.add_button('Далее', color=VkKeyboardColor.SECONDARY)
        return next_key
    
    def show_liked_photos(self) -> VkKeyboard:
        s_l_p = VkKeyboard(inline=False, one_time=True)
        s_l_p.add_button('Показать понравившиеся фотографии', color=VkKeyboardColor.POSITIVE)
        return s_l_p
    
    def black_list(self) -> VkKeyboard:
        black_list_key = VkKeyboard(inline=False, one_time=True)
        black_list_key.add_button('Добавить в чёрный список', color=VkKeyboardColor.NEGATIVE)
        return black_list_key
    
    def show_black_list(self) -> VkKeyboard:
        show_list = VkKeyboard(inline=False, one_time=True)
        show_list.add_button('Показать чёрный список', color=VkKeyboardColor.SECONDARY)
        return show_list
    
    def delete_black_list(self) -> VkKeyboard:
        delete_black_list = VkKeyboard(inline=False, one_time=True)
        delete_black_list.add_button('Удалить из чёрного списка', color=VkKeyboardColor.NEGATIVE)
        return delete_black_list