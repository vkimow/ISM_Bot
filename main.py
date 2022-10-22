from classes.bot import Bot
import telebot
import config
import os

from telebot import types
from config import Paths, Resources
from markup import Markup
from google_service_creator import create_google_drive_service, create_google_sheet_service
from google_service_container import GoogleServices


bot = Bot(  telegram_bot = telebot.TeleBot(config.BotTokens.main),
            google_services = GoogleServices(create_google_drive_service(), create_google_sheet_service()),
            data = None)

bot.setup()

def show_actions(message):
    bot.send_message(message.chat.id, text = 'Актуальные акции')
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
    bot.send_message(message.chat.id, text=bot.data.about.get_text(), photo_path=Resources.Photos.background('About'), reply_markup=Markup.About.main(bot.data.links))

def show_services(message):
    bot.send_message(message.chat.id, photo_path=Resources.Photos.background('Services'), reply_markup=Markup.Services.main())

def show_education(message):
    bot.send_message(message.chat.id, photo_path=Resources.Photos.background('Education'), reply_markup=Markup.Education.main(bot.data.courses, bot.data.links))
    return

def show_help(message):
    return


@bot.telegram_bot.message_handler(commands=['start'])
def start_command(message):
    return

@bot.telegram_bot.message_handler(commands=['help'])
def help_command(message):
    show_help(message)

@bot.telegram_bot.message_handler(commands=['resetup'])
def resetup_command(message):
    bot.setup()
    bot.send_message(message.chat.id, text = 'Загрузка закончилась')


@bot.telegram_bot.message_handler(commands=['about'])
def about_command(message):
    show_about(message)

@bot.telegram_bot.message_handler(commands=['services'])
def appointment_command(message):
    show_services(message)

@bot.telegram_bot.message_handler(commands=['education'])
def education_command(message):
    show_education(message)


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'about')
def about_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'main':
        bot.edit_reply_markup(call.message, reply_markup=Markup.About.main(bot.data.links))
    elif keyword == 'maps':
        bot.edit_reply_markup(call.message, reply_markup=Markup.About.maps(bot.data.links))

    bot.answer_callback_query(call.id)


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'services')
def services_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'main':
        bot.edit_text(call.message, text = '', reply_markup=Markup.Services.main())
    elif keyword == 'actions':
        bot.delete_message(call.message)
        show_actions(call.message)
    elif keyword == 'specialist':
        bot.edit_text(call.message, text = 'Выберите специалиста', reply_markup=Markup.Services.specialists_list(bot.data.massage.specialists))
    elif keyword == 'all_services':
        bot.edit_text(call.message, text = 'Выберите услугу', reply_markup=Markup.Services.services_list(bot.data.massage.services))

    bot.answer_callback_query(call.id)

@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'education')
def education_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'main':
        bot.edit_text(call.message, text='', reply_markup = Markup.Education.main(bot.data.courses, bot.data.links))
    elif keyword == 'course':
        index = int(call.data.split()[2])
        course = bot.data.courses[index]
        bot.edit_text(call.message, text=course.get_text(), reply_markup = Markup.Education.course(course))

    bot.answer_callback_query(call.id)


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'specialist')
def specialist_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'back':
        bot.edit_message(call.message, text='Выберите специалиста', photo_path=Resources.Photos.background('Services'), reply_markup=Markup.Services.specialists_list(bot.data.massage.specialists))
    elif keyword == 'concrete':
        index = int(call.data.split()[2])
        specialist = bot.data.massage.specialists[index]
        bot.edit_message(call.message, text=specialist.get_full_description(), photo_path = specialist.get_photo_path(), reply_markup = Markup.Specialist.concrete(specialist))
    bot.answer_callback_query(call.id)



bot.telegram_bot.polling(none_stop=True)
