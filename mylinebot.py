# -*- coding: UTF-8 -*-

TITLE=(
"""
***************************************************
**                                               **
**      Line Bot  V0.26                          **
**                cnwang. 2018/09                **
***************************************************

"""
)  


import json
from flask import Flask,  abort
from flask import request as frequest
#from defJSON import fitFlex2,Par2String

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton)
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
#from lineutil import generateStockJSON,getHomeTemps, sendHOME
from lineUtil import (getHomeTemps,generateStockJSON,generateHomeJSON,generateStockByUser)
from stock import getPrice

import datetime
import time
import os
import pandas as pd
import ssl
import twstock

import urllib.request
import urllib.parse
from urllib import request
import gzip

from modeldb import dbListAllByUser



app = Flask(__name__)

#db.init_app(app)


startTime=time.time()
print(TITLE)

#main start here
lineToken='WMKL9EQXMJ48ZgHD79wR3FJ800N7fOfYoq2X0OXcn1FOphbxOdKt7r/GYQ7grI+MVx7mB6kh6/6j6P2OxjBlQX6FmLacktBQc1q09r5JyUVCgt2GDK4UyI9nHeRvlDPU8v20xxSoWCiuzGJdwDMj2wdB04t89/1O/w1cDnyilFU='
lineUid='U769b97b52c66fec77eb598a6223f30a3'
channelSecret='f5aa158a43b2f6ee60674dd17a24c5ff'
line_bot_api = LineBotApi(lineToken)
handler = WebhookHandler(channelSecret)


blynkServer='lugia.synology.me:8080'
blynkAuth='c3ab4ab0345d4d81934600ed4ac1dadc'


currency = [['USD','--','--'],['AUD','--','--'],['CNY','--','--'],['JPY','--','--']]

stock = [[u'中美晶','5483','???','???','???','*','991111'],
		['UMC','2303','???','???','???','>20','119911'],
		['TSMC','2330','???','???','???','<200','991111'],
		['大力光','3008','???','???','???','*','119911'],
    ['鴻海','2317','???','???','???','*','119911']]

par = [currency,stock]


#simpleStr= Par2String(par)
#t=fitFlex2('0','0','0','0','0')
#print (t)

stockHeader = u'匯率股票訊息'
stockTitle = u' 問的'
stockAddress = 'cnwang406@gmail.com'
#pDate=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def processStock(event, username):
  startTime=time.time()
  par = dbListAllByUser(event.source.user_id,'c')
  par.append(dbListAllByUser(event.source.user_id,'s'))
  print (par)
  getPrice(par)
  if str(event.reply_token)=='00000000000000000000000000000000' :
    line_bot_api.push_message(lineUid, FlexSendMessage('Stock message is here', json.loads(generateStockJSON(stockHeader,u'小汪汪'+stockTitle,stockAddress,par,startTime))))
  else:
    line_bot_api.reply_message(event.reply_token, FlexSendMessage('Stock message is here', json.loads(generateStockJSON(stockHeader,getUserName(event)+stockTitle,stockAddress,par,startTime))))

def processStatus(event):
  startTime=time.time()
  if event.reply_token=='00000000000000000000000000000000':
    line_bot_api.push_message(lineUid, FlexSendMessage('home temperature is here', json.loads(getHomeTemps(blynkServer, blynkAuth,startTime))))
  else:
    line_bot_api.reply_message(event.reply_token, FlexSendMessage('home temperature is here', json.loads(getHomeTemps(blynkServer, blynkAuth,startTime))))

def processHOME1():
    line_bot_api.push_message(lineUid, FlexSendMessage('welcome',json.loads(generateHomeJSON())))

def processHOME(event):

  if event.reply_token=='00000000000000000000000000000000':
    line_bot_api.push_message(lineUid, FlexSendMessage('welcome',json.loads(generateHomeJSON())))
  else:
    line_bot_api.reply_message(event.reply_token, FlexSendMessage('welcome',json.loads(generateHomeJSON())))

def processStockList(event):
#generateStockByUser(uid, userName, startTime)
  startTime=time.time()
  line_bot_api.reply_message(event.reply_token, FlexSendMessage('Stock message is here', json.loads(generateStockByUser(event.source.user_id, getUserName(event), startTime))))


def getUserName(event):
  if isinstance(event.source, SourceUser) :
      profile = line_bot_api.get_profile(event.source.user_id)
      replyUserStr = str(profile.display_name) ## +' | '+ str(profile.status_message)
        
  else:
    replyUserStr='You-Know-Who'
  return replyUserStr



welcomeStr="""
***********************
  小汪汪	          
************* V0.26 ***

"""
line_bot_api.push_message(lineUid, TextSendMessage(welcomeStr))

#processStatus()
#processStock()
processHOME1()

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST']) # Use postback/message will call this.
def callback():
	# get X-Line-Signature header value
	#print (request)
  print ('*'*40)
  signature = frequest.headers['X-Line-Signature']


	# get request body as text
  body = frequest.get_data(as_text=True)

  app.logger.info("Request body: " + body) 
  print ('body=',body)
	#keyword = body.events.postback.data
  
	#print (event.message.text)
	# handle webhook body
  try:
    print ('start to call handler.handle({0}, {1})'.format(body,signature))
    handler.handle(body, signature)
    print ('exit from hand.handle')
  except InvalidSignatureError:
    abort(400)
    print ('abort 400')

  return 'OK'


@handler.add(MessageEvent, message=TextMessage)  # message will call this. 
def handle_message(event):
  print ('-'*30)  
  print('into handle_message')
  print ('event =',event)
  print('reply token={0} \n, text={1}'.format(event.reply_token, event.message.text))
   #  line_bot_api.push_message(uid, TextSendMessage(text=event.message.text))


  keyword=event.message.text.upper()
  replyUserStr=getUserName(event)
#  if isinstance(event.source, SourceUser) :
#    profile = line_bot_api.get_profile(event.source.user_id)
#    replyUserStr = str(profile.display_name) ## +' | '+ str(profile.status_message)      
#  else:
#    replyUserStr='You-Know-Who'

  print ('user name is ',replyUserStr)  
  print ('now, keyword=',keyword)
  if keyword==u'FINANCE' or keyword==u'STOCK':
    processStock(event, replyUserStr)
  elif keyword==u'TEMP' or keyword ==u'STATUS':
    processStatus(event)
  elif keyword==u'MENU' or keyword == u'SCHEDULE':
    processHOME(event)
    #line_bot_api.reply_message(, FlexSendMessage('test',json.loads(sendHOME())))
  elif keyword == 'PROFILE':
    if isinstance(event.source, SourceUser) :
      profile = line_bot_api.get_profile(event.source.user_id)
      profileStr = str(profile.display_name)+' | '+ str(profile.status_message)
      line_bot_api.reply_message( event.reply_token,
        TextSendMessage(text=profileStr))
    else:
        line_bot_api.reply_message(
          event.reply_token,
          TextSendMessage(text='LBA cannot retreive user profile without user_id'))
  elif keyword == 'LIST':
        processStockList(event)
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text=txt))


  else:
    print ('no key word found. and in else, event.message.text = ',event.message.text)
    print ('call line_bot_api.reply_message('+event.reply_token)
    if (event.reply_token=='00000000000000000000000000000000'):   # from line
      line_bot_api.push_message(lineUid, TextSendMessage(text=event.message.text))   
    else :
    
      line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))
    #line_bot_api.push_message(uid, TextSendMessage(text=keyword))   
# 

if __name__ == "__main__":
  app.config['DEBUG'] = True
  port = int(os.environ.get('PORT', 5000))
  app.run(host='0.0.0.0', port=port)