import sys
import os
import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

# ================== НАСТРОЙКИ И ИМПОРТЫ ==================
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game import Game
from models.user_registration import UserRegistrationDTO
from services.shop_service import shop_service
from repositories.shop_repository import shop_storage

TOKEN = "vk1.a.OGgSNguAOhnJYU6LwhHbsBRmXJplU6x5nbM1zn6FczBo5eaK6hWNL1wczJAjZbvWFX2FgSakZABjNN0gEzr9FpXNG67aVOMc8U-RL67V7jj6GFxy9cc4yaQLdb9VJeeM5ScckIxUDTblvd5sZEDTqgVJNg6SXtdEt0kslC9O1-Bnkpdw_ZcKKLVNn72RxBE5wthaK0PbAR2D8gSRNeOEwg"
GROUP_ID = 237640143

game = Game()
user_states = {}

# ================== КЛАВИАТУРЫ ==================
def get_auth_menu():
    kb = VkKeyboard(inline=True)
    kb.add_button('📝 Регистрация', color=VkKeyboardColor.PRIMARY)
    kb.add_line()
    kb.add_button('🔐 Вход', color=VkKeyboardColor.PRIMARY)
    return kb.get_keyboard()

def get_start_menu():
    kb = VkKeyboard(inline=True)
    kb.add_button('🎮 Играть', color=VkKeyboardColor.PRIMARY)
    kb.add_button('👤 Профиль', color=VkKeyboardColor.SECONDARY)
    kb.add_line()
    kb.add_button('🚪 Выйти', color=VkKeyboardColor.NEGATIVE)
    return kb.get_keyboard()

def get_game_menu():
    kb = VkKeyboard(inline=True)
    kb.add_button('⚔️ Арена', color=VkKeyboardColor.SECONDARY)
    kb.add_button('🎒 Инвентарь', color=VkKeyboardColor.SECONDARY)
    kb.add_button('🛒 Магазин', color=VkKeyboardColor.POSITIVE)
    kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.PRIMARY)
    return kb.get_keyboard()

def get_back_to_play_menu():
    kb = VkKeyboard(inline=True)
    kb.add_button('🔙 Назад', color=VkKeyboardColor.PRIMARY)
    return kb.get_keyboard()

def get_dynamic_shop_menu():
    from repositories.shop_repository import shop_storage
    kb = VkKeyboard(inline=True)
    cards = shop_storage.get_all_shop_cards()
    
    # Распределяем товары по рядам (максимум 4 кнопки в ряду, максимум 5 рядов)
    rows = [[]]
    for c in cards:
        if len(rows[-1]) < 4:
            rows[-1].append(c['id'])
        else:
            if len(rows) < 5:
                rows.append([c['id']])
            else:
                break # Больше 20 товаров физически не влезут в лимиты ВК
    
    # Строим сетку кнопок
    for i, row in enumerate(rows):
        for card_id in row:
            kb.add_button(f"/buy_{card_id}", color=VkKeyboardColor.POSITIVE)
        # Переносим строку, если это еще не последний ряд товаров
        if i < len(rows) - 1:
            kb.add_line()
            
    # Добавляем финальный ряд для кнопки Назад
    if rows and rows[0]:
        kb.add_line()
    kb.add_button('🔙 Назад', color=VkKeyboardColor.PRIMARY)
    
    return kb.get_keyboard()

# ================== ОТПРАВКА СООБЩЕНИЙ ==================
def send_msg(vk, peer_id, text, keyboard=None):
    if not text: 
        return
    clean_text = text.replace("<b>", "").replace("</b>", "").replace("<pre>", "").replace("</pre>", "")
    clean_text = clean_text.replace("<code>", "").replace("</code>", "")
    vk.messages.send(peer_id=peer_id, message=clean_text, random_id=0, keyboard=keyboard)

