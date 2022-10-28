from classes.users import User

class AdminsHandler:
    def __init__(self, admins):
        self.__admins = admins
        self.__phone_numbers_to_admins = dict()
        self.__usernames_to_admins = dict()

        for admin in admins:
            if admin.username:
                self.__usernames_to_admins[admin.username] = admin

            if admin.phone_number:
                self.__phone_numbers_to_admins[admin.phone_number] = admin

    def is_admin(self, user: User):
        return user.username in self.__usernames_to_admins or user.phone_number in self.__phone_numbers_to_admins

    def get_admin(self, user: User):
        if user.username in self.__usernames_to_admins:
            return self.__usernames_to_admins[user.username]

        if user.phone_number in self.__phone_numbers_to_admins:
            return self.__phone_numbers_to_admins[user.phone_number]

        return None
