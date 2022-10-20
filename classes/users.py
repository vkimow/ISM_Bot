from config import Paths

class UserData:
    def __init__(self, admins, users):
        self.admins = admins
        self.users = users

class Admin:
    def __init__(self, telegram):
        self.telegram = telegram

class User:
    def __init__(self, user_id, name, number):
        self.user_id = user_id
        self.name = name
        self.number = number
