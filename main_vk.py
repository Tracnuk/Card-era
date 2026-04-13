import asyncio
from vkbottle import Keyboard, KeyboardButtonColor, Text, CtxStorage, BaseStateGroup
from vkbottle.bot import Bot, Message

# ================== НАСТРОЙКИ ==================
TOKEN = "vk1.a.3eT4UDP7iFtGbewGgn8O3wIs3iC9F8RLX1vU32tysHa670ks_bgfBBmCXu5vxbthh87gKVSVBNFlVP2Nm0LPLMm6c3KpF4-P7AVc7WR9WMrMCxgP2MnfbXZrM-CMTXRv6hOKMwIgYmb31cceeE0c8BkSkCCuHtJoKo4qPNNQU7YkiFwvWXY-6RbnAD1-LX_zLiEMs91lqqEh4WUENmtsVA"
bot = Bot(token=TOKEN)
ctx = CtxStorage() # Хранилище для данных регистрации

# Импорты твоей логики
from game.game import Game
from models.user_registration import UserRegistrationDTO
from services.shop_service import shop_service

game = Game()

# ================== СОСТОЯНИЯ (FSM) ==================
class RegisterStates(BaseStateGroup):
    NICKNAME = 0
    LOGIN = 1
    PASSWORD = 2
    NAME = 3

class LoginStates(BaseStateGroup):
    LOGIN = 0
    PASSWORD = 1

# ================== КЛАВИАТУРЫ ==================

def get_auth_menu():
    return (Keyboard(inline=True)
            .add(Text("📝 Регистрация", {"cmd": "register"}), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text("🔐 Вход", {"cmd": "login"}), color=KeyboardButtonColor.PRIMARY)
            .get_json())

def get_start_menu():
    return (Keyboard(one_time=False)
            .add(Text("🎮 Играть"), color=KeyboardButtonColor.PRIMARY)
            .add(Text("👤 Профиль"), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text("🚪 Выйти"), color=KeyboardButtonColor.NEGATIVE)
            .get_json())

def get_game_menu():
    return (Keyboard(inline=True)
            .add(Text("⚔️ Арена"), color=KeyboardButtonColor.SECONDARY)
            .add(Text("🎒 Инвентарь"), color=KeyboardButtonColor.SECONDARY)
            .row()
            .add(Text("🛒 Магазин"), color=KeyboardButtonColor.POSITIVE)
            .row()
            .add(Text("🔙 Назад"), color=KeyboardButtonColor.SECONDARY)
            .get_json())

# ================== ОБРАБОТЧИКИ ==================

def clean_html(text):
    return text.replace("<b>", "").replace("</b>", "").replace("<code>", "").replace("</code>", "")

@bot.on.message(text=["Начать", "Start", "🔙 Назад"])
async def start_handler(message: Message):
    if game.verification():
        await message.answer("👋 С возвращением!", keyboard=get_start_menu())
    else:
        await message.answer("👋 Добро пожаловать! Войдите или зарегистрируйтесь:", keyboard=get_auth_menu())

# --- РЕГИСТРАЦИЯ ---
@bot.on.message(payload={"cmd": "register"})
async def reg_start(message: Message):
    await bot.state_dispenser.set(message.peer_id, RegisterStates.NICKNAME)
    return "Шаг 1/4: Введите никнейм:"

@bot.on.message(state=RegisterStates.NICKNAME)
async def reg_nick(message: Message):
    ctx.set(f"reg_{message.peer_id}", {"nickname": message.text})
    await bot.state_dispenser.set(message.peer_id, RegisterStates.LOGIN)
    return "Шаг 2/4: Введите логин:"

@bot.on.message(state=RegisterStates.LOGIN)
async def reg_login(message: Message):
    data = ctx.get(f"reg_{message.peer_id}")
    data["login"] = message.text
    ctx.set(f"reg_{message.peer_id}", data)
    await bot.state_dispenser.set(message.peer_id, RegisterStates.PASSWORD)
    return "Шаг 3/4: Введите пароль:"

@bot.on.message(state=RegisterStates.PASSWORD)
async def reg_pass(message: Message):
    data = ctx.get(f"reg_{message.peer_id}")
    data["password"] = message.text
    ctx.set(f"reg_{message.peer_id}", data)
    await bot.state_dispenser.set(message.peer_id, RegisterStates.NAME)
    return "Шаг 4/4: Введите имя героя:"

@bot.on.message(state=RegisterStates.NAME)
async def reg_finish(message: Message):
    data = ctx.get(f"reg_{message.peer_id}")
    try:
        user_dto = UserRegistrationDTO(
            nickname=data['nickname'], login=data['login'],
            password=data['password'], first_name=message.text
        )
        success, msg = game.register(user_dto)
        await bot.state_dispenser.delete(message.peer_id)
        await message.answer(clean_html(str(msg)), keyboard=get_auth_menu())
    except Exception as e:
        await message.answer(f"❌ Ошибка регистрации: {e}")

# --- МАГАЗИН И ПРОФИЛЬ ---
@bot.on.message(text="🛒 Магазин")
async def shop_handler(message: Message):
    if not game.verification(): return "❌ Сначала войдите!"
    text = shop_service.get_shop_menu_text()
    await message.answer(clean_html(text), keyboard=get_game_menu())

@bot.on.message(text="👤 Профиль")
async def profile_handler(message: Message):
    await message.answer(clean_html(game.get_current_user()), keyboard=get_start_menu())

@bot.on.message(text="🎮 Играть")
async def play_handler(message: Message):
    await message.answer("🎯 Выберите раздел:", keyboard=get_game_menu())

@bot.on.message(text="🚪 Выйти")
async def logout_handler(message: Message):
    game.logout()
    await message.answer("👋 Вы вышли!", keyboard=get_auth_menu())

if __name__ == "__main__":
    print("🚀 VK Бот запущен...")
    bot.run_forever()