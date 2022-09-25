import imp
import telebot
import config

from config import create_google_service

bot = telebot.TeleBot(config.BotTokens.Main)
service = create_google_service()


# def send_message(id, photo_path=None, photo=None, text=None, reply_markup=None, parse_mode='Markdown'):
#     if photo:
#         return bot.send_photo(chat_id=id, photo=photo, caption=text, reply_markup=reply_markup, parse_mode=parse_mode)
#     elif photo_path:
#         with open(photo_path, 'rb') as photo:
#             return bot.send_photo(chat_id=id, photo=photo, caption=text, reply_markup=reply_markup,
#                                   parse_mode=parse_mode)
#     else:
#         return bot.send_message(chat_id=id, text=text, reply_markup=reply_markup, parse_mode=parse_mode)


# def edit_message(message, text=None, reply_markup=None, parse_mode='Markdown'):
#     if message.photo:
#         return bot.edit_message_caption(chat_id=message.chat.id, message_id=message.message_id, caption=text,
#                                         reply_markup=reply_markup, parse_mode=parse_mode)
#     else:
#         return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=text,
#                                      reply_markup=reply_markup, parse_mode=parse_mode)


# def edit_photo(message, photo_path=None, photo=None, reply_markup=None, parse_mode='Markdown'):
#     if message.photo:
#         if photo:
#             media = types.InputMediaPhoto(photo)
#             return bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id,
#                                           reply_markup=reply_markup)
#         elif photo_path:
#             with open(photo_path, 'rb') as photo:
#                 media = types.InputMediaPhoto(photo)
#                 return bot.edit_message_media(media=media, chat_id=message.chat.id, message_id=message.message_id,
#                                               reply_markup=reply_markup)
#         else:
#             return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
#                                          text='ОШИБКА! Вы не передали фото для изменения!', reply_markup=None,
#                                          parse_mode=parse_mode)
#     else:
#         return bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
#                                      text='ОШИБКА! У этого сообщения нет фото, которое можно изменить!',
#                                      reply_markup=None, parse_mode=parse_mode)


# def show_timetable(message):
#     send_message(message.chat.id, photo_path=Resources.Timetable.today, reply_markup=Markup.Timetable.today)


# def show_services(message):
#     services_info = solovki.get_services_info()
#     send_message(message.chat.id, photo_path=Resources.Images.background_3, text=services_info)


# def show_squads(message):
#     send_message(message.chat.id, photo_path=Resources.Images.background_1, reply_markup=Markup.Squads.show)


# def show_commanders(message):
#     commanders_info = solovki.get_commanders_info()
#     send_message(message.chat.id, photo_path=Resources.Images.background_5, text=commanders_info, reply_markup=Markup.Commanders.show)


# def show_people(message):
#     info = Person.Info.Compact
#     send_message(message.chat.id, text=solovki.get_squad_people_info(Person.Sort.surname, info),
#                  reply_markup=Markup.People.show)


# def show_other(message):
#     send_message(message.chat.id, photo_path=Resources.Images.background_4,
#                  reply_markup=Markup.Other.show(message.from_user))


# def show_edit(message):
#     if is_right_user(message.from_user, admins.get_users_who_can_edit_something()):
#         send_message(message.chat.id, photo_path=Resources.Images.background_4,
#                      reply_markup=Markup.Edit.show(message.from_user))


# def show_admins(message):
#     if is_right_user(message.from_user, admins.get_users_who_can_manage_admins()):
#         send_message(message.chat.id, photo_path=Resources.Images.background_4, reply_markup=Markup.Admins.show)


# def show_help(message):
#     send_message(message.chat.id, text='help')


# def show_sbor(message):
#     sbor_info = solovki.get_solovki_info()
#     send_message(message.chat.id, photo_path=Resources.Images.background_2, text=sbor_info)


# @bot.message_handler(commands=['start'])
# def start_command(message):
#     Tools.log(message=message)
#     users.add_user(message.from_user.id)
#     users.save()
#     send_message(message.chat.id, text='Привет!', reply_markup=Markup.Main.show)


# @bot.message_handler(commands=['restart'])
# def restart_command(message):
#     Tools.log(message=message)
#     start_command(message)


# @bot.message_handler(commands=['edit'], is_admin=True)
# def edit_command(message):
#     Tools.log(message=message)
#     show_edit(message)


