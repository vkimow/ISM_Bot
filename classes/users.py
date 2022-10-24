from config import Paths
from classes.number import Number

class Admin:
    def __init__(self, telegram):
        self.telegram = telegram

class User:
    def __init__(self, id, first_name = None, last_name = None, phone_number = None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number if Number.IsUnifiedStyleNumber(phone_number) else None

    def has_all_additional_info(self):
        return self.first_name and self.last_name and self.phone_number
