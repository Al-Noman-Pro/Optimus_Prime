from threading import Thread
from telegram import Update
from telegram.ext import CommandHandler

from Optimus_Prime import dispatcher, LOGGER
from Optimus_Prime.modules.helper_funcs.clone_helper.message_utils import auto_delete_message, sendMessage
from Optimus_Prime.modules.helper_funcs.filters import CustomFilters
from Optimus_Prime.modules.helper_funcs.clone_helper import gdriveTools
from Optimus_Prime.modules.helper_funcs.clone_helper.bot_utils import is_gdrive_link


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
