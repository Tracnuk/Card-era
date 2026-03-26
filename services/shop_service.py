from repositories.shop_repository import shop_storage

class ShopService:
    def get_shop_menu_text(self):
        try:
            cards = shop_storage.get_all_shop_cards()
            if not cards:
                return "🛒 <b>Магазин пока пуст!</b>"
            
            text = "🛒 <b>МАГАЗИН ЖИВОТНЫХ</b>\n"
            text += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            
            for c in cards:
                text += f"<code>{c['Иконка']}</code>\n"
                text += f"🔹 <b>{str(c['ИМЯ']).upper()}</b>\n"
                text += f"Цена: 💰 <b>{c['ЦЕНА']}</b> | Ранг: {c['Редкость']}\n"
                text += f"Купить: /buy_{c['rowid']}\n\n"
            
            return text
        except Exception as e:
            return f"❌ Ошибка в сервисе: {e}"

shop_service = ShopService()