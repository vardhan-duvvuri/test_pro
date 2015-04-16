#! /usr/bin/python
# -*=- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.template import Context, loader
from django.db import transaction
from django.db import connection
import datetime
import os


from models import *

from test_crud.store import Create
from test_crud.delete import Delete
from test_crud.search import search_db
import re
from django.views.decorators.csrf import csrf_exempt
MIMETYPE = 'application/javascript; charset=utf-8'

# Helper method
def _getResponse(data):
	return HttpResponse(simplejson.dumps(data, ensure_ascii=False).replace('\\"','"'), MIMETYPE)

def _getUploadedFilePath(req):
	f = req.FILES.get('file', None)
	if f == None:
		return None
	
	if hasattr(f, 'temporary_file_path'):
		return f.temporary_file_path

	dt = datetime.datetime.today()	
	tmp_file = '/tmp/%s-%d' %(dt.strftime('%s'), dt.microsecond)	
	dest = open(tmp_file, 'wb+')
	for chunk in f.chunks():
		dest.write(chunk)
	dest.close()
	return tmp_file			

@csrf_exempt
def upload(req, fileType):
	resp_data = {'s': 0}
	if fileType.lower() != 'xls':
		resp_data['e'] = 'only file type allowed is : xls'
		return _getResponse(resp_data) 

	filePath = _getUploadedFilePath(req)
	if filePath == None:
		resp_data['e'] = 'No file is uploaded!!!'
		return _getResponse(resp_data)
	cr = Create(filePath, True)
	cr.build()
	
	'''remove temp file'''
	os.unlink(filePath)

	resp_data['s'] = 1
	return _getResponse(resp_data)

@csrf_exempt
def update(req, fileType):
	resp_data = {'s': 0}
	if fileType.lower() != 'xls':
		resp_data['e'] = 'only file type allowed is : xls'
		return _getResponse(resp_data) 

	filePath = _getUploadedFilePath(req)
	if filePath == None:
		resp_data['e'] = 'No file is uploaded!!!'
		return _getResponse(resp_data)
	cr = Create(filePath, False)
	cr.build()
	
	'''remove temp file'''
	os.unlink(filePath)

	resp_data['s'] = 1
	return _getResponse(resp_data)

@csrf_exempt
def delete(req, fileType):
	resp_data = {'s': 0}
	if fileType.lower() != 'xls':
		resp_data['e'] = 'only file type allowed is : xls'
		return _getResponse(resp_data) 

	filePath = _getUploadedFilePath(req)
	if filePath == None:
		resp_data['e'] = 'No file is uploaded!!!'
		return _getResponse(resp_data)
	dl = Delete(filePath)
	count=dl.delete()
	'''remove temp file'''
	os.unlink(filePath)
	if count==0:
		resp_data['e'] = "Something Error Happened"
	else:
		resp_data['s'] = 1
		resp_data['count'] = "No.of rows deleted : "+str(count)
	return _getResponse(resp_data)

@csrf_exempt
def search(req):
	resp_data={}
	if not req.POST.has_key('text'):
		resp_data['s']=0
		resp_data['e'] = 'Key to be searched for is not found !!!'
		return _getResponse(resp_data)
	
	text = req.POST.get('text')
	#resp_data['s']=1
	resp = search_db(text)
	if resp:
		resp_data=resp[0]
	else:
		resp_data['s']=0
		resp_data['e'] = 'Key was not found in DB !!!'
	return _getResponse(resp_data)
@csrf_exempt
def dashboard(req):
	html = '''
		<html>
			<head>
				<title>Test Interface</title>
				<script type="text/javascript" src="/static/jquery-1.7.2.min.js"></script>
				<script type="text/javascript">
					$(document).ready(function(){
						$('#upload_form_btn').click(function(e){
							e.preventDefault();
							var targetUrl = "../upload/xls/";
							$("#upload_form").attr("action", targetUrl);
							$("#upload_form").submit();	
						});
						$('#update_form_btn').click(function(e){
							e.preventDefault();
							var targetUrl = "../update/xls/";
							$("#update_form").attr("action", targetUrl);
							$("#update_form").submit();	
						});
						$('#search_form_btn').click(function(e){
							e.preventDefault();
							var targetUrl = "../search/";
							$("#search_form").attr("action", targetUrl);
							$("#search_form").submit();	
						});
						$('#delete_form_btn').click(function(e){
							e.preventDefault();
							var targetUrl = "../delete/xls/";
							$("#delete_form").attr("action", targetUrl);
							$("#delete_form").submit();	
						});
					});
			
				</script>
			</head>
			<body>
				<form id="upload_form" enctype="multipart/form-data" method="post">
					<label>Choose file to upload...</label>
					<input type="file" size="40" name="file">
					<input type="submit" value="Upload" id="upload_form_btn">
				</form>
				<form id="update_form" enctype="multipart/form-data" method="post">
					<label>Choose file to update...</label>
					<input type="file" size="40" name="file">
					<input type="submit" value="Update" id="update_form_btn">
				</form>
				<form method="post" id="search_form">
					<label>Search...&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>
					<input type="text" name="text"/>
					<input type="submit" id="search_form_btn">
				</form>
				<form id="delete_form" enctype="multipart/form-data" method="post">
					<label>Choose file having rows to delete...</label>
					<input type="file" size="40" name="file">
					<input type="submit" value="Delete" id="delete_form_btn">
				</form>
			</body>
		</html>
	'''		
	return HttpResponse(html)	

