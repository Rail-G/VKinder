# VKinder - бот для знакомств
Бот VK для поиска второй половинки.  
Клиент заходит в чат с ботом, бот подбирает потенциальных кандидатов для клиента. Клиент может добавить пользователя в избранное, в черный список или пропустить.  
Так же у клиента есть возможность поставить фотографиям кандидата лайк и позже просматривать лайкнутые фотографии.
## Для работы необходимы
- #### Python от 3.7 
- #### PostgreSQL
## Установка
1) #### Сделайте клон репозитория к себе в рабочую область:
```
git clone https://github.com/Rail-G/VKinder.git
```
А затем перейдите к нему:
```
cd VKinder
```
2) #### Все зависимости указанны в файле requirements.txt. Для установки воспользуйтесь терминалом и командой
```
pip install -r requirements.txt.  
```
3) #### Создайте базу данных и введите ваши данные в файл config.py
    Получения USER_TOKEN:
    - Перейдите на сайт https://vkhost.github.io/
    - Нажмите на поле vk.com
    - Нажать на кнопку разрешить
    - Скопировать длинный текст находящийся между `acces_token=` и `&expires`
    
    Получения GROUP_TOKEN и подготовка сообщества к работе с ботом:
    - Создать и зайти в ваше сообщество в ВКонтакте
    - Придерживатся инструкции:
      - Профиль сообщества -> Еще -> Разрешить сообщения
      - Управления -> Настройки -> Работа с API -> В разделе Long Poll Api в разделе `тип событий` поставить на все галочки, в пункте сообщения -> Создать ключ -> Разрешить доступ к управлению и сообщениям сообщетсва -> Создать. При необходимости подвердить через SMS
      - Управления -> Сообщения -> Включить сообщения сообщества
      - Управления -> Сообщения -> Настройки для бота -> Включить возможности бота
    
    Получения GROUP_ID:
    - Перейти в страницу сообщетсва
    - Нажать на адресную строку
    - Скопировать числа после `vk.com/club`

# Эксплуатация бота
1) Запустить бота в файле main_menu.py.
```
python main_menu.py
```
2) Перейдите в чат группы.
3) Ввести команду /start чтобы начать общения с ботом.
4) Нажимайте на кнопки, чтобы передвигаться по боту

### Прежде всего, бот создан не как полноценный готовый продукт. VKinder не несет ответственность за разбитые сердца и за ваши переоцененные ожидания! И вообще, идите лучше на улицу и ищите себе партнера без помощи бота! С уважением команда разработчиков VKinder.
