from socket import socket,AF_INET,SOCK_STREAM,SHUT_WR,gethostname
from threading import Thread
from playsound import playsound
def Server():
    global running,serversocket
    print("Bell started")
    serversocket.bind((gethostname(),80))
    serversocket.listen(5)
    while True: Thread(target=ServerRespond,args=serversocket.accept()).start()
def ServerRespond(clientsocket,other):
    stop = False
    pieces = clientsocket.recv(5000).decode().split("\n")
    path = ""
    if len(pieces) > 0:
        try: path = pieces[0].split(" ")[1].lower()
        except IndexError : pass
    data = ""
    contenttype = "text/html"
    httpcode = 200
    if path == "/":
        f = open("HomePage.html",mode="r")
        data=f.read()
        f.close()
    elif path == "/bell.json":
        print(GetPostData(pieces,{"name":"Someone"})["name"] + " rang the bell")
        playsound("Bell-ringing-sound-effect.mp3")
        data = ""
    elif path == "/shutdown":
        data = "<title>Bell shut down</title><h1>Bell shut down</h1>"
        stop = True
    else: httpcode = 404
    if httpcode == 200: clientsocket.sendall(("HTTP/1.1 200 OK\r\nContent-Type: "+contenttype+"; charset=utf-8\r\n\r\n"+data+"\r\n\r\n").encode())
    elif httpcode == 404: clientsocket.sendall(("HTTP/1.1 404 NOT FOUND\r\n<title>Page not found</title><h1>This page wasn't found</h1>\r\n\r\n").encode())
    clientsocket.shutdown(SHUT_WR)
    if stop: end()
def GetPostData(data,post):
    data = data[len(data)-1].split("&")
    for item in data:
        item = item.split("=")
        if item[0] in post:
            post[item[0]]=item[1].replace("+"," ")
    return post
def end():
    global serversocket
    serversocket.close()
    print("Bell shut down")
    quit()
serversocket = socket(AF_INET, SOCK_STREAM)
Server()
