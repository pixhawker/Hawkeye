import urllib2
import urllib
import time
import json
import argparse
import warnings
ap = argparse.ArgumentParser()
ap.add_argument( "--conf", required=True,
    help="path to the JSON configuration file")
args = vars(ap.parse_args())

warnings.filterwarnings("ignore")
conf = json.load(open(args["conf"]))
key=conf["key"]
print key
secret=conf["secret"]
print secret
tokens="b50f514a3a58d800cdf16c4875799282"
tags="kedadiyishuai"
faceset_token="d52a41419f7a39c7db0d1d1ee1009e05"
http_url=' https://api-cn.faceplusplus.com/facepp/v3/faceset/addface'
print http_url
boundary = '----------%s' % hex(int(time.time() * 1000))
data = []
data.append('--%s' % boundary)

data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
data.append(key)
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
data.append(secret)
data.append('--%s' % boundary)
data.append('Content-Disposition: form-data; name="%s"\r\n' % 'faceset_token')
data.append(faceset_token)
data.append('--%s' % boundary)
data.append('Content-Disposition:form-data; name="%s"\r\n' % 'face_tokens')
data.append(tokens)

#data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
#data.append('Content-Type: %s\r\n' % 'application/octet-stream')
#data.append(fr.read())
#fr.close()
data.append('--%s--\r\n' % boundary)

http_body='\r\n'.join(data)
#buld http request

req=urllib2.Request(http_url)
#header
req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
req.add_data(http_body)
print req
try:
	#req.add_header('Referer','http://remotserver.com/')
	#post data to server
	resp = urllib2.urlopen(req, timeout=5)
	#get response
	qrcont=resp.read()
	print qrcont

except urllib2.HTTPError as e:
    print e.read()
