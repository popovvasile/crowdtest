# Matis Krisztian Telegram chatbot task
# @MKtaskbot


from telegram.ext import MessageHandler, Filters, CommandHandler, Updater, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import logging
import csv

import os
PORT = int(os.environ.get('PORT', 5000))

TOKEN = "1089104157:AAGangZbH9Y7OcyPfi2-lQ5MtsB-x3DnskQ"
# S3 AWS - bucket (GoogleDrive)
# 1) Linux (Ubuntu/Debian)
# 2) PyCharm/VisualStudio
# 3) Git
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

NAME, BIRTH_DATE, COUNTRY, LOCALITY, COURSE_TYPE = range(5)

data = []


def start(update, context):
    update.message.reply_text(
        'Hi! To sign up to our programming course, please provide the following information:\n'
        'You can cancel this conversation by typing /cancel.\n'
        'First and last name:'
    )
    data.clear()
    return NAME


def name(update, context):
    update.message.from_user
    data.append(update.message.text)
    logger.info("Name: %s", update.message.text)
    update.message.reply_text(
        'Date of birth:\n'
        '(Format: yyyy.mm.dd)'
    )

    return BIRTH_DATE


def birthdate(update, context):
    update.message.from_user
    data.append(update.message.text)
    logger.info("Birthdate: %s", update.message.text)
    update.message.reply_text(
        'Country:'
    )

    return COUNTRY


def country(update, context):
    update.message.from_user
    data.append(update.message.text)
    logger.info("Country: %s", update.message.text)

    update.message.reply_text(
        'Locality:'
    )

    return LOCALITY


def locality(update, context):
    update.message.from_user
    data.append(update.message.text)
    logger.info("Locality: %s", update.message.text)

    reply_keyboard = [
        ['Backend', 'Frontend'],
        ['Data Analysis', 'Hardware'],
        ['System Administration']
    ]

    update.message.reply_text(
        'Course type:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return COURSE_TYPE


def course(update, context):
    update.message.from_user
    data.append(update.message.text)
    logger.info("Course tyipe: %s", update.message.text)
    update.message.reply_text(
        'Thank you!',
        reply_markup=ReplyKeyboardRemove()
    )

    with open('participant_list.csv', mode='a') as part_list:
        part_writer = csv.writer(part_list, delimiter=',', quotechar='"',
                                 quoting=csv.QUOTE_MINIMAL)
        part_writer.writerow(data)

    return ConversationHandler.END


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'The conversation has been cancelled.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def unknown(update, context):
    update.message.reply_text(
        "Sorry, I didn't understand that command."
    )


def main():
    TOKEN = "1089104157:AAGangZbH9Y7OcyPfi2-lQ5MtsB-x3DnskQ"
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NAME: [MessageHandler(Filters.text & ~Filters.command, name)],
            BIRTH_DATE: [MessageHandler(Filters.regex(r'\d{4}.\d{2}.\d{2}') & ~Filters.command, birthdate)],
            COUNTRY: [MessageHandler(Filters.text & ~Filters.command, country)],
            LOCALITY: [MessageHandler(Filters.text & ~Filters.command, locality)],
            COURSE_TYPE: [MessageHandler(Filters.regex('^(Backend|Frontend|Data Analysis|Hardware|System Administration)$'), course)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)

    unk = MessageHandler(Filters.command, unknown)
    dp.add_handler(unk)
    updater.start_polling()
    #
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=TOKEN)
    # updater.bot.setWebhook('https://mk-task-bot.herokuapp.com/' + TOKEN)
    #
    # updater.idle()


if __name__ == '__main__':
    main()
