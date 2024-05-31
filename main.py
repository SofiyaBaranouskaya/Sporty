from telebot import TeleBot, types
import psycopg2
import re
import config
import os


TOKEN = config.TOKEN
bot = TeleBot(TOKEN)

def create_connection():
    conn = psycopg2.connect(
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        host=config.DB_HOST,
        port=config.DB_PORT
    )
    return conn

def update_or_insert_user(chat_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", (chat_id,))
    user_exists = cursor.fetchone()
    if user_exists:
        # Сброс всех полей пользователя в базе данных
        cursor.execute("""
            UPDATE users 
            SET name = NULL, gender = NULL, age = NULL, interests = NULL, evaluation = NULL, about = NULL, photo_file_id = NULL, nickname = NULL 
            WHERE chat_id = %s
        """, (chat_id,))
    else:
        # Вставка нового пользователя с NULL значениями для всех полей, кроме id и chat_id
        cursor.execute("""
            INSERT INTO users (chat_id, name, gender, age, interests, evaluation, about, photo_file_id, nickname) 
            VALUES (%s, 'Не указано', 'Не указано', 'Не указано', 'Не указано', 'Не указано', 'Не указано', 'D:\\pythonProject\\Sporty_bot\\Sporty_bot\\images\\notfound.png', 'Не указано')
        """, (chat_id,))
    conn.commit()
    conn.close()



@bot.message_handler(commands=['start'])
def handle_start(message):
    update_or_insert_user(message.chat.id)
    bot.send_message(message.chat.id, "Время составить анкету ;)\nВведите пол:", reply_markup=create_gender_keyboard())
    bot.register_next_step_handler(message, handle_gender)

def handle_gender(message):
    gender = message.text
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET gender = %s WHERE chat_id = %s", (gender, message.chat.id))
    conn.commit()
    conn.close()
    hide_keyboard = types.ReplyKeyboardRemove()  # Создаем клавиатуру для скрытия клавиатуры
    bot.send_message(message.chat.id, "Введите имя:", reply_markup=hide_keyboard)
    bot.register_next_step_handler(message, handle_name)


def create_gender_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text="М")
    itembtn2 = types.KeyboardButton(text="Ж")
    markup.add(itembtn1, itembtn2)
    return markup

@bot.message_handler(func=lambda message: message.text.lower() in ['ж', 'м'])
def handle_gender(message):
    gender = 'Ж' if message.text.lower() == 'ж' else 'М'
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET gender = %s WHERE chat_id = %s", (gender, message.chat.id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Введи своё имя:")
    bot.register_next_step_handler(message, handle_name)

def handle_name(message):
    name = message.text
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s WHERE chat_id = %s", (name, message.chat.id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Введите возраст:")
    bot.register_next_step_handler(message, handle_age)

