#! /usr/bin/python
# -*- coding: utf-8 -*-


from django.core.management import setup_environ
from test_pro import settings
setup_environ(settings)

from test_crud.models import *
from test_crud.input import Input

from django.db import transaction
import xlrd

class Create:

	def __init__(self, file_name=None, upload=False):
		self._file_name = file_name
		self._upload = upload

	@transaction.commit_on_success
	def build(self):
		input = Input(self._file_name)
		rows = input.rows()
		'''while True:
			row = rows.next()'''
		for row in rows:
			#if not row: break
			try:
				if self._upload:
					self.add_kwd(row)
				else:
					self.update_kwd(row)
			except Exception,e:
				print e
	
	def add_kwd(self, row):
		exist_obj = None
		try: 
			objs = IMAGE_INTENSIFICATION_BASED_DEVICES.objects.filter(DEVICE_NAME=row['device_name'])
			if len(objs) != 0:
				exist_obj = exp_objs[0]
		except: pass
		if not exist_obj:
			exist_obj = IMAGE_INTENSIFICATION_BASED_DEVICES()
			exist_obj.DEVICE_NAME = row['device_name']
			exist_obj.MGNIFICATION = row['magnification']
			exist_obj.FIELD_OF_VIEW = row['field_of_view']
			exist_obj.RANGE = row['range']
			exist_obj.save()

	def update_kwd(self, row):
		exist_obj = None
		try: 
			objs = IMAGE_INTENSIFICATION_BASED_DEVICES.objects.filter(DEVICE_NAME=row['device_name'])
			if len(objs) != 0:
				exist_obj = exp_objs[0]
		except: pass
		if not exist_obj:
			exist_obj = IMAGE_INTENSIFICATION_BASED_DEVICES()
			exist_obj.DEVICE_NAME = row['device_name']
			exist_obj.MGNIFICATION = row['magnification']
			exist_obj.FIELD_OF_VIEW = row['field_of_view']
			exist_obj.RANGE = row['range']
			exist_obj.save()
		else:
			exist_obj.MGNIFICATION = row['magnification']
			exist_obj.FIELD_OF_VIEW = row['field_of_view']
			exist_obj.RANGE = row['range']
			exist_obj.save()
