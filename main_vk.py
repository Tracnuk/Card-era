import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import sys
import os
import logging
import re

# Настройка путей и логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game import Game
from models.user_registration import UserRegistrationDTO

# Глобальный объект игры (чтобы не вылетало из аккаунта)
game = Game()
user_states = {}

# Твои настройки
TOKEN = "vk1.a.OGgSNguAOhnJYU6LwhHbsBRmXJplU6x5nbM1zn6FczBo5eaK6hWNL1wczJAjZbvWFX2FgSakZABjNN0gEzr9FpXNG67aVOMc8U-RL67V7jj6GFxy9cc4yaQLdb9VJeeM5ScckIxUDTblvd5sZEDTqgVJNg6SXtdEt0kslC9O1-Bnkpdw_ZcKKLVNn72RxBE5wthaK0PbAR2D8gSRNeOEwg"
GROUP_ID = 237640143 

# ================== КЛАВИАТУРЫ ==================
def get_auth_menu():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('📝 Регистрация', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('🔐 Вход', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()

def get_game_menu():
    keyboard = VkKeyboard(inline=True)
    keyboard.add_button('⚔️ Арена', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('🎒 Инвентарь', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('🛒 Магазин', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('🔙 Назад', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()

# ================== ФУНКЦИЯ ОЧИСТКИ И ОТПРАВКИ ==================
def send_msg(vk, peer_id, text, keyboard=None):
    if not text: return
    
    # ПЕРЕНОС ЛОГИКИ: Чистим всё, что ломает вид в ВК
    clean_text = text.replace("<b>", "").replace("</b>", "")
    clean_text = clean_text.replace("<pre>", "").replace("</pre>", "")
    clean_text = clean_text.replace("<code>", "» ").replace("</code>", " «")
    
    params = {"peer_id": peer_id, "message": clean_text, "random_id": 0}
    if keyboard: params["keyboard"] = keyboard
    vk.messages.send(**params)

# ================== ОБРАБОТЧИК ==================
def handle_message(vk, event):
    peer_id = event.message.peer_id
    text = event.message.text.strip()
    t_low = text.lower()

    if t_low in ["начать", "start", "назад", "🔙 назад"]:
        user_states.pop(peer_id, None)
        if game.verification():
            send_msg(vk, peer_id, "🎮 Вы в игре!", get_game_menu())
        else:
            send_msg(vk, peer_id, "👋 Привет! Войдите или зарегистрируйтесь:", get_auth_menu())
        return

    # Логика регистрации/входа (FSM)
    if peer_id in user_states:
        st = user_states[peer_id]
        if st['mode'] == 'register':
            if st['step'] == 'nick':
                st['data']['nick'] = text
                st['step'] = 'log'; send_msg(vk, peer_id, "Введите логин:")
            elif st['step'] == 'log':
                st['data']['log'] = text
                st['step'] = 'pass'; send_msg(vk, peer_id, "Введите пароль:")
            elif st['step'] == 'pass':
                st['data']['pass'] = text
                st['step'] = 'name'; send_msg(vk, peer_id, "Имя героя:")
            elif st['step'] == 'name':
                dto = UserRegistrationDTO(nickname=st['data']['nick'], login=st['data']['log'], 
                                         password=st['data']['pass'], first_name=text)
                _, msg = game.register(dto)
                send_msg(vk, peer_id, str(msg), get_auth_menu())
                user_states.pop(peer_id)
            return
        elif st['mode'] == 'login':
            if st['step'] == 'log':
                st['data']['log'] = text
                st['step'] = 'pass'; send_msg(vk, peer_id, "Пароль:")
            elif st['step'] == 'pass':
                if game.login(st['data']['log'], text):
                    send_msg(vk, peer_id, "✅ Успешный вход!", get_game_menu())
                else:
                    send_msg(vk, peer_id, "❌ Ошибка входа.", get_auth_menu())
                user_states.pop(peer_id)
            return

    # КНОПКИ МЕНЮ
    if "регистрация" in t_low:
        user_states[peer_id] = {'mode': 'register', 'step': 'nick', 'data': {}}
        send_msg(vk, peer_id, "Шаг 1: Никнейм:")
    elif "вход" in t_low:
        user_states[peer_id] = {'mode': 'login', 'step': 'log', 'data': {}}
        send_msg(vk, peer_id, "Логин:")
    elif "играть" in t_low:
        send_msg(vk, peer_id, "🎯 Меню игры:", get_game_menu())
    
    # РАБОЧИЙ ИНВЕНТАРЬ
    elif "инвентарь" in t_low:
        if game.verification():
            # Вызываем твою рабочую логику из OwnerService через Game
            inv_text = game.get_inventory_info() 
            send_msg(vk, peer_id, inv_text, get_game_menu())
        else:
            send_msg(vk, peer_id, "❌ Сначала войдите!", get_auth_menu())

def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)
    print("🚀 Бот ВК запущен!")
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:
            handle_message(vk_session.get_api(), event)

if __name__ == "__main__":
    main()