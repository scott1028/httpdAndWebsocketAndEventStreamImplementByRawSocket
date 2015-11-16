# coding:utf-8
# 實作 HTTP Daemon

import socket, re, sys, time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
sock.bind(("127.0.0.1", 9999))  
sock.listen(10)
counter = 0

while True:
    con, address = sock.accept()
    try:
        # 因為要避免 con 斷線的時候 host send client 拋錯
        print con, address
        con.send('HTTP/1.1 200 OK\r\n')
        con.send('Access-Control-Allow-Origin: *\r\n')
        con.send('Content-Type: text/event-stream\r\n')

        # SSE 最基本的資料格式就是以 data: 開頭，加上資料的內容，最後以兩個換行字元 \n\n 結尾
        while True:
            time.sleep(1)
            con.send('data: test\n\n')
            con.send('data: {\n')
            con.send('data: timestamp: ' + str(time.time()) +',\n')
            con.send('data: counter: ' + str(counter) +'\n')
            con.send('data: }\n\n')
            counter += 1
        con.close()
    except:
        pass

sock.close()

# [說明]
# Open Your Browser visit: http://127.0.0.1:9999
# 就可以看到非常類似 Ajax Polling 的效果！
# 或著使用 socket_implement_eventStream_SSE.html 再打開 Console 來看 Log！
 
# [傳輸資料的格式]
# 如果要傳送 JSON 格式的資料，可以這樣寫：
# data: {\n
# data: "msg": "hello world",\n
# data: "id": 12345\n
# data: }\n\n

# [已知情況]
# 斷線回自動連線！
# 斷線過程中沒收到的資料在重新連線之後也會不會重送，也就是會 Miss 斷線過程中的資料！

# [nc + tail]
# 甚至可以把 "data: " 去除直接用瀏覽器開啟！
# ex: (echo -e 'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\nContent-type: text/event-stream\n' && tail -f /var/www/xxx/xxx/xxx/xxx/web.log) | nc -l 3000
