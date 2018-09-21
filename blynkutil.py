import urllib.request
import urllib.parse
import json
import pandas as pd
import gzip



#blynkServer='lugia.synology.me:8080'
#auth='c3ab4ab0345d4d81934600ed4ac1dadc'


def blynkGetPinValue(blynkServer, auth, pin):

	requestStr='http://'+blynkServer+'/'+auth+'/get/'+pin

	js=urllib.request.urlopen(requestStr).read()
	value=json.loads(js)[0]
	return value



def blynkGetPinHistoryValue(blynkServer, auth,pin,name):
	
	requestStr = 'http://'+blynkServer+'/'+auth+'/data/'+pin
	colName=[name,'timestamp','0']
	#print ('request=(\''+requestStr+')\'')
	#import urllib.request

	s = urllib.request.urlopen(requestStr).read()
	
	df=pd.Series(gzip.decompress(s).decode("utf-8").split('\n'))
	df=df.str.split(',', expand=True)
	df.columns = colName
	
	#print (df.dtypes)

	df[colName[0]]=pd.to_numeric(df[colName[0]])
	df[colName[1]]=pd.to_numeric(df[colName[1]])
	df=df.drop(columns=['0'])
	
	return df
