from telegram.ext import Updater, CommandHandler
import requests
from telebot.credentials import Token

def cryptoPriceCheck(context):
    chat_id = context.job.context[0]
    contents = requests.get('https://api.wazirx.com/api/v2/tickers').json()

    text = contents['btcinr']['last']
    context.bot.send_message(chat_id=chat_id,text=text)

def start(update,context):
    context.job_queue.run_repeating(cryptoPriceCheck,interval=2,first=1,context=[update.message.chat_id])
    context.bot.send_message(chat_id=update.effective_chat.id,text='Hello there!')

def main():
    updater = Updater(Token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()