def handle_age(message):
    try:
        age = int(message.text)
        if age < 12:
            bot.send_message(message.chat.id, "Тебе нужно подрасти.")
        else:
            conn = create_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET age = %s WHERE chat_id = %s", (age, message.chat.id))
            conn.commit()
            conn.close()

            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            itembtn1 = types.KeyboardButton(text="Футбол")
            itembtn2 = types.KeyboardButton(text="Баскетбол")
            itembtn3 = types.KeyboardButton(text="Теннис")
            itembtn4 = types.KeyboardButton(text="Волейбол")
            itembtn5 = types.KeyboardButton(text="Хоккей")
            itembtn6 = types.KeyboardButton(text="Бейсбол")
            itembtn7 = types.KeyboardButton(text="Гольф")
            itembtn8 = types.KeyboardButton(text="Бокс")
            itembtn9 = types.KeyboardButton(text="ММА (смешанные единоборства)")
            itembtn10 = types.KeyboardButton(text="Плавание")
            itembtn11 = types.KeyboardButton(text="Бег")
            itembtn12 = types.KeyboardButton(text="Беговые лыжи")
            itembtn13 = types.KeyboardButton(text="Горные лыжи")
            itembtn14 = types.KeyboardButton(text="Сноубординг")
            itembtn15 = types.KeyboardButton(text="Велоспорт")
            itembtn16 = types.KeyboardButton(text="Паркур")
            itembtn17 = types.KeyboardButton(text="Тренажерный зал")
            itembtn18 = types.KeyboardButton(text="Йога")
            itembtn19 = types.KeyboardButton(text="Пилатес")
            itembtn20 = types.KeyboardButton(text="Скалолазание")
            itembtn21 = types.KeyboardButton(text="Серфинг")
            itembtn22 = types.KeyboardButton(text="Скейтбординг")
            itembtn23 = types.KeyboardButton(text="Кайтсерфинг")
            itembtn24 = types.KeyboardButton(text="Стритбол")
            itembtn25 = types.KeyboardButton(text="Фрисби")
            itembtn26 = types.KeyboardButton(text="Кроссфит")
            itembtn27 = types.KeyboardButton(text="Бадминтон")
            itembtn28 = types.KeyboardButton(text="Регби")
            itembtn29 = types.KeyboardButton(text="Гандбол")
            itembtn30 = types.KeyboardButton(text="Автоспорт")
            itembtn31 = types.KeyboardButton(text="Водные виды спорта")
            itembtn32 = types.KeyboardButton(text="Экстремальные виды спорта")

            itembtn33 = types.KeyboardButton(text="Продолжить")

            markup.add(
                itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6, itembtn7, itembtn8, itembtn9, itembtn10,
                itembtn11, itembtn12, itembtn13, itembtn14, itembtn15, itembtn16, itembtn17, itembtn18, itembtn19,
                itembtn20, itembtn21, itembtn22, itembtn23, itembtn24, itembtn25, itembtn26, itembtn27, itembtn28,
                itembtn29, itembtn30, itembtn31, itembtn32, itembtn33
            )
            bot.send_message(message.chat.id, "Какие виды спорта тебе интересны? (если этого варианта нет, то просто отправь текстовым сообщением)", reply_markup=markup)
            bot.register_next_step_handler(message, handle_interests)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка: Введите корректный возраст.")
        bot.send_message(message.chat.id, "Введите возраст:")
        bot.register_next_step_handler(message, handle_age)


# Функция для обновления выбранных интересов в базе данных
def update_interests_in_database(interests, chat_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET interests = %s WHERE chat_id = %s", ([interests], chat_id))
    conn.commit()
    conn.close()


# Функция для отправки выбранных интересов пользователю
def send_interests(chat_id):
    interests = ', '.join(user_data['interests'])
    # Сохранение выбранных интересов в базе данных
    update_interests_in_database(interests, chat_id)


user_data = {}

def handle_interests(message):
    interests = message.text
    if interests.lower() == 'продолжить':
        send_interests(message.chat.id)
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        levels = ["Начинающий", "Средний", "Профи"]
        for level in levels:
            markup.add(types.KeyboardButton(text=level))
        bot.send_message(message.chat.id, "Выберите ваш уровень:", reply_markup=markup)
        evaluation = message.text
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET evaluation = %s WHERE chat_id = %s", (evaluation, message.chat.id))
        conn.commit()
        conn.close()
        bot.register_next_step_handler(message, handle_level)
    else:
        if 'interests' not in user_data:
            user_data['interests'] = []
        user_data['interests'].append(interests)
        markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        sports = [
            "Футбол", "Баскетбол", "Теннис", "Волейбол", "Хоккей", "Бейсбол", "Гольф", "Бокс",
            "ММА (смешанные единоборства)", "Плавание", "Бег", "Беговые лыжи", "Горные лыжи",
            "Сноубординг", "Велоспорт", "Паркур", "Тренажерный зал", "Йога", "Пилатес",
            "Скалолазание", "Серфинг", "Скейтбординг", "Кайтсерфинг", "Стритбол", "Фрисби",
            "Кроссфит", "Бадминтон", "Регби", "Гандбол", "Автоспорт", "Водные виды спорта",
            "Экстремальные виды спорта"
        ]

        buttons = []
        for sport in sports:
            button_text = sport
            if sport in user_data['interests']:
                button_text = "✅ " + sport
            buttons.append(button_text)

        for i in range(0, len(buttons), 2):
            markup.row(buttons[i], buttons[i+1] if i+1 < len(buttons) else None)

        markup.add(types.KeyboardButton(text="Продолжить"))
        bot.send_message(message.chat.id, "Ещё?", reply_markup=markup)
        bot.register_next_step_handler(message, handle_interests)

def handle_level(message):
    level = message.text
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET evaluation = %s WHERE chat_id = %s", (level, message.chat.id))
    conn.commit()
    conn.close()
    hide_keyboard = types.ReplyKeyboardRemove()  # Создаем клавиатуру для скрытия клавиатуры
    bot.send_message(message.chat.id, "В каком городе ты живешь?", reply_markup=hide_keyboard)
    bot.register_next_step_handler(message, handle_about)

def handle_about(message):
    about = message.text
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET about = %s WHERE chat_id = %s", (about, message.chat.id))
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, "Отправьте фото для аватарки:")
    bot.register_next_step_handler(message, handle_photo)


