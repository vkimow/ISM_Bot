import asyncio
from config import Paths


class UserData:
    def __init__(self, admins, users):
        self.admins = admins
        self.__users = users
        self.__users_lock = asyncio.Lock()
        self.external_users_lock = asyncio.Lock()

    async def try_set_user(self, user):
        async with self.__users_lock:
            if user.user_id not in self.__users:
                return False

            self.__users[user.user_id] = user
            return True

    async def try_add_user(self, user):
        async with self.__users_lock:
            if user.user_id in self.__users:
                return False

            self.__users[user.user_id] = user
            return True

    async def try_remove_user(self, user_id):
        async with self.__users_lock:
            if user_id not in self.__users:
                return False

            del self.__users[user_id]
            return True

    async def get_users(self):
        async with self.__users_lock:
            return self.__users


class Admin:
    def __init__(self, telegram):
        self.telegram = telegram

class User:
    def __init__(self, user_id, name = None, number = None):
        self.user_id = user_id
        self.name = name
        self.number = number