# @bot.message_handler(commands=['admins'], is_admin=True)
# def admins_command(message):
#     Tools.log(message=message)
#     show_admins(message)


# @bot.message_handler(commands=['help'])
# def help_command(message):
#     Tools.log(message=message)
#     show_help(message)


# @bot.message_handler(commands=['solovki'])
# def help_command(message):
#     Tools.log(message=message)
#     show_sbor(message)


# @bot.message_handler(commands=['timetable'])
# def help_command(message):
#     Tools.log(message=message)
#     show_timetable(message)


# @bot.message_handler(commands=['commanders'])
# def help_command(message):
#     Tools.log(message=message)
#     show_commanders(message)


# @bot.message_handler(commands=['squads'])
# def help_command(message):
#     Tools.log(message=message)
#     show_squads(message)


# @bot.message_handler(commands=['services'])
# def help_command(message):
#     Tools.log(message=message)
#     show_services(message)


# @bot.message_handler(commands=['people'])
# def help_command(message):
#     Tools.log(message=message)
#     show_people(message)


# @bot.message_handler(commands=['other'])
# def help_command(message):
#     Tools.log(message=message)
#     show_other(message)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'other')
# def other_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     if keyword == 'search':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=None)
#         message = send_message(call.message.chat.id,
#                                text='Введите имя и/или фамилию человека, которого хотите найти. *Лучше вводить только фамилию.*',
#                                reply_markup=Markup.Exit.people_search_exit)
#         bot.register_next_step_handler(message, find_people)
#     elif keyword == 'message':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=None)
#         message = send_message(call.message.chat.id,
#                                text='Отправьте сообщение, которое хотите передать всему сбору. Это может быть текст, фото, музыка, опрос или файл.',
#                                reply_markup=Markup.Exit.public_message_exit)
#         bot.register_next_step_handler(message, public_message)
#     elif keyword == 'edit':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=Markup.Edit.show(call.from_user))
#     elif keyword == 'admins':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=Markup.Admins.show)
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'edit', is_admin=True)
# def edit_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     if keyword == 'timetable':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=None)
#         message = send_message(call.message.chat.id, text='Отправьте фото расписания)',
#                                reply_markup=Markup.Exit.timetable_edit_exit)
#         bot.register_next_step_handler(message, edit_timetable, )
#     elif keyword == 'commanders':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=None)
#         message = send_message(call.message.chat.id,
#                                text='Отправьте ID ДКС и всех ДКО через пробел. ДКС обязательно первым!',
#                                reply_markup=Markup.Exit.commander_edit_exit)
#         bot.register_next_step_handler(message, edit_commanders)
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'admins')
# def timetable_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     if keyword == 'list':
#         edit_message(call.message, text='*Список админов*')
#         for admin in admins.get_admins_info():
#             send_message(id=call.message.chat.id, text=admin)
#     elif keyword == 'roles':
#         edit_message(call.message, text='*Список ролей*')
#         text = '\n\n'.join(admins.get_roles_info())
#         send_message(id=call.message.chat.id, text=text)
#     elif keyword == 'add':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=None)
#         message = send_message(call.message.chat.id, text='Отправьте Telegram и ID роли нового админа',
#                                reply_markup=Markup.Exit.admins_add_exit)
#         bot.register_next_step_handler(message, add_admin)
#     elif keyword == 'edit_role':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=None)
#         message = send_message(call.message.chat.id, text='Отправьте ID админа и ID его новой роли',
#                                reply_markup=Markup.Exit.admins_edit_role_exit)
#         bot.register_next_step_handler(message, edit_role_of_admins)
#     elif keyword == 'remove':
#         bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                       reply_markup=None)
#         message = send_message(call.message.chat.id, text='Отправьте ID админа, которого хотите удалить',
#                                reply_markup=Markup.Exit.admins_remove_exit)
#         bot.register_next_step_handler(message, remove_admin)
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'timetable')
# def timetable_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     if keyword == 'today':
#         edit_photo(call.message, photo_path=Resources.Timetable.today, reply_markup=Markup.Timetable.today)
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'commanders')
# def timetable_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     if keyword == 'refresh':
#         commanders_info = solovki.get_commanders_info()
#         edit_message(call.message, text=commanders_info, reply_markup=Markup.Commanders.show)
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'squads')
# def squads_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     if keyword == 'show_squad':
#         squad_id = int(call.data[-1:])
#         squad = solovki.get_squad(squad_id)
#         squad_info = solovki.get_squad_info_with_people(squad)
#         edit_message(call.message, text=squad_info, reply_markup=Markup.Squads.hide)
#     elif keyword == 'hide_buttons':
#         bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.Squads.hide)
#     elif keyword == 'show_buttons':
#         bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.Squads.show)
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'people')
# def people_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     if keyword == 'sort':
#         bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id,
#                                       reply_markup=Markup.People.sort(call.from_user))
#     elif keyword == 'hide_buttons':
#         bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.People.hide)
#     elif keyword == 'show_buttons':
#         bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.People.show)
#     elif keyword == 'back':
#         bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=Markup.People.show)
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'people_sort')
# def people_sort_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     info = Person.Info.Compact
#     if keyword == 'id':
#         edit_message(call.message, text=solovki.get_all_people_info(Person.Sort.id, info),
#                      reply_markup=Markup.People.sort(call.from_user))
#     elif keyword == 'name':
#         edit_message(call.message, text=solovki.get_squad_people_info(Person.Sort.name, info, name_first=True),
#                      reply_markup=Markup.People.sort(call.from_user))
#     elif keyword == 'surname':
#         edit_message(call.message, text=solovki.get_squad_people_info(Person.Sort.surname, info),
#                      reply_markup=Markup.People.sort(call.from_user))
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'message')
# def public_message_callback(call):
#     keyword = call.data.split()[1]
#     Tools.log(call=call)
#     info = Person.Info.Compact
#     if keyword == 'send':
#         forward_message_to_all(call.message.reply_to_message)
#         edit_message(call.message, text='Сообщение отправлено!',reply_markup=None)
#     elif keyword == 'cancel':
#         edit_message(call.message, text='Отправка сообщения отменена!',reply_markup=None)
#     bot.answer_callback_query(call.id)


