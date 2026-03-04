from repositories.shop_repository import shop_storage
from repositories.user_repository import user_storage
from repositories.card_ownership import card_ownership_storage
from repositories.card_db_repository import cards_db_storage

class ShopService:
    def get_shop_menu_text(self):  # <--- ПРОВЕРЬ ЭТО ИМЯ
        try:
            cards = shop_storage.get_all_shop_cards()
            if not cards:
                return "🛒 <b>Магазин временно пуст!</b>\n(Убедитесь, что в БД у карт цена > 0)"
            
            text = "🛒 <b>Магазин карт</b>\n"
            text += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            for c in cards:
                # c[0]-id, c[1]-name, c[2]-price, c[3]-rarity
                text += f"🔹 <b>{c[1]}</b>\nЦена: 💰 <code>{c[2]}</code> | {c[3]}\n"
                text += f"Купить: /buy_{c[0]}\n\n"
            return text
        except Exception as e:
            return f"❌ Ошибка магазина: {e}"

    def process_purchase(self, user_id, card_id):
        # Логика покупки (проверка золота и т.д.)
        card = cards_db_storage.get_card_by_id(card_id)
        if not card: return "❌ Карта не найдена."
        
        price = card[8] 
        user = user_storage.get_user_by_id(user_id)
        if user[5] < price:
            return "❌ Недостаточно золота!"

        user_storage.update_gold(user_id, user[5] - price)
        card_ownership_storage.add_card_and_account(card_id, user_id)
        return f"✅ Куплено: {card[3]}"

shop_service = ShopService()