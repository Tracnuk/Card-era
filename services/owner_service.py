import re
from repositories.card_ownership import card_ownership_storage
from repositories.card_db_repository import cards_db_storage

class OwnerService:
    def get_inventory_text(self, account_id):
        try:
            # Получаем список кортежей вида [(5,), (5,)]
            owned_data = card_ownership_storage.get_cards_in_account(account_id)
            
            if not owned_data:
                return "📦 Твой инвентарь пуст! Загляни в магазин."

            counts = {}
            for item in owned_data:
                # ИСПРАВЛЕНО: Берем индекс 0, так как в SQL только одна колонка
                card_id = item[0] 
                counts[card_id] = counts.get(card_id, 0) + 1

            msg = "🎒 ТВОЙ ИНВЕНТАРЬ:\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            
            for card_id, count in counts.items():
                card = cards_db_storage.get_card_by_id(card_id)
                if card:
                    # Индексы согласно твоей структуре БД
                    name = card[3]
                    icon_raw = card[9]
                    hp = card[5]
                    dmg = card[6]
                    rare = card[1]

                    # Форматируем рисунок карты для ВК
                    parts = re.split(r'\s{2,}', icon_raw)
                    icon_fixed = "\n".join([p.strip() for p in parts if p.strip()])

                    # Собираем чистый текст без тегов <b> и <pre>
                    msg += f"● {name.upper()} (x{count})\n"
                    msg += f"{icon_fixed}\n" 
                    msg += f"❤️ HP: {hp} | ⚔️ DMG: {dmg} | ⭐ {rare}\n"
                    msg += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            
            return msg
        except Exception as e:
            return f"❌ Ошибка в OwnerService: {str(e)}"