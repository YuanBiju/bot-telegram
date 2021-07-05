from telegram.ext import Updater, CommandHandler
import requests
from telebot.credentials import Token

def cryptoPriceCheck(pairName):
    contents = requests.get('https://api.wazirx.com/api/v2/tickers').json()
    text = contents[pairName]['last']

    return text

def cryptoPriceAlert(context):
    crypto = context.job.context[0]
    sign = context.job.context[1]
    price = context.job.context[2]
    chat_id = context.job.context[3]

    send = False
    spot_price = cryptoPriceCheck(crypto)

    if sign == '<':
        if float(price) >= float(spot_price):
            send = True

    else:
        if float(price) <= float(spot_price):
            send = True

    if send:
        response = f"{crypto} has surpassed {price} and has reached {spot_price}"

        context.job.schedule_removal()

        context.bot.send_message(chat_id=chat_id,text=response)

def start(update,context):
    if len(context.args)>2:
        crypto = context.args[0]
        sign = context.args[1]
        price  = context.args[2]

        context.job_queue.run_repeating(cryptoPriceAlert,interval=2,first=1,context=[crypto, sign, price, update.message.chat_id])
        response = f"Current status of {crypto} is : "+cryptoPriceCheck(crypto)
    
    else:
        response = "Wrong command"
    context.bot.send_message(chat_id=update.effective_chat.id,text=response)

def main():
    updater = Updater(Token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start',start))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()