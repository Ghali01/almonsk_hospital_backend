from waitress import serve
from hospital.wsgi import application
from utilities.network import getIP
import sys
import socket

    
   
def main():

    # print(getattr(sys,'_MEIPASS',None))
    print(getIP())
    serve(application,host='0.0.0.0',port=58967)

if __name__=='__main__':
    main()