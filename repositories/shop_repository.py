def get_all_shop_cards(self):
        try:
            with self._get_conn() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT rowid, * FROM cards')
                rows = cursor.fetchall()
                
                if not rows:
                    print("⚠️ Таблица 'cards' пуста или не найдена.")
                    return []

                # Определяем реальные имена колонок в твоей базе
                col_names = rows[0].keys()
                print(f"🔎 Колонки в БД: {col_names}")

                # Ищем индекс колонки, которая называется "ЦЕНА" (игнорируя пробелы и регистр)
                price_key = next((k for k in col_names if "ЦЕНА" in k.upper().strip()), None)
                name_key = next((k for k in col_names if "ИМЯ" in k.upper().strip()), None)
                icon_key = next((k for k in col_names if "ИКОНКА" in k.upper().strip()), None)

                shop_items = []
                for row in rows:
                    # Извлекаем цену по найденному ключу
                    raw_price = row[price_key] if price_key else 0
                    
                    try:
                        price_val = int(raw_price) if raw_price else 0
                        if price_val > 0:
                            # Превращаем row в обычный словарь для удобства сервиса
                            item = {
                                "rowid": row["rowid"],
                                "ИМЯ": row[name_key] if name_key else "Без названия",
                                "ЦЕНА": price_val,
                                "Иконка": row[icon_key] if icon_key else "",
                                "Редкость": row[0] # Обычно первая колонка
                            }
                            shop_items.append(item)
                    except (ValueError, TypeError):
                        continue
                
                print(f"✅ Найдено товаров: {len(shop_items)}")
                return shop_items
        except Exception as e:
            print(f"❌ Критическая ошибка в ShopRepository: {e}")
            return []