from classes.bot import Bot
import telebot
import config
import os

from telebot import types
from config import Paths, Resources, SpreadsheetIds
from markup import Markup
from google_service_creator import create_google_drive_service, create_google_sheet_service
from google_service_container import GoogleServices
from massage_parser import MassageParser
from massage_downloader import MassageDownloader
from massage_downloader import load


bot = Bot(  telegram_bot = telebot.TeleBot(config.BotTokens.main),
            google_services = GoogleServices(create_google_drive_service(), create_google_sheet_service()),
            data = None)

bot.setup()

def show_actions(message):
    bot.send_message(message.chat.id, text = 'Акции, доступные на сегодня')
    for root, dirs, files in os.walk(Paths.actions):
        for file in files:
            bot.send_message(message.chat.id, photo_path=Resources.Photos.action(file))

def show_appointment(message):
    bot.send_message(message.chat.id, text = 'Выберите одного из специалистов', photo_path=Resources.Photos.background('Appointment'), reply_markup=Markup.Appointment.main(bot.data.massage.specialists))

def show_specialist(message, specialist):
    bot.send_message(message.chat.id, text=specialist.get_full_description(), photo_path=specialist.get_photo_path(), reply_markup = Markup.Appointment.specialist(specialist))

def show_organ(message, organ):
    bot.send_message(message.chat.id, text=organ.content, photo_path=Resources.Photos.organ(organ.name), reply_markup=Markup.Anatomy.organ(organ))

def show_about(message):
    return

def show_education(message):
    return

@bot.telegram_bot.message_handler(commands=['start'])
def start_command(message):
    return

@bot.telegram_bot.message_handler(commands=['about'])
def about_command(message):
    show_about(message)

@bot.telegram_bot.message_handler(commands=['appointment'])
def appointment_command(message):
    show_appointment(message)

@bot.telegram_bot.message_handler(commands=['education'])
def education_command(message):
    show_education(message)

@bot.telegram_bot.message_handler(commands=['resetup'])
def resetup_command(message):
    bot.setup()
    bot.send_message(message.chat.id, text = 'Загрузка закончилась')

@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'appointment')
def appointment_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'cancel':
        bot.edit_message(call.message, text='Запись отменена')
    if keyword == 'specialist':
        index = int(call.data.split()[2])
        specialist = bot.data.massage.specialists[index]
        show_specialist(call.message, specialist)
        bot.delete_message(call.message)

    bot.answer_callback_query(call.id)

@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'specialist')
def specialist_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'back':
        show_appointment(call.message)
        bot.delete_message(call.message)
    bot.answer_callback_query(call.id)

bot.telegram_bot.polling(none_stop=True)
