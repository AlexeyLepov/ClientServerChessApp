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

sock=connect_with_host(9091)
for i in range(6):
    tag = codecs.decode(sock.recv(1024))
    if (tag=='2'):
        movestr=input("твой ход: ")
        sock.send(codecs.encode(movestr))
    else:
        print("ход соперника")
    receve_board(sock)

    #ty=sock.recv(1024)

sock.close()
