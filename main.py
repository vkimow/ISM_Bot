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


bot = Bot(  telegram_bot = telebot.TeleBot(config.BotTokens.main),
            google_services = GoogleServices(create_google_drive_service(), create_google_sheet_service()),
            data = None)

bot.setup_all()

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

def show_help(chat_id):
    return

def show_admin(chat_id):
    bot.send_message(chat_id, photo_path=Resources.Photos.background('Admin'), reply_markup=Markup.Admin.main())
    return

def show_request_phone_number(chat_id):
    message = bot.send_message(chat_id, text='Для доступа к обущающим матераиалам поделитесь своим номером', reply_markup=Markup.GetContact.main())
    bot.register_next_step_handler(message, get_contact)


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

@bot.telegram_bot.message_handler(commands=['start'], is_active=True)
def start_command(message):
    add_user(message.from_user.id)

@bot.telegram_bot.message_handler(commands=['help'], is_active=True)
def help_command(message):
    show_help(message.chat.id)

@bot.telegram_bot.message_handler(commands=['admin'], is_active=True)
def admin_command(message):
    show_admin(message.chat.id)

@bot.telegram_bot.message_handler(commands=['about'], is_active=True)
def about_command(message):
    show_about(message.chat.id)

@bot.telegram_bot.message_handler(commands=['services'], is_active=True)
def appointment_command(message):
    show_services(message.chat.id)

@bot.telegram_bot.message_handler(commands=['education'], is_active=True)
def education_command(message):
    if(user_has_number(message.from_user.id)):
        show_education(message.chat.id, message.from_user.id)
    else:
        show_request_phone_number(message.chat.id)


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'about', is_active=True)
def about_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'main':
        bot.edit_reply_markup(call.message, reply_markup=Markup.About.main(bot.data.links))
    elif keyword == 'maps':
        bot.edit_reply_markup(call.message, reply_markup=Markup.About.maps(bot.data.links))

    bot.answer_callback_query(call.id)


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'services', is_active=True)
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


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'education', is_active=True)
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


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'specialist', is_active=True)
def specialist_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'back':
        bot.edit_message(call.message, text='Выберите специалиста', photo_path=Resources.Photos.background('Services'), reply_markup=Markup.Services.specialists_list(bot.data.massage.specialists))
    elif keyword == 'concrete':
        index = int(call.data.split()[2])
        specialist = bot.data.massage.specialists[index]
        bot.edit_message(call.message, text=specialist.get_full_description(), photo_path = specialist.get_photo_path(), reply_markup = Markup.Specialist.concrete(specialist))
    bot.answer_callback_query(call.id)


@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'admin', is_active=True)
def admin_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'main':
        bot.edit_message(call.message, text = '', reply_markup=Markup.Admin.main())
    elif keyword == 'refresh':
        bot.edit_reply_markup(call.message, reply_markup=Markup.Admin.refresh())
    elif keyword == 'forward':
        bot.edit_reply_markup(call.message, reply_markup=None)
        message = bot.send_message(call.message.chat.id, text='Отправьте сообщение, которым хотите поделиться')
        bot.register_next_step_handler(message, request_to_forward_message)
    bot.answer_callback_query(call.id)

@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'refresh', is_active=True)
def refresh_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'all':
        bot.setup_all()
        bot.edit_message(call.message, text='Вся информация успешно обновлена!')
    elif keyword == 'admins':
        bot.setup_admins()
        bot.edit_message(call.message, text='Список админов успешно обновлен!')

    bot.answer_callback_query(call.id)

@bot.telegram_bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'forward', is_active=True)
def forward_callback(call):
    keyword = call.data.split()[1]
    if keyword == 'accept':
        bot.edit_reply_markup(call.message, reply_markup=None)
        forward_message_to_all(call.message.reply_to_message)
        bot.edit_message(call.message, text = 'Сообщение успешно отправлено!')
    elif keyword == 'cancel':
        bot.edit_message(call.message, text= 'Отправка сообщения отменена!',  reply_markup=None)
    bot.answer_callback_query(call.id)


@bot.telegram_bot.message_handler(content_types=["text"], is_active=True)
def message_handler(message):
    bot.send_message(message.chat.id, text = 'Этот бот не распознает текст. Используйте комманды, чтобы воспользоваться доступными функциями.', reply_markup=Markup.remove)


def get_contact(message):
    if message.text and message.text == "Отмена":
        bot.send_message(message.chat.id, text = 'Отмена перехода в раздел обучения',reply_markup=Markup.remove)
        return

    if not message.contact:
        show_request_phone_number(message.chat.id)
        return

    contact = message.contact
    user = User(id=message.from_user.id, first_name=contact.first_name, last_name=contact.last_name, phone_number=contact.phone_number)
    bot.data.users_handler.set_user(user)
    bot.send_message(message.chat.id, text = 'Информация получена! Теперь у вас есть доступ к разделу обучение',reply_markup=Markup.remove)

def request_to_forward_message(message):
    if message.text == 'Выход из режима публикации сообщения' or message.text == 'Отмена':
        bot.send_message(message.chat.id, text='Отмена публикации сообщения', reply_markup=Markup.remove)
        return

    bot.send_message(message.chat.id, text = 'Сообщение получено!', reply_markup=Markup.remove)
    bot.send_message(message.chat.id, text = 'Вы уверены, что хотите *ОТПРАВИТЬ ВСЕМ* это сообщение? Отправку нельзя отменить.', reply_to_message_id=message.message_id, reply_markup=Markup.Admin.forward())

def forward_message_to_all(message):
    for user_id in bot.data.users_handler.get_users():
        if user_id == message.chat.id:
            continue
        try:
            bot.forward_message(user_id, message.chat.id, message.message_id)
        except Exception:
            continue


bot.telegram_bot.polling(none_stop=True)
