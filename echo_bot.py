import csv
from telegram import Updater
import logging
import datetime

logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Привет! Чтобы узнать свое расписание на сегодняшний день, напиши номер своей группы.")

def help(bot, update):
    bot.sendMessage(update.message.chat_id, text="Чтобы узнать свое расписание на сегодняшний день, напиши номер своей группы.")

def pair_time(number):
    return {
        '1': '8:00-9:30',
        '2': '9:40-11:10',
        '3': '11:20-12:50',
        '4': '13:20-14:50',
        '5': '15:00-16:30',
        '6': '16:40-18:10',
        '7': '18:20-19:50'
    }[number]

def echo(bot, update):
    dt = datetime.datetime.now()
    today = dt.strftime('%Y%m%d')
    msg = update.message.text
    if(msg.isdigit()):
        with open(msg + '.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if(row['Дата'] == today):
                    bot.sendMessage(update.message.chat_id, text=pair_time(row['Номер пары']) + ' ' + row['Предмет'] + ' ' + row['Преподаватель'] + ' ' + row['Кабинет'])

def error(bot, update, error):
    logger.warn('Update %s" caused error "%s"' % (update, error))

def main():
    updater = Updater(token='TOKEN')
    dp = updater.dispatcher

    dp.addTelegramCommandHandler("start", start)
    dp.addTelegramCommandHandler("help", help)

    dp.addTelegramMessageHandler(echo)

    dp.addErrorHandler(error)

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()
