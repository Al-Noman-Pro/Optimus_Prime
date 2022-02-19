from threading import Thread
from telegram import Update
from telegram.ext import CommandHandler
from telegram.message import Message

from Optimus_Prime import dispatcher, LOGGER, AUTO_DELETE_MESSAGE_DURATION
from Optimus_Prime.modules.helper_funcs.filters import CustomFilters
from Optimus_Prime.modules.helper_funcs.clone_helper import gdriveTools

def is_gdrive_link(url: str):
    return "drive.google.com" in url

def auto_delete_message(bot, cmd_message: Message, bot_message: Message):
    if AUTO_DELETE_MESSAGE_DURATION != -1:
        sleep(AUTO_DELETE_MESSAGE_DURATION)
        try:
            # Skip if None is passed meaning we don't want to delete bot xor cmd message
            deleteMessage(bot, cmd_message)
            deleteMessage(bot, bot_message)
        except AttributeError:
            pass


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


def deletefile(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    if len(args) > 1:
        link = args[1]
    elif reply_to is not None:
        link = reply_to.text
    else:
        link = ''
    if is_gdrive_link(link):
        LOGGER.info(link)
        drive = gdriveTools.GoogleDriveHelper()
        msg = drive.deletefile(link)
    else:
        msg = 'Send Gdrive link along with command or by replying to the link by command'
    reply_message = sendMessage(msg, context.bot, update)
    Thread(target=auto_delete_message, args=(context.bot, update.message, reply_message)).start()

delete_handler = CommandHandler("del", deletefile, filters=CustomFilters.owner_filter, run_async=True)

dispatcher.add_handler(delete_handler)
