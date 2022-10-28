from config import Paths
from classes.number import Number

class Admin:
    def __init__(self, username, phone_number):
        self.username = username
        self.phone_number = phone_number

class User:
    def __init__(self, id, username = None, first_name = None, last_name = None, phone_number = None):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number if Number.IsUnifiedStyleNumber(phone_number) else None

    @staticmethod
    def create_from_telegram_user(telegram_user):
        return User(telegram_user.id,
                    username = telegram_user.username,
                    first_name = telegram_user.first_name,
                    last_name = telegram_user.last_name)

    @staticmethod
    def create_from_telegram_user_and_contact(telegram_user, contact):
        return User(telegram_user.id,
                    username = telegram_user.username,
                    first_name = contact.first_name,
                    last_name = contact.last_name,
                    phone_number = contact.phone_number)

    def has_all_additional_info(self):
        return self.first_name and self.last_name and self.phone_number
