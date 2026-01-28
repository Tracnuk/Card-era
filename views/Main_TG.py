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

# ================== ЛОГГЕР ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

# === Добавляем корень проекта ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.battle import *
from game.game import Game
from helpers.const import *
from models.user_registration import UserRegistrationDTO

# ================== НАСТРОЙКИ ==================
TOKEN = "8329664891:AAFuF4HaqWaAvzeFZJCNTped-eqWuwjO9pA"  # лучше вынести в .env
game = Game()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ================== FSM ==================
class RegisterStates(StatesGroup):
    nickname = State()
    login = State()
    password = State()
    name = State()

class LoginStates(StatesGroup):
    login = State()
    password = State()

# ================== ВСПОМОГАТЕЛЬНОЕ ==================
def process_game_result(result):
    if result is None:
        return "❌ Произошла ошибка (None)"
    if isinstance(result, tuple):
        if len(result) >= 2:
            return str(result[1])
        return str(result)
    return str(result)

# ================== КЛАВИАТУРЫ ==================
def get_register_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📝 Регистрация', callback_data="register")],
        [InlineKeyboardButton(text="🔐 Вход", callback_data="login")],
        [InlineKeyboardButton(text="❌ Удалить аккаунт", callback_data="delete_user")],
        [InlineKeyboardButton(text="🎮 Играть", callback_data="play")],
        [InlineKeyboardButton(text="ℹ️ Текущий пользователь", callback_data="current_user")],
        [InlineKeyboardButton(text="👥 Все пользователи", callback_data="all_users")]
    ])

def get_game_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Арена", callback_data="arena")],
        [InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inventory")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="🛒 Магазин", callback_data="shop")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="exit")]
    ])

# ================== START ==================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("👋 Добро пожаловать в игру!", reply_markup=get_register_menu())

# ================== РЕГИСТРАЦИЯ ==================
@dp.callback_query(F.data == "register")
async def register_user(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите никнейм:")
    await state.set_state(RegisterStates.nickname)

@dp.message(RegisterStates.nickname)
async def get_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer("Введите логин:")
    await state.set_state(RegisterStates.login)

@dp.message(RegisterStates.login)
async def get_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль:")
    await state.set_state(RegisterStates.password)

@dp.message(RegisterStates.password)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer("Введите имя:")
    await state.set_state(RegisterStates.name)

@dp.message(RegisterStates.name)
async def get_name(message: types.Message, state: FSMContext):
    logger.info(f"Имя получено: {message.text}")
    data = await state.get_data()

    try:
        user_data = UserRegistrationDTO(
            nickname=data["nickname"],
            login=data["login"],
            password=data["password"],
            first_name=message.text
        )

        result = game.register(user_data)
        await message.answer(
            process_game_result(result),
            reply_markup=get_register_menu()
        )

    except Exception as e:
        logger.exception("Ошибка регистрации")
        await message.answer(f"❌ Ошибка регистрации: {e}")

    finally:
        await state.clear()

# ================== ВХОД ==================
@dp.callback_query(F.data == "login")
async def login_user(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите логин:")
    await state.set_state(LoginStates.login)

@dp.message(LoginStates.login)
async def login_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль:")
    await state.set_state(LoginStates.password)

@dp.message(LoginStates.password)
async def login_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    result = game.login(data["login"], message.text)
    await message.answer(process_game_result(result), reply_markup=get_register_menu())
    await state.clear()

# ================== ИГРА ==================
@dp.callback_query(F.data == "play")
async def play(callback: types.CallbackQuery):
    if game.verification():
        await callback.message.answer("🎮 Игра началась!", reply_markup=get_game_menu())
    else:
        await callback.message.answer("❌ Сначала войдите в аккаунт")

@dp.callback_query(F.data == "arena")
async def arena_cb(callback: types.CallbackQuery):
    arena()
    await callback.message.answer("⚔️ Арена")

@dp.callback_query(F.data == "inventory")
async def inventory_cb(callback: types.CallbackQuery):
    inventory()
    await callback.message.answer("🎒 Инвентарь")

@dp.callback_query(F.data == "settings")
async def settings_cb(callback: types.CallbackQuery):
    settings()
    await callback.message.answer("⚙️ Настройки")

@dp.callback_query(F.data == "shop")
async def shop_cb(callback: types.CallbackQuery):
    shop()
    await callback.message.answer("🛒 Магазин")

@dp.callback_query(F.data == "exit")
async def exit_cb(callback: types.CallbackQuery):
    await callback.message.answer("🚪 Выход", reply_markup=get_register_menu())

# ================== ПОЛЬЗОВАТЕЛИ ==================
@dp.callback_query(F.data == "current_user")
async def current_user(callback: types.CallbackQuery):
    await callback.message.answer(str(game.get_current_user()))

@dp.callback_query(F.data == "all_users")
async def all_users(callback: types.CallbackQuery):
    users = game.get_all_users()
    await callback.message.answer(str(users)[:4000])

# ================== УДАЛЕНИЕ ==================
@dp.callback_query(F.data == "delete_user")
async def delete_user(callback: types.CallbackQuery):
    result = game.delete_user()
    await callback.message.answer(
        process_game_result(result),
        reply_markup=get_register_menu()
    )

# ================== ЗАПУСК ==================
async def main():
    logger.info("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
