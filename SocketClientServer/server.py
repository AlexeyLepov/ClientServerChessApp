import socket
import codecs
import itertools

def is_port_in_use(port: int) -> bool:
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


class Board:
    def __init__(self) -> None:
        self.positions = []
        self.moovs = []
        self.nummov = 0
        pass

    def add_mov(self, message):
        self.moovs.append(message)

    def set_board(self):
        self.positions=["RHBQKBHR","pppppppp","********","********",
                        "********","********","pppppppp","RHBKQBHR"]

    def show_board(self):
        for i in range(8):
            print(self.positions[i])

    def give_board(self):
        return self.positions

    def make_mov(self, x1, y1, x2, y2):
        buf1 = self.positions[x1][y1]
        buf2 = self.positions[x2][y2]
        newm=["","","","","","","",""]
        for i, j in itertools.product(range(8), range(8)):
            if (((i==x1)and(j!=y1))or((i!=x1)and(j==y1))or((i!=x2)and(j==y2))or((i==x2)and(j!=y2))):
                newm[i]+=self.positions[i][j]
            if ((i==x1)and(j==y1)):
                newm[i]+=buf2
            if ((i==x2)and(j==y2)):
                newm[i]+=buf1
        self.positions=newm
        self.show_board()
        self.nummov+=1
    def update_movs(self, move):
        self.moovs.append(move)


        

def made_sock():
    sock= socket.socket()
    print("socket is made")
    return sock
    
def connect(sock, port):
    sock.bind(('', port))
    sock.listen(1)
    conn, addr = sock.accept()
    print("connection is complete")
    return conn, addr
    
def receive_from_client(conn):
    data = conn.recv(1024)
    print("data were received")
    return data
    
def send_to_client(conn ,message):
    conn.send(message)
    print("data were sent")

def send_board(conn,arr):
    R=""
    R=arr[0]+arr[1]+arr[2]+arr[3]+arr[4]+arr[5]+arr[6]+arr[7]
    send_to_client(conn,codecs.encode(R))

def copy_pos(pos):
    # pos1=[]
    # for m in pos:
    #     pos1.append(m)
    # return pos1
    return list(pos)

board=Board()
board.set_board()
board.show_board()


sock1=made_sock()
sock2=made_sock()

conn1, addr1 = connect(sock1,9090)
conn2, addr2 = connect(sock2,9091)

for i in range(6):
    tag=str(i%2+1)
    send_to_client(conn1, codecs.encode(tag))
    send_to_client(conn2, codecs.encode(tag))
    if(tag=='1'):
        move=codecs.decode(receive_from_client(conn1))
    else:
        move=codecs.decode(receive_from_client(conn2))
    board.update_movs(move)
    movearr=move.split(' ')
    print(movearr)
    board.make_mov(int(movearr[0]),int(movearr[1]),int(movearr[2]),int(movearr[3]))
    send_board(conn1,copy_pos(board.positions))
    send_board(conn2,copy_pos(board.positions))
    #conn1.send(b'k')
    #conn2.send(b'k')
