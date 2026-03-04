import asyncio
import sys
import os
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# ================== НАСТРОЙКИ И ИМПОРТЫ ==================
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

# Добавляем корневую папку в путь, чтобы импорты из других папок работали
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.game import Game
from models.user_registration import UserRegistrationDTO
from services.shop_service import shop_service  # Импорт нового сервиса магазина

TOKEN = "8329664891:AAFuF4HaqWaAvzeFZJCNTped-eqWuwjO9pA" 
game = Game()
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================== СОСТОЯНИЯ (FSM) ==================
class RegisterStates(StatesGroup):
    nickname = State()
    login = State()
    password = State()
    name = State()

class LoginStates(StatesGroup):
    login = State()
    password = State()

# ================== КЛАВИАТУРЫ ==================
def get_auth_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📝 Регистрация', callback_data="register")],
        [InlineKeyboardButton(text="🔐 Вход", callback_data="login")]
    ])

def get_start_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", callback_data="play")],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="logout")]
    ])

def get_game_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Арена", callback_data="arena")],
        [InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inventory")],
        [InlineKeyboardButton(text="🛒 Магазин", callback_data="shop")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])

# ================== ОБРАБОТЧИКИ (HANDLERS) ==================

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if game.verification():
        await message.answer("👋 С возвращением!", reply_markup=get_start_menu())
    else:
        await message.answer("👋 Добро пожаловать! Войдите или зарегистрируйтесь:", reply_markup=get_auth_menu())

# --- РЕГИСТРАЦИЯ ---
@dp.callback_query(F.data == "register")
async def reg_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Шаг 1/4: Введите никнейм:")
    await state.set_state(RegisterStates.nickname)

@dp.message(RegisterStates.nickname)
async def reg_nick(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer("Шаг 2/4: Введите логин:")
    await state.set_state(RegisterStates.login)

@dp.message(RegisterStates.login)
async def reg_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Шаг 3/4: Введите пароль:")
    await state.set_state(RegisterStates.password)

@dp.message(RegisterStates.password)
async def reg_pass(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer("Шаг 4/4: Введите имя героя:")
    await state.set_state(RegisterStates.name)

@dp.message(RegisterStates.name)
async def reg_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    try:
        user_dto = UserRegistrationDTO(
            nickname=data['nickname'], login=data['login'],
            password=data['password'], first_name=message.text
        )
        success, msg = game.register(user_dto)
        await message.answer(str(msg), reply_markup=get_auth_menu())
    except Exception as e:
        await message.answer(f"❌ Ошибка регистрации: {e}")
    finally:
        await state.clear()

# --- ВХОД ---
@dp.callback_query(F.data == "login")
async def login_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("🔑 Введите логин:")
    await state.set_state(LoginStates.login)

@dp.message(LoginStates.login)
async def login_get_log(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("🔑 Введите пароль:")
    await state.set_state(LoginStates.password)

@dp.message(LoginStates.password)
async def login_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if game.login(data.get("login"), message.text):
        await message.answer("✅ Успешный вход!", reply_markup=get_start_menu())
    else:
        await message.answer("❌ Неверный логин или пароль.", reply_markup=get_auth_menu())
    await state.clear()

# --- ГЕЙМПЛЕЙ И МАГАЗИН ---
@dp.callback_query(F.data == "play")
async def play_menu(callback: types.CallbackQuery):
    if game.verification():
        await callback.message.edit_text("🎯 Выберите раздел:", reply_markup=get_game_menu())
    else:
        await callback.answer("❌ Вы не авторизованы!", show_alert=True)

@dp.callback_query(F.data == "shop")
async def shop_cb(callback: types.CallbackQuery):
    if not game.verification():
        await callback.answer("❌ Сначала войдите!")
        return
    
    # Получаем текст товаров из сервиса
    text = shop_service.get_shop_menu_text()
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="play")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="HTML")

@dp.message(F.text.startswith("/buy_"))
async def buy_handler(message: types.Message):
    if not game.verification():
        await message.answer("❌ Сначала войдите в аккаунт!")
        return

    try:
        # Извлекаем ID карты из команды /buy_1 -> 1
        card_id = int(message.text.split("_")[1])
        user_id = game.current_user[0]
        
        result = shop_service.process_purchase(user_id, card_id)
        
        # Обновляем данные текущего пользователя в объекте game, 
        # чтобы золото обновилось в профиле мгновенно
        game.login(game.current_user[2], game.current_user[3]) 
        
        await message.answer(result, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Ошибка при покупке: {e}")
        await message.answer("❌ Используйте формат: /buy_ID (например /buy_1)")

@dp.callback_query(F.data == "inventory")
async def inventory_cb(callback: types.CallbackQuery):
    await callback.answer()
    inventory_text = game.get_inventory_info()
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="🔙 Назад", callback_data="play")]])
    await callback.message.answer(inventory_text, reply_markup=kb, parse_mode="HTML")

@dp.callback_query(F.data == "profile")
async def profile_cb(callback: types.CallbackQuery):
    await callback.message.answer(game.get_current_user(), reply_markup=get_start_menu(), parse_mode="HTML")

@dp.callback_query(F.data == "logout")
async def logout_cb(callback: types.CallbackQuery):
    game.logout()
    await callback.message.edit_text("👋 До свидания! Вы вышли из аккаунта.", reply_markup=get_auth_menu())

@dp.callback_query(F.data == "back_to_main")
async def back_main(callback: types.CallbackQuery):
    await callback.message.edit_text("🏠 Главное меню:", reply_markup=get_start_menu())

# --- ЗАПУСК ---
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass