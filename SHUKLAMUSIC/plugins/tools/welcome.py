'''from SHUKLAMUSIC import app
from pyrogram import filters, enums
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageChops
import asyncio, os
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

# ---------------- IMAGE UTILS ---------------- #

def circle(pfp, size=(535, 535)):
    pfp = pfp.resize(size).convert("RGBA")
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + size, fill=255)
    pfp.putalpha(mask)
    return pfp


def welcomepic(pic, user_id):
    bg = Image.open("SHUKLAMUSIC/assets/wel2.png")
    pfp = Image.open(pic).convert("RGBA")
    pfp = circle(pfp)

    draw = ImageDraw.Draw(bg)
    font = ImageFont.truetype("SHUKLAMUSIC/assets/font.ttf", 60)

    draw.text((655, 465), f"ID: {user_id}", fill="white", font=font)
    bg.paste(pfp, (50, 90), pfp)

    path = f"downloads/welcome_{user_id}.png"
    bg.save(path)
    return path

# ---------------- COMMAND ---------------- #

@app.on_message(filters.command("welcome") & ~filters.private)
async def welcome_toggle(_, message):
    if len(message.command) != 2:
        return await message.reply("**Usage:** `/welcome on | off`")

    member = await app.get_chat_member(message.chat.id, message.from_user.id)
    if member.status not in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        return await message.reply("**Only admins can use this command.**")

    if message.command[1].lower() == "on":
        await wlcm.enable(message.chat.id)
        await message.reply("✅ **Welcome enabled**")

    elif message.command[1].lower() == "off":
        await wlcm.disable(message.chat.id)
        await message.reply("❌ **Welcome disabled**")

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
        pic = await app.download_media(user.photo.big_file_id, f"pp_{user.id}.png")
    except:
        pic = "SHUKLAMUSIC/assets/upic.png"

    try:
        if temp.MELCOW.get(chat_id):
            await temp.MELCOW[chat_id].delete()

        img = welcomepic(pic, user.id)

        buttons = []
        if user.username:
            buttons.append([
                InlineKeyboardButton("👤 View User", url=f"https://t.me/{user.username}")
            ])

        msg = await app.send_photo(
            chat_id,
            photo=img,
            caption=f"""
ㅤㅤ◦•●◉✿ ᴡᴇʟᴄᴏᴍᴇ ✿◉●•◦
**▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬**

**☉ ɴᴀᴍᴇ ⧽** {user.mention}
**☉ ɪᴅ ⧽** `{user.id}`
**☉ ᴜ_ɴᴀᴍᴇ ⧽** @{user.username if user.username else 'None'}
**☉ ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀs ⧽** {count}

**▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬**
""",
            reply_markup=InlineKeyboardMarkup(buttons) if buttons else None
        )

        temp.MELCOW[chat_id] = msg
        await asyncio.sleep(300)
        await msg.delete()

    except Exception as e:
        LOGGER.error(e)

    finally:
        for f in [pic, img]:
            if f and os.path.exists(f):
                os.remove(f)

'''
