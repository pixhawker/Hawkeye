# -*- coding: utf-8 -*-
import urllib2
import urllib
import time
import json
import re
def search():
	http_url='https://api-cn.faceplusplus.com/facepp/v3/search'
	key = "ONam7gChKzvXg4zql5Y8sP82okBKYqlG"
	secret = "F3IFAcb2iGkI4ZmYefGffwPB-9BZUgYD"
	filepath = r"/home/pi/Pictures/shareall/face.jpg"
	faceset="d52a41419f7a39c7db0d1d1ee1009e05"
	return_result_count="1"
	boundary = '----------%s' % hex(int(time.time() * 1000))
	data = []
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
	data.append(key)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
	data.append(secret)
	data.append('--%s' % boundary)
	fr=open(filepath,'rb')
	data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
	data.append('Content-Type: %s\r\n' % 'application/octet-stream')
	data.append(fr.read())
	fr.close()
	data.append('--%s' % boundary)

	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'faceset_token')
	data.append(faceset)
	data.append('--%s' % boundary)
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_result_count')
	data.append(return_result_count)

	data.append('--%s--\r\n' % boundary)

	http_body='\r\n'.join(data)
	#buld http request
	req=urllib2.Request(http_url)
	#header
	req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)
	req.add_data(http_body)
	try:
	#req.add_header('Referer','http://remotserver.com/')
	#post data to server
		resp = urllib2.urlopen(req, timeout=5)
	#get response
		qrcont=resp.read()
		qrcont_dict=json.loads(qrcont)
                qrcont_str=str(qrcont_dict)
               # print qrcont_str,type(qrcont_str)
                l=re.split("u'confidence': ",qrcont_str)
                
                ll=l[1]
                lll=str(ll)
                llll=re.split(", u'user_id':",lll)
               # print lll[0]
               # llll=re.split("face_token': u'",ll)
               # lllll=str(llll)
               # llllll=lllll[1]
               # print llll[0],type(llll)
                k=re.split(" u'user_id': u'', u'face_token': u'",qrcont_str)
                kk=k[1]
                kkk=str(kk)
                kkkk=re.split("'}], u'image_id'",kkk)
               # print "\n"
               # print kkkk[0],type(kkkk[0])
                return(llll[0],kkkk[0])
	except urllib2.HTTPError as e:
   	        print e.read()
if __name__=='__main__':
 print   search()
