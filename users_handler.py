class UsersHandler:
    def __init__(self, users, users_db_handler):
        self.__users = users
        self.__users_db_handler = users_db_handler

    def set_user(self, user):
        self.__users[user.id] = user
        self.__users_db_handler.add_or_update_user(user)
        return True

    def try_add_user(self, user):
        if user.id in self.__users:
            return False

        self.__users[user.id] = user
        self.__users_db_handler.try_add_user(user)
        return True

    def try_remove_user(self, user_id):
        if user_id not in self.__users:
            return False

        del self.__users[user_id]
        self.__users_db_handler.try_delete_user(user_id)
        return True

    def get_user(self, user_id):
        return self.__users[user_id] if user_id in self.__users else None

    def get_users(self):
        return self.__users
