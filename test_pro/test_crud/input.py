#! /usr/bin/python
# -*=- coding: utf-8 -*-
from django.db import transaction
from models import *

import xlrd
import re


class Input:
	
	def __init__(self, file_name=None, upload=False):
		self._file_name = file_name
		self._doc = None
		self._sheet = None
		self._upload = upload
	def rows(self):
		try: 
			self._doc = xlrd.open_workbook(self._file_name)
			self._sheet = self._doc.sheet_by_index(0)
		except Exception, e: 
			#print 'exception : %s', (e,)
			yield None
			
		for row in xrange(2,self._sheet.nrows):
			final_row = {'device_name': None, 'magnification': None, 'field_of_view': None, 'range': None}
			try: 
				final_row['device_name'] = str(self._sheet.cell_value(row,0)).strip()
				final_row['magnification'] = str(self._sheet.cell_value(row,1)).strip()
				final_row['field_of_view'] = str(self._sheet.cell_value(row,2)).strip()
				final_row['range'] = str(self._sheet.cell_value(row,3)).strip()
				yield final_row
			except Exception, e:
				yield None