# @bot.callback_query_handler(func=lambda call: call.data.split()[0] == 'cancel')
# def people_group_callback(call):
#     Tools.log(call=call)
#     bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
#     bot.answer_callback_query(call.id)


# def save_photo(message, path):
#     Tools.log(message=message)
#     if not message.photo:
#         return False

#     file = bot.get_file(message.photo[-1].file_id)
#     photo = bot.download_file(file.file_path)
#     with open(path, 'wb') as photo_file:
#         photo_file.write(photo)

#     return True


# def edit_timetable(message):
#     Tools.log(message=message)
#     if message.text and (message.text == 'Выход из режима изменения расписания' or message.text == 'Отмена'):
#         send_message(message.chat.id, text='Отмена изменений', reply_markup=Markup.Main.show)
#         return

#     result = save_photo(message, Resources.Timetable.today)
#     if not result:
#         send_message(message.chat.id, text='Вы не передали фото расписания. Повторите.',
#                      reply_markup=Markup.Exit.timetable_edit_exit)
#         bot.register_next_step_handler(message, edit_timetable)
#         return

#     send_message(message.chat.id, text='Новое расписание сохранено!', reply_markup=Markup.Main.show)


# def edit_commanders(message):
#     Tools.log(message=message)
#     if not message.text:
#         send_message(message.chat.id, text='Вы не передали ID новых коммандиров. Повторите.',
#                      reply_markup=Markup.Exit.commander_edit_exit)
#         bot.register_next_step_handler(message, edit_commanders)
#         return

#     if message.text == 'Выход из режима изменения ДКС и ДКО' or message.text == 'Отмена':
#         send_message(message.chat.id, text='Отмена изменений', reply_markup=Markup.Main.show)
#         return

#     id_strings = message.text.split()

#     ids = []
#     for id_string in id_strings:
#         if not id_string.isdigit():
#             send_message(message.chat.id,
#                          text='Вы должны передать ID командиров. Повторите.'.format(solovki.get_people_count()))
#             bot.register_next_step_handler(message, edit_commanders)
#             return
#         id = int(id_string)
#         ids.append(id)

