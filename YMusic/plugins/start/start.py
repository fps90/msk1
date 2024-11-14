from pyrogram import filters
from YMusic import app
from config import DEV_USER, DEV_CHANNEL
from YMusic.filters import command
import config

HELP_COMMAND = ["/start","اوامر", "أوامر", "الاوامر", "الأوامر","start"]

HELP_MESSAGE = f"""
أهلا عزيزي في أوامر حساب التشغيل 
⎯ ⎯ ⎯ ⎯
- يمكنك رؤية الأوامر التالية :
~ شغلنا ـ بالرد او بالأسم لتشغيل صوت من اليوتيوب 
~ فيديو ـ بالرد او بالأسم لتشغيل فيديو من اليوتيوب 
~ انضم - مع يوزر القناة لأنضمام الحساب في قناة
~ نزلي فيديو - يحمل فيديو من اليوتيوب
~ ايقاف ـ لإيقاف تشغيل الصوت الحالي
~ سكب ـ لتخطي الصوت المشغل الحالي
~ يوت ـ لبحث وتنزيل صوت من اليوتيوب
~ البنك ـ لعرض بنك الحساب المشغل الحالي
~ الادنى - وضع حد اقصى لمدة التشغيل
~ مؤقت ـ ايقاف الصوت مؤقتا
~ استمرار ـ استمرار عملية التشغيل 
~ تكرار ـ يمكنك تكرار عدد مرات الصوت
~ الطابور ـ لعرض قائمة التشغيل الحالية
~ السورس ـ لعرض سورس التنصيب 
⎯ ⎯ ⎯ ⎯

- 🪬 مالك الحساب : [Click .](https://t.me/{DEV_USER}) 
- 🪬 قناة المطور : [Click .](https://t.me/{DEV_CHANNEL}) 
"""

# @app.on_message(filters.private & filters.command(START_COMMAND, PREFIX))
# async def _start(_, message):
    # await message.reply_text(
        # "Hey user how are you.\nIf you need any help just ping me I am here to help you."
    # )

@app.on_message(command(HELP_COMMAND))
async def _help(_, message):
    await message.reply_text(HELP_MESSAGE)
