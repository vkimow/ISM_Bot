from classes.users import User

class UsersHandler:
    def __init__(self, users, users_db_handler):
        self.__users = users
        self.__users_db_handler = users_db_handler

    def set_user(self, user: User):
        self.__users[user.id] = user
        self.__users_db_handler.add_or_update_user(user)
        return True

    def try_add_user(self, user: User):
        if user.id in self.__users:
            return False

        self.__users[user.id] = user
        self.__users_db_handler.try_add_user(user)
        return True

    def try_remove_user(self, user):
        if user.id not in self.__users:
            return False

        del self.__users[user.id]
        self.__users_db_handler.try_delete_user(user.id)
        return True

    def get_user(self, user):
        return self.__users[user.id] if user.id in self.__users else None

    def get_user_or_add_if_none(self, user):
        if not isinstance(user, User):
            user = User.create_from_telegram_user(user)

        if user.id in self.__users:
            return self.__users[user.id]

        self.try_add_user(user)
        return user

    def get_users(self):
        return self.__users
