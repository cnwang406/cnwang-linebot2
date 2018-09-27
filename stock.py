# -*- coding: UTF-8 -*-
import pandas
from urllib import request
import ssl
import twstock
	
def getXrate(xrate):
	url='https://rate.bot.com.tw/xrt?Lang=zh-TW'
	context = ssl._create_unverified_context()
	response = request.urlopen(url, context=context)
	html = response.read()

	dfs = pandas.read_html(html)
	#print (dfs[:10])
	currency = dfs[0]
	currency = currency.ix[:,0:5]
	currency.columns = [u'幣別',u'現金匯率-本行買入',u'現金匯率-本行賣出',u'即期匯率-本行買入',u'即期匯率-本行賣出']
	currency[u'幣別'] = currency[u'幣別'].str.extract('\((\w+)\)')
	for xd in xrate[0]:
		d=(currency.loc[currency[u'幣別']==xd[0]])
		if (len(d)):
			xd[1]=d.iloc[0,1]
			xd[2]=d.iloc[0,2]
		else:	# no such symbol
			xd[1]='---'
			xd[2]='---'

def getStock(par):
	lCurrency = par[0]
	lStock=par[1]

	for ls in lStock:
		print ('getting ',ls[1])
		s = twstock.realtime.get(ls[1])
		if (s['Success']):
			output = '{0} ({1}) close price is {2} ('.format(ls[1],s['info']['name'],s['realtime']['latest_trade_price'])

			dif=round(float(s['realtime']['latest_trade_price']) - float(s['realtime']['open']),2)
			ls[0]=str(s['info']['name'])
			ls[3]=str(dif)
			ls[4]=str(round(float(ls[3])/float(s['realtime']['open'])*100,1))+'%'
			if dif>0:
				ls[6]='aa0000'
			elif dif==0:
				ls[6]='111111'
			else:
				ls[6]='00aa00'
			output += ' diff {0} ({1})'.format(ls[3],ls[4])	
			print (output)
			ls[2]=s['realtime']['latest_trade_price'][:6]
		else:
			utput = '{0} ({1}) not found, check again'
			ls[0]='####'
			ls[3]='---'
			ls[4]='-- %'
			ls[6]='010101'
			output += ' diff {0} ({1})'.format(ls[3],ls[4])	
			print (output)
			ls[2]='----'
	print ('-'*20)

def getPrice(par):
	getXrate(par)
	getStock(par)	