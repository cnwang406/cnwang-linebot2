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
def dbListAllByUser(userId):
	#con = None
	output=[]
	con=dbConn()
	try:
	    cur = con.cursor()
	    cur.execute("SELECT * FROM stocks WHERE userid = '{0}'".format(userId))
	    ver=cur.fetchall()
	    #cur.execute("SELECT * FROM Cars WHERE Id=%s", (uId,))
	    #con.commit()

	except psycopg2.DatabaseError as e:
	    print('=Error %s' % e)
	    sys.exit(1)
	finally:
	    if con:
	        con.close()
	    
	for c in ver:
		output.append(c)
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
"""
addStk= dict(
	userid = 'U769b97b52c66fec77eb598a6223f30a3',
	type = 's',
	fid = '2308',
	criteria ='<120')

chkStk= dict(
	userid = 'U769b97b52c66fec77eb598a6223f30a3',
	fid = '2317'
)

print(dbListAllByUser(myId))
dbAddbyUser(addStk)
print(dbListAllByUser(myId))
"""
