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
TOKEN = "8329664891:AAFuF4HaqWaAvzeFZJCNTped-eqWuwjO9pA" 
game = Game()

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ================== FSM (Состояния) ==================
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
        return "❌ Произошла ошибка: Данные не получены"
    
    # Если результат - кортеж (например, при удалении), объединяем все строки
    if isinstance(result, tuple):
        return "\n".join(map(str, result))
    
    return str(result)

# ================== КЛАВИАТУРЫ ==================

# Меню для тех, кто НЕ вошел
def get_auth_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='📝 Регистрация', callback_data="register")],
        [InlineKeyboardButton(text="🔐 Вход", callback_data="login")]
    ])

# Меню для тех, кто ВОШЕЛ (изначальный выбор: играть или профиль)
def get_start_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Играть", callback_data="play")],
        [InlineKeyboardButton(text="ℹ️ Мой профиль", callback_data="current_user")],
        [InlineKeyboardButton(text="❌ Удалить аккаунт", callback_data="delete_user")]
    ])

# Игровое меню (когда нажали "Играть")
def get_game_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⚔️ Арена", callback_data="arena")],
        [InlineKeyboardButton(text="🎒 Инвентарь", callback_data="inventory")],
        [InlineKeyboardButton(text="🛒 Магазин", callback_data="shop")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings")],
        [InlineKeyboardButton(text="🚪 Выйти", callback_data="exit")]
    ])

# ================== START ==================
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    if game.verification():
        await message.answer("👋 С возвращением! Выберите действие:", reply_markup=get_start_menu())
    else:
        await message.answer("👋 Добро пожаловать! Пожалуйста, войдите или зарегистрируйтесь:", reply_markup=get_auth_menu())

# ================== ВХОД (после успешного логина) ==================
@dp.message(LoginStates.password)
async def login_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if not data:
        await message.answer("❌ Ошибка авторизации. Попробуйте снова.")
        await state.clear()
        return
        
    result = game.login(data.get("login"), message.text)
    
    # Если вход успешен, показываем игровое меню, если нет - меню входа
    if game.verification():
        await message.answer(f"✅ Успешный вход!\n{process_game_result(result)}", reply_markup=get_start_menu())
    else:
        await message.answer(f"❌ {process_game_result(result)}", reply_markup=get_auth_menu())
    
    await state.clear()

# ================== РЕГИСТРАЦИЯ ==================
@dp.callback_query(F.data == "register")
async def register_user(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Шаг 1/4: Введите никнейм:")
    await state.set_state(RegisterStates.nickname)

@dp.message(RegisterStates.nickname)
async def get_nickname(message: types.Message, state: FSMContext):
    await state.update_data(nickname=message.text)
    await message.answer("Шаг 2/4: Введите логин для входа:")
    await state.set_state(RegisterStates.login)

@dp.message(RegisterStates.login)
async def get_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Шаг 3/4: Введите пароль:")
    await state.set_state(RegisterStates.password)

@dp.message(RegisterStates.password)
async def get_password(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.answer("Шаг 4/4: Введите имя вашего персонажа:")
    await state.set_state(RegisterStates.name)

@dp.message(RegisterStates.name)
async def get_name(message: types.Message, state: FSMContext):
    # 1. Получаем данные
    data = await state.get_data()
    
    # 2. ЖЕСТКАЯ ПРОВЕРКА: Если данных нет, не идем дальше
    if not data:
        await message.answer("❌ Ошибка: Сессия регистрации потеряна (возможно, бот был перезагружен). Начните заново с команды /start")
        await state.clear()
        return

    # 3. Безопасно достаем поля через .get()
    nick = data.get("nickname")
    log = data.get("login")
    pwd = data.get("password")
    fname = message.text

    # Если вдруг какое-то поле пустое
    if not all([nick, log, pwd]):
        await message.answer("❌ Ошибка: Некоторые данные регистрации отсутствуют. Начните заново.")
        await state.clear()
        return

    try:
        user_data = UserRegistrationDTO(
            nickname=nick,
            login=log,
            password=pwd,
            first_name=fname
        )

        # Вызываем регистрацию и получаем результат (который теперь кортеж)
        success, result_msg = game.register(user_data)
        
        await message.answer(str(result_msg), reply_markup=get_register_menu())

    except Exception as e:
        logger.exception("Критическая ошибка в хендлере регистрации")
        await message.answer(f"❌ Системная ошибка: {e}")
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
    if not data:
        await message.answer("❌ Ошибка авторизации. Попробуйте снова.")
        await state.clear()
        return
        
    result = game.login(data.get("login"), message.text)
    await message.answer(process_game_result(result), reply_markup=get_register_menu())
    await state.clear()

# ================== ИГРА ==================
@dp.callback_query(F.data == "play")
async def play(callback: types.CallbackQuery):
    if game.verification():
        await callback.message.answer("🎮 Добро пожаловать в игровой мир!", reply_markup=get_game_menu())
    else:
        await callback.answer("❌ Сначала войдите в аккаунт!", show_alert=True)

@dp.callback_query(F.data == "arena")
async def arena_cb(callback: types.CallbackQuery):
    arena()
    await callback.message.answer("⚔️ Вы на арене!")

# ================== ИНВЕНТАРЬ ==================
@dp.callback_query(F.data == "inventory")
async def inventory_cb(callback: types.CallbackQuery):
    try:
        # Сразу отвечаем на колбэк, чтобы убрать "часики"
        await callback.answer() 
        
        # 1. Проверка авторизации
        if not game.verification():
            await callback.message.answer("❌ Сначала войдите в аккаунт!")
            return # Выходим из функции, чтобы код ниже не выполнялся

        # 2. Получаем текст инвентаря
        # Убедись, что внутри game.get_inventory_info() используется логика с HTML и <pre>
        inventory_text = game.get_inventory_info()
        
        # 3. Проверка на пустой результат
        if not inventory_text:
            inventory_text = "📦 <b>Инвентарь пуст или произошла ошибка.</b>"

        # 4. Создаем клавиатуру
        inventory_kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⚔️ Арена", callback_data="arena")],
            [InlineKeyboardButton(text="🚪 Меню", callback_data="play")]
        ])

        # 5. Отправляем сообщение
        # ВАЖНО: parse_mode="HTML" для работы тегов <b> и <pre>
        await callback.message.answer(
            text=inventory_text,
            reply_markup=inventory_kb,
            parse_mode="HTML" 
        )
        
    except Exception as e:
        print(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
        # Используем f-строку правильно, чтобы не вызвать новую ошибку при выводе ошибки
        await callback.message.answer(f"⚠️ Произошла системная ошибка. Проверьте консоль.")

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
    await callback.message.answer("🚪 Вы вышли в главное меню", reply_markup=get_register_menu())

# ================== ПОЛЬЗОВАТЕЛИ ==================
@dp.callback_query(F.data == "current_user")
async def current_user(callback: types.CallbackQuery):
    user = game.get_current_user()
    await callback.message.answer(f"👤 Информация о вас:\n{user}")

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
    # Удаляем вебхуки и запускаем поллинг
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")