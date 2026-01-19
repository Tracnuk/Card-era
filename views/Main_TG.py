import asyncio
import sys
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

# === Добавляем корень проекта для импорта ===
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.battle import *
from game.game import Game
from models.user_registration import UserRegistrationDTO

# === НАСТРОЙКИ ===
TOKEN = "8329664891:AAFuF4HaqWaAvzeFZJCNTped-eqWuwjO9pA"
bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# === GAME НА КАЖДОГО ПОЛЬЗОВАТЕЛЯ ===
games: dict[int, Game] = {}

def get_game(user_id: int) -> Game:
    if user_id not in games:
        games[user_id] = Game()
    return games[user_id]

# === FSM ===
class RegisterStates(StatesGroup):
    nickname = State()
    login = State()
    password = State()
    name = State()

class LoginStates(StatesGroup):
    login = State()
    password = State()

# === МЕНЮ ===
def get_register_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Регистрация", callback_data="register")],
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

# === /start ===
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("👋 Добро пожаловать в игру!\nВыберите действие:", reply_markup=get_register_menu())

# === РЕГИСТРАЦИЯ ===
@dp.callback_query(F.data == "register")
async def register(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(RegisterStates.nickname)
    await callback.message.answer("Введите никнейм:")

@dp.message(RegisterStates.nickname)
async def reg_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await state.set_state(RegisterStates.login)
    await message.answer("Введите логин:")

@dp.message(RegisterStates.login)
async def reg_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(RegisterStates.password)
    await message.answer("Введите пароль:")

@dp.message(RegisterStates.password)
async def reg_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await state.set_state(RegisterStates.name)
    await message.answer("Введите имя:")

@dp.message(RegisterStates.name)
async def reg_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not data:
        await message.answer("❌ Данные потеряны. Начните регистрацию заново.", reply_markup=get_register_menu())
        await state.clear()
        return

    game = get_game(message.from_user.id)
    user = UserRegistrationDTO(
        nickname=data.get("nickname"),
        login=data.get("login"),
        password=data.get("password"),
        first_name=message.text
    )
    result = game.register(user)
    await message.answer(result, reply_markup=get_register_menu())
    await state.clear()

# === ВХОД ===
@dp.callback_query(F.data == "login")
async def login(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LoginStates.login)
    await callback.message.answer("Введите логин:")

@dp.message(LoginStates.login)
async def login_input(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(LoginStates.password)
    await message.answer("Введите пароль:")

@dp.message(LoginStates.password)
async def login_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not data:
        await message.answer("❌ Данные входа утеряны.", reply_markup=get_register_menu())
        await state.clear()
        return

    game = get_game(message.from_user.id)
    result = game.login(data.get("login"), message.text)
    await message.answer(result, reply_markup=get_register_menu())
    await state.clear()

# === ИГРА ===
@dp.callback_query(F.data == "play")
async def play(callback: types.CallbackQuery):
    game = get_game(callback.from_user.id)
    if game.verification():
        await callback.message.answer("🎮 Добро пожаловать в игру!", reply_markup=get_game_menu())
    else:
        await callback.message.answer("❌ Вы не вошли в аккаунт")

@dp.callback_query(F.data == "arena")
async def arena_cb(callback: types.CallbackQuery):
    arena()
    await callback.message.answer("⚔️ Битва началась!")

@dp.callback_query(F.data == "inventory")
async def inventory_cb(callback: types.CallbackQuery):
    inventory()
    await callback.message.answer("🎒 Инвентарь открыт")

@dp.callback_query(F.data == "settings")
async def settings_cb(callback: types.CallbackQuery):
    settings()
    await callback.message.answer("⚙️ Настройки открыты")

@dp.callback_query(F.data == "shop")
async def shop_cb(callback: types.CallbackQuery):
    shop()
    await callback.message.answer("🛒 Магазин открыт")

@dp.callback_query(F.data == "exit")
async def exit_cb(callback: types.CallbackQuery):
    await callback.message.answer("🚪 Главное меню", reply_markup=get_register_menu())

# === ПОЛЬЗОВАТЕЛИ ===
@dp.callback_query(F.data == "current_user")
async def current_user(callback: types.CallbackQuery):
    game = get_game(callback.from_user.id)
    await callback.message.answer(str(game.get_current_user()))

@dp.callback_query(F.data == "all_users")
async def all_users(callback: types.CallbackQuery):
    game = get_game(callback.from_user.id)
    users = game.get_all_users()
    if not users:
        await callback.message.answer("📭 Нет пользователей")
        return
    text = "\n".join(str(u) for group in users for u in group)
    await callback.message.answer(text)

@dp.callback_query(F.data == "delete_user")
async def delete_user(callback: types.CallbackQuery):
    game = get_game(callback.from_user.id)
    result = game.delete_user()  # ⚡ внутри delete_user теперь открывается соединение SQLite на каждый запрос
    await callback.message.answer(result, reply_markup=get_register_menu())

# === ЗАПУСК ===
async def main():
    print("✅ Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
