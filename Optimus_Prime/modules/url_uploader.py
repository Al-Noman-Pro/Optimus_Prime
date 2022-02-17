import aiohttp
import asyncio
import datetime
import math
import os
import time
import traceback

from telethon import events
from Optimus_Prime import telethn as bot

DOWNLOADPATH = "./"


async def progress(current, total, event, start, type_of_ps):
    """Generic progress_callback for both
    upload.py and download.py"""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "[{0}{1}]\n🅿 Percent: {2}\n".format(
            "".join(["✅" for i in range(math.floor(percentage / 10))]),
            "".join(["☑" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))
        tmp = progress_str + "📥 DD: {0} of {1}\n⏰ ETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time))
        await event.edit("{}\n {}".format(type_of_ps, tmp))


def convert_from_bytes(size):
    power = 2 ** 10
    n = 0
    units = {0: "", 1: "kilobytes", 2: "megabytes", 3: "gigabytes", 4: "terabytes"}
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + "d, ") if days else "")
        + ((str(hours) + "h, ") if hours else "")
        + ((str(minutes) + "m, ") if minutes else "")
        + ((str(seconds) + "s, ") if seconds else "")
        + ((str(milliseconds) + "ms, ") if milliseconds else ""))
    return tmp[:-2]
    

def get_date_in_two_weeks():
    """
    get maximum date of storage for file
    :return: date in two weeks
    """
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()


async def download_file(url, file_name, message, start_time, bot):
    async with aiohttp.ClientSession() as session:
        time.time()
        await download_coroutine(session, url, file_name, message, start_time, bot)
    return file_name


async def download_coroutine(session, url, file_name, event, start, bot):

    CHUNK_SIZE = 1024 * 6  # 2341
    downloaded = 0
    display_message = ""
    async with session.get(url) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await event.edit(
            """**Initiating Download**

**URL:** {}

**File Name:** {}

**File Size:** {}

**@Optimus_Prime_Pro_Bot**""".format(
                url,
                os.path.basename(file_name).replace("%20", " "),
                humanbytes(total_length)),
            parse_mode="md")
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 10.00) == 0:  # downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = (
                        round((total_length - downloaded) / speed) * 1000
                    )
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        if total_length < downloaded:
                            total_length = downloaded
                        current_message = """Downloading : {}%

URL: {}

File Name: {}

File Size: {}
Downloaded: {}
ETA: {}""".format(
                            "%.2f" % (percentage),
                            url,
                            file_name.split("/")[-1],
                            humanbytes(total_length),
                            humanbytes(downloaded),
                            time_formatter(estimated_total_time))
                        if (
                            current_message != display_message
                            and current_message != "empty"
                        ):
                            print(current_message)
                            await event.edit(current_message, parse_mode="html")

                            display_message = current_message
                    except Exception as e:
                        print("Error", e)
                        # logger.info(str(e))
        return await response.release()


@bot.on(events.NewMessage(pattern="/upload"))
async def up(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("Downloading...")

        try:
            filename = os.path.join(DOWNLOADPATH, os.path.basename(url.text))
            await download_file(url.text, filename, ilk, start, bot)
        except Exception as e:
            print(e)
            await event.respond(f"Downloading Failed\n\n**Error:** {e}")

        await ilk.delete()

        try:
            orta = await event.respond("Uploading In Telegram...")

            dosya = await bot.upload_file(
                filename,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, orta, start, "Uploading In Telegram...")
                ))

            str(time.time() - start)
            await bot.send_file(
                event.chat.id,
                dosya,
                force_document=True,
                caption=f"Uploaded By @Optimus_Prime_Pro_Bot")
        except Exception as e:
            traceback.print_exc()

            print(e)
            await event.respond(f"Uploading Failed\n\n**Error:** {e}")

        await orta.delete()

    raise events.StopPropagation


def main():
    if not os.path.isdir(DOWNLOADPATH):
        os.mkdir(DOWNLOADPATH)


if __name__ == "__main__":
    main()
