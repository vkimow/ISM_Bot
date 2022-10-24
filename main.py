from classes.number import Number
from classes.bot import Bot
import telebot
from classes.users import User
import config
import os

from telebot import types
from config import Paths, Resources
from markup import Markup
from google_service_creator import create_google_drive_service, create_google_sheet_service
from google_service_container import GoogleServices


bot = Bot(  telegram_bot = telebot.TeleBot(config.BotTokens.test),
            google_services = GoogleServices(create_google_drive_service(), create_google_sheet_service()),
            data = None)

bot.setup()

def show_actions(chat_id):
    bot.send_message(chat_id, text = 'Актуальные акции')
    for root, dirs, files in os.walk(Paths.actions):
        for file in files:
            bot.send_message(chat_id, photo_path=Resources.Photos.action(file))

def show_about(chat_id):
    bot.send_message(chat_id, text=bot.data.about.get_text(), photo_path=Resources.Photos.background('About'), reply_markup=Markup.About.main(bot.data.links))

def show_services(chat_id):
    bot.send_message(chat_id, photo_path=Resources.Photos.background('Services'), reply_markup=Markup.Services.main())

def show_education(chat_id, user_id):
    phone_number = get_user_number(user_id)
    courses = list(filter(lambda course: phone_number in course.numbers, bot.data.courses))
    text = 'Вы еще не проходили обучение. Запишитесь и вам откроется доступ к материалам!' if len(courses) == 0 else ''
    bot.send_message(chat_id, photo_path=Resources.Photos.background('Education'), text= text, reply_markup=Markup.Education.main(courses, bot.data.links))

def request_phone_number(chat_id):
    message = bot.send_message(chat_id, text='Для доступа к обущающим матераиалам поделитесь своим номером', reply_markup=Markup.GetContact.main())
    bot.register_next_step_handler(message, get_contact)

def show_help(chat_id):
    return

def add_user(user_id):
    user = User(user_id)
    bot.data.users_handler.try_add_user(user)

def user_has_number(user_id):
    user = bot.data.users_handler.get_user(user_id)
    if not user:
        add_user(user_id)
        return False

    if not user.phone_number:
        return False

    return True

def get_user_number(user_id):
    user = bot.data.users_handler.get_user(user_id)
    return user.phone_number

@bot.telegram_bot.message_handler(commands=['start'])
def start_command(message):
    add_user(message.from_user.id)

@bot.telegram_bot.message_handler(commands=['help'])
def help_command(message):
    show_help(message.chat.id)

@bot.telegram_bot.message_handler(commands=['resetup'])
def resetup_command(message):
    bot.setup()
    bot.send_message(message.chat.id, text = 'Загрузка закончилась')


@bot.telegram_bot.message_handler(commands=['about'])
def about_command(message):
    show_about(message.chat.id)

@bot.telegram_bot.message_handler(commands=['services'])
def appointment_command(message):
    show_services(message.chat.id)

@bot.telegram_bot.message_handler(commands=['education'])
def education_command(message):
    if(user_has_number(message.from_user.id)):
        show_education(message.chat.id, message.from_user.id)
    else:
        request_phone_number(message.chat.id)


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
        show_actions(call.message.chat.id)
    elif keyword == 'specialist':
        bot.edit_text(call.message, text = 'Выберите специалиста', reply_markup=Markup.Services.specialists_list(bot.data.massage.specialists))
    elif keyword == 'all_services':
        bot.edit_text(call.message, text = 'Выберите услугу', reply_markup=Markup.Services.services_list(bot.data.massage.services))

    bot.answer_callback_query(call.id)


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'education')
def education_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'main':
        phone_number = get_user_number(call.from_user.id)
        courses = list(filter(lambda course: phone_number in course.numbers, bot.data.courses))
        text = 'Вы еще не проходили обучение. Запишитесь и вам откроется доступ к материалам!' if len(courses) == 0 else ''
        bot.edit_text(call.message, text=text, reply_markup = Markup.Education.main(courses, bot.data.links))
    elif keyword == 'course':
        phone_number = get_user_number(call.from_user.id)
        index = int(call.data.split()[2])
        course = bot.data.courses[index]
        lessons = list(filter(lambda lesson: phone_number in lesson.numbers, course.lessons))
        bot.edit_text(call.message, text=course.get_text(), reply_markup = Markup.Education.course(course, lessons))

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


def get_contact(message):
    if message.text and message.text == "Отмена":
        bot.send_message(message.chat.id, text = 'Отмена перехода в раздел обучения',reply_markup=Markup.remove)
        return

    if not message.contact:
        request_phone_number(message.chat.id)
        return

    contact = message.contact
    user = User(id=message.from_user.id, first_name=contact.first_name, last_name=contact.last_name, phone_number=contact.phone_number)
    bot.data.users_handler.set_user(user)
    bot.send_message(message.chat.id, text = 'Информация получена! Теперь у вас есть доступ к разделу обучение',reply_markup=Markup.remove)


bot.telegram_bot.polling(none_stop=True)
