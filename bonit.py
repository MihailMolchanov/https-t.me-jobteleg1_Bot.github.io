import telebot
from telebot import types

bot = telebot.TeleBot('7643465592:AAGiSBCQ3RQ5YDQfrKTbYv2Wm4DeSg7omts')

user_data = {}

ADMIN_CHAT_ID = '1717331690'

@bot.message_handler(commands=['start'])
def send_message(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Услуги', callback_data='uslugi'))

    bot.send_message(message.chat.id, 'Здравствуйте, я бот для заказа услуг грузоперевозок.', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    chat_id = message.chat.id

    if chat_id in user_data and user_data[chat_id].get('waiting_for_input'):
        service_type = user_data[chat_id]['waiting_for_input']

        admin_message = f"Новый заказ:\n"
        admin_message += f"Услуга: {service_type}\n"
        admin_message += f"Данные: {message.text}\n"
        admin_message += f"От пользователя: @{message.from_user.username} (ID: {message.from_user.id})"


        bot.send_message(ADMIN_CHAT_ID, admin_message)

        bot.send_message(chat_id, "Спасибо! Ваш заказ принят. Мы свяжемся с вами в ближайшее время.")

        user_data[chat_id]['waiting_for_input'] = None
    else:
        bot.send_message(chat_id, "Пожалуйста, выберите услугу из меню.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    if chat_id in user_data and 'last_message' in user_data[chat_id]:
        try:
            bot.delete_message(chat_id, user_data[chat_id]['last_message'])
        except:
            pass

    if call.data == 'uslugi':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Грузоперевозки щебня', callback_data='scheben'))
        markup.add(types.InlineKeyboardButton('Кольца канализационные', callback_data='colca'))
        markup.add(types.InlineKeyboardButton('Плитка тротуарная', callback_data='plitka'))
        markup.add(types.InlineKeyboardButton('Услуги манипулятора', callback_data='manip'))
        sent_msg = bot.send_message(chat_id, 'Наши услуги.', reply_markup=markup)
        user_data[chat_id] = {
            'last_message': sent_msg.message_id, 'prev_menu': None}

    elif call.data == 'plitka':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Назад', callback_data='nazad'))
        with open('0lckc74mdkcen1vo4cmt2nexiba586ui.jpg', 'rb') as photo:
            sent_msg = bot.send_photo(call.message.chat.id, photo, 'Плитка тротуарная \nКвадрат 26р. \nБардюр 1 метр 10р. \n\nНапишите сколько квадратов плитки и бардюров вам нужно, адрес и номер телефона для связи.', reply_markup=markup)
        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'uslugi', 'waiting_for_input': 'Плитка тротуарная' }

    elif call.data == 'scheben':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Щебень гранитный - 100р. тонна', callback_data='100p'))
        markup.add(types.InlineKeyboardButton('Фракция 5/20, 20/40', callback_data='frakcia'))
        markup.add(types.InlineKeyboardButton('Природный от 70р. тонна', callback_data='priroda'))
        markup.add(types.InlineKeyboardButton('Назад', callback_data='nazad'))
        with open('Vidy_shebnya_foto1.jpg', 'rb') as photo:
           sent_msg = bot.send_photo(call.message.chat.id, photo, 'Выберите вид щебня',  reply_markup=markup)

        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'uslugi'}

    elif call.data == '100p':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Назад', callback_data='nnn'))
        sent_msg = bot.send_message(chat_id, 'Щебень гранитный - 100р. тонна. \n\nНапишите сколько тонн вам нужно, адрес и номер телефона для связи.', reply_markup=markup)

        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'scheben', 'waiting_for_input': 'Щебень гранитный - 100р. тонна'}

    elif call.data == 'frakcia':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Назад', callback_data='nnn'))
        sent_msg = bot.send_message(chat_id, 'Фракция 5/20, 20/40 - 100р. тонна. \n\nНапишите сколько тонн вам нужно, адрес и номер телефона для связи.', reply_markup=markup)

        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'scheben', 'waiting_for_input': 'Фракция 5/20, 20/40'}

    elif call.data == 'priroda':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Назад', callback_data='nnn'))
        sent_msg = bot.send_message(chat_id, 'Щебень природный - 70р. тонна. \n\nНапишите сколько тонн вам нужно, адрес и номер телефона для связи.', reply_markup=markup)

        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'scheben', 'waiting_for_input': 'Щебень природный - 70р. тонна'}



    elif call.data == 'nnn':

        chat_id = str(call.message.chat.id)

        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Щебень гранитный - 100р. тонна', callback_data='100p'))
            markup.add(types.InlineKeyboardButton('Фракция 5/20, 20/40', callback_data='frakcia'))
            markup.add(types.InlineKeyboardButton('Природный от 70р. тонна', callback_data='priroda'))
            markup.add(types.InlineKeyboardButton('Назад', callback_data='nazad'))
            with open('Vidy_shebnya_foto1.jpg', 'rb') as photo_file:
             sent_msg = bot.send_photo(chat_id=chat_id, photo=photo_file, caption='Выберите вид щебня', reply_markup=markup)
             user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'scheben'}

    elif call.data == 'nazad':
        if chat_id in user_data:
            try:
                bot.delete_message(chat_id, call.message.message_id)
            except:
                pass

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Грузоперевозки щебня', callback_data='scheben'))
            markup.add(types.InlineKeyboardButton('Кольца канализационные', callback_data='colca'))
            markup.add(types.InlineKeyboardButton('Плитка тротуарная', callback_data='plitka'))
            markup.add(types.InlineKeyboardButton('Услуги манипулятора', callback_data='manip'))
            sent_msg = bot.send_message(chat_id, 'Наши услуги.', reply_markup=markup)

            user_data[chat_id] = {
                'last_message': sent_msg.message_id,
                'prev_menu': None
            }

    elif call.data == 'colca':
        chat_id = call.message.chat.id
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Кольца 1.5, крышка 135 - 140р.', callback_data='140'))
        markup.add(types.InlineKeyboardButton('Метровые 100р. Крышка 95р.', callback_data='metr'))
        markup.add(types.InlineKeyboardButton('Назад', callback_data='nazad'))
        with open('311_original.jpg', 'rb') as photo:
            sent_msg = bot.send_photo(call.message.chat.id, photo,  'Выберите кольца из ниже перечисленных.', reply_markup=markup)
        user_data[chat_id] = {'last_message': sent_msg.message_id,  'prev_menu': 'uslugi'}

    elif call.data == 'metr':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Назад', callback_data='vev'))
        sent_msg = bot.send_message(chat_id,
                                    'Метровые 100р. \nКрышка 95р. \n\nНапишите сколько колец вам нужно, адрес и номер телефона для связи.',
                                    reply_markup=markup)
        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'uslugi'}
        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'colca',
                              'waiting_for_input': 'Метровые 100р. Крышка 95р.'}

    elif call.data == '140':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Назад', callback_data='vev'))
        sent_msg = bot.send_message(chat_id,'Кольцо 1.5 - 140p. \nКрышка - 135р. \n\nНапишите сколько колец вам нужно, адрес и номер телефона для связи.', reply_markup=markup)
        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'uslugi'}
        user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': 'colca',
                              'waiting_for_input': 'Кольца 1.5, крышка 135 - 140р.'}

    elif call.data == 'vev':
        chat_id = str(call.message.chat.id)

        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Кольца 1.5, крышка 135 - 140р.', callback_data='140'))
            markup.add(types.InlineKeyboardButton('Метровые 100р. Крышка 95р.', callback_data='metr'))
            markup.add(types.InlineKeyboardButton('Назад', callback_data='nazad'))
            with open('311_original.jpg', 'rb') as photo_file:
               sent_msg = bot.send_photo(chat_id=chat_id, photo=photo_file, caption= 'Выберите кольца из ниже перечисленных.', reply_markup=markup)

            user_data[chat_id] = {'last_message': sent_msg.message_id, 'prev_menu': None}

    elif call.data == 'manip':
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Назад', callback_data='nazad'))
        with open('Copilot_20250710_020155.png','rb') as photo:
            sent_msg = bot.send_photo(call.message.chat.id, photo,
            'Услуги манипулятора:\n'
            'Перевозим: стройматериалы, кирпич, блоки и плиты, кольца жби, промышленное оборудование, станки, бытовки, контейнера, автоматические ворота, заборы, деревья и кабель, рекламные щиты.\n'
            'Услуги самосвала, доставка щебня, песка и дров.\n'
            'Стрела 8 метров, грузоподъемность 10 тонн.\n\n'
            'Напишите, что вам нужно перевезти, адрес и номер телефона для связи.',
            reply_markup=markup
        )
        user_data[chat_id] = {
            'last_message': sent_msg.message_id,
            'prev_menu': 'uslugi',
            'waiting_for_input': 'Услуги манипулятора'

        }

bot.polling(none_stop=True)