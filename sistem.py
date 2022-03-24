import os
import json
import re
import time
import requests
import random
import tiktok_module
from requests import *
from datetime import datetime
from config import *

api = f"https://api.telegram.org/bot{token_bot}/"
update_id = 0
last_use = 1

def SendVideo(userid,msgid):
	res = post(f"{api}sendvideo",
    data={"chat_id":userid,
      "caption":"<b>Video skachat qiluvchi</b> @SSTaTaBot!\n\n<b>EN</b> : <i>agar video oq kelsa ssilkani boshqattan junating!</i>\n<b>ID</b> : <i>yordam uchun aloqaga chiqing</i>",
      "parse_mode":"html",
      "reply_to_message_id":msgid,
      "reply_markup":json.dumps(
        {"inline_keyboard":[
          [
            {"text":"Aloqa ^-^",
            "url":"https://t.me/@Mediajon"
            }
          ]
          ]
        }
      )},
    files={"video":open("video.mp4","rb")})

def SendMsg(userid,text,msgid):
	post(f"{api}sendmessage",
    json={
      "chat_id":userid,
      "text":text,
      "parse_mode":"html",
      "reply_to_message_id":msgid
    }
  )

def get_time(tt):
	ttime = datetime.fromtimestamp(tt)
	return f"{ttime.hour}-{ttime.minute}-{ttime.second}-{ttime.day}-{ttime.month}-{ttime.year}"

def Bot(update):
  try:
    global last_use
    userid = update['message']['chat']['id']
    pesan = update['message']['text']
    msgid = update['message']['message_id']
    timee = update['message']['date']
    if update['message']['chat']['type'] != "private":
      SendMsg(userid,"Bu bot faqat shaxsiy rejimda ishlaydi !",msgid)
      return
    first_name = update['message']['chat']['first_name']
    print(f"{get_time(timee)}-> {userid} - {first_name} -> {pesan}")
    if pesan.startswith('/start'):
      SendMsg(userid,"<b>TaTa Fayl Skachat qilishga hush kelibsiz !</b>\n\n<b>Botni qanday ishlataman </b>:\n<i>video ssilkasini ushbu botga junatishingiz yetarli </i>!!\n",msgid)
    elif "tiktok.com" in pesan and "https://" in pesan :
      getvid = tiktok_module.Tiktok().musicallydown(url=pesan)
      if getvid == False:
        SendMsg(userid,"<i>Videoni skachat qilolmadi</i>\n\n<i>Yana harakat qlib kuring</i>",msgid)
        return
      elif getvid == "private/removed":
        SendMsg(userid,"<i>Videoni skachat qilolmadi</i>\n\n<i>Video shaxsiyga berkitilgan ekan</i>",msgid)
      elif getvid == "file size is to large":
        SendMsg(userid,"<i>Videoni skachat qilolmadi</i>\n\n<i>Video hajmi juda ham katta ekan</i>",msgid)
      else:
        SendVideo(userid,msgid)
    elif "/help" in pesan:
      SendMsg(userid,"Botni qanday ishlatsh :\nvideo ssilkasini ushbu botga junatishingiz yetarli !\n\n/donation - for donation bot\n/status - show status bot",msgid)
    elif pesan.startswith("/donation"):
      SendMsg(userid,"Bizn qullab quvvatlang!",msgid)
  except KeyError:
    return
