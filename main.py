print('starting...')
import asyncio
from pyrogram import Client, idle
import re
import runserver
import os
from utiles import download_file_from_url, download_tgFile, upload_tgFile, get_file_name, get_message_info
# import db

# global status

# if db.status != 'on':
if True:
    print('iniciando')
    api_id = "5095599"
    api_hash = "ac087d6bb97a885e4f64571cf7ead8a4"
    bot_token = '5673311462:AAFC2f3UBp6RCoqOdLgkd5ALb5HTvY2Doqg'
    app = Client('client',api_id=api_id, api_hash=api_hash, bot_token=bot_token)

    clients = [app]

    @app.on_message()
    async def message_handler(app, message):
        # if message.chat.id != 1935578948 or message.chat.id != 885488992:return
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
        if not os.path.exists('ONLINE'):
            app.start()
            app.send_message(1935578948, 'online')
            print("Bot Started")
            # async def i():
            #     await db.write(db.dbname, 'on')
            # asyncio.get_event_loop_policy().get_event_loop().run_until_complete(i())
            idle()
            app.stop()
            if os.path.exists('ONLINE'):
                os.unlink('ONLINE')
        # asyncio.get_event_loop_policy().get_event_loop().run_forever()

