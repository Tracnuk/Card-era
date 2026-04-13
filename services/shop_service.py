from repositories.shop_repository import shop_storage

class ShopService:
    def get_shop_menu_text(self):
        try:
            cards = shop_storage.get_all_shop_cards()
            
            # Если база вернула пустоту
            if not cards:
                return "🛒 <b>В магазине пока нет товаров.</b>\n\nСкорее всего, цены еще не установлены или товары закончились."
            
            text = "🛒 <b>МАГАЗИН ЖИВОТНЫХ</b>\n"
            text += "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n"
            
            for c in cards:
                # Пропускаем «битые» карточки прямо в цикле на всякий случай
                try:
                    price = float(c.get('price', 0))
                    if price <= 0:
                        continue
                except (ValueError, TypeError):
                    continue

                # Формируем карточку товара
                text += f"<code>{c.get('icon', '🐾')}</code>\n"
                text += f"🔹 <b>{str(c['name']).upper()}</b>\n"
                text += f"Цена: 💰 <code>{c['price']}</code> | Ранг: {c['rarity']}\n"
                text += f"Купить: /buy_{c['id']}\n\n"
            
            # Если после фильтрации список стал пустым
            if text == "🛒 <b>МАГАЗИН ЖИВОТНЫХ</b>\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n":
                 return "🛒 <b>Магазин временно пуст.</b>\nДоступных товаров с ценой не найдено."

            return text
            
        except Exception as e:
            # Не палим подробности ошибки юзеру, пишем просто
            return "❌ Не удалось загрузить список товаров. Попробуйте позже."

shop_service = ShopService()