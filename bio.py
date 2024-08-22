import os
import telebot
from telebot import types
from flask import Flask, request

TOKEN = os.environ.get("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Flask app setup
app = Flask(__name__)

# Path for storing files
FILE_PATH = "/app/files"
OWNER_ID = int(os.environ.get("OWNER_ID"))

# Global variables
current_subject = None
current_section = None
current_lecture = None

editable_buttons_term1 = [
    "الكيمياء الحيوية الطبيعية",
    "الماده الاختياريه من داخل التخصص",
    "الوراثة الميكروبية",
    "فيسيولوجيا الميكروبات",
    "أسس الهندسة الوراثية",
    "الماده الاختياريه من خارج التخصص"
]

internal_options = {
    "الكيمياء الحيوية الطبيعية": {
        "نظري": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "عملي": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "تلخيصات": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "امتحانات وأسئلة": ["المحاضرة الأولى", "المحاضرة الثانية"]
    },
    "الماده الاختياريه من داخل التخصص": {
        "نظري": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "عملي": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "تلخيصات": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "امتحانات وأسئلة": ["المحاضرة الأولى", "المحاضرة الثانية"]
    },
    "الوراثة الميكروبية": {
        "نظري": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "عملي": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "تلخيصات": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "امتحانات وأسئلة": ["المحاضرة الأولى", "المحاضرة الثانية"]
    },
    "فيسيولوجيا الميكروبات": {
        "نظري": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "عملي": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "تلخيصات": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "امتحانات وأسئلة": ["المحاضرة الأولى", "المحاضرة الثانية"]
    },
    "أسس الهندسة الوراثية": {
        "نظري": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "عملي": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "تلخيصات": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "امتحانات وأسئلة": ["المحاضرة الأولى", "المحاضرة الثانية"]
    },
    "الماده الاختياريه من خارج التخصص": {
        "نظري": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "عملي": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "تلخيصات": ["المحاضرة الأولى", "المحاضرة الثانية"],
        "امتحانات وأسئلة": ["المحاضرة الأولى", "المحاضرة الثانية"]
    }
}

# Bot handlers
def generate_keyboard(options, include_back=True, include_home=True):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for option in options:
        button = types.KeyboardButton(text=option)
        keyboard.add(button)
    if include_back:
        keyboard.add(types.KeyboardButton(text="رجوع"))
    if include_home:
        keyboard.add(types.KeyboardButton(text="رجوع إلى الصفحة الرئيسية"))
    return keyboard

def generate_subject_keyboard(subject_name):
    section_options = internal_options.get(subject_name, {})
    return generate_keyboard(section_options.keys())

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = generate_keyboard(["الترم الأول", "الترم الثاني"], include_back=False, include_home=False)
    bot.reply_to(message, text=f"مرحباً يا {message.from_user.first_name}! اختر الترم:", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == "رجوع إلى الصفحة الرئيسية")
def handle_home(message):
    send_welcome(message)

@bot.message_handler(func=lambda message: message.text == "الترم الأول")
def handle_term1(message):
    keyboard_term1 = generate_keyboard(editable_buttons_term1)
    bot.reply_to(message, text="اختر المادة:", reply_markup=keyboard_term1)

@bot.message_handler(func=lambda message: message.text == "الترم الثاني")
def handle_term2(message):
    bot.send_message(message.chat.id, text="لا يوجد محتوى للترم الثاني")

@bot.message_handler(func=lambda message: message.text in editable_buttons_term1)
def handle_subject(message):
    global current_subject
    current_subject = message.text
    keyboard_subject = generate_subject_keyboard(current_subject)
    bot.reply_to(message, text="اختر ما تريد:", reply_markup=keyboard_subject)

@bot.message_handler(func=lambda message: current_subject and message.text in internal_options.get(current_subject, {}))
def handle_section(message):
    global current_section
    current_section = message.text
    if current_subject in internal_options and current_section in internal_options[current_subject]:
        lecture_options = internal_options[current_subject][current_section]
        keyboard_lecture = generate_keyboard(lecture_options)
        bot.reply_to(message, text="اختر المحاضرة:", reply_markup=keyboard_lecture)
    else:
        bot.reply_to(message, "حدث خطأ. الرجاء إعادة المحاولة.")

@bot.message_handler(func=lambda message: current_subject and current_section and message.text in internal_options[current_subject].get(current_section, []))
def handle_lecture(message):
    global current_lecture
    current_lecture = message.text
    if current_subject and current_section and current_lecture:
        files_path = os.path.join(FILE_PATH, current_subject, current_section, current_lecture)
        if os.path.exists(files_path):
            files = os.listdir(files_path)
            if files:
                for file_name in files:
                    file_path = os.path.join(files_path, file_name)
                    with open(file_path, 'rb') as f:
                        bot.send_document(message.chat.id, f)
            else:
                bot.reply_to(message, f"لا توجد ملفات في {current_lecture}.")
        else:
            bot.reply_to(message, f"لا توجد ملفات في {current_lecture}.")
    else:
        bot.reply_to(message, "حدث خطأ. يرجى التأكد من اختيار المادة والقسم والمحاضرة بشكل صحيح.")

@bot.message_handler(func=lambda message: message.text == "رجوع")
def handle_back(message):
    global current_section, current_lecture, current_subject

    if current_section:
        if current_subject in internal_options:
            keyboard_section = generate_keyboard(internal_options[current_subject].keys())
            bot.reply_to(message, text="اختر ما تريد:", reply_markup=keyboard_section)
            current_section = None
            current_lecture = None
        else:
            bot.reply_to(message, "حدث خطأ. الرجاء إعادة المحاولة.")
    elif current_subject:
        keyboard_subject = generate_subject_keyboard(current_subject)
        bot.reply_to(message, text="اختر ما تريد:", reply_markup=keyboard_subject)
        current_subject = None
    else:
        keyboard_term1 = generate_keyboard(editable_buttons_term1)
        bot.reply_to(message, text="اختر المادة:", reply_markup=keyboard_term1)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    if message.from_user.id == OWNER_ID:
        try:
            if current_subject and current_section and current_lecture:
                file_info = bot.get_file(message.document.file_id)
                if file_info:
                    downloaded_file = bot.download_file(file_info.file_path)

                    save_path = os.path.join(FILE_PATH, current_subject, current_section, current_lecture)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)

                    file_name = message.document.file_name
                    file_full_path = os.path.join(save_path, file_name)

                    with open(file_full_path, 'wb') as new_file:
                        new_file.write(downloaded_file)
                    bot.reply_to(message, "تم حفظ الملف بنجاح.")
                else:
                    bot.reply_to(message, "تعذر الحصول على معلومات الملف. يرجى المحاولة مرة أخرى.")
        except Exception as e:
            bot.reply_to(message, f"حدث خطأ أثناء حفظ الملف: {str(e)}")

# Webhook setup
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    try:
        json_str = request.get_data().decode('UTF-8')
        update = telebot.types.Update.de_json(json_str)
        if update:
            bot.process_new_updates([update])
        else:
            return "Invalid update", 400
    except Exception as e:
        return f"Error processing update: {str(e)}", 500
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=f"https://{os.environ.get('RAILWAY_STATIC_URL')}/" + TOKEN)
    return "Webhook set!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
