import sqlite3
import os

# Папка и путь к базе
os.makedirs("repositories", exist_ok=True)
db_path = os.path.join("repositories", "cards.db")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Создаем таблицу, если ее нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rarity TEXT NOT NULL,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    count INTEGER,
    hp INTEGER,
    damage INTEGER,
    energy INTEGER,
    price INTEGER NOT NULL,
    link_of_picture TEXT
)
''')

# Полностью очищаем таблицу и сбрасываем счетчик ID, 
# чтобы автонумерация началась строго с 1
cursor.execute('DELETE FROM cards')
cursor.execute('DELETE FROM sqlite_sequence WHERE name="cards"')

# Твой полный список карт
cards_data = [
    ("1", "security", "обычный медведь", 1, 3, 1, 4, 70, r"_/□\_    ʕ•ᴥ•ʔ"),
    ("1", "attack", "обычный кот", 20, 2, 2, 3, 100, r"/\/\   ( •·•)"),
    ("1", "buffer", "обычный кролик", 1, 2, 1, 3, 50, r"/) /)    ( • ,•)"),
    ("1", "deathrattle", "обычный мини-пиг", 2, 2, 1, 2, 60, r"()____()      (^(oo)^)"),
    ("1", "deathrattle", "обычный воробей", 0, 1, 1, 1, 80, r"_|¦|_    / * >"), # <-- Это будет ID 5!
    ("1", "impaler", "обычная капибара", 1, 1, 1, 2, 70, r"△    /   * )"),
    ("2", "deathrattle", "Редкий мини-пиг", 2, 2, 2, 3, 200, r"()____()    (^(oo)^)"),
    ("2", "buffer", "редкий кролик", 2, 2, 3, 3, 250, r"/) /)    ( • ,•)"),
    ("2", "security", "Редкий медведь", 1, 4, 2, 4, 300, r"_/□\_    ʕ•ᴥ•ʔ"),
    ("2", "impaler", "Редкая капибара", 1, 2, 2, 3, 300, r"△    /   * )"),
    ("2", "debuffer", "редкий мистер карп", 1, 2, 1, 2, 250, r"_|¯|_      (°)#))<<"),
    ("2", "deathrattle", "редкий воробей", 2, 1, 1, 2, 450, r"_|¦|_    / * >"),
    ("3", "attack", "легендарный кот", 35, 2, 2, 4, 900, r"/\/\    ( •·•)"),
    ("3", "twins", "легендарный пес", 1, 3, 2, 4, 800, r"_/‾\_    U'ᴥ'U"),
    ("3", "security attack", "легендарный медведь", 1, 5, 2, 7, 1000, r"_/□\_    ʕ•ᴥ•ʔ"),
    ("3", "debuffer", "легендарный мистер карп", 2, 2, 1, 3, 700, r"_|¯|_      (°)#))<<"),
    ("3", "blitz", "легендарный баран", 1, 3, 2, 4, 750, r" @___ @    U^ｪ^U")
]

# Вставляем данные. executemany сам безопасно подставит все значения
cursor.executemany('''
INSERT INTO cards (rarity, type, name, count, hp, damage, energy, price, link_of_picture)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', cards_data)

conn.commit()
conn.close()

print("✅ База данных восстановлена: 17 карт успешно загружены!")