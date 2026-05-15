import telebot

TOKEN = '8522823157:AAG9cIxf3WJ0RTti5iK0SFjrEqqf0ivd4ho'
ADMIN_ID = 6029010108

bot = telebot.TeleBot(TOKEN)
user_data = {}

TOURS = {
    '🌊 Териберка': 'Настоящее путешествие на край Северного Ледовитого океана. Заброшенный посёлок, дикий берег, огромные валуны и бескрайнее море. Один из самых популярных маршрутов региона.',
    '🏔 Сейдозеро': 'Три в одном: авто, лодка и пеший лесной маршрут. Священное озеро саамов, окружённое горами. Место где чувствуешь себя частью чего-то большого.',
    '🐋 Фотоохота на китов': 'Фотосафари на китов в водах Северного Ледовитого океана. Выходим в открытое море на лодке — киты совсем рядом. Незабываемые кадры гарантированы.',
    '🚙 Джип-тур Дальние Зеленцы': 'Заброшенные дома, ржавый берег и ветер с океана. Едем на внедорожнике туда куда обычная машина не доедет. Настоящее приключение.',
    '❄️ Северное сияние': 'Охота за полярным сиянием в тундре. Выезжаем в лучшие точки региона подальше от городских огней. Сезон: ноябрь — март.',
}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "🏔 Добро пожаловать в Сердце Севера 51!\n\n"
        "Авторские туры по Мурманской области.\n"
        "Выберите действие 👇",
        reply_markup=main_menu())

def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('🗺 Выбрать тур')
    markup.row('📋 Оставить заявку')
    markup.row('🌐 Открыть сайт')
    return markup

@bot.message_handler(func=lambda m: m.text == '🗺 Выбрать тур')
def show_tours(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    for tour in TOURS:
        markup.row(tour)
    markup.row('🤔 Не могу выбрать — помогите!')
    markup.row('🔙 Назад')
    bot.send_message(message.chat.id, "Выберите тур:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in TOURS)
def tour_selected(message):
    user_data[message.chat.id] = {'tour': message.text}
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('✅ Оставить заявку на этот тур')
    markup.row('🔙 Назад к турам')
    bot.send_message(message.chat.id,
        f"{message.text}\n\n{TOURS[message.text]}",
        reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == '🔙 Назад к турам')
def back_to_tours(message):
    show_tours(message)

@bot.message_handler(func=lambda m: m.text == '🤔 Не могу выбрать — помогите!')
def cant_choose(message):
    user_data[message.chat.id] = {'tour': 'Помогите выбрать'}
    bot.send_message(message.chat.id, "Как вас зовут?")
    bot.register_next_step_handler(message, ask_date)

@bot.message_handler(func=lambda m: m.text == '✅ Оставить заявку на этот тур')
def ask_name(message):
    bot.send_message(message.chat.id, "Как вас зовут?")
    bot.register_next_step_handler(message, ask_date)

@bot.message_handler(func=lambda m: m.text == '📋 Оставить заявку')
def ask_name_direct(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, "Как вас зовут?")
    bot.register_next_step_handler(message, ask_tour_direct)

def ask_tour_direct(message):
    user_data[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, "Какой тур вас интересует?")
    bot.register_next_step_handler(message, ask_date)

def ask_date(message):
    user_data[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, "Когда планируете приехать?")
    bot.register_next_step_handler(message, ask_days)

def ask_days(message):
    user_data[message.chat.id]['date'] = message.text
    bot.send_message(message.chat.id, "На сколько дней планируете?")
    bot.register_next_step_handler(message, ask_people)

def ask_people(message):
    user_data[message.chat.id]['days'] = message.text
    bot.send_message(message.chat.id, "Сколько человек будет? Будут ли дети (если да, то какой возраст)?")
    bot.register_next_step_handler(message, ask_contact)

def ask_contact(message):
    user_data[message.chat.id]['people'] = message.text
    bot.send_message(message.chat.id, "Оставьте контакт для связи (телефон или Telegram):")
    bot.register_next_step_handler(message, finish)

def finish(message):
    data = user_data[message.chat.id]
    tour = data.get('tour', 'не указан')
    bot.send_message(message.chat.id,
        "✅ Заявка принята! Сергей свяжется с вами в ближайшее время 🙂",
        reply_markup=main_menu())
    bot.send_message(ADMIN_ID,
        f"🔔 Новая заявка!\n"
        f"Имя: {data.get('name', '—')}\n"
        f"Тур: {tour}\n"
        f"Дата: {data.get('date', '—')}\n"
        f"Дней: {data.get('days', '—')}\n"
        f"Люди: {data.get('people', '—')}\n"
        f"Контакт: {message.text}")

@bot.message_handler(func=lambda m: m.text == '🌐 Открыть сайт')
def open_site(message):
    bot.send_message(message.chat.id,
        "🌐 Наш сайт: https://heartofthenorth51.ru/")

@bot.message_handler(func=lambda m: m.text == '🔙 Назад')
def go_back(message):
    start(message)

bot.polling()