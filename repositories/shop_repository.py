import sqlite3
import os

class ShopRepository:
    def __init__(self):
        # Поднимаемся на уровень выше из папки repositories в корень проекта
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir) 
        
        self.db_path = os.path.join(project_root, "cards.db")
        
        # Контрольный принт в консоль при запуске
        print(f"DEBUG: Бот подключается к базе по пути: {self.db_path}")

    def _get_conn(self):
        # Добавим проверку, вообще есть ли файл
        if not os.path.exists(self.db_path):
            print(f"⚠️ ВНИМАНИЕ: Файл базы {self.db_path} не найден!")
            
        conn = sqlite3.connect(self.db_path, timeout=20)
        conn.row_factory = sqlite3.Row 
        return conn

    def get_all_shop_cards(self):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                
                # --- ДИАГНОСТИКА ---
                cursor.execute('SELECT count(*) as total FROM cards')
                total = cursor.fetchone()['total']
                print(f"--- ДИАГНОСТИКА: Всего строк в таблице cards: {total} ---")
                
                if total > 0:
                    cursor.execute('SELECT id, name, price FROM cards LIMIT 3')
                    samples = cursor.fetchall()
                    for s in samples:
                        print(f"DEBUG: Пример в базе -> ID: {s['id']}, Name: {s['name']}, Price: {s['price']}")
                # -------------------

                cursor.execute('SELECT * FROM cards WHERE price > 0')
                rows = cursor.fetchall()
                
                shop_items = []
                for row in rows:
                    shop_items.append({
                        "id": row["id"],
                        "name": row["name"],
                        "price": row["price"],
                        "icon": row["link_of_picture"] if "link_of_picture" in row.keys() else "🐾",
                        "rarity": row["rarity"]
                    })
                
                if not shop_items:
                    print("⚠️ Магазин пуст: либо строк 0, либо у всех цена <= 0")
                else:
                    print(f"✅ Успешно подгружено: {len(shop_items)} товаров")
                    
                return shop_items
        except Exception as e:
            print(f"❌ Ошибка в ShopRepository: {e}")
            return []

shop_storage = ShopRepository()