def handle_photo(message):
    if message.photo:
        # Удаление предыдущей фотографии, если она была сохранена
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT photo_file_id FROM users WHERE chat_id = %s", (message.chat.id,))
        result = cursor.fetchone()
        if result is not None:
            previous_photo_path = result[0]
            if previous_photo_path is not None:
                os.remove(previous_photo_path)

        photo = message.photo[-1]
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        save_directory = os.path.join(os.path.dirname(__file__), 'images')
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        unique_filename = str(message.chat.id) + '.jpg'
        save_path = os.path.join(save_directory, unique_filename)
        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Сохранение пути фотографии в базу данных
        cursor.execute("UPDATE users SET photo_file_id = %s WHERE chat_id = %s", (save_path, message.chat.id))
        conn.commit()
        conn.close()

        bot.send_message(message.chat.id, "Напиши ник тг для связи:")
        bot.register_next_step_handler(message, handle_nickname)

    else:
        bot.send_message(message.chat.id, "Вы не отправили фотографию. Пожалуйста, отправьте фотографию.")
        bot.register_next_step_handler(message, handle_photo)


def handle_nickname(message):
    nickname = message.text
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET nickname = %s WHERE chat_id = %s", (nickname, message.chat.id))
    conn.commit()
    conn.close()
    handle_final(message)

def handle_final(message):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", (message.chat.id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        data = {
            'Пол': result[3],
            'Имя': result[4],
            'Возраст': result[5],
            'Интересы': ', '.join(
                set([re.sub(r'[^a-zA-Zа-яА-Я, ]', '', interest.strip().lower()) for interest in result[6]])),
            'Уровень подготовки': result[7],
            'Город': result[8],
            'Ник в Telegram': "@" + result[9]
        }

        output = ""
        for key, value in data.items():
            if key == 'Интересы':
                output += f"{key}: {value}\n"
            else:
                output += f"{key}: {value}\n"

        bot.send_message(message.chat.id, "Анкета готова!")

        photo_filename = f"{message.chat.id}.jpg"
        photo_path = os.path.join(os.path.dirname(__file__), 'images', photo_filename)
        with open(photo_path, 'rb') as photo_file:
            bot.send_photo(message.chat.id, photo_file)
        bot.send_message(message.chat.id, output)

        bot.send_message(message.chat.id, "Теперь чтобы посмотреть анкеты других - напиши /find\nЧтобы посмотреть, с кем совпали интересы - напиши /match", reply_markup=create_comands_keyboard())

    else:
        bot.send_message(message.chat.id, "Ваши данные не найдены.")

def create_comands_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = types.KeyboardButton(text="/find - Поиск")
    itembtn2 = types.KeyboardButton(text="/match - Понравившиеся")
    markup.add(itembtn1, itembtn2)
    return markup




##########################################################################---find---########################################################################################

user_states = {}

