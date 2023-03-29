print('starting...')
import asyncio
from pyrogram import Client, idle
import re
import runserver
from utiles import download_file_from_url, download_tgFile, upload_tgFile, get_file_name, get_message_info
'-------- Login ----------'
from logging import INFO, basicConfig, log

basicConfig(format="[%(levelname)s]: %(message)s", level=INFO, force=True)
log(INFO, "Initializing...")
'---------------------------------------------'

api_id = "5095599"
api_hash = "ac087d6bb97a885e4f64571cf7ead8a4"
bot_token = '1906762390:AAH0bT5eB_mwBbNiaeHnrjDSbfa_XTt6l48'
app = Client('client',api_id=api_id, api_hash=api_hash, bot_token=bot_token)

clients = [app]

@app.on_message()
async def message_handler(app, message):
    if message.chat.id != 1935578948 or message.chat.id != 885488992:return
    if message.text == '/start':
        await message.reply('i am online')
        return
    reply = await message.reply('processing...')
    file_list = []
    if message.document or message.audio or message.video or message.sticker or message.photo:
        info = get_message_info(message)
        file = await download_tgFile(clients, message.chat.id, reply.id, message, info['file_name'], info['file_size']) 
        file_list.append(file)
    else:
        regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
        url = re.findall(regex,message.text)
        urls = [x[0] for x in url]
        if len(urls) > 0:
            for url in urls:
                file = await download_file_from_url(clients, message.chat.id, reply.id, url)
                if file:
                    file_list.append(file)
    if len(file_list) > 0:
        for item in file_list:
            await upload_tgFile(app, reply, str(item), message.chat.id, m = reply, delete_message=False)



if __name__ == '__main__':      
    app.start()
    app.send_message(1935578948, 'online')
    log(INFO, "Bot Started")
    idle()
    app.stop()
    # asyncio.get_event_loop_policy().get_event_loop().run_forever()

