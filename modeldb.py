# -*- coding: utf-8 -*-
import psycopg2
import sys

con=None
def dbConn():
	con = psycopg2.connect(database='dbqd8ec5asbl2',user='ncgbtvdegevxoc',
	    					 password='b9f43bc8591aeff58c8a715b619a90ae2530958368391b3b71020ddbd7c26d02',
	    					 host = 'ec2-54-83-50-145.compute-1.amazonaws.com'
	    					 )
	return con
myId = 'U769b97b52c66fec77eb598a6223f30a3'	    
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ncgbtvdegevxoc:b9f43bc8591aeff58c8a715b619a90ae2530958368391b3b71020ddbd7c26d02@ec2-54-83-50-145.compute-1.amazonaws.com:5432/dbqd8ec5asbl2'
def dbDumpAll():
	output=[]
	con=dbConn()
	sqlStr="SELECT * FROM stocks"
	
	try:
	    cur = con.cursor()
	    cur.execute(sqlStr)
	    rows=cur.fetchall()
	except psycopg2.DatabaseError as e:
	    print('=Error %s' % e)
	    sys.exit(1)
	finally:
	    if con:
	        con.close()
	
	for row in rows:
		output.append(row)
	return rows



def dbListAllByUser(userId, stype):
	#con = None
	output=[]
	con=dbConn()
	if (stype) :
		sqlStr = "SELECT id, type, fid, fidtxt, criteria FROM stocks WHERE (userid = '{0}' AND type='{1}')".format(userId, stype)

	else:
		sqlStr = "SELECT id, type, fid, fidtxt, criteria FROM stocks WHERE userid = '{0}'".format(userId)
	try:
	    cur = con.cursor()
	    cur.execute(sqlStr)
	    ver=cur.fetchall()
	except psycopg2.DatabaseError as e:
	    print('=Error %s' % e)
	    sys.exit(1)
	finally:
	    if con:
	        con.close()
	    
	for c in ver:
		output.append(list(c))
	return output

def dbListAllByUserForJSON(userId):
	output=[]
	con=dbConn()

	try:
	    cur = con.cursor()
	    cur.execute( "SELECT id, type, fid, fidtxt, criteria FROM stocks WHERE (userid = '{0}' AND type='c')".format(userId))
	    curr=cur.fetchall()
	    cur.execute( "SELECT id, type, fid, fidtxt, criteria FROM stocks WHERE (userid = '{0}' AND type='s')".format(userId))
	    stkr=cur.fetchall()
	except psycopg2.DatabaseError as e:
	    print('=Error %s' % e)
	    sys.exit(1)
	finally:
	    if con:
	    	con.close()
	

	#currency = [['USD','美金', --','--','criteria'],['AUD','--','--','criteria'],['CNY','--','--','criteria'],['JPY','--','--','criteria']]

	#stock = [[u'中美晶','5483','???','???','???','*','991111'],
	tmpCur=['USD','美金','buy','sell','criteria']
	tmpStk=['中美晶','5483','成交','漲跌','漲跌百分比','criteria','color']
	tmpCurL=[]
	tmpStkL=[]
	for c in curr:
		tmpCur[0] = c[2]
		tmpCur[4] = c[4]
		tmpCur[1]=c[3]
		if tmpCur[4]=='' : tmpCur[4]='*'
		tmpCurL.append(list(tmpCur))

	for s in stkr:
		tmpStk[1]=s[2]
		tmpStk[5]=s[4]
		if tmpStk[5]=='' : tmpStk[5]='*'
		tmpStkL.append(list(tmpStk))
	output = [tmpCurL, tmpStkL]
	print ('dbListAllByUserForJSON({0}'.format(userId))
	print (output)
	return output


def dbAddByUser(param):
	#print (param['userid'])
	con=dbConn()
	ck=dbCheckExist(param)
	
	if (not ck) :
		sqlStr = "INSERT INTO stocks (userid, type, fid, fidtxt, criteria) VALUES ('{userid}', '{type}', '{fid}', '{fidtxt}','{criteria}')".format(
				userid=param['userid'], type=param['type'], fid=param['fid'], fidtxt=param['fidtxt'],
				criteria=param['criteria'])
	else :
		print ('exist, update, update criteria from {0} to {1}'.format(ck[4],param['criteria']))
		sqlStr = "UPDATE stocks SET criteria='{0}' WHERE ID ='{1}'".format(param['criteria'],ck[0])

	print ('calling dbUpdateBySQL({0})'.format(sqlStr))
	dbUpdateBySQL(sqlStr)
	print ('------ done')
	print(dbDumpAll())

def dbRemoveByUser(param):
	con=dbConn
	sqlStr="DELETE FROM stocks WHERE userid='{userid}' AND id='{id}'".format(
		userid=param['userid'],
		id=param['id'])
	print ('calling dbUpdateBySQL({0})'.format(sqlStr))
	dbUpdateBySQL(sqlStr)
	print ('------ done')
	print(dbDumpAll())

def dbUpdateBySQL(sqlStr):
	con=dbConn()
	success=True
	try:
		cur = con.cursor()
		cur.execute(sqlStr)
		con.commit()
	except psycopg2.DatabaseError as e:
		con.rollback()
		success=False	
	finally:
		if con:
			con.close()
		print ('modeldb: dbUpdateBySQL : done')
	return success


def dbCheckExist(param):
	sqlStr = "SELECT * FROM stocks WHERE userid='{0}' and fid='{1}'".format(param['userid'],param['fid'])
	con=dbConn()
	cur = con.cursor()
	cur.execute(sqlStr)
	ver=cur.fetchone()
	print (ver)
	con.close() 
	if ver :
		return None
	else:
		return ver[0]

	

#print (dbListAllByUser('U769b97b52c66fec77eb598a6223f30a3'))

addStk= dict(
	userid = 'U769b97b52c66fec77eb598a6223f30a3',
	type = 's',
	fid = '2308',
	criteria ='<120')

chkStk= dict(
	userid = 'U769b97b52c66fec77eb598a6223f30a3',
	fid = '2317'
)

#print(dbListAllByUser(myId))
#print(dbListAllByUser(myId, ''))
#print(dbListAllByUser(myId))