def get_users_to_show(chat_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.id, users.gender, users.name, users.age, users.interests, users.evaluation, users.about
        FROM users
        LEFT JOIN user_views ON users.id = user_views.viewed_id AND user_views.viewer_id = %s
        WHERE users.chat_id!= %s
        AND (
            user_views.viewed_id IS NULL -- Пользователь ещё не был показан
            OR user_views.viewed_id IN (
                SELECT viewed_id FROM user_views WHERE viewer_id = %s AND liked = false -- Пользователь был показан, но не понравился
            )
        );
    """, (chat_id, chat_id, chat_id))
    users_to_show = cursor.fetchall()
    cursor.close()
    conn.close()
    return users_to_show


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=config.DB_NAME,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            host=config.DB_HOST,
            port=config.DB_PORT
        )
        return conn
    except Exception as e:
        raise Exception(f"Ошибка подключения к базе данных: {e}")

def get_user_id_by_name(name):
    conn = connect_to_db()
    cursor = conn.cursor()
    name = str(name)
    cursor.execute("SELECT id FROM users WHERE name = %s", (name,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_current_user_id(chat_id):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE chat_id = %s", (chat_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def update_liked_status(chat_id, viewed_id, liked_status):
    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        viewer_id = get_current_user_id(chat_id)
        if viewer_id is None:
            print("Пользователь не найден -_-.")
            return

        if viewed_id is None:
            print("Пользователь не найден.")
            return

        cursor.execute(
            """
            UPDATE user_views 
            SET liked = %s 
            WHERE viewer_id = %s AND viewed_id = %s
            """, (liked_status, viewer_id, viewed_id))
        conn.commit()
        # print("Статус обновлен успешно.")
    except Exception as e:
        print(f"Ошибка обновления статуса: {e}")
    finally:
        cursor.close()
        conn.close()

user_views = {}

@bot.message_handler(commands=['find'])
def handle_find_command(message):
    chat_id = message.chat.id

    viewer_id = get_current_user_id(chat_id)  # Получаем id текущего пользователя
    users_to_show = get_users_to_show(chat_id)
    user_states[chat_id] = users_to_show

    if users_to_show:
        # Отправляем первую анкету
        user_data = users_to_show[0]  # Берем первую анкету из списка
        viewed_id = get_user_id_by_name(user_data[2])
        if viewed_id is None:
            print("Не удалось получить ID пользователя по имени.")
            return  # Выходим из функции, если ID не найден
        send_user_profile(chat_id, user_data, viewed_id, viewer_id)
    else:
        bot.send_message(chat_id, "К сожалению, больше нет анкет для показа.")

def send_user_profile(chat_id, user_data, viewed_id, viewer_id):
    if viewed_id is None:
        print("viewed_id не определено. Не могу продолжить.")
        return

    conn = connect_to_db()
    cursor = conn.cursor()

    conn = connect_to_db()
    cursor = conn.cursor()

    # Проверяем, существует ли уже запись с таким viewer_id и viewed_id
    query = "SELECT 1 FROM user_views WHERE viewer_id = %s AND viewed_id = %s"
    values = (viewer_id, viewed_id)
    cursor.execute(query, values)
    exists = cursor.fetchone()

    if exists:
        bot.send_message(chat_id, "Все анкеты были показаны.", reply_markup=create_comands_keyboard())
        cursor.close()
        return

    # Если записи нет, добавляем viewed_id в таблицу user_views
    insert_query = "INSERT INTO user_views (viewer_id, viewed_id) VALUES (%s, %s)"
    insert_values = (viewer_id, viewed_id)
    cursor.execute(insert_query, insert_values)
    conn.commit()

    cursor.close()

    data = {
        'Пол': user_data[1],
        'Имя': user_data[2],
        'Возраст': user_data[3],
        'Интересы': ', '.join(
            set([re.sub(r'[^a-zA-Zа-яА-Я, ]', '', interest.strip().lower()) for interest in user_data[4]])),
        'Уровень подготовки': user_data[5],
        'Город': user_data[6],
    }

    output = ""
    for key, value in data.items():
        if key == 'Интересы':
            output += f"{key}: {value}\n"
        else:
            output += f"{key}: {value}\n"

    user_id = get_current_user_id(chat_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    yes_button = types.KeyboardButton('Да')
    no_button = types.KeyboardButton('Нет')
    markup.add(yes_button, no_button)

    # Сначала отправляем фотографию
    conn = connect_to_db()  # Открываем новое соединение
    cursor = conn.cursor()  # Создаем новый курсор
    query = "SELECT photo_file_id FROM users WHERE id = %s"
    cursor.execute(query, (viewed_id,))
    result = cursor.fetchone()
    if result:
        photo_file_id = result[0]  # Используем полученный chat_id для отправки фотографии
        with open(photo_file_id, 'rb') as photo:
            bot.send_photo(chat_id, photo)

    # Затем отправляем текстовое сообщение
    bot.send_message(chat_id, f"{output} \nЧто скажешь?", reply_markup=markup)

    bot.register_next_step_handler_by_chat_id(chat_id, handle_response, user_id, viewed_id)



def check_interests_match(viewer_id, viewed_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM user_views
        WHERE ((viewer_id = %s AND viewed_id = %s) OR (viewer_id = %s AND viewed_id = %s)) AND liked = true
    """, (viewed_id, viewer_id, viewer_id, viewed_id))

    rows = cursor.fetchall()
    if len(rows) >= 2:
        # Если количество совпадений больше или равно 2, значит интересы совпали
        return True
    else:
        return False

    cursor.close()
    conn.close()

    # Если счетчик больше или равен 2 и максимальное значение liked равно TRUE,
    # значит условия выполнены, и мы можем считать, что интересы совпали
    return count >= 2 and count > 0


