from telegram.ext import CommandHandler

from Optimus_Prime import dispatcher
from Optimus_Prime.modules.helper_funcs.clone_helper.gdriveTools import GoogleDriveHelper
from Optimus_Prime.modules.helper_funcs.clone_helper.message_utils import deleteMessage, sendMessage
from Optimus_Prime.modules.helper_funcs.filters import CustomFilters
from Optimus_Prime.modules.helper_funcs.clone_helper.bot_utils import is_gdrive_link, is_gdtot_link, new_thread
from Optimus_Prime.modules.helper_funcs.clone_helper.direct_link_generator import gdtot
from Optimus_Prime.modules.helper_funcs.clone_helper.exceptions import DirectDownloadLinkException

@new_thread
def countNode(update, context):
    args = update.message.text.split(" ", maxsplit=1)
    reply_to = update.message.reply_to_message
    if len(args) > 1:
        link = args[1]
        if update.message.from_user.username:
            tag = f"@{update.message.from_user.username}"
        else:
            tag = update.message.from_user.mention_html(update.message.from_user.first_name)
    elif reply_to is not None:
        link = reply_to.text
        if reply_to.from_user.username:
            tag = f"@{reply_to.from_user.username}"
        else:
            tag = reply_to.from_user.mention_html(reply_to.from_user.first_name)
    else:
        link = ''
    gdtot_link = is_gdtot_link(link)
    if gdtot_link:
        try:
            link = gdtot(link)
        except DirectDownloadLinkException as e:
            return sendMessage(str(e), context.bot, update)
    if is_gdrive_link(link):
        msg = sendMessage(f"Counting: <code>{link}</code>", context.bot, update)
        gd = GoogleDriveHelper()
        result = gd.count(link)
        deleteMessage(context.bot, msg)
        cc = f'\n\n<b>cc: </b>{tag}'
        sendMessage(result + cc, context.bot, update)
        if gdtot_link:
            gd.deletefile(link)
    else:
        sendMessage('Send Gdrive link along with command or by replying to the link by command', context.bot, update)

count_handler = CommandHandler("count", countNode, filters=CustomFilters.authorized_chat | CustomFilters.authorized_user | CustomFilters.owner_filter, run_async=True)

dispatcher.add_handler(count_handler)
