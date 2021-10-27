from waitress import serve
from hospital.wsgi import application
from utilities.network import getIP
import sys
import socket

    
   
def main():

    # print(getattr(sys,'_MEIPASS',None))
    port=58967
    print(getIP()+":"+str(port))
    serve(application,host='0.0.0.0',port=port)

if __name__=='__main__':
    main()