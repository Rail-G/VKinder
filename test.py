"TABLES"
users = []
photos = []
favorites = []
blocked = []
likeddisliked = []

# "INSER INTO Первый поиск"
# users.extend(['Ivan', 'Oleg', 'Stepan'])
# photos.extend([[1,2,3], [1,2,3], [1,2,3]])
# favorites.append('Ivan')
# blocked.append('Oleg')
# likeddisliked.extend([[2],[3]])
# print(f"Первый поиск\nusers: {users}\nphotos: {photos}\nfavorites: {favorites}\nblocked: {blocked}\nlikeddisliked: {likeddisliked}\n\n")


# "INSERT INTO Второй поиск"
# """В НАШЕМ МЕТОДЕ ЕСТЬ create и drop одновременно. Удалятся все данные"""
# users.clear()
# photos.clear()
# favorites.clear()
# blocked.clear()
# likeddisliked.clear()

# users.extend(['Madi', 'Tolik', 'Sasha'])
# photos.extend([[5,6,7], [5,6,7], [5,6,7]])
# favorites.extend(['Tolik', 'Madi'])
# print(f"ВТорой поиск\nusers: {users}\nphotos: {photos}\nfavorites: {favorites}\nblocked: {blocked}\nlikeddisliked: {likeddisliked}")

# """КАК ВИДИМ ТАБЛИЦА FAVORITES, BLOCKED, LIKEDDISLIKED не сохранили данные. Это наш метод БД"""




"""МОЙ МЕТОД БД"""
"INSER INTO Первый поиск"
users.extend(['Ivan', 'Oleg', 'Stepan'])
photos.extend([[1,2,3], [1,2,3], [1,2,3]])
favorites.append('Ivan')
blocked.append('Oleg')
likeddisliked.extend([[2],[3]])
print(f"Поиск первый\nusers: {users}\nphotos: {photos}\nfavorites: {favorites}\nblocked: {blocked}\nlikeddisliked: {likeddisliked}\n\n")


"INSERT INTO Второй поиск"
"""В МОЕМ МЕТОДЕ create и drop будут только у Users и Photos."""

users.clear()
photos.clear()
# favorites            Останется не тронутым
# blocked              Останется не тронутым
# likeddisliked.       Останется не тронутым
"""А ДЛЯ favorites blocked likeddisliked будет только в крайнем случае, на это команду придумаю."""

users.extend(['Madi', 'Tolik', 'Sasha'])
photos.extend([[5,6,7], [5,6,7], [5,6,7]])
favorites.extend(['Tolik', 'Madi'])
blocked.append('Sasha')
likeddisliked.extend([[5]])
print(f"Поиск второй\nusers: {users}\nphotos: {photos}\nfavorites: {favorites}\nblocked: {blocked}\nlikeddisliked: {likeddisliked}")

"""КАК ВИДНО Favorites, blocked, likeddisliked остался не тронутым"""