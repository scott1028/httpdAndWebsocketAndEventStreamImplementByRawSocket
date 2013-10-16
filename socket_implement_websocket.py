# coding:utf-8
# 實作 HTTP Daemon

import socket,re,sys
import hashlib,base64

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(("", 80))  
sock.listen(10)

while True:
	con, address = sock.accept()
	try:
		# 因為要避免 con 斷線的時候 host send client 拋錯
		print con, address

		data=con.recv(1024)

		sha1=hashlib.sha1()

		print data

		host=re.findall('Host:.*?([A-z0-9].*?)\r\n',data)[0]
		key=re.findall('Sec-WebSocket-Key:.*?([A-z0-9].*?)\r\n',data)[0]

		sha1.update(key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11')
		SWSA=base64.b64encode(sha1.digest())

		con.send('HTTP/1.1 101 Switching Protocols\r\n')
		con.send('Upgrade: websocket\r\n')
		con.send('Connection: Upgrade\r\n')
		con.send('Sec-WebSocket-Accept: '+SWSA+'\r\n')
		con.send('Sec-WebSocket-Origin: null\r\n')
		con.send('Sec-WebSocket-Location: ws://'+host+'/\r\n\r\n')
		# con.close() # WebSocket 不關閉
	except:
		pass

sock.close()