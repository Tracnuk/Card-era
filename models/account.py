class Account():
    def __init__(self, nickname, login, password, cash=0, level=0, account_id=-1, person_id=-1):
        self.id = account_id
        self.nickname = nickname
        self.person_id = account_id
        self.login = login
        self.password = password
        self.cash = cash
        self.level = level

    def __str__(self):
        return f'''логин: {self.login}
пароль: {self.password}
количество денег: {self.cash}
уровень: {self.level}'''
