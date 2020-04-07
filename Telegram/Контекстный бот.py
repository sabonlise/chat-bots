from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from settings import TOKEN
from telegram.ext import CommandHandler


REQUEST_KWARGS = {
    'proxy_url': 'socks5://96.96.33.133:1080',
}


def help(update, context):
    update.message.reply_text('Я -- простой бот-опросник.\n'
                              'Напишите /start для начала диалога')


def start(update, context):
    update.message.reply_text(
        "Привет. Пройдите небольшой опрос, пожалуйста!\n"
        "Вы можете прервать опрос, послав команду /stop.\n"
        "В каком городе вы живёте?")

    return 1


def first_response(update, context):
    locality = update.message.text
    if locality == '/skip':
        update.message.reply_text('Какая погода у вас за окном?')
    else:
        update.message.reply_text(
            "Какая погода в городе {locality}?".format(**locals()))
    return 2


def second_response(update, context):
    weather = update.message.text
    update.message.reply_text("Спасибо за участие в опросе! Всего доброго!")
    return ConversationHandler.END


def stop(update, context):
    update.message.reply_text("Спасибо за участие в опросе.")
    return ConversationHandler.END


def main():
    updater = Updater(TOKEN, use_context=True,
                      request_kwargs=REQUEST_KWARGS)

    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            1: [MessageHandler(Filters.text, first_response)],
            2: [MessageHandler(Filters.text, second_response)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
