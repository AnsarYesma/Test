import telebot
import urllib
import os
import json

def get_response(url):
	operUrl = urllib.request.urlopen(url)
	if(operUrl.getcode()==200):
		data = operUrl.read()
		jsonData = json.loads(data)
	else:
		print("Error receiving data", operUrl.getcode())
	return jsonData

def get_blob(file_id):
    url = "https://api.telegram.org/bot%s/getFile?file_id=%s" % (token, id)
	json_file = get_response(url)
	image_path = json_file["result"]["file_path"]
	url = "https://api.telegram.org/file/bot%s/%s" % (token, image_path)
    filename = "%s.jpg" % file_id
	urllib.request.urlretrieve(url, filename)
    with open(filename, 'rb') as file:
        blob_data = file.read()
	os.remove(filename)
    return blob_data
