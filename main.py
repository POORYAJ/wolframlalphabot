from telegram.ext import Updater, InlineQueryHandler, MessageHandler, Filters
import telegram
import re
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

token = "YOUR TELEGRAM BOT TOKEN HERE"
wolframId = "YOUR WOLFRAMALPHA ID HERE"

# uncomment to enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)

def FindAnswer(bot, update):
    chat_id = update.message.chat_id
    user_question = quote(update.message.text, safe='')
    url = f'http://api.wolframalpha.com/v2/query?appid={wolframId}&input=solve+{user_question}&podstate=Step-by-step%20solution'
    answer = requests.get(url)
    soup = BeautifulSoup(answer.text, 'html.parser')
    images = soup.find_all('subpod')
    for image in images:
        image_url = image.find('img')['src']
        bot.send_photo(chat_id=chat_id, photo=image_url)

def main():
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, FindAnswer))
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()