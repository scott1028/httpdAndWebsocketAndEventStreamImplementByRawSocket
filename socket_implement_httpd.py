# coding:utf-8
# 實作 HTTP Daemon

import socket,re,sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(("", 9999))  
sock.listen(10)

while True:
    con, address = sock.accept()
    try:
        # 因為要避免 con 斷線的時候 host send client 拋錯
        print con, address
        con.send('HTTP/1.1 200 OK\r\n')
        con.send('Content-Type: text/html\r\n')
        con.send('Content-Length: 10\r\n\r\n')
        con.send('hello world')
        data=con.recv(1024)
        con.close()
        print data
    except:
        pass

sock.close()