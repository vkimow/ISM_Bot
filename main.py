import telebot
import config
import os

from telebot import types
from config import Paths, Resources, SpreadsheetIds
from markup import Markup
from google_service_creator import create_google_drive_service, create_google_sheet_service
from google_service_container import GoogleServices
from massage_parser import parse
from massage_downloader import load

bot = telebot.TeleBot(config.BotTokens.main)
google_services = GoogleServices(create_google_drive_service(), create_google_sheet_service())
massage = None

def setup():
    global massage
    massage, files_to_download = parse(google_services, SpreadsheetIds.main)
    load(google_services, files_to_download)

setup()

def send_message(id, photo_path=None, text=None, reply_markup=None, parse_mode='Markdown'):
    if photo_path:
        with open(photo_path, 'rb') as photo:
            return bot.send_photo(chat_id=id, photo=photo, caption=text, reply_markup=reply_markup,
                                parse_mode=parse_mode)
    else:
        return bot.send_message(chat_id=id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)


def edit_message(message, text=None, reply_markup=None, parse_mode='Markdown'):
    if message.photo:
        return bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption=text,
                                        reply_markup=reply_markup, parse_mode=parse_mode)
    else:
        return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text,
                                     reply_markup=reply_markup, parse_mode=parse_mode)


def edit_photo(message, photo_path=None, reply_markup=None, parse_mode='Markdown'):
    if message.photo:
        if photo_path:
            with open(photo_path, 'rb') as photo:
                media = types.InputMediaPhoto(photo)
                return bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id,
                                              reply_markup=reply_markup)
        else:
            return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                         text='ОШИБКА! Вы не передали фото для изменения!', reply_markup=None,
                                         parse_mode=parse_mode)
    else:
        return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                     text='ОШИБКА! У этого сообщения нет фото, которое можно изменить!',
                                     reply_markup=None, parse_mode=parse_mode)

def delete_message(message):
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)



def show_actions(message):
    send_message(message.chat.id, text = 'Акции, доступные на сегодня')
    for root, dirs, files in os.walk(Paths.actions):
        for file in files:
            send_message(message.chat.id, photo_path=Resources.Photos.action(file))

def show_appointment(message):
    send_message(message.chat.id, text = 'Выберите одного из специалистов', photo_path=Resources.Photos.background('Appointment'), reply_markup=Markup.Appointment.main(massage.specialists))

def show_specialist(message, specialist):
    send_message(message.chat.id, text=specialist.get_full_description(), photo_path=specialist.get_photo_path(), reply_markup = Markup.Appointment.specialist(specialist))

def show_lectures(message):
    send_message(message.chat.id, photo_path=Resources.Photos.background('Lectures'), reply_markup=Markup.Lectures.main(massage.lectures))

def show_anatomy(message):
    send_message(message.chat.id, photo_path=Resources.Photos.background('Anatomy'), reply_markup=Markup.Anatomy.main(massage.anatomy))

def show_organ(message, organ):
    send_message(message.chat.id, text=organ.content, photo_path=Resources.Photos.organ(organ.name), reply_markup=Markup.Anatomy.organ(organ))

@bot.message_handler(commands=['start'])
def start_command(message):
    show_appointment(message)

@bot.message_handler(commands=['appointment'])
def appointment_command(message):
    show_appointment(message)

@bot.message_handler(commands=['actions'])
def actions_command(message):
    show_actions(message)

@bot.message_handler(commands=['lectures'])
def lectures_command(message):
    show_lectures(message)

@bot.message_handler(commands=['anatomy'])
def anatomy_command(message):
    show_anatomy(message)

@bot.message_handler(commands=['resetup'])
def resetup_command(message):
    setup()
    send_message(message.chat.id, text = 'Загрузка закончилась')

@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'appointment')
def appointment_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'cancel':
        edit_message(call.message, text='Запись отменена')
    if keyword == 'specialist':
        index = int(call.data.split()[2])
        specialist = massage.specialists[index]
        show_specialist(call.message, specialist)
        delete_message(call.message)

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'specialist')
def specialist_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'back':
        show_appointment(call.message)
        delete_message(call.message)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'anatomy')
def anatomy_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'organ':
        rogan_name = call.data.split()[2]
        organ = massage.anatomy[rogan_name]
        show_organ(call.message, organ)
        delete_message(call.message)

    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'organ')
def anatomy_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'back':
        show_anatomy(call.message)
        delete_message(call.message)

    bot.answer_callback_query(call.id)

bot.polling(none_stop=True)
