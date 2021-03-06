from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from plugins.vc.handlers import skip_current_song, skip_item
from plugins.vc.queues import QUEUE, clear_queue

@Client.on_message(filters.command(['skip', 'next', 'n', '/skip', '/next'], prefixes=f"{HNDLR}"))
async def skip(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if len(m.command) < 2:
        op = await skip_current_song(chat_id)
        if op == 0:
            await m.reply("**ππ»ππππβπ πππππππ ππ πππ πππππ ππ ππππ!**")
        elif op == 1:
            await m.reply("**π©π¬ππππ πΈππππ, π³ππππππ π½ππππ πͺπππ**")
        else:
            await m.reply(
                f"**β­ Skipped** \n**π§ Now playing** - [{op[0]}]({op[1]}) | `{op[2]}`",
                disable_web_page_preview=True,
            )
    else:
        skip = m.text.split(None, 1)[1]
        OP = "**ποΈ πΉππππππ πππ πππππππππ πππππ ππππ πππ πΈππππ: -**"
        if chat_id in QUEUE:
            items = [int(x) for x in skip.split(" ") if x.isdigit()]
            items.sort(reverse=True)
            for x in items:
                if x == 0:
                    pass
                else:
                    hm = await skip_item(chat_id, x)
                    if hm == 0:
                        pass
                    else:
                        OP = OP + "\n" + f"**#β£{x}** - {hm}"
            await m.reply(OP)        
      

@Client.on_message(filters.command(['end', 'stop', '/end', '/stop', 'x'], prefixes=f"{HNDLR}"))
async def stop(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.leave_group_call(chat_id)
            clear_queue(chat_id)
            await m.reply("**πEnd**")
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**π€¨π΅ππππππ ππ πππππππ !**")

   
@Client.on_message(filters.command(['pause', '/pause', 'wait', 'ruko'], prefixes=f"{HNDLR}"))
async def pause(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.pause_stream(chat_id)
            await m.reply(
                f"**βΈ Paused.**\n\nβ’ To resume playback, use the command "
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**π€¨Nothing is playing!**")
      

@Client.on_message(filters.command(['resume', 'r', '/resume'], prefixes=f"{HNDLR}"))
async def resume(client, m: Message):
    await m.delete()
    chat_id = m.chat.id
    if chat_id in QUEUE:
        try:
            await call_py.resume_stream(chat_id)
            await m.reply(
                f"**βΆ Resumed**\n\nβ’ To pause playback, use the command**"
            )
        except Exception as e:
            await m.reply(f"**ERROR** \n`{e}`")
    else:
        await m.reply("**π΅ππππππ ππ πππππππππ ππππππβ**")
