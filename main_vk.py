import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sys
import os
import json

# Подключаем твои модули
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game import Game
from models.user_registration import UserRegistrationDTO
from services.shop_service import shop_service
from repositories.card_ownership import card_ownership_storage

TOKEN = "vk1.a.OGgSNguAOhnJYU6LwhHbsBRmXJplU6x5nbM1zn6FczBo5eaK6hWNL1wczJAjZbvWFX2FgSakZABjNN0gEzr9FpXNG67aVOMc8U-RL67V7jj6GFxy9cc4yaQLdb9VJeeM5ScckIxUDTblvd5sZEDTqgVJNg6SXtdEt0kslC9O1-Bnkpdw_ZcKKLVNn72RxBE5wthaK0PbAR2D8gSRNeOEwg"
GROUP_ID = 237640143 

game = Game()
user_states = {}

# --- КЛАВИАТУРЫ ---
def get_auth_menu():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('📝 Регистрация', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🔐 Вход', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()

def get_start_menu():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('🎮 Играть', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('👤 Профиль', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('🚪 Выйти', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

def get_game_menu():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('⚔️ Арена', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('🎒 Инвентарь', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('🛒 Магазин', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад', color=VkKeyboardColor.DEFAULT)
    return keyboard.get_keyboard()

def send_msg(vk, peer_id, text, keyboard=None):
    # Очистка текста от HTML-тегов
    clean_text = text.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", "")
    
    # Формируем параметры запроса
    params = {
        "peer_id": peer_id,
        "message": clean_text,
        "random_id": 0
    }
    
    # Если передана клавиатура, упаковываем её правильно
    if keyboard:
        # ПРОВЕРКА: записываем строго в params["keyboard"]
        if isinstance(keyboard, (dict, list)):
            params["keyboard"] = json.dumps(keyboard, ensure_ascii=False)
        else:
            params["keyboard"] = keyboard
            
    try:
        vk.messages.send(**params)
    except Exception as e:
        print(f"❌ Ошибка VK API: {e}")

# --- ГЛАВНАЯ ЛОГИКА ---
def handle_message(vk, event):
    peer_id = event.message.peer_id
    text = event.message.text.strip()
    t_low = text.lower()

    # 1. Обработка регистрации (FSM)
    if peer_id in user_states:
        state = user_states[peer_id]
        if state['mode'] == 'reg':
            steps = ['nick', 'login', 'pass', 'name']
            curr_idx = steps.index(state['step'])
            
            if state['step'] == 'nick': state['nickname'] = text
            elif state['step'] == 'login': state['login'] = text
            elif state['step'] == 'pass': state['password'] = text
            elif state['step'] == 'name':
                try:
                    dto = UserRegistrationDTO(state['nickname'], state['login'], state['password'], text)
                    success, msg = game.register(dto)
                    if success:
                        game.login(state['login'], state['password'])
                        acc_id = game.current_user[0]
                        for _ in range(5): 
                            card_ownership_storage.add_card_and_account(5, acc_id)
                        send_msg(vk, peer_id, "✅ Регистрация успешна! 5 воробьёв выдано.", get_start_menu())
                    else:
                        send_msg(vk, peer_id, f"❌ {msg}", get_auth_menu())
                except Exception as e:
                    send_msg(vk, peer_id, f"Ошибка: {e}", get_auth_menu())
                del user_states[peer_id]
                return

            next_step = steps[curr_idx + 1]
            state['step'] = next_step
            prompts = {
                'login': "🔑 Введите логин:", 
                'pass': "🔒 Введите пароль:", 
                'name': "🎭 Введите имя героя:"
            }
            send_msg(vk, peer_id, prompts[next_step], get_auth_menu())
            return

    # 2. Навигация
    if t_low in ["начать", "start", "🔙 назад"]:
        if True:
            send_msg(vk, peer_id, "🏠 Главное меню:", get_start_menu())
        else:
            send_msg(vk, peer_id, "👋 Привет! Войдите или зарегистрируйтесь:", get_auth_menu())

    elif "регистрация" in t_low:
        user_states[peer_id] = {'mode': 'reg', 'step': 'nick'}
        send_msg(vk, peer_id, "👤 Шаг 1/4: Введите никнейм:", get_auth_menu())

    elif "вход" in t_low:
        send_msg(vk, peer_id, "🔑 Введите логин:", get_auth_menu())

    elif "играть" in t_low:
        if game.verification(): 
            send_msg(vk, peer_id, "🎯 Выберите раздел:", get_game_menu())
        else: 
            send_msg(vk, peer_id, "⚠️ Нужно войти!", get_auth_menu())

    elif "инвентарь" in t_low:
        if game.verification(): 
            send_msg(vk, peer_id, game.get_inventory_info(), get_game_menu())

    elif "профиль" in t_low:
        if game.verification(): 
            send_msg(vk, peer_id, f"👤 Ваш профиль:\n{game.current_user}", get_start_menu())

def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    print("🚀 Бот запущен!")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            handle_message(vk, event)

if __name__ == "__main__":
    main()