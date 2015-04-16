from django.core.management import setup_environ
from test_pro import settings
setup_environ(settings)

from test_crud.models import *
from test_crud.input import Input

from django.db import transaction
import xlrd

import MySQLdb as md

class Delete:

	def __init__(self, file_name=None):
		self._file_name = file_name

	def delete(self):
		try: 
			self._doc = xlrd.open_workbook(self._file_name)
			self._sheet = self._doc.sheet_by_index(0)
		except Exception, e: 
			return 0
			
		try:
			con=md.connect('localhost','test_crud','test_crud','test_crud')
			cur=con.cursor()
			count=0
			for row in xrange(self._sheet.nrows):
				key=str(self._sheet.cell_value(row,0)).strip()
				sql='''DELETE FROM test_crud_image_intensification_based_devices WHERE DEVICE_NAME="%s"	'''%(key)
				cur.execute(sql)
				count+=1
			con.commit()
			cur.close()
			con.close()
			return count
		except Exception,e:
			print e
			pass
		cur.close()
		con.close()
		return 0
