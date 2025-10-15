import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import CommandStart, Command
import os
import sys

# Добавляем пути для импорта твоих модулей
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from game.battle import *
from game.game import Game
from helpers.const import *
from models.user_registration import UserRegistrationDTO

# === Настройки ===
TOKEN = "8329664891:AAFuF4HaqWaAvzeFZJCNTped-eqWuwjO9pA"
game = Game()

# === Инициализация бота ===
bot = Bot(token=TOKEN)
dp = Dispatcher()


# === Главное меню регистрации ===
def get_register_menu():
    kb = [
        [InlineKeyboardButton(text="📝 Регистрация", callback_data="register")],
        [InlineKeyboardButton(text="🔐 Вход", callback_data="login")],
        [InlineKeyboardButton(text="❌ Удалить аккаунт", callback_data="delete_user")],
        [InlineKeyboardButton(text="🎮 Играть", callback_data="play")],
        [InlineKeyboardButton(text="ℹ️ Текущий пользователь", callback_data="current_user")],
        [InlineKeyboardButton(text="👥 Все пользователи", callback_data="all_users")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# === Игровое меню ===
def get_game_menu():
    kb = [
        [InlineKeyboardButton(text="⚔️ Арена", callback_data="arena")],
        [InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inventory")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="🛒 Магазин", callback_data="shop")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="exit")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


# === Старт ===
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("👋 Добро пожаловать в игру!\nВыберите действие:", reply_markup=get_register_menu())


# === Обработка кнопок регистрации ===
@dp.callback_query(F.data == "register")
async def register_user(callback: types.CallbackQuery):
    await callback.message.answer("Введите никнейм:")
    await dp.current_state(user=callback.from_user.id).set_state("register_nickname")


@dp.message(F.text, state="register_nickname")
async def get_nickname(message: types.Message, state):
    await state.update_data(nickname=message.text)
    await message.answer("Введите логин:")
    await state.set_state("register_login")


@dp.message(F.text, state="register_login")
async def get_login(message: types.Message, state):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль:")
    await state.set_state("register_password")


@dp.message(F.text, state="register_password")
async def get_password(message: types.Message, state):
    await state.update_data(password=message.text)
    await message.answer("Введите имя:")
    await state.set_state("register_name")


@dp.message(F.text, state="register_name")
async def get_name(message: types.Message, state):
    data = await state.get_data()
    user_data = UserRegistrationDTO(
        nickname=data['nickname'],
        login=data['login'],
        password=data['password'],
        first_name=message.text
    )
    result = game.register(user_data)
    await message.answer(result, reply_markup=get_register_menu())
    await state.clear()


# === Вход ===
@dp.callback_query(F.data == "login")
async def login_user(callback: types.CallbackQuery):
    await callback.message.answer("Введите логин:")
    await dp.current_state(user=callback.from_user.id).set_state("login_login")


@dp.message(F.text, state="login_login")
async def get_login_input(message: types.Message, state):
    await state.update_data(login=message.text)
    await message.answer("Введите пароль:")
    await state.set_state("login_password")


@dp.message(F.text, state="login_password")
async def get_password_input(message: types.Message, state):
    data = await state.get_data()
    result = game.login(data['login'], message.text)
    await message.answer(result, reply_markup=get_register_menu())
    await state.clear()


# === Игровое меню ===
@dp.callback_query(F.data == "play")
async def play(callback: types.CallbackQuery):
    if game.verification():
        await callback.message.answer("🎮 Добро пожаловать в игру!", reply_markup=get_game_menu())
    else:
        await callback.message.answer("❌ Вы не вошли в аккаунт")


# === Обработка игровых кнопок ===
@dp.callback_query(F.data == "arena")
async def arena_cb(callback: types.CallbackQuery):
    arena()
    await callback.message.answer("⚔️ Битва началась!")


@dp.callback_query(F.data == "inventory")
async def inventory_cb(callback: types.CallbackQuery):
    inventory()
    await callback.message.answer("🎒 Ваш инвентарь открыт!")


@dp.callback_query(F.data == "settings")
async def settings_cb(callback: types.CallbackQuery):
    settings()
    await callback.message.answer("⚙️ Настройки открыты!")


@dp.callback_query(F.data == "shop")
async def shop_cb(callback: types.CallbackQuery):
    shop()
    await callback.message.answer("🛒 Добро пожаловать в магазин!")


@dp.callback_query(F.data == "exit")
async def exit_cb(callback: types.CallbackQuery):
    await callback.message.answer("🚪 Вы вышли в главное меню.", reply_markup=get_register_menu())


# === Пользователи ===
@dp.callback_query(F.data == "current_user")
async def current_user(callback: types.CallbackQuery):
    user = game.get_current_user()
    await callback.message.answer(f"👤 Текущий пользователь:\n{user}")


@dp.callback_query(F.data == "all_users")
async def all_users(callback: types.CallbackQuery):
    users = game.get_all_users()
    text = "\n\n".join([str(u) for group in users for u in group])
    await callback.message.answer(f"👥 Все пользователи:\n{text}")


# === Удаление ===
@dp.callback_query(F.data == "delete_user")
async def delete_user(callback: types.CallbackQuery):
    result = game.delete_user()
    await callback.message.answer(result, reply_markup=get_register_menu())


# === Запуск ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
