import telebot
import urllib.request
import os
import json
from botData import token

def get_response(url):
	operUrl = urllib.request.urlopen(url)
	if(operUrl.getcode()==200):
		data = operUrl.read()
		jsonData = json.loads(data)
	else:
		print("Error receiving data", operUrl.getcode())
	return jsonData

def get_blob(file_id):
	url = "https://api.telegram.org/bot%s/getFile?file_id=%s" % (token, str(file_id))
	json_file = get_response(url)
	image_path = json_file["result"]["file_path"]
	url = "https://api.telegram.org/file/bot%s/%s" % (token, image_path)
	print("URL:\n", url)
	url = str(url).replace(" ", "+") # just in case, no space in url
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'none', 'Accept-Language': 'en-US,en;q=0.8', 'Connection': 'keep-alive'}
	req = urllib.request.Request(url, headers=hdr)
	try:
		page = urllib.request.urlopen(req)
		return page.read()
	except urllib.request.HTTPError as e:
		print(e.fp.read())
	return ''

# def get_image(url, filename):
# 	url = str(url).replace(" ", "+") # just in case, no space in url
# 	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
# 		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# 		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
# 		'Accept-Encoding': 'none',
# 		'Accept-Language': 'en-US,en;q=0.8',
# 		'Connection': 'keep-alive'}
# 	req = urllib.request.Request(url, headers=hdr)
# 	try:
# 		page = urllib.request.urlopen(req)
# 		with open(filename, 'wb') as f:
# 			f.write(page.read())
# 	except urllib.request.HTTPError as e:
# 		print(e.fp.read())
