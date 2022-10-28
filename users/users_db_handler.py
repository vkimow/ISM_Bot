import os
import sqlite3
from config import Paths
from classes.users import User

class SqliteConnectionFactory:
    __connection = None

    @classmethod
    def connection(cls):
        if not cls.__connection:
            def create_folder(folder_path):
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
            create_folder(Paths.resource)
            create_folder(Paths.local)

            path = f'{Paths.data}/users.db'
            if not os.path.isfile(path):
                open(path, 'a').close()

            cls.__connection = sqlite3.connect(path, check_same_thread=False)
        return cls.__connection

class UsersDataBaseHandler:
    def __init__(self):
        self.__db = SqliteConnectionFactory.connection()
        self.__sql = self.__db.cursor()
        self.__init_users_db()

    def __init_users_db(self):
        self.__sql.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id         INTEGER NOT NULL,
                username        TEXT,
                first_name      TEXT,
                last_name       TEXT,
                phone_number    TEXT
            )
        ''')
        self.__db.commit()

    def try_add_user(self, user: User):
        if self.__contains_user(user.id):
            return False

        self.__add_user(user.id, user.username, user.first_name, user.last_name, user.phone_number)
        return True

    def try_delete_user(self, user_id):
        if not self.__contains_user(user_id):
            return False

        self.__delete_user(user_id)
        return True

    def add_or_update_user(self, user: User):
        if self.__contains_user(user.id):
            self.__update_user(user.id, user.username, user.first_name, user.last_name, user.phone_number)
        else:
            self.__add_user(user.id, user.username, user.first_name, user.last_name, user.phone_number)

    def __add_user(self, user_id, username, first_name, last_name, phone_number):
        self.__sql.execute(f'INSERT INTO users (user_id, username, first_name, last_name, phone_number) VALUES ({user_id}, "{username}", "{first_name}", "{last_name}", "{phone_number}")')
        self.__db.commit()

    def __delete_user(self, user_id):
        self.__sql.execute(f'DELETE FROM users WHERE user_id = {user_id}')
        self.__db.commit()

    def __update_user(self, user_id, username, first_name, last_name, phone_number):
        self.__sql.execute(f'UPDATE users SET username = "{username}",first_name = "{first_name}", last_name = "{last_name}", phone_number = "{phone_number}" WHERE user_id = {user_id}')
        self.__db.commit()

    def __contains_user(self, user_id):
        self.__sql.execute(f'SELECT user_id FROM users WHERE user_id = {user_id}')
        return self.__sql.fetchone() is not None


    def get_all_users(self):
        users = {}

        def get_none_if_string_none(string):
            return string if string != 'None' else None

        for [user_id, username, first_name, last_name, phone_number] in self.__sql.execute(f'SELECT * FROM users'):
            if user_id in users:
                continue

            username = get_none_if_string_none(username)
            first_name = get_none_if_string_none(first_name)
            last_name = get_none_if_string_none(last_name)
            phone_number = get_none_if_string_none(phone_number)

            user = User(user_id,
                username = username,
                first_name = first_name,
                last_name = last_name,
                phone_number = phone_number)
            users[user_id] = user

        return users