# ================== ОБРАБОТЧИКИ СООБЩЕНИЙ ==================
def handle_message(vk, event):
    peer_id = event.message.peer_id
    text = event.message.text.strip()
    text_lower = text.lower()

    # --- СТЕЙТЫ РЕГИСТРАЦИИ И ВХОДА ---
    if peer_id in user_states:
        state_data = user_states[peer_id]
        current_state = state_data['state']

        if current_state == "RegisterStates:nickname":
            state_data['nickname'] = text
            state_data['state'] = "RegisterStates:login"
            send_msg(vk, peer_id, "Шаг 2/4: Введите логин:")
            return
            
        elif current_state == "RegisterStates:login":
            state_data['login'] = text
            state_data['state'] = "RegisterStates:password"
            send_msg(vk, peer_id, "Шаг 3/4: Введите пароль:")
            return
            
        elif current_state == "RegisterStates:password":
            state_data['password'] = text
            state_data['state'] = "RegisterStates:name"
            send_msg(vk, peer_id, "Шаг 4/4: Введите имя героя:")
            return
            
        elif current_state == "RegisterStates:name":
            try:
                user_dto = UserRegistrationDTO(
                    nickname=state_data['nickname'], 
                    login=state_data['login'],
                    password=state_data['password'], 
                    first_name=text
                )
                success, msg = game.register(user_dto)
                send_msg(vk, peer_id, str(msg), get_auth_menu())
            except Exception as e:
                send_msg(vk, peer_id, f"❌ Ошибка регистрации: {e}")
            finally:
                del user_states[peer_id]
            return

        elif current_state == "LoginStates:login":
            state_data['login'] = text
            state_data['state'] = "LoginStates:password"
            send_msg(vk, peer_id, "🔑 Введите пароль:")
            return
            
        elif current_state == "LoginStates:password":
            login_val = state_data.get("login")
            if game.login(peer_id, login_val, text):
                send_msg(vk, peer_id, "✅ Успешный вход!", get_start_menu())
            else:
                send_msg(vk, peer_id, "❌ Неверный логин или пароль.", get_auth_menu())
            del user_states[peer_id]
            return

    # --- НАВИГАЦИЯ И КНОПКИ ---
    if text_lower in ["/start", "начать"]:
        if game.verification(peer_id):
            send_msg(vk, peer_id, "👋 С возвращением!", get_start_menu())
        else:
            send_msg(vk, peer_id, "👋 Добро пожаловать! Войдите или зарегистрируйтесь:", get_auth_menu())

    elif text == "📝 Регистрация":
        user_states[peer_id] = {'state': "RegisterStates:nickname"}
        send_msg(vk, peer_id, "Шаг 1/4: Введите никнейм:")

    elif text == "🔐 Вход":
        user_states[peer_id] = {'state': "LoginStates:login"}
        send_msg(vk, peer_id, "🔑 Введите логин:")

    elif text == "🎮 Играть":
        if game.verification(peer_id):
            send_msg(vk, peer_id, "🎯 Выберите раздел:", get_game_menu())
        else:
            send_msg(vk, peer_id, "❌ Вы не авторизованы!")

    elif text == "🛒 Магазин":
        if not game.verification(peer_id):
            send_msg(vk, peer_id, "❌ Сначала войдите!")
            return
        shop_text = shop_service.get_shop_menu_text()
        # Выдаем динамическую клавиатуру с кнопками /buy_ID
        send_msg(vk, peer_id, shop_text, get_dynamic_shop_menu())

    elif text_lower.startswith("/buy_"):
        if not game.verification(peer_id):
            send_msg(vk, peer_id, "❌ Сначала войдите в аккаунт!")
            return
            
        parts = text.split("_")
        if len(parts) > 1 and parts[1].isdigit():
            try:
                card_id = int(parts[1])
                user_data = game.sessions.get(peer_id)
                account_id = user_data[0]
                
                result = shop_service.process_purchase(account_id, card_id)
                send_msg(vk, peer_id, result, get_back_to_play_menu())
            except Exception as e:
                logger.error(f"Ошибка при покупке: {e}")
                send_msg(vk, peer_id, "❌ Произошла техническая ошибка при покупке.")
        else:
            send_msg(vk, peer_id, "❌ Неверный формат. Используйте кнопки или формат: /buy_1")

    elif text == "🎒 Инвентарь":
        if not game.verification(peer_id):
            send_msg(vk, peer_id, "❌ Сначала войдите в аккаунт!")
            return
        
        # Инвентарь починен: передаем peer_id
        inventory_text = game.get_inventory_info(peer_id) 
        send_msg(vk, peer_id, inventory_text, get_back_to_play_menu())

    elif text == "👤 Профиль":
        send_msg(vk, peer_id, game.get_current_user(peer_id), get_start_menu())

    elif text == "🚪 Выйти":
        game.logout(peer_id)
        send_msg(vk, peer_id, "👋 До свидания! Вы вышли из аккаунта.", get_auth_menu())

    elif text in ["🔙 Назад", "back_to_main"]:
        send_msg(vk, peer_id, "🏠 Главное меню:", get_start_menu())

    elif text_lower == "/reset_inventory":
        if not game.verification(peer_id):
            send_msg(vk, peer_id, "❌ Сначала войдите!")
            return
            
        user_data = game.sessions.get(peer_id)
        if user_data:
            from repositories.card_ownership import card_ownership_storage
            account_id = user_data[0]
            card_ownership_storage.delete_all_user_cards(account_id)
            for _ in range(5):
                card_ownership_storage.add_card_and_account(5, account_id)
            send_msg(vk, peer_id, "✅ Инвентарь сброшен! Теперь только воробей.")

# ================== ЗАПУСК БОТА ==================
def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)

    logger.info("🚀 Бот ВК запущен!")
    
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            handle_message(vk, event)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass