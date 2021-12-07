import os
from waitress import serve
from utilities.network import getIP
os.environ['server']="yes"
import utilities.usb
def main():
    if  utilities.usb.checkOnUSBDongle():
        from hospital.wsgi import application
        port=58967
        print(getIP()+":"+str(port))
        serve(application,host='0.0.0.0',port=port)
    else:
        print('dongle not connected')
if __name__=='__main__':
    main()