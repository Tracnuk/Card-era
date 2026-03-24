import sqlite3
import os

class ShopRepository:
    def __init__(self):
        # Используем ту же базу, где лежат карты
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "cards.db")

    def _get_conn(self):
        return sqlite3.connect(self.db_path, timeout=20)

    def get_all_shop_cards(self):
        """Возвращает карты, у которых есть цена (price > 0)"""
        with self._get_conn() as conn:
            cursor = conn.cursor()
            # Предполагаем, что цена лежит в 8-й колонке (индекс 8)
            cursor.execute('SELECT id, ИМЯ, ЦЕНА, Редкость')
            return cursor.fetchall()

shop_storage = ShopRepository()