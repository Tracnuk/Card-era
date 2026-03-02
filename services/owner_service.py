import re
# Теперь эти имена будут найдены в файлах
from repositories.card_ownership import card_ownership_storage
from repositories.card_db_repository import cards_db_storage

class OwnerService:
    def get_inventory_text(self, account_id):
        try:
            # Вызываем метод через импортированный объект
            owned_data = card_ownership_storage.get_cards_in_account(account_id)
            
            if not owned_data:
                return "📦 <b>Твой инвентарь пуст!</b>"

            counts = {}
            for item in owned_data:
                # Берем card_id (обычно второй элемент в кортеже из БД)
                card_id = item[1] if len(item) > 1 else item[0]
                counts[card_id] = counts.get(card_id, 0) + 1

            msg = "🎒 <b>Твой инвентарь:</b>\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            
            for card_id, count in counts.items():
                card = cards_db_storage.get_card_by_id(card_id)
                
                if card:
                    # Индексы: 3-name, 9-picture, 5-hp, 6-dmg, 1-rarity
                    name = card[3]
                    icon_raw = card[9]
                    hp = card[5]
                    dmg = card[6]
                    rare = card[1]

                    # Форматируем рисунок в 2 строки
                    parts = re.split(r'\s{2,}', icon_raw)
                    icon_fixed = "\n".join([p.strip() for p in parts if p.strip()])

                    msg += f"<b>{name.upper()}</b> (x{count})\n"
                    msg += f"<pre>{icon_fixed}</pre>\n" 
                    msg += f"❤️ {hp} | ⚔️ {dmg} | ⭐ {rare}\n"
                    msg += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            
            return msg

        except Exception as e:
            return f"❌ Ошибка в OwnerService: {str(e)}"