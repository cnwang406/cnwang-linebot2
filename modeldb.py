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
def dbListAllByUser(userId, stype):
	#con = None
	output=[]
	con=dbConn()
	if (stype) :
		sqlStr = "SELECT id, type, fid, criteria FROM stocks WHERE (userid = '{0}' AND type='{1}')".format(userId, stype)

	else:
		sqlStr = "SELECT id, type, fid, criteria FROM stocks WHERE userid = '{0}'".format(userId)
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
	if (stype) :
		sqlStr = "SELECT id, type, fid, criteria FROM stocks WHERE (userid = '{0}' AND type='{1}')".format(userId, stype)

	else:
		sqlStr = "SELECT id, type, fid, criteria FROM stocks WHERE userid = '{0}'".format(userId)
	try:
	    cur = con.cursor()
	    cur.execute( "SELECT id, type, fid, criteria FROM stocks WHERE (userid = '{0}' AND type='c')".format(userId))
	    curr=cur.fetchall()
	    cur.execute( "SELECT id, type, fid, criteria FROM stocks WHERE (userid = '{0}' AND type='s')".format(userId))
	    stkr=cur.fetchall()
	except psycopg2.DatabaseError as e:
	    print('=Error %s' % e)
	    sys.exit(1)
	finally:
	    if con:
	    	con.close()
	

	#currency = [['USD','--','--'],['AUD','--','--'],['CNY','--','--'],['JPY','--','--']]

	#stock = [[u'中美晶','5483','???','???','???','*','991111'],
	tmpCur=['','','']
	tmpStk=['','','','','','','']
	for c in curr:
		tmpCur[0] = c[2]
		output.append(list(tmpCur))

	for s in stkr:
		tmpStk[1]=s[2]
		output.append(list(tmpStk))
	print ('dbListAllByUserForJSON({0}'.format(userId))
	print (output)
	return output


def dbAddbyUser(param):
	#print (param['userid'])
	con=dbConn()
	sqlStr = "INSERT INTO stocks (userid, type, fid, criteria) VALUES ('{0}', '{1}', '{2}', '{3}')".format(
				param['userid'], param['type'], param['fid'], param['criteria'])
	print ('Sql = ', sqlStr)
	ck=dbCheckExist(param)

	if (not ck) :
		print ('execute')
		
	else :
		print ('exist, update, update criteria from {0} to {1}'.format(ck[4],param['criteria']))
		sqlStr = "UPDATE stocks SET criteria='{0}' WHERE ID ='{1}'".format(param['criteria'],ck[0])
		print ('sqlstr = ',sqlStr)
	try:
		cur = con.cursor()
		cur.execute(sqlStr)
		con.commit()
	except psycopg2.DatabaseError as e:
		con.rollback()
	finally:
		if con:
			con.close()
		print ('done')


def dbCheckExist(param):
	sqlStr = "SELECT * FROM stocks WHERE userid='{0}' and fid='{1}'".format(param['userid'],param['fid'])
	con=dbConn()
	cur = con.cursor()
	cur.execute(sqlStr)
	ver=cur.fetchone()
	con.close() 

	return ver
	

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

