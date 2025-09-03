class Account:
    def __init__(self, login,
                password,
                nickname,
                account_id = -1, 
                person_id = -1,
                cash = -1,
                level = -1, 
                mana = -1, 
                health = -1):

    def __str__(self):
        retutn f'''Логин : {self.login}
        Никнейм : {self.nickname}
        Деньги  : {self.cash}
        Уровень : {self.level}
        Мана    : {self.mana}
        
