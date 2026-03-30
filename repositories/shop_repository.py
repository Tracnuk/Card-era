import sqlite3
import os

class ShopRepository:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(current_dir, "cards.db")

    def _get_conn(self):
        conn = sqlite3.connect(self.db_path, timeout=20)
        conn.row_factory = sqlite3.Row # Чтобы обращаться по именам колонок
        return conn

    def get_all_shop_cards(self):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                # Используем реальные имена из твоей схемы
                cursor.execute('SELECT * FROM cards WHERE price > 0')
                rows = cursor.fetchall()
                
                shop_items = []
                for row in rows:
                    shop_items.append({
                        "id": row["id"],
                        "name": row["name"],
                        "price": row["price"],
                        "icon": row["link_of_picture"], # Твой ASCII-арт лежит здесь
                        "rarity": row["rarity"]
                    })
                
                print(f"✅ Найдено в магазине: {len(shop_items)} карт")
                return shop_items
        except Exception as e:
            print(f"❌ Ошибка ShopRepository: {e}")
            return []

shop_storage = ShopRepository()