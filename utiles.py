import asyncio
import os
import random
import time
from urllib.parse import unquote
import aiohttp
import requests
from pyrogram import enums
from pyrogram.errors.exceptions.bad_request_400 import (MessageNotModified)

from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            ReplyKeyboardMarkup)

loop = asyncio.get_event_loop()

############## funciones del locales #########################################
def remove_invalid_chars(filename: str):
    valores = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-".replace("", "*").split("*")
    filename = str(filename).replace(" ", "-").replace("_", "-").replace("á", "a").replace("Á", "A").replace("é", "e").replace("É", "E").replace("í", "i").replace("Í", "I").replace("ó", "o").replace("Ó", "O").replace("ú", "u").replace("Ú", "U").replace("Ñ", "-N-").replace("ñ", "-n-").replace("", "*").split("*")
    nombre = []
    for f in filename:
        if f != '':nombre.append(f)
    res = [i for i in nombre if i in valores];filename = ''.join(res)
    if ".mpv" in filename:filename = filename.replace(".mpv", ".mkv")
    return filename.replace('---','-').replace('--','-')


def new_name(filename, path=None):
    if not path:path='./'
    if len(filename.split('.')) >=3:
        if 'part' in filename.split('.')[-2].lower() or '7z' in filename.split('.')[-2].lower():ext =  '.'.join([filename.split('.')[-2], filename.split('.')[-1]])
        else:ext = filename.split('.')[-1]; filename = filename.split(ext)[0]
    elif len(filename.split('.')) == 2:ext = filename.split('.')[-1]
    else: ext = ''
    if ext == '':nombre = filename
    else:nombre = filename.replace('.'+ext, '')
    c = 1
    while True:
        if ext != '':
            new_name = f'{nombre}-{c}.{ext}'
        elif ext == '':
            new_name = f'{nombre}-{c}'
        if os.path.exists(new_name):c+=1
        else:break
    return new_name

def get_name_from_text(text):
    val = '1 2 3 4 5 6 7 8 9 0 fin end'.split(' '); name = ''
    for l in text.splitlines():
        for v in val:
            if v in l.lower() and not l in name:
                if name == '':name += l.strip()
                else:name += '-' + l.strip()
    return name[:70]
def cxs(segundos):
    segundos = int(segundos);horas = int((segundos) / 60 / 60);segundos -= horas*60*60;minutos = int(segundos/60);segundos -= minutos*60;return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def cxb(num):
    num = float(num);step_unit = 1024.0
    for x in [' bytes', ' KB', ' MB', ' GB', ' TB']:
        if num < step_unit:return "%3.1f%s" % (num, x)
        num /= step_unit


