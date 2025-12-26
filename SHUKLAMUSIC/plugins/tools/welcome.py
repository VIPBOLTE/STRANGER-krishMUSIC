# -----------------------------------------------
# 🔸 StrangerMusic Project
# 🔹 Developed & Maintained by: Shashank Shukla
# -----------------------------------------------

from SHUKLAMUSIC import app
from pyrogram import filters, enums
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops
import asyncio
import os
from logging import getLogger

LOGGER = getLogger(__name__)

# ---------------- DATABASE ---------------- #

class WelDatabase:
    def __init__(self):
        self.data = {}

    async def is_enabled(self, chat_id: int):
        return self.data.get(chat_id, True)

    async def enable(self, chat_id: int):
        self.data[chat_id] = True

    async def disable(self, chat_id: int):
        self.data[chat_id] = False


wlcm = WelDatabase()

# ---------------- TEMP STORAGE ---------------- #

class temp:
    MELCOW = {}

# ---------------- IMAGE FUNCTIONS ---------------- #

def circle(pfp, size=(535, 535), brightness_factor=1.2):
    pfp = pfp.resize(size).convert("RGBA")
    pfp = ImageEnhance.Brightness(pfp).enhance(brightness_factor)

    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size)

    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp


def welcomepic(pic, user_id):
    background = Image.open("SHUKLAMUSIC/assets/wel2.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)

    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype("SHUKLAMUSIC/assets/font.ttf", size=60)

    draw.text((655, 465), f"ID: {user_id}", fill=(255, 255, 255), font=font)
    background.paste(pfp, (50, 90), pfp)

    path = f"downloads/welcome_{user_id}.png"
    background.save(path)
    return path

# ---------------- COMMAND ---------------- #

@app.on_message(filters.command("welcome") & ~filters.private)
async def welcome_toggle(_, message):
    if len(message.command) != 2:
        return await message.reply_text("**Usage:** `/welcome on | off`")

    member = await app.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply_text("**Only admins can use this command.**")

    state = message.command[1].lower()

    if state == "on":
        await wlcm.enable(message.chat.id)
        await message.reply_text("✅ **Welcome enabled**")
    elif state == "off":
        await wlcm.disable(message.chat.id)
        await message.reply_text("❌ **Welcome disabled**")
    else:
        await message.reply_text("**Usage:** `/welcome on | off`")

# ---------------- WELCOME EVENT ---------------- #

@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id

    if not await wlcm.is_enabled(chat_id):
        return

    if not member.new_chat_member or member.old_chat_member:
        return

    user = member.new_chat_member.user
    count = await app.get_chat_members_count(chat_id)

    try:
        pic = await app.download_media(
            user.photo.big_file_id,
            file_name=f"pp_{user.id}.png"
        )
    except:
        pic = "SHUKLAMUSIC/assets/upic.png"

    try:
        if temp.MELCOW.get(chat_id):
            await temp.MELCOW[chat_id].delete()

        welcomeimg = welcomepic(pic, user.id)

        buttons = []
        if user.username:
            buttons.append([InlineKeyboardButton("👤 View User", url=f"https://t.me/{user.username}")])

        msg = await app.send_photo(
            chat_id,
            photo=welcomeimg,
            caption=f"""
🎉 **Welcome to {member.chat.title}**

👤 **Name:** {user.mention}
🆔 **ID:** `{user.id}`
👥 **Members:** {count}
""",
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )

        temp.MELCOW[chat_id] = msg

        await asyncio.sleep(300)
        await msg.delete()
        temp.MELCOW.pop(chat_id, None)

    except Exception as e:
        LOGGER.error(e)

    finally:
        if os.path.exists(pic):
            os.remove(pic)
        if os.path.exists(welcomeimg):
            os.remove(welcomeimg)
        state = message.text.split(None, 1)[1].strip().lower()
        if state == "off":
            if A:
                await message.reply_text("**ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ ᴀʟʀᴇᴀᴅʏ ᴅɪsᴀʙʟᴇᴅ !**")
            else:
                await wlcm.add_wlcm(chat_id)
                await message.reply_text(f"**ᴅɪsᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɪɴ** {message.chat.title}")
        elif state == "on":
            if not A:
                await message.reply_text("**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɴᴏᴛɪғɪᴄᴀᴛɪᴏɴ.**")
            else:
                await wlcm.rm_wlcm(chat_id)
                await message.reply_text(f"**ᴇɴᴀʙʟᴇᴅ ᴡᴇʟᴄᴏᴍᴇ ɪɴ** {message.chat.title}")
        else:
            await message.reply_text(usage)
    else:
        await message.reply("**sᴏʀʀʏ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴇɴᴀʙʟᴇ ᴡᴇʟᴄᴏᴍᴇ!**")


@app.on_chat_member_updated(filters.group, group=-3)
async def greet_new_member(_, member: ChatMemberUpdated):
    chat_id = member.chat.id
    count = await app.get_chat_members_count(chat_id)
    A = await wlcm.find_one(chat_id)
    if A:
        return

    if member.new_chat_member and not member.old_chat_member and member.new_chat_member.status != "kicked":
        user = member.new_chat_member.user
        try:
            pic = await app.download_media(user.photo.big_file_id, file_name=f"pp{user.id}.png")
        except AttributeError:
            pic = "SHUKLAMUSIC/assets/upic.png"

        if temp.MELCOW.get(f"welcome-{chat_id}") is not None:
            try:
                await temp.MELCOW[f"welcome-{chat_id}"].delete()
            except Exception as e:
                LOGGER.error(e)

        try:
            welcomeimg = welcomepic(pic, user.first_name, member.chat.title, user.id, user.username)
            button_text = "๏ ᴠɪᴇᴡ ɴᴇᴡ ᴍᴇᴍʙᴇʀ ๏"
            add_button_text = "✙ ᴋɪᴅɴᴀᴘ ᴍᴇ ✙"
            deep_link = f"tg://openmessage?user_id={user.id}"
            add_link = f"https://t.me/{app.username}?startgroup=true"

            msg = await app.send_photo(
                chat_id,
                photo=welcomeimg,
                caption=f"""
ㅤㅤ◦•●◉✿ ᴡᴇʟᴄᴏᴍᴇ ✿◉●•◦
**▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬**

**☉ ɴᴀᴍᴇ ⧽** {user.mention}
**☉ ɪᴅ ⧽** `{user.id}`
**☉ ᴜ_ɴᴀᴍᴇ ⧽** @{user.username if user.username else 'None'}
**☉ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ⧽** {count}

**▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬**
""",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)],
                    [InlineKeyboardButton(text=add_button_text, url=add_link)],
                ])
            )

            temp.MELCOW[f"welcome-{chat_id}"] = msg

            # ✅ Auto-delete welcome message in 3 minutes
            await asyncio.sleep(300)
            await msg.delete()

        except Exception as e:
            LOGGER.error(e)
