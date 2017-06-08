import urllib2
import urllib
import time
import json
import re

#qrcontm=[]
def creat_faceid():
        #qrcontl=[]
	http_url='https://api-cn.faceplusplus.com/facepp/v3/detect'
	key = "ONam7gChKzvXg4zql5Y8sP82okBKYqlG"
	secret = "F3IFAcb2iGkI4ZmYefGffwPB-9BZUgYD"
	filepath = r"/home/pi/Pictures/wb2.jpg"
	attributes="gender,age,smiling,headpose,facequality,blur,eyestatus,ethnicity"
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
	data.append('Content-Disposition: form-data; name="%s"\r\n' % 'return_attributes')
	data.append(attributes)
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
		qrcont_json=resp.read()
               # print qrcont_json
                qrcont_dict=json.loads(qrcont_json)
		qrcontm= qrcont_dict['faces']
         #       print qrcontm,type(qrcontm)
               # ll="".join(qrcontm)
                qrcontm_str=str(qrcontm)
               # dict1=eval(qrcontm_str)
                qrcontm_face_token1=re.split("face_token': u'",qrcontm_str)
                qrcontm_face_token2=  qrcontm_face_token1[1]
                qrcontm_face_token3= str(qrcontm_face_token2)
                #print qrcontm_face_token2
                qrcontm_face_token4=re.split("', u'face_rectangle",qrcontm_face_token3)
                faceid=qrcontm_face_token4[0]
                print qrcontm_face_token4[0],type(qrcontm_face_token4[0])
               # print faceid
               # print ll
                return faceid
	except urllib2.HTTPError as e:
    		print e.read()
if __name__ == '__main__':
        creat_faceid()
    
