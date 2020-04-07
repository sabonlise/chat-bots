from telegram.ext import Updater
from settings import TOKEN
from telegram.ext import CommandHandler
import time as tm
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


REQUEST_KWARGS = {
    'proxy_url': 'socks5://96.96.33.133:1080',
}
reply_keyboard = [['/time', '/date']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def close_keyboard(update, context):
    update.message.reply_text(
        "Ok",
        reply_markup=ReplyKeyboardRemove()
    )


def start(update, context):
    update.message.reply_text(
        "Я бот. Какая информация вам нужна?",
        reply_markup=markup
    )


def help(update, context):
    update.message.reply_text(
        'Команды /date и /time.',
        reply_markup=markup
    )


def time(update, context):
    current_time = tm.asctime().split()
    update.message.reply_text(f'Current time is {current_time[3]}')


def date(update, context):
    current_date = tm.asctime().split()
    dt = f'Today is {current_date[2]} {current_date[1]} of {current_date[-1]}, {current_date[0]}'
    update.message.reply_text(dt)


def main():
    updater = Updater(TOKEN, use_context=True,
                      request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("time", time))
    dp.add_handler(CommandHandler("date", date))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("close", close_keyboard))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
