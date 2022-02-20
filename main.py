import logging
import os
from configparser import ConfigParser

import requests
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler

import ipmicommands as ipmi

# Change to desired config type (env or ini)
config_type = 'ini'

current_version = str('1.2')

latest_version = requests.get("https://api.github.com/repos/realdeadbeef/ipmi-bot/releases/latest")
latest_version = str(latest_version.json()["tag_name"])


def make_config(path):  # sourcery skip: extract-method, last-if-guard, remove-unnecessary-else,
    # swap-if-else-branches
    if not os.path.isdir('./config'):
        os.mkdir('./config')
    if not os.path.isfile(path):
        from configparser import ConfigParser
        config_obj = ConfigParser()

        config_obj["IPMI"] = {
            "serverIP": "0.0.0.0",
            "username": "ipmiguy",
            "password": "password"
        }

        config_obj["TELEGRAM"] = {
            "token": "token",
            "chatID": "chatid"
        }
        with open(path, 'w') as conf:
            config_obj.write(conf)

        print("Config file has been created, please make your changes and re-run this script")
        exit(0)
    else:
        return True


ini_path = '/usr/src/bot/config/config.ini'

make_config(ini_path)

config_object = ConfigParser()
config_object.read(ini_path)

ipmi_config_data = config_object["IPMI"]

server_ip = ipmi_config_data["serverip"]
username = ipmi_config_data["username"]
password = ipmi_config_data["password"]

telegram_config_data = config_object["TELEGRAM"]

token = telegram_config_data["token"]
chat_id = int(telegram_config_data["chatID"])

if latest_version != current_version:
    print(f'You are running version {current_version} of IPMI-bot which has been outdated by {latest_version}.\nPlease '
          f'update for the latest bug fixes and improvements!')
elif latest_version == current_version:
    print(f'You are running version {current_version} of IPMI-Bot which is the latest version!')
else:
    print('ERROR WHILE CHECKING FOR UPDATES')

updater = Updater(token=f'{token}', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def power_usage(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ipmi.powerUsage(server_ip, username, password))
        if latest_version != current_version:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'You are running version {current_version} of '
                                          f'IPMI-Bot which has been outdated by version '
                                          f'{latest_version}\nPlease go to '
                                          f'https://github.com/realdeadbeef/ipmi-bot '
                                          f'and follow the instructions for upgrading.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def power_on(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
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


def power_off(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data='poweroff'),
                InlineKeyboardButton("No", callback_data='cancel'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('This command sends a hard shutdown to the server. You might want to use the '
                                  '/softshutdown command instead. Do you wish to proceed?', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def soft_shutdown(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
        keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data='soft'),
                InlineKeyboardButton("No", callback_data='cancel'),
            ],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text('Are you sure you want to gracefully shutdown the server?', reply_markup=reply_markup)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def power_status(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ipmi.powerStatus(server_ip, username, password))
        if latest_version != current_version:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'You are running version {current_version} of '
                                          f'IPMI-Bot which has been outdated by version '
                                          f'{latest_version}\nPlease go to '
                                          f'https://github.com/realdeadbeef/ipmi-bot '
                                          f'and follow the instructions for upgrading.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def power_cycle(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
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


def sdr_list(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ipmi.sdrList(server_ip, username, password))
        if latest_version != current_version:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'You are running version {current_version} of '
                                          f'IPMI-Bot which has been outdated by version '
                                          f'{latest_version}\nPlease go to '
                                          f'https://github.com/realdeadbeef/ipmi-bot '
                                          f'and follow the instructions for upgrading.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def fan_status(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text=ipmi.fanStatus(server_ip, username, password))
        if latest_version != current_version:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'You are running version {current_version} of '
                                          f'IPMI-Bot which has been outdated by version '
                                          f'{latest_version}\nPlease go to '
                                          f'https://github.com/realdeadbeef/ipmi-bot '
                                          f'and follow the instructions for upgrading.')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def cb_query_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    if query.data == 'cancel':
        query.edit_message_text(text='Cancelled')
    elif query.data == 'poweron':
        query.edit_message_text(text=ipmi.powerOn(server_ip, username, password))
    elif query.data == 'poweroff':
        query.edit_message_text(text=ipmi.powerOff(server_ip, username, password))
    elif query.data == 'powercycle':
        query.edit_message_text(text=ipmi.powerCycle(server_ip, username, password))
    elif query.data == 'soft':
        query.edit_message_text(text=ipmi.soft_shutdown(server_ip, username, password))
    else:
        query.edit_message_text(text='wat')
    if latest_version != current_version:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=f'You are running version {current_version} of '
                                      f'IPMI-Bot which has been outdated by version '
                                      f'{latest_version}\nPlease go to '
                                      f'https://github.com/realdeadbeef/ipmi-bot '
                                      f'and follow the instructions for upgrading.')


def start(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Here are a list of commands to get '
                                                                        'started:\n\n'
                                                                        '/powerusage\n'
                                                                        '/poweron\n'
                                                                        '/poweroff\n'
                                                                        '/powerstatus\n'
                                                                        '/powercycle\n'
                                                                        '/sdrlist\n'
                                                                        '/fanstatus\n'
                                                                        '/version\n')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


def version(update: Update, context: CallbackContext):
    if update.effective_chat.id == chat_id:
        if current_version != latest_version:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'You are running version {current_version} of '
                                          f'IPMI-Bot which has been outdated by version '
                                          f'{latest_version}\nPlease go to '
                                          f'https://github.com/realdeadbeef/ipmi-bot '
                                          f'and follow the instructions for upgrading.')
        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f'You are running the latest version of IPMI-Bot: {current_version}')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='You do not have permission to run this '
                                                                        'command!')


updater.dispatcher.add_handler(CommandHandler('powerusage', power_usage))
updater.dispatcher.add_handler(CommandHandler('poweron', power_on))
updater.dispatcher.add_handler(CommandHandler('poweroff', power_off))
updater.dispatcher.add_handler(CommandHandler('softshutdown', soft_shutdown))
updater.dispatcher.add_handler(CommandHandler('powerstatus', power_status))
updater.dispatcher.add_handler(CommandHandler('powercycle', power_cycle))
updater.dispatcher.add_handler(CommandHandler('sdrlist', sdr_list))
updater.dispatcher.add_handler(CommandHandler('fanstatus', fan_status))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('version', version))
updater.dispatcher.add_handler(CallbackQueryHandler(cb_query_handler))

updater.start_polling()
updater.idle()
