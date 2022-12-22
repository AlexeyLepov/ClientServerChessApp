import socket
import codecs
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind (('127.0.0.1',5000))
client = [] # Массив где храним адреса клиентов
print ('Start Server')
n=0

data , addres = sock.recvfrom(1024)
print (addres[0], addres[1])
if  addres not in client : 
        client.append(addres)

data , addres = sock.recvfrom(1024)
print (addres[0], addres[1])
if  addres not in client : 
        client.append(addres)

trust_moves = ['a', 'b', 'c', 'd']#возможные ходы

while 1 :
        us = n%2
        if (us == 0):#очерёдность хода
                sock.sendto(codecs.encode('1'),client[0])
                sock.sendto(codecs.encode('0'),client[1])
        else:
                sock.sendto(codecs.encode('0'),client[0])
                sock.sendto(codecs.encode('1'),client[1])
        data3 = '-'
        while(data3 == '-'):#перезапись хода, если он неправильный
                data , addres = sock.recvfrom(1024)
                if (codecs.decode(data) in trust_moves):
                        data3 = '+'
                else:
                        data3 = '-'
                if (us == 0):
                        sock.sendto(codecs.encode(data3), client[0])
                else:
                        sock.sendto(codecs.encode(data3), client[1])
        print(codecs.decode(data))
        
        

        if (us == 0): #отправка хода соперника
                sock.sendto(data, client[1])
        else:
                sock.sendto(data, client[0])
        n+=1