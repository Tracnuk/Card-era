import sqlite3
import os

class UserRepository:
    def __init__(self):
        # Путь к базе данных в той же папке
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "users.db")
        self.__create_table()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=20)

    def __create_table(self):
        with self._get_conn() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nickname TEXT,
                    login TEXT UNIQUE,
                    password TEXT,
                    first_name TEXT,
                    gold INTEGER DEFAULT 100,
                    lvl INTEGER DEFAULT 1
                )
            ''')

    def create_user(self, dto):
        """Метод для регистрации"""
        try:
            with self._get_conn() as conn:
                conn.execute(
                    "INSERT INTO users (nickname, login, password, first_name) VALUES (?, ?, ?, ?)",
                    (dto.nickname, dto.login, dto.password, dto.first_name)
                )
                return True, "Пользователь успешно создан!"
        except sqlite3.IntegrityError:
            return False, "Этот логин уже занят!"
        except Exception as e:
            return False, str(e)

    def auth_user(self, login, password):
        """Метод для входа"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE login = ? AND password = ?", 
                (login, password)
            )
            return cursor.fetchone()

# Создаем объект, который будем импортировать
user_storage = UserRepository()