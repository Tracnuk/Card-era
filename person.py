class Person:
    def __init__(self, name,
                surname = '',
                lastname = '', 
                email = '', 
                phone_number = '', 
                person_id = -1,
                account_id = -1):

    def __str__(self):
        return f'''Имя : {self.name}
        Фамилия : {self.surname}
        Отчество : {self.lastname}
        Почта : {self.email}
        Телефон : {self.phone_number}'''