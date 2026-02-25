import re
# Импортируем классы из твоих файлов
from repositories.card_ownership import CardOwnership
from repositories.card_db_repository import CardDbRepository

# СОЗДАЕМ ОБЪЕКТЫ (ЭКЗЕМПЛЯРЫ). 
# Именно через них нужно вызывать методы, чтобы self передавался автоматически.
card_ownership_storage = CardOwnership()
cards_db_storage = CardDbRepository()

class OwnerService:
    def get_inventory_text(self, account_id):
        try:
            # Вызываем через ОБЪЕКТ (с маленькой буквы), а не через КЛАСС
            owned_data = card_ownership_storage.get_cards_in_account(account_id)
            
            if not owned_data:
                return "📦 <b>Твой инвентарь пуст!</b>"

            counts = {}
            for item in owned_data:
                # В зависимости от твоей БД: (id, card_id, account_id) -> берем card_id
                card_id = item[1] if len(item) > 1 else item[0]
                counts[card_id] = counts.get(card_id, 0) + 1

            msg = "🎒 <b>Твой инвентарь:</b>\n"
            msg += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            
            for card_id, count in counts.items():
                card = cards_db_storage.get_card_by_id(card_id)
                
                if card:
                    # Извлекаем данные по индексам твоей таблицы cards
                    name = card[3]
                    icon_raw = card[9]
                    hp = card[5]
                    dmg = card[6]
                    rare = card[1]

                    # Логика разбиения рисунка на 2 строки (по 2+ пробелам)
                    parts = re.split(r'\s{2,}', icon_raw)
                    icon_fixed = "\n".join([p.strip() for p in parts if p.strip()])

                    msg += f"<b>{name.upper()}</b> (x{count})\n"
                    msg += f"<pre>{icon_fixed}</pre>\n" 
                    msg += f"❤️ {hp} | ⚔️ {dmg} | ⭐ {rare}\n"
                    msg += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
                else:
                    msg += f"❓ <b>Неизвестная карта #{card_id}</b> — {count} шт.\n\n"
            
            return msg

        except Exception as e:
            return f"❌ Ошибка в OwnerService: {str(e)}"