class UserRegistrationDTO():
    def __init__(self, nickname, login, password, first_name):
        self.first_name = first_name
        self.nickname = nickname
        self.login = login
        self.password = password

    def __str__(self):
        return f'''логин: {self.login}
пароль: {self.password}
никнэйм: {self.nickname}
имя: {self.first_name}'''