def handle_response(message, viewer_id, viewed_id, *args):
    chat_id = message.chat.id

    if message.text.lower() == 'да':
        liked_status = True
        update_liked_status(chat_id, viewed_id, liked_status)
        # Проверяем, совпадают ли интересы
        interests_match = check_interests_match(viewer_id, viewed_id)
        if interests_match:
            bot.send_message(chat_id, "Ура, интересы совпали")
        else:
            bot.send_message(chat_id, "Классно!")
    elif message.text.lower() == 'нет':
        liked_status = False
        update_liked_status(chat_id, viewed_id, liked_status)
        bot.send_message(chat_id, "Понял, продолжим.")

    # Удаление первого элемента из очереди пользователей
    if user_states.get(chat_id):
        user_states[chat_id].pop(0)

    # Проверка, остались ли еще пользователи в очереди
    if user_states.get(chat_id):
        next_user_data = user_states[chat_id][0]
        next_viewed_id = get_user_id_by_name(next_user_data[2])  # Получаем id следующего пользователя по его имени
        send_user_profile(chat_id, next_user_data, next_viewed_id, viewer_id)  # Передаем viewer_id для следующего профиля
    else:
        bot.send_message(chat_id, "Все анкеты были показаны.")


##################################################################---match----################################################################################################

def get_nickname_by_id(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT nickname FROM users WHERE id = %s", (user_id,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return "Никнейм не найден."


def get_matching_user_profiles(viewer_id):
    conn = connect_to_db()
    cursor = conn.cursor()

    # Выполняем запрос к базе данных для получения анкет пользователей, чьи идентификаторы находятся в одной строке с viewer_id и liked=True
    query = "SELECT * FROM user_views WHERE (viewer_id = %s OR viewed_id = %s) AND liked = true"
    cursor.execute(query, (viewer_id, viewer_id))
    user_profiles = cursor.fetchall()

    cursor.close()
    conn.close()

    return user_profiles


@bot.message_handler(commands=['match'])
def match(message):
    chat_id = message.chat.id
    viewer_id = get_current_user_id(chat_id)

    # Получаем анкеты пользователей, чьи идентификаторы находятся в одной строке с viewer_id и liked=True
    user_profiles = get_matching_user_profiles(viewer_id)

    filtered_ids = [user_profile[0] for user_profile in user_profiles if user_profile[0] != viewer_id]

    if not filtered_ids:
        bot.send_message(chat_id, "Пока совпадений нет.")
        return

    for user_id in filtered_ids:
        nickname = get_nickname_by_id(user_id)
        data = {
            'Пол': '',
            'Имя': '',
            'Возраст': '',
            'Интересы': '',
            'Уровень подготовки': '',
            'Город': '',
        }

        # Выполняем выборку из таблицы users для каждого id
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT gender, name, age, interests, evaluation, about FROM users WHERE id = %s",
                       (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            data['Пол'] = result[0]
            data['Имя'] = result[1]
            data['Возраст'] = result[2]
            data['Интересы'] = ', '.join(
            set([re.sub(r'[^a-zA-Zа-яА-Я, ]', '', interest.strip().lower()) for interest in result[3]])),
            data['Уровень подготовки'] = result[4]
            data['Город'] = result[5]

        output = ""
        for key, value in data.items():
            if key == 'Интересы':
                output += f"{key}: {value}\n"
            else:
                output += f"{key}: {value}\n"

        bot.send_message(chat_id, f"У вас совпали интересы с @{nickname}, поздравляю)\n\n{output}")

bot.polling(none_stop=True)