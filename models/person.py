class Person:
    def __init__(self, first_name, surname='',
                 last_name='', email='', phone_number='', account_id=-1, person_id=-1):
        self.person_id = person_id
        self.first_name = first_name
        self.surname = surname
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.account_id = account_id
        
    def __str__(self):
        return f'''person_id: {self.person_id}
account_id: {self.account_id}
Имя: {self.first_name}
Фамилия: {self.surname}
Отчество: {self.last_name}
Почта: {self.email}
Телефон: {self.phone_number}'''