def progressbar(p):
    p = int(p) ; ch='•' ; left=ch*(int(p//2.7)) ; right=ch*(int(37-(p//2.7)))
    if p >=100:left=ch*(int(p//2.7-1))
    if p<10:p=f'0{p}'
    return ''+left + f'[-{p}%-]' + right + ''

# def progressbar(p):
#     return '⬢' * (int(p)//5) + '⬡'*( 20 -( int(p)//5))


# def msg_callback(head, p, current, total):
#     msg = f'''
# **{head}… Please wait

# **[{progressbar(p)}] **
# Processing… : {p}%
# {cxb(current)} of {cxb(total)}
# Speed : {speed}/s
# ETA : {cxs(segundos)}'''

def async_run(func):
    def run(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return asyncio.get_event_loop_policy().get_event_loop().run_in_executor(None, func, *args, **kwargs)
    return run


##################################################################################

####################### funciones en la red ######################################
async def get_size(url):
    def fun():
        try:
            s = requests.Session();r = s.get(url,stream = True)
            if r.headers:return r.headers['Content-Length']
            else:return 'Desconocido'
        except:return 'Desconocido'
    async def ini_fun():loop = asyncio.get_running_loop();return await loop.run_in_executor(None, fun)
    return await ini_fun()

async def get_name_from_url(url):
    def fun():
        try:
            s = requests.Session();r = s.get(url,stream = True)
            if r.headers:return r.headers['filename']
            else:return 'Desconocido'
        except:return 'Desconocido'
    async def ini_fun():loop = asyncio.get_running_loop();return await loop.run_in_executor(None, fun)
    return await ini_fun()

async def download_file_from_url(clients, chat_id, message_id, url, fname=None,reply_markup=None):
    inicio = time.time();vlist = []
    if '*' in url:fname=url.split('*')[1]   ;   url=url.split('*')[0]
    if fname == None:
        if '.' in unquote(url.split('/')[-1]):fname = unquote(url.split('/')[-1])
        else:
            name = await get_name_from_url(url)
            if name != 'Desconocido':fname = name
            else:fname = f'file-{random.randint(100, 999)}.file'
    session: aiohttp.ClientSession = aiohttp.ClientSession();timeout = aiohttp.ClientTimeout(total=60*60*24)
    fname = remove_invalid_chars(fname)
    if os.path.exists(fname):
        fname = new_name(fname)
    f = open(fname, 'wb')
    try:
        async with session.get(url=url, timeout=timeout, verify_ssl=False,headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}) as response:
            data_to_read = True;t_ini = time.time()
            if response.headers.get("content-length"):total_bytes = int(response.headers.get("content-length"))
            else:total_bytes=1
            received_bytes=0;ini= time.time();len_count = 0
            while data_to_read:
                data = bytearray();red = 0;i = time.time()
                while red < 1024:
                    chunk = await response.content.read(1024- red)
                    if not chunk:data_to_read = False;break
                    data.extend(chunk);red += len(chunk);len_count+=len(chunk)
                f.write(data);received_bytes += red
                if time.time() - ini>= 1:
                    p = round(int(received_bytes) * 100 / int(total_bytes), 2);t = cxb(total_bytes);d = cxb(received_bytes);vlist.append(len_count);vm = 0
                    for v in vlist:
                        if v > vm:vm = v
                    vm = cxb(vm);speed = cxb(len_count);len_count = 0
                    app = clients[random.randint(0, len(clients)-1)]
                    try:
                        await app.edit_message_text(chat_id, message_id,
                            f'''**Downloading...**\n\n{progressbar(p)}\n\n**➩ File Name : __{fname}__**\n\n**➩ __{d}__ Of __{t}__**\n\n**➩ Speed : __{speed}/s__**\n\t\t       **🔝 __{vm}/s__**\n\n**➩ Time Left : __{cxs(time.time() - inicio)}__**''',
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Cancelar', "task_cancel")]]))
                    except MessageNotModified:pass
                    #     print(f'➩ {fname} {p}% 🔽 {t}  {speed}/s  {cxs(time.time() - inicio)}.......',end='\r',flush=False)
                    # else: print(f'➩ {fname} {p}% 🔽 {t}  {speed}/s  {cxs(time.time() - inicio)}.......',end='\r',flush=False)
                    ini = time.time()
            ret  = fname
    except:
            ret = False
    await session.close()
    return ret

############################################################################################

################## funciones en telegram ####################################################


async def send_chatAction(app, chat_id, ext):
    while True:
        await app.send_chat_action(chat_id, ext)
        await asyncio.sleep(4)


def get_file_name(file_name, text, file_date):
        file_name_in_text = False
        filename_ok = False
        for i in '1 2 3 4 5 6 7 8 9 0 fin end'.split(' '):
            if i in str(text).lower():
                file_name_in_text = True;break
        for i in '1 2 3 4 5 6 7 8 9 0 fin end'.split(' '):
            if i in str(file_name).lower():
                filename_ok = True;break
        if filename_ok:file_name=file_name
        elif file_name_in_text:file_name=get_name_from_text(str(text))
        else:file_name=str(file_date).split(' ')[0] + '-' + file_name
        file_name = remove_invalid_chars(file_name)
        return file_name


def get_message_info(message):
        message_id = message.id
        message_date = message.date
        text = message.text
        forward_from_message_id = message.forward_from_message_id

        if message.from_user:
            first_name = message.from_user.first_name
            username = message.from_user.username
            user_id = message.from_user.id
        else:
            first_name, username, user_id = None,None,None
        if message.chat:
            chat_id = message.chat.id
            chat_title = message.chat.title
        else:
            chat_id, chat_title= None,None
        if message.sender_chat:
            sender_chat_title, sender_chat_id = message.sender_chat.title,message.sender_chat.id
        else:
            sender_chat_title,sender_chat_id = None,None
        if message.media:
            file = eval(f"message.{str(message.media).replace('MessageMediaType.','').lower()}")
            file_date = file.date
            file_size = file.file_size
            file_id = file.file_id
            file_name = str(file.file_name)
            file_name = get_file_name(file_name, str(message.caption), file_date)

        else:
            file_name,file_date, file_size, file_id = None, None, None, None
        info = {
            'message_id':message_id,
            'message_date':message_date,
            'text':text,
            'first_name':first_name,
            'username':username,
            'user_id':user_id,
            'chat_id':chat_id,
            'chat_title':chat_title,
            'sender_chat_title':sender_chat_title,
            'sender_chat_id':sender_chat_id,
            'file_date':file_date,
            'file_size':file_size,
            'file_id':file_id,
            'file_name':file_name,
        }
        return info


async def download_tgFile(clients, chat_id, message_id, message, file_name, file_size, reply_markup=None, path=None):
    app = clients[random.randint(0, len(clients)-1)]
    message = await app.get_messages(chat_id, message.id)

    if path == None:path = "./"
    if os.path.exists(path + file_name):
        file_name = new_name(file_name)
    len_count = 0
    total_download = 0
    old_time=time.time()
    f = open(path + file_name, 'wb')
    try:
    # if True:
        async for chunk in app.stream_media(message):
                    data = bytearray()
                    data.extend(chunk)
                    f.write(data)
                    total_download += len(chunk)
                    len_count += len(chunk)
                    porcent=total_download * 100 / file_size
                    if porcent > 100: porcent=100
                    if time.time() - old_time >= 1:
                        try:
                        # if True:
                            client = clients[random.randint(0, len(clients)-1)]
                            msg = f'''Ｄｏｗｎｌｏａｄｉｎｇ．．．\n\n{progressbar(porcent)}\n\n➩ File Name : {file_name}\n\n➩ {cxb(total_download)} Of {cxb(file_size)}\n\n➩ Speed : {cxb(len_count)}/s\n\n➩ Time Left : {cxs(file_size/len_count)}'''
                            await client.edit_message_text(chat_id, message_id,msg,
                                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Cancelar', "task_cancel")]]))
                        except MessageNotModified:pass
                        len_count = 0
                        old_time= time.time()
        f.close()
    except:
        f.close()
        file_name = False

    return file_name


async def upload_tgFile(app, message, file_name, chat_id=None, save_as=None, m=None, text=None,reply_to_message_id=None, delete_message=True, delete_file=False):
            # try:
                # print(file_name);return
                if m ==None:m = await message.reply('Procesando...')
                if save_as == None:save_as = "./"
                if text==None:text=file_name
                if chat_id == None:
                    if message.chat:chat_id = message.chat.id
                    elif message.from_user:chat_id = message.from_user.id
                    elif message.sender_chat:chat_id = message.sender_chat.id
                    else:return False

                async def progress(current, total, id_datas, file_name):
                    if time.time()-globals()[f'old_time{id_datas}'] >= 1:
                        porcent=current * 100 / total
                        if porcent > 100: porcent=100
                        msg = f'''Uploading．．．\n\n{progressbar(porcent)}\n\n➩ File Name : {file_name}\n\n➩ {cxb(current)} Of {cxb(total)}\n\n➩ Speed : {cxb(current - globals()[f'old_current{id_datas}'])}/s\n\n➩ Time Left : {cxs(time.time()-globals()[f'time_ini{id_datas}'])}'''
                        await m.edit(msg)
                        globals()[f'old_current{id_datas}'] = current
                        globals()[f'old_time{id_datas}'] = time.time()

                id_datas = random.randint(100,999);globals()[f'old_current{id_datas}'] = 0;globals()[f'old_time{id_datas}'] = 0; globals()[f'time_ini{id_datas}'] = time.time()

                file_name = str(file_name) ; ext = str(file_name).split('.')[-1]

                if ext in 'jpg.jpeg.png.gif.tiff.psd.bmp.webp.tgs':ext = enums.ChatAction.UPLOAD_PHOTO
                elif ext in 'mp4.mov.wmv.avi.avchd.flv.f4v.swf.mkv.webm.html5': ext = enums.ChatAction.UPLOAD_VIDEO
                elif ext in 'wav.aiff.au.flac..shorten.tta.atrac.mp3.aac.wma.opus.ogg.dsd.mqa': ext = enums.ChatAction.UPLOAD_AUDIO
                else:ext = enums.ChatAction.UPLOAD_DOCUMENT

                action = asyncio.run_coroutine_threadsafe(send_chatAction(app, chat_id, ext), loop)
                message_media = await app.send_document(chat_id=chat_id, document=save_as + file_name, caption=f'```{text}```', progress=progress, progress_args=(id_datas,file_name))
                action.cancel() ; await app.send_chat_action(chat_id, enums.ChatAction.CANCEL)
                if delete_file:os.unlink(save_as + file_name)

                if delete_message:await m.delete()
                return True, message_media
            # except Exception as error:await message.reply(error); print('Error:',error)
