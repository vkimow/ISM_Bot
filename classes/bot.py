from classes.users import UserData
import telebot

from telebot import types
from config import Paths, Resources, SpreadsheetIds
from massage_parser import MassageParser
from massage_downloader import MassageDownloader

class BotData:
    def __init__(self, about, links, massage, courses, user_data):
        self.about = about
        self.links = links
        self.massage = massage
        self.courses = courses
        self.user_data = user_data

class Bot:
    def __init__(self, telegram_bot, google_services, data):
        self.telegram_bot = telegram_bot
        self.google_services = google_services
        self.data = data

    def setup(self):
        massage_parser = MassageParser(self.google_services)
        massage_downloader = MassageDownloader(self.google_services)

        about, links, info_files_to_download = massage_parser.parse_info(SpreadsheetIds.info)
        massage, massage_files_to_download = massage_parser.parse_massage(SpreadsheetIds.services)
        courses = massage_parser.parse_education(SpreadsheetIds.education)
        admins = massage_parser.parse_admins(SpreadsheetIds.admins)
        users = massage_parser.parse_users(SpreadsheetIds.users)

        user_data = UserData(admins, users)
        data = BotData(about, links, massage, courses, user_data)
        self.data = data

        files_to_download = info_files_to_download + massage_files_to_download
        massage_downloader.load(files_to_download)

    def send_message(self, id, photo_path=None, text=None, reply_markup=None, parse_mode='Markdown'):
        if photo_path:
            with open(photo_path, 'rb') as photo:
                return self.telegram_bot.send_photo(chat_id=id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode=parse_mode)
        else:
            return self.telegram_bot.send_message(chat_id=id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)

    def edit_text(self, message, text=None, reply_markup=None, parse_mode='Markdown'):
        if message.photo:
            return self.telegram_bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption=text, reply_markup=reply_markup, parse_mode=parse_mode)
        else:
            return self.telegram_bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)

    def edit_photo(self, message, photo_path=None):
        if message.photo:
            if photo_path:
                with open(photo_path, 'rb') as photo:
                    media = types.InputMediaPhoto(photo)
                    return self.telegram_bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id)
            else:
                return self.telegram_bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                            text='ОШИБКА! Вы не передали фото для изменения!', reply_markup=None)
        else:
            return self.telegram_bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                        text='ОШИБКА! У этого сообщения нет фото, которое можно изменить!', reply_markup=None)

    def edit_message(self, message, text = None, photo_path = None, reply_markup = None, parse_mode='Markdown'):
        result = None
        if photo_path:
            result = self.edit_photo(message, photo_path)

        if text or reply_markup:
            result = self.edit_text(message, text, reply_markup, parse_mode)

        return result

    def clear_text(self, message):
        if message.photo:
            return self.telegram_bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption='', reply_markup=None)
        else:
            return self.telegram_bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text='', reply_markup=None)

    def edit_reply_markup(self, message, reply_markup):
        return self.telegram_bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=reply_markup)

    def delete_message(self, message):
        return self.telegram_bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    def answer_callback_query(self, call_id):
        return self.telegram_bot.answer_callback_query(call_id)