#     result, error = solovki.edit_commanders(ids[0], ids[1:])
#     if result:
#         send_message(message.chat.id, text=solovki.get_commanders_info(), reply_markup=Markup.Main.show)
#         send_message(message.chat.id, text='Информация сохранена!')
#         solovki.save()
#     else:
#         send_message(message.chat.id, text=error + ' Повторите.')
#         bot.register_next_step_handler(message, edit_commanders)


# def edit_role_of_admins(message):
#     Tools.log(message=message)
#     if not message.text:
#         send_message(message.chat.id, text='Вы не передали ID админа и ID новой роли. Повторите.',
#                      reply_markup=Markup.Exit.admins_edit_role_exit)
#         bot.register_next_step_handler(message, edit_role_of_admins)
#         return

#     if message.text == 'Выход из режима изменения роли админа' or message.text == 'Отмена':
#         send_message(message.chat.id, text='Отмена изменения роли админа', reply_markup=Markup.Main.show)
#         return

#     id_strings = message.text.split()

#     if len(id_strings) != 2:
#         send_message(message.chat.id, text='Нужно передать 2 числа. ID админа и ID новой роли. Повторите.',
#                      reply_markup=Markup.Exit.admins_edit_role_exit)
#         bot.register_next_step_handler(message, edit_role_of_admins)
#         return

#     ids = []
#     for id_string in id_strings:
#         if not id_string.isdigit():
#             send_message(message.chat.id,
#                          text='Нужно передать ID числами, а не словами. Повторите.'.format(solovki.get_people_count()),
#                          reply_markup=Markup.Exit.admins_edit_role_exit)
#             bot.register_next_step_handler(message, edit_role_of_admins)
#             return
#         id = int(id_string)
#         ids.append(id)

#     result, error = admins.edit_role_admin(ids[0], ids[1])
#     if result:
#         send_message(message.chat.id, text=admins.get_admin_info(admins.get_admin(ids[0])),
#                      reply_markup=Markup.Main.show)
#         send_message(message.chat.id, text='Информация сохранена!')
#         admins.save()
#     else:
#         send_message(message.chat.id, text=error + ' Повторите.', reply_markup=Markup.Exit.admins_edit_role_exit)
#         bot.register_next_step_handler(message, edit_role_of_admins)


# def add_admin(message):
#     Tools.log(message=message)
#     if not message.text:
#         send_message(message.chat.id, text='Вы не передали Telegram админа и ID его роли. Повторите.',
#                      reply_markup=Markup.Exit.admins_add_exit)
#         bot.register_next_step_handler(message, add_admin)
#         return

#     if message.text == 'Выход из режима добавления админа' or message.text == 'Отмена':
#         send_message(message.chat.id, text='Отмена добавления админа', reply_markup=Markup.Main.show)
#         return

#     id_strings = message.text.split()

#     if len(id_strings) != 2:
#         send_message(message.chat.id, text='Нужно передать 2 значения. Telegram админа и ID его роли. Повторите.',
#                      reply_markup=Markup.Exit.admins_add_exit)
#         bot.register_next_step_handler(message, add_admin)
#         return

#     if not id_strings[1].isdigit():
#         send_message(message.chat.id,
#                      text='Нужно передать ID роли числом, а не словом. Повторите.'.format(solovki.get_people_count()),
#                      reply_markup=Markup.Exit.admins_add_exit)
#         bot.register_next_step_handler(message, add_admin)
#         return

#     result, error = admins.add_admin(id_strings[0], int(id_strings[1]))
#     if result:
#         send_message(message.chat.id, text=admins.get_admin_info(admins.get_admin(admins.get_admins_count())),
#                      reply_markup=Markup.Main.show)
#         send_message(message.chat.id, text='Информация сохранена!')
#         admins.save()
#     else:
#         send_message(message.chat.id, text=error + ' Повторите.', reply_markup=Markup.Exit.admins_add_exit)
#         bot.register_next_step_handler(message, add_admin)


# def remove_admin(message):
#     Tools.log(message=message)
#     if not message.text:
#         send_message(message.chat.id, text='Вы не передали ID админа. Повторите.',
#                      reply_markup=Markup.Exit.admins_remove_exit)
#         bot.register_next_step_handler(message, remove_admin)
#         return

#     if message.text == 'Выход из режима удаления админа' or message.text == 'Отмена':
#         send_message(message.chat.id, text='Отмена удаления админа', reply_markup=Markup.Main.show)
#         return

