import socket
from mysql.connector.errors import DatabaseError
import os 
import signal
from mysql.connector import connect
from time import sleep, time
from tempfile  import gettempdir
# from android_tools import isAndroid
def getIP():
    # if isAndroid():
    #     return os.environ['ip']
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
    import psutil
    import shutil
    for proc in psutil.process_iter():
        if proc.name()=='hospital-server.exe':
            print(proc.pid)
            os.kill(proc.pid,signal.SIGTERM)
    cachePath=os.path.join(gettempdir(),'hs-cache')
    print(cachePath)
    if os.path.exists(cachePath):
        for cacheDir in os.listdir(cachePath):
            cacheDir=os.path.join(cachePath,cacheDir)
            print(cacheDir)
            if os.path.isdir(cacheDir):
                shutil.rmtree(cacheDir)
            elif os.path.isfile(cacheDir):
                os.remove(cacheDir)
def pingOnMySQL(host,user,password,port):
    try:
        s=time()
        conn =connect(host=host,user=user,password=password,port=port)
        e=time()
        conn.close()
        return True,e-s
    except DatabaseError:
        return False,0.0
if __name__=='__main__':
    print(getIP())