import socket
import psutil
import os 
import signal
def getIP():
    hostName=socket.gethostname()
    ip= socket.gethostbyname(hostName)
    return  ip

def pingOnServer():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 58967))
            return True
    except:
        return False
def killAllServers():
    for proc in psutil.process_iter():
        if proc.name()=='hospital-server.exe':
            print(proc.pid)
            os.kill(proc.pid,signal.SIGTERM)
if __name__=='__main__':
    print(getIP())