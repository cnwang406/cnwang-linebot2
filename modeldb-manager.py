"""
*******************************
to modify postgresql databse

one-time

*******************************
"""



from modeldb import (dbDumpAll, myId,dbUpdateBySQL)
from stock import (getStockName,getXrateNameInit,getXrateName)
from linebot import (LineBotApi, WebhookHandler)



lineToken='WMKL9EQXMJ48ZgHD79wR3FJ800N7fOfYoq2X0OXcn1FOphbxOdKt7r/GYQ7grI+MVx7mB6kh6/6j6P2OxjBlQX6FmLacktBQc1q09r5JyUVCgt2GDK4UyI9nHeRvlDPU8v20xxSoWCiuzGJdwDMj2wdB04t89/1O/w1cDnyilFU='
lineUid='U769b97b52c66fec77eb598a6223f30a3'
channelSecret='f5aa158a43b2f6ee60674dd17a24c5ff'
line_bot_api = LineBotApi(lineToken)

def getUserNameById(UId):
  #if isinstance(event.source, SourceUser) :
  profile = line_bot_api.get_profile(UId)
  replyUserStr = str(profile.display_name) ## +' | '+ str(profile.status_message)
  if replyUserStr=='':      
    replyUserStr='You-Know-Who'
  return replyUserStr


print ('start')
#print (getUserNameById(myId))
getXrateNameInit()
#print (getXrateName('AUD'))
s=dbDumpAll()
count=0
for ss in s:
	ss = list(ss)
	print (ss)
	username=getUserNameById(ss[1])
	print ('user=',username)
	if ss[2]=='c':
		ss[5]=str(getXrateName(ss[3]))
		sqlStr = "UPDATE stocks SET fidtxt ='{xname}', useridtxt='{username}' WHERE ID ='{id}'".format(
				xname=ss[5], username=username, id=ss[0])
		print ('SQL=',sqlStr)
	elif ss[2]=='s':
		ss[5]=str(getStockName(ss[3]))
		sqlStr = "UPDATE stocks SET fidtxt ='{sname}', useridtxt='{username}' WHERE ID ='{id}'".format(
				sname=ss[5], username=username, id=ss[0])
		print ('SQL=',sqlStr)
	if (dbUpdateBySQL(sqlStr)):
		print ('SQL={0} is success updated'.format(sqlStr))
	else :
		print ('SQL={0}, ohoh....something wrong'.format(sqlStr))

