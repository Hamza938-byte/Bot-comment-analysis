import telebot
import sentiment
import re
from datetime import datetime
import os
from parser_wb import Parser_WB


"""   Реализация бота в Telegram.   """

current_date = datetime.now()
formatted_date = current_date.strftime("%d-%m-%Y")

# токен от BotFather
# Основной бот
TOKEN = '7552551692:AAGfImzCXCO96fWmMrBJLL8plWzlHzrNE-o'
bot = telebot.TeleBot(TOKEN)


def process_link(link):
    return f'Получен айдишник: {link}'


# Приветственное сообщение от бота.
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_name = message.from_user.first_name
    welcome_message = ("Приветствую тебя, мой дорогой друг, "
                       "пришли мне артикулы на товар через запятую, а я "
                       "выведу тебе краткую статистику😄")
    bot.send_message(message.chat.id, welcome_message)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_text(message):

    # Отправляет сообщение о процессе обработки запроса
    bot.reply_to(message, text='Обрабатываю...')

    # Ищем артикул в тексте сообщения с помощью регулярного выражения
    links = message.text.split(",")
    links = [link.strip() for link in links if link.strip()]
    #links = re.findall(r'^\d+', message.text)

    # Если найден хотя бы один артикул, обрабатываем его
    if links:
        for link in links:
            try:
                # Вызов функции Parser_WB(), которая возвращает отзывы к товару под артикулом link
                filename = Parser_WB(link)
                # Производим анализ применяя функцию analysis() из файла sentiment.py
                result = sentiment.analysis(f'./results/{filename}')

                if len(result) > 4095:
                    for x in range(0, len(result), 4095):
                        bot.reply_to(message, text=result[x:x+4095])
                else:
                    bot.reply_to(message, text=result)

                # Удаление датасета с результатами
                os.remove(f'./results/{filename}')

            except: bot.reply_to(message, text='Произошла ошибка... Пожалуйста, попробуйте ещё раз')

    # Сообщение об отправке результата пользователю.
    print('sent!')


# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)