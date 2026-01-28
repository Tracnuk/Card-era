class Account:
    def __init__(self, nickname, login, password, person_id, cash=0, level=0, account_id=-1):
        self.id = account_id
        self.nickname = nickname
        self.person_id = person_id
        self.login = login
        self.password = password
        self.cash = cash
        self.level = level

    def __str__(self):
        return (
            f"👤 Аккаунт\n"
            f"ID аккаунта: {self.id}\n"
            f"ID персонажа: {self.person_id}\n"
            f"Никнейм: {self.nickname}\n"
            f"Логин: {self.login}\n"
            f"Деньги: {self.cash}\n"
            f"Уровень: {self.level}"
        )

    def __repr__(self):
        return self.__str__()
