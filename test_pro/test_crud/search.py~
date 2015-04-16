#! /usr/bin/python
# -*- coding: utf-8 -*-


from django.core.management import setup_environ
from test_pro import settings
setup_environ(settings)

import MySQLdb as md

def search_db(text):
	con=md.connect('localhost','test_crud','test_crud','test_crud')
	cur=con.cursor()
	sql='''
		SELECT * FROM test_crud_image_intensification_based_devices WHERE DEVICE_NAME="%s"
	'''%(text)
	cur.execute(sql)
	rows=cur.fetchall()
	con.commit()
	cur.close()
	con.close()
	results=[]
	result={}
	for row in rows:
		result['DEVICE_NAME']=row[0]
		result['MGNIFICATION']=row[1]
		result['FIELD_OF_VIEW']=float(row[2])
		result['RANGE']=row[3]
		results.append(result)
	return results
