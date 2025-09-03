from person import Person

class User(Person):
    def __init__(self, login,
                 password,
                 first_name='',
                 last_name='',
                 email='',
                 phone='',
                 user_id=-1):
        
        super().__init__(first_name, last_name)
        self.email = email
        self.phone = phone
        self.login = login
        self.password = password
        self.id = user_id

    def __str__(self):
        return f'''Имя : {self.first_name}
Фамилия : {self.last_name}
Почта: {self.email}
Телефон: {self.phone}
Логин: {self.login}
Пароль: {self.password}'''