#     id_strings = message.text.split()

#     if len(id_strings) != 1:
#         send_message(message.chat.id, text='Нужно передать 1 значение. ID админа. Повторите.')
#         bot.register_next_step_handler(message, remove_admin)
#         return

#     if not id_strings[0].isdigit():
#         send_message(message.chat.id,
#                      text='Нужно передать ID админа числом, а не словом. Повторите.'.format(solovki.get_people_count()))
#         bot.register_next_step_handler(message, remove_admin)
#         return

#     admin_id = int(id_strings[0])
#     admin_telegram = admins.get_admin(admin_id).telegram
#     result, error = admins.remove_admin(admin_id)
#     if result:
#         send_message(message.chat.id, text='Админ `{}` удален!'.format(admin_telegram), reply_markup=Markup.Main.show)
#         admins.save()
#     else:
#         send_message(message.chat.id, text=error + ' Повторите.', reply_markup=Markup.Exit.admins_remove_exit)
#         bot.register_next_step_handler(message, remove_admin)


# def find_people(message):
#     Tools.log(message=message)
#     if not message.text:
#         send_message(message.chat.id,
#                      text='Вы не передали данные для поиска человека. Нужно передать имя и/или фамилию человека. Повторите.',
#                      reply_markup=Markup.Exit.people_search_exit)
#         bot.register_next_step_handler(message, find_people)
#         return

#     if message.text == 'Выход из режима поиска' or message.text == 'Отмена':
#         send_message(message.chat.id, text='Поиск закончен', reply_markup=Markup.Main.show)
#         return

#     keys = message.text.split()
#     if len(keys) > 2:
#         send_message(message.chat.id,
#                      text='Передано слишком много аргументов. Нужно передать только имя и/или фамилию человека. Повторите.', reply_markup=Markup.Exit.people_search_exit)
#         bot.register_next_step_handler(message, find_people)
#         return

#     for key in keys:
#         if key.isdigit():
#             if len(keys) == 1 and is_right_user(message.from_user, admins.get_users_who_can_see_ids()):
#                 break
#             send_message(message.chat.id,
#                         text='Вы передали числа. Нужно передать имя и/или фамилию человека. Повторите.', reply_markup=Markup.Exit.people_search_exit)
#             bot.register_next_step_handler(message, find_people)
#             return

#         if len(key) < 3:
#             send_message(message.chat.id,
#                         text='Нужно передать больше 2-ух символов для поиска человека. Повторите.', reply_markup=Markup.Exit.people_search_exit)
#             bot.register_next_step_handler(message, find_people)
#             return

#     people = solovki.find_people(keys)
#     if not people:
#         send_message(message.chat.id, text='Не найдено ни одного человека. Повторите.', reply_markup=Markup.Exit.people_search_exit)
#         bot.register_next_step_handler(message, find_people)
#         return

#     info = Person.Info.Debug if is_right_user(message.from_user,
#                                               admins.get_users_who_can_see_ids()) else Person.Info.Full
#     send_message(message.chat.id, text='Вот кого я нашел', reply_markup=Markup.Exit.people_search_exit)
#     for person in people:
#         send_message(message.chat.id, text=solovki.get_person_info(person, info))
#     bot.register_next_step_handler(message, find_people)


# def public_message(message):
#     Tools.log(message=message)
#     if message.text == 'Выход из режима публикации сообщения' or message.text == 'Отмена':
#         send_message(message.chat.id, text='Отмена публикации сообщения', reply_markup=Markup.Main.show)
#         return

#     send_message(message.chat.id, text='Сообщение получено!', reply_markup=Markup.Main.show)
#     bot.send_message(chat_id=message.chat.id, text = 'Вы уверены, что хотите *ОТПРАВИТЬ ВСЕМ* это сообщение? Отправку нельзя отменить.',
#                     reply_to_message_id=message.message_id, reply_markup=Markup.Message.show, parse_mode='Markdown')


# def forward_message_to_all(message):
#     for user in users.get_users():
#         if user == message.chat.id:
#             continue
#         try:
#             bot.forward_message(user, message.chat.id, message.message_id)
#         except Exception:
#             users.remove_user(user)


# bot.polling(none_stop=True)
