from services.owner_service import OwnerService
from repositories.user_repository import user_storage

class Game:
    def __init__(self):
        self.sessions = {} # Сессии игроков {peer_id: user_data}
        self.owner_service = OwnerService()

    def register(self, user_dto):
        success, message = user_storage.create_user(user_dto)
        if success:
            user = user_storage.auth_user(user_dto.login, user_dto.password)
            if user:
                from repositories.card_ownership import card_ownership_storage
                for _ in range(5):
                    card_ownership_storage.add_card_and_account(5, user[0])
                return True, "✅ Регистрация успешна!"
        return success, message

    def login(self, peer_id, login, password):
        user = user_storage.auth_user(login, password)
        if user:
            self.sessions[peer_id] = user
            return True
        return False

    def verification(self, peer_id):
        return peer_id in self.sessions

    def get_current_user(self, peer_id):
        u = self.sessions.get(peer_id)
        if not u:
            return "❌ Вы не вошли в аккаунт!"
        return f"👤 Ник: {u[1]} | 💰 Золото: {u[5]}"

    def get_inventory_info(self, peer_id):
        user = self.sessions.get(peer_id)
        if not user:
            return "❌ Сначала войдите в аккаунт!"
        # Берем ID аккаунта (user[0]) и достаем инвентарь
        return self.owner_service.get_inventory_text(user[0])

    def logout(self, peer_id):
        if peer_id in self.sessions:
            del self.sessions[peer_id]
        return True