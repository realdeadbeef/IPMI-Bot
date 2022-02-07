import logging
import ipmicommands as ipmi
import os

from configparser import ConfigParser
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler


# Change to desired config type (env or ini)
configType = 'env'

if configType == 'ini':
    def iniConfigExists():
        if os.path.isfile('config.ini'):
            pass
        else:
            from configparser import ConfigParser
            config_object = ConfigParser()

            config_object["IPMI"] = {
                "serverIP": "0.0.0.0",
                "username": "ipmiguy",
                "password": "password"
            }

            config_object["TELEGRAM"] = {
                "token": "token",
                "chatID": "chatid"
            }
            with open('config.ini', 'w') as conf:
                config_object.write(conf)

            print("Config file has been created, please make your changes and re-run this script")
            exit(0)


    iniConfigExists()

    config_object = ConfigParser()
    config_object.read("config.ini")

    ipmiconfigdata = config_object["IPMI"]

    serverIP = ipmiconfigdata["serverip"]
    userName = ipmiconfigdata["username"]
    password = ipmiconfigdata["password"]

    telegramconfigdata = config_object["TELEGRAM"]

    telegramToken = telegramconfigdata["token"]
    chatId = int(telegramconfigdata["chatID"])
elif configType == 'env':
    serverIP = os.environ.get('IPMI_IP')
    userName = os.environ.get('IPMI_USER')
    password = os.environ.get('IPMI_PASSWORD')

    telegramToken = os.environ.get('TOKEN')
    chatId = int(os.environ.get('CHAT_ID'))
else:
    print('Invalid config type!')
    exit(0)

updater = Updater(token=f'{telegramToken}', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def powerUsage(update: Update, context: CallbackContext):
    if update.effective_chat.id == chatId:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ipmi.powerUsage(serverIP, userName, password))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def powerOn(update: Update, context: CallbackContext):
    if update.effective_chat.id == chatId:
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data='poweron'),
                InlineKeyboardButton("No", callback_data='cancel'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Are you sure you want to start the server?', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def powerOff(update: Update, context: CallbackContext):
    if update.effective_chat.id == chatId:
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data='poweroff'),
                InlineKeyboardButton("No", callback_data='cancel'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Are you sure you want to shut down the server?', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def powerStatus(update: Update, context: CallbackContext):
    if update.effective_chat.id == chatId:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ipmi.powerStatus(serverIP, userName, password))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def powerCycle(update: Update, context: CallbackContext):
    if update.effective_chat.id == chatId:
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data='powercycle'),
                InlineKeyboardButton("No", callback_data='cancel'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Are you sure you want to power cycle the server?', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def sdrList(update: Update, context: CallbackContext):
    if update.effective_chat.id == chatId:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ipmi.sdrList(serverIP, userName, password))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def fanStatus(update: Update, context: CallbackContext):
    if update.effective_chat.id == chatId:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ipmi.fanStatus(serverIP, userName, password))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def cbQueryHandler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'cancel':
        query.edit_message_text(text='Cancelled')
    elif query.data == 'poweron':
        query.edit_message_text(text=ipmi.powerOn(serverIP, userName, password))
    elif query.data == 'poweroff':
        query.edit_message_text(text=ipmi.powerOff(serverIP, userName, password))
    elif query.data == 'powercycle':
        query.edit_message_text(text=ipmi.powerCycle(serverIP, userName, password))
    else:
        query.edit_message_text(text='wat')


def start(update: Update, context: CallbackContext):
    if update.effective_chat.id == chatId:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Here are a list of commands to get '
                                                                        'started:\n\n '
                                                                        '/powerusage\n'
                                                                        '/poweron\n'
                                                                        '/poweroff\n'
                                                                        '/powerstatus\n'
                                                                        '/powercycle\n'
                                                                        '/sdrlist\n'
                                                                        '/fanstatus\n')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


updater.dispatcher.add_handler(CommandHandler('powerusage', powerUsage))
updater.dispatcher.add_handler(CommandHandler('poweron', powerOn))
updater.dispatcher.add_handler(CommandHandler('poweroff', powerOff))
updater.dispatcher.add_handler(CommandHandler('powerstatus', powerStatus))
updater.dispatcher.add_handler(CommandHandler('powercycle', powerCycle))
updater.dispatcher.add_handler(CommandHandler('sdrlist', sdrList))
updater.dispatcher.add_handler(CommandHandler('fanstatus', fanStatus))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(cbQueryHandler))

updater.start_polling()
updater.idle()
