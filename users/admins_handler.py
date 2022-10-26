class AdminsHandler:
    def __init__(self, admins):
        self.__admins = admins

    def is_admin(self, user):
        return user.username in self.__admins.telegrams or user.phone_number in self.__admins.phone_numbers
