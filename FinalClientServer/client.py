import socket
import threading
import codecs

def read_sok():
    while 1 :
        data1 = sor.recv(1024)#получение очерёдности
        if codecs.decode(data1)=='1':
            data2 = input("your move: ")#первичная запись хода
            sor.sendto(codecs.encode(data2), server)
            data3 = sor.recv(1024)
            while(codecs.decode(data3) == '-'):#перезапись хода
                data2 = input("your new move: ")
                sor.sendto(codecs.encode(data2), server)
                data3 = sor.recv(1024)
        else:
            data2 = sor.recv(1024)
            print("data2 = " + codecs.decode(data2))
    

server = '127.0.0.1',5000  # Данные сервера
alias = input() # Вводим наш псевдоним
sor = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sor.bind(('', 0)) # Задаем сокет как клиент
sor.sendto((alias+' Connect to server').encode('utf-8'), server)# Уведомляем сервер о подключении
potok = threading.Thread(target= read_sok)
potok.start()
