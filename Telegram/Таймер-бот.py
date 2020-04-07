from telegram.ext import Updater
from settings import TOKEN
from telegram.ext import CommandHandler
import time as tm
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


REQUEST_KWARGS = {
    'proxy_url': 'socks5://96.96.33.133:1080',
}
reply_keyboard = [['/time', '/date', '/set_timer']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def unset_timer(update, context):
    if 'job' not in context.chat_data:
        update.message.reply_text('Нет активного таймера.')
        return
    job = context.chat_data['job']
    job.schedule_removal()
    del context.chat_data['job']
    update.message.reply_text('Хорошо, вернулся сейчас!')


def task(context):
    job = context.job
    context.bot.send_message(job.context, text='Вернулся!')


def set_timer(update, context):
    """Добавляем задачу в очередь"""
    chat_id = update.message.chat_id
    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text(
                'Извините, не умеем возвращаться в прошлое.')
            return

        if 'job' in context.chat_data:
            old_job = context.chat_data['job']
            old_job.schedule_removal()
        new_job = context.job_queue.run_once(task, due, context=chat_id)
        context.chat_data['job'] = new_job
        update.message.reply_text(f'Вернусь через {due} секунд.')

    except (IndexError, ValueError):
        update.message.reply_text('Использование: /set_timer  <секунд>.')


def close_keyboard(update, context):
    update.message.reply_text(
        "Клавиатура закрыта.",
        reply_markup=ReplyKeyboardRemove()
    )


def start(update, context):
    update.message.reply_text(
        "Я бот. Какая информация вам нужна? Напишите /help.",
        reply_markup=markup
    )


def help(update, context):
    update.message.reply_text(
        'Команды:\n'
        '/date: вывод текущей даты\n'
        '/time: вывод текущего времени\n'
        '/set_timer <секунд>: таймер',
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
    dp.add_handler(CommandHandler("set_timer", set_timer,
                                  pass_args=True,
                                  pass_job_queue=True,
                                  pass_chat_data=True))
    dp.add_handler(CommandHandler("unset", unset_timer,
                                  pass_chat_data=True))
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
