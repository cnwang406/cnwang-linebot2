# -*- coding: UTF-8 -*-
import pandas
from urllib import request
import ssl
import twstock
import time

currency=None
currencyTimestamp=None
def getStockName(stockId):
	s=twstock.realtime.get(stockId)
	if (s['success']) :
		return str(s['info']['name'])
	else:
		return None
def getXrateInit():

	global currency
	url='https://rate.bot.com.tw/xrt?Lang=zh-TW'
	context = ssl._create_unverified_context()
	response = request.urlopen(url, context=context)
	html = response.read()

	dfs = pandas.read_html(html)
	#print (dfs[:10])
	currency = dfs[0]
	currency = currency.iloc[:,0:5]
	currency.columns = [u'幣別',u'現金匯率-本行買入',u'現金匯率-本行賣出',u'即期匯率-本行買入',u'即期匯率-本行賣出']
	currency[u'幣別txt'] = currency[u'幣別'].str.extract('(\w+)')
	currency[u'幣別'] = currency[u'幣別'].str.extract('\((\w+)\)')
	currencyTimestamp=time.time()
	print (currency)

def checkCurrencyUpdated():
	if not currency:	#not initilized
		getXrateInit()
	else :				# need to check timestampe
		if (time.time()-currencyTimestamp)>600: 	# 10 min update
			getXrateNameInit()

def getXrateName(XrateId):
	checkCurrencyUpdated()
	d=currency.loc[currency[u'幣別']==XrateId]
	if (len(d)):
		return d.iloc[0,5]
	else:	# no such symbol
		return '---'

def getXrate(xrate):
	checkCurrencyUpdated()
	"""
	url='https://rate.bot.com.tw/xrt?Lang=zh-TW'
	context = ssl._create_unverified_context()
	response = request.urlopen(url, context=context)
	html = response.read()

	dfs = pandas.read_html(html)
	#print (dfs[:10])
	currency = dfs[0]
	currency = currency.ix[:,0:5]
	currency.columns = [u'幣別',u'現金匯率-本行買入',u'現金匯率-本行賣出',u'即期匯率-本行買入',u'即期匯率-本行賣出','幣別txt']
	currency[u'幣別'] = currency[u'幣別'].str.extract('\((\w+)\)')
	"""

	#['JPY', '0.2599', '0.2727', 'sell', '*']
	for xd in xrate[0]:
		d=(currency.loc[currency[u'幣別']==xd[0]])
		if (len(d)):
			xd[1]=d.iloc[0,5]
			xd[2]=d.iloc[0,1]
			xd[3]=d.iloc[0,2]
		else:	# no such symbol
			xd[1]='---'
			xd[2]='---'
			xd[3]='---'
			xd[4]='---'


def getXrateById(xrateId):
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

	d=(currency.loc[currency[u'幣別']==xrateId])
	if (len(d)):
		output =d.iloc[0,1]

	else:	# no such symbol
		output='---'
	return output


	#currency = [['USD','美金', --','--','criteria'],['AUD','--','--','criteria'],['CNY','--','--','criteria'],['JPY','--','--','criteria']]

	#stock = [[u'中美晶','5483','成交','漲跌','漲跌幅','*','991111'],

def getStockById(stockId):

	s = twstock.realtime.get(stockId)
	if (s['success']):
		output = s['realtime']['latest_trade_price']
	else:
		output = '---'
	return output	

	
def getStock(par):
	lCurrency = par[0]
	lStock=par[1]

	for ls in lStock:
		print ('getting ',ls[1])
		s = twstock.realtime.get(ls[1])
		if (s['success']):
			output = '{0} ({1}) close price is {2} ('.format(ls[1],s['info']['name'],s['realtime']['latest_trade_price'])

			dif=round(float(s['realtime']['latest_trade_price']) - float(s['realtime']['open']),2)
			ls[0]=str(s['info']['name'])
			ls[3]=str(dif)
			ls[4]=str(round(float(ls[3])/float(s['realtime']['open'])*100,1))+'%'

			if (ls[5]=='') : ls[5]=str('**') 

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

			if (ls[5]=='') : ls[5]=str('**') 
			



	print ('-'*20)

def getPrice(par):
	getXrate(par)
	getStock(par)	
	print (par)
