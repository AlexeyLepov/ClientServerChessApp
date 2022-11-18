import socket
import codecs

def show_board(L):
        for i in range(8):
            print(L[i])

def connect_with_host(port):
    sock = socket.socket()
    sock.connect(('localhost', port))
    print("connection was made")
    return sock

def receve_board(sock):
    print(sock.recv(1024))

sock=connect_with_host(9090)
for i in range(6):
    tag = codecs.decode(sock.recv(1024))
    if (tag=='1'):
        movestr=input("твой ход: ")
        print(movestr)
        sock.send(codecs.encode(movestr))
        print('sent')
    else:
        print("ход соперника")
    #ty=sock.recv(1024)
    receve_board(sock)

sock.close()
