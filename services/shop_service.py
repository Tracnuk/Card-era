from repositories.shop_repository import shop_storage

class ShopService:
    def get_shop_menu_text(self):
        try:
            cards = shop_storage.get_all_shop_cards()
            if not cards:
                return "🛒 <b>Магазин пуст!</b>\n\nПроверь, чтобы в колонке <b>price</b> стояли числа больше 0."
            
            text = "🛒 <b>МАГАЗИН ЖИВОТНЫХ</b>\n"
            text += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            
            for c in cards:
                # ASCII-арт (icon) выводим моноширинным шрифтом
                text += f"<code>{c['icon']}</code>\n"
                text += f"🔹 <b>{str(c['name']).upper()}</b>\n"
                text += f"Цена: 💰 <code>{c['price']}</code> | Ранг: {c['rarity']}\n"
                text += f"Купить: /buy_{c['id']}\n\n"
            
            return text
        except Exception as e:
            return f"❌ Ошибка сервиса: {e}"

shop_service = ShopService()