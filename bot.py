import telebot
import sentiment
import re
import yt_public
# from yt_public import comment_threads as CommentParser
from pytube import extract
from datetime import datetime
import os

current_date = datetime.now()
formatted_date = current_date.strftime("%d-%m-%Y")

# токен от BotFather
# TOKEN = '' # Основной бот
TOKEN = '7552551692:AAGfImzCXCO96fWmMrBJLL8plWzlHzrNE-o' # Тест бот

bot = telebot.TeleBot(TOKEN)

def process_link(link):
    return f'Получена ссылка: {link}'

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    welcome_message = "Приветствую тебя, мой дорогой друг, пришли мне ссылку на видео из YouTube, а я выведу тебе краткую статистику😄"
    bot.send_message(message.chat.id, welcome_message)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    bot.reply_to(message, text = 'Обрабатываю ссылку...')
    # Ищем ссылку в тексте сообщения с помощью регулярного выражения
    links = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.text)
    
    # Если найдена хотя бы одна ссылка, обрабатываем её
    if links:
        for link in links:
            try:
                id=extract.video_id(link)
                response = yt_public.comment_threads(id,to_csv=True)
                result = sentiment.analysis(f'comments_{id}_{formatted_date}.csv')
                # bot.reply_to(message, text=result)
                if len(result) > 4095:
                    for x in range(0, len(result), 4095):
                        bot.reply_to(message, text=result[x:x+4095])
                else:
                    bot.reply_to(message, text=result)
                os.remove(f'comments_{id}_{formatted_date}.csv')
            except: bot.reply_to(message, text='Произошла ошибка... Пожалуйста, попробуйте ещё раз')

        # После отправки ответа, перезапускайте бота
    # os.execv(sys.executable,sys.executable)
        
    print('sent!')


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)