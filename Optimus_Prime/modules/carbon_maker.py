import aiofiles
import aiohttp
import speedtest
import sys
import traceback
import codecs
import pickle

from functools import wraps
from asyncio import gather, get_running_loop
from io import BytesIO
from math import atan2, cos, radians, sin, sqrt
from random import randint
from re import findall
from time import time
from datetime import timedelta, datetime
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from wget import download

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden

from Optimus_Prime import pbot
from Optimus_Prime import pbot as app
from Optimus_Prime import JOIN_LOGGER
from Optimus_Prime import aiohttpsession as aiosession


def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ''
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line
    else:
        result.append(small_msg)

    return result


async def make_carbon(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            await app.leave_chat(message.chat.id)
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb,
            )
            error_feedback = split_limits(
                '**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n'.format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    ''.join(errors),
                ),
            )
            for x in error_feedback:
                await app.send_message(
                    JOIN_LOGGER,
                    x
                )
            raise err
    return capture


@pbot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "`Reply to a text message to make carbon.`"
        )
    if not message.reply_to_message.text:
        return await message.reply_text(
            "`Reply to a text message to make carbon.`"
        )
    m = await message.reply_text("`Preparing Carbon`")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("`Uploading`")
    await pbot.send_document(message.chat.id, carbon)
    await m.delete()
    carbon.close()
