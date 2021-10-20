import socket


if __name__=='__main__':
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(('127.0.0.1',58967))
    print('connected')
    s.close()