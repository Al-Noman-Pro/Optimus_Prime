from threading import Thread
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton
from telegram.update import Update
from telegram.message import Message
from telegram.error import RetryAfter

from Optimus_Prime import bot, LOGGER, dispatcher
from Optimus_Prime.modules.helper_funcs.filters import CustomFilters
from Optimus_Prime.modules.helper_funcs.clone_helper.gdriveTools import GoogleDriveHelper


def sendMessage(text: str, bot, update: Update):
    try:
        return bot.send_message(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=text, allow_sending_without_reply=True, parse_mode='HTMl', disable_web_page_preview=True)
    except RetryAfter as r:
        LOGGER.warning(str(r))
        sleep(r.retry_after * 1.5)
        return sendMessage(text, bot, update)
    except Exception as e:
        LOGGER.error(str(e))
        return

def editMessage(text: str, message: Message, reply_markup=None):
    try:
        bot.edit_message_text(text=text, message_id=message.message_id,
                              chat_id=message.chat.id,reply_markup=reply_markup,
                              parse_mode='HTMl', disable_web_page_preview=True)
    except RetryAfter as r:
        LOGGER.warning(str(r))
        sleep(r.retry_after * 1.5)
        return editMessage(text, message, reply_markup)
    except Exception as e:
        LOGGER.error(str(e))
        return

def sendMarkup(text: str, bot, update: Update, reply_markup: InlineKeyboardMarkup):
    try:
        return bot.send_message(update.message.chat_id,
                            reply_to_message_id=update.message.message_id,
                            text=text, reply_markup=reply_markup, allow_sending_without_reply=True,
                            parse_mode='HTMl', disable_web_page_preview=True)
    except RetryAfter as r:
        LOGGER.warning(str(r))
        sleep(r.retry_after * 1.5)
        return sendMarkup(text, bot, update, reply_markup)
    except Exception as e:
        LOGGER.error(str(e))
        return

class ButtonMaker:
    def __init__(self):
        self.button = []

    def buildbutton(self, key, link):
        self.button.append(InlineKeyboardButton(text = key, url = link))

    def sbutton(self, key, data):
        self.button.append(InlineKeyboardButton(text = key, callback_data = data))

    def build_menu(self, n_cols, footer_buttons=None, header_buttons=None):
        menu = [self.button[i:i + n_cols] for i in range(0, len(self.button), n_cols)]
        if header_buttons:
            menu.insert(0, header_buttons)
        if footer_buttons:
            menu.append(footer_buttons)
        return menu

def list_buttons(update, context):
    user_id = update.message.from_user.id
    try:
        key = update.message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return sendMessage('Send a search key along with command', context.bot, update)
    buttons = ButtonMaker()
    buttons.sbutton("Drive Root", f"types {user_id} root")
    buttons.sbutton("Recursive", f"types {user_id} recu")
    buttons.sbutton("Cancel", f"types {user_id} cancel")
    button = InlineKeyboardMarkup(buttons.build_menu(2))
    sendMarkup('Choose option to list.', context.bot, update, button)

def select_type(update, context):
    query = update.callback_query
    user_id = query.from_user.id
    msg = query.message
    key = msg.reply_to_message.text.split(" ", maxsplit=1)[1]
    data = query.data
    data = data.split(" ")
    if user_id != int(data[1]):
        query.answer(text="Not Yours!", show_alert=True)
    elif data[2] in ["root", "recu"]:
        query.answer()
        buttons = ButtonMaker()
        buttons.sbutton("Folders", f"types {user_id} folders {data[2]}")
        buttons.sbutton("Files", f"types {user_id} files {data[2]}")
        buttons.sbutton("Both", f"types {user_id} both {data[2]}")
        buttons.sbutton("Cancel", f"types {user_id} cancel")
        button = InlineKeyboardMarkup(buttons.build_menu(2))
        editMessage('Choose option to list.', msg, button)
    elif data[2] in ["files", "folders", "both"]:
        query.answer()
        list_method = data[3]
        item_type = data[2]
        editMessage(f"<b>Searching for <i>{key}</i></b>", msg)
        Thread(target=_list_drive, args=(key, msg, list_method, item_type)).start()
    else:
        query.answer()
        editMessage("list has been canceled!", msg)

def _list_drive(key, bmsg, list_method, item_type):
    LOGGER.info(f"listing: {key}")
    list_method = list_method == "recu"
    gdrive = GoogleDriveHelper()
    msg, button = gdrive.drive_list(key, isRecursive=list_method, itemType=item_type)
    if button:
        editMessage(msg, bmsg, button)
    else:
        editMessage(f'No result found for <i>{key}</i>', bmsg)

list_handler = CommandHandler("list", list_buttons, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user | CustomFilters.owner_filter, run_async=True)
list_type_handler = CallbackQueryHandler(select_type, pattern="types", run_async=True)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(list_type_handler)
