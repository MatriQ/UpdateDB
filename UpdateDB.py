#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-08-06 17:05:21
# @Author  : Matri (matrixdom@126.com)
# @Link    : https://github.com/MatriQ
# @Version : 0.1

import os
import socket
import MySQLdb
import threading
import time
from time import ctime,sleep

checkTime=5

hostURL='x.xsprite.net'
dbhost='localhost'
dbuesr='root'
dbpass=''

mysqlUser='root'

updateSQL='update mysql.user set Host="%s" where User="%s" and Host="%s"'
getlastHostSQL='select Host from mysql.user where Host like "222.%" limit 1'


class DB(object):
	conn=None
	"""docstring for DB"""
	def __init__(self, host,user,passwd,db="mysql",port=3306):
		super(DB, self).__init__()
		self.host=host
		self.user=user
		self.passwd=passwd
		self.db=db
		self.port=port
	def open(self,db=None):
		try:
			self.conn=MySQLdb.connect(host=self.host,
									user=self.user,
									passwd=self.passwd,
									db=db if db else self.db,
									port=self.port)
		except Exception, e:
			print("open database %s:%s error " % (self.host,db if db else self.db))
		
	def close(self):	
		if self.conn:
			self.conn.close()
	
	def getConn(self):
		return self.conn


def db_selectone(db,strSql):
	result=None
	cur=None

	db.open()
	try:
		#conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='mysql',port=3306)
		#print(dir(conn))
		cur=db.getConn().cursor()
		cur.execute(getlastHostSQL)
		data = cur.fetchone()
		if len(data)>0 :
			result= data[0]

		cur.close()
	except Exception, e:
		print("get all user from db error")
	finally:
		db.close()
	return result

def db_select(db,strSql):
	result=None
	cur=None
	db.open()
	try:
		#conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='mysql',port=3306)
		#print(dir(conn))
		cur=db.getConn().cursor()
		cur.execute(getlastHostSQL)
		result = cur.fetchall()
		cur.close()
	except Exception, e:
		print("get all user from db error")
	finally:
		db.close()
	return result

def db_exec(db,strSql):
	result=None
	cur=None
	db.open()
	try:
		#conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='mysql',port=3306)
		#print(dir(conn))
		cur=db.getConn().cursor()
		cur.execute(strSql)
		cur.close()
	except Exception, e:
		print("get all user from db error")
	finally:
		db.close()
	return result

	

def getHostByURL(url):  
	ip = socket.gethostbyname(url)  
	return ip  

def getlastIp(db):
	user=db_selectone(db,'select Host from mysql.user where Host like "222.%"')
	return user

def updateHost():
	db=DB(dbhost,dbuesr,dbpass)

	ip=getHostByURL(hostURL)
	#print ip
	lastIp=getlastIp(db)
	#print lastIp
	if lastIp != ip:
		db_exec(db,updateSQL%(ip,mysqlUser,lastIp))
		print("Updated host")
		restartMysql()

def restartMysql():
	ret=os.system('service mysqld restart')
	print("restart mysql return %d" % ret)

def checkHost():
	keepRun=True
	while keepRun:
		print("check host")
		time.sleep(checkTime)
		updateHost()

def main():
	print("start check host")
	t=threading.Thread(target=checkHost)
	t.setDaemon(True)
	t.start()
	try:
		while 1:
			alive = False
			alive = alive or t.isAlive()
			if not alive:
				t.close()
				break
	finally:
		pass

	#keeprun=True
	#while keeprun:
	#	cmd = input("input exit to exit:\n")
	#	if cmd=='exit':
	#		keeprun=False]]]
	print("stop check host")

if __name__ == '__main__':
	try:
		main()
	finally:
		print("process closed")
	
