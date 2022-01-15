from django.core.management import call_command
import sys
import os
import datetime
from tempfile import gettempdir
from utilities.usb import checkOnUSBDongle,DongleError
def main():
    stdout=sys.stdout 
    try:
        if not checkOnUSBDongle():
            raise DongleError
        from hospital.wsgi import application
        tmpdatapath=os.path.join(gettempdir(),'hs-cache',f'data{datetime.datetime.now().strftime("%Y-%m-%d %H-%S")}.json')
        if sys.argv[1]=='migratetomysql':
            f=open(tmpdatapath ,'w',encoding='utf-8')
            sys.stdout=f
            call_command('dumpdata')
            sys.stdout=stdout
            f.close()
            tmp =open(os.devnull,'w')
            sys.stdout=tmp

            call_command('migrate' ,'--database=newDB')
            call_command('loaddata','--database=newDB',tmpdatapath)
            tmp.close()
            sys.stdout=stdout
            print(1)
        elif sys.argv[1]=='export2sqlite': 
            tmp =open(os.devnull,'w')
            sys.stdout=tmp
            call_command('migrate','--database=export')
            f=open(tmpdatapath,'w',encoding='utf-8')
            sys.stdout=f
            call_command('dumpdata',"--exclude",'contenttypes')
            f.close()
            sys.stdout=tmp
            call_command('loaddata','--database=export',tmpdatapath)
            tmp.close()
            sys.stdout=stdout
            print(1)
        elif sys.argv[1]=='importfromsqlite':
            z=open(os.devnull,'w')
            sys.stdout=z
            call_command('migrate','--database=import')
            file=open(tmpdatapath,'w',encoding='utf-8')
            sys.stdout=file
            call_command('dumpdata','--database=import',"--exclude",'contenttypes')
            sys.stdout=open(os.devnull,'w')
            file.close()
            
            call_command('loaddata',tmpdatapath)
            sys.stdout=stdout
            
            print(1)
        elif sys.argv[1]=='migratetoflash':
            file=open(tmpdatapath,'w',encoding='utf-8')
            sys.stdout=file     
            call_command('dumpdata')
            sys.stdout=open(os.devnull,'w')                  
            
            file.close()
            call_command('migrate','--database=newDB')
            call_command('loaddata','--database=newDB',tmpdatapath) 
            sys.stdout=stdout
            print(1)
        elif sys.argv[1] =="migrate":
            sys.stdout=open(os.devnull,'w')
            call_command('migrate','--database=newDB')
            sys.stdout=stdout
            print(1)
        else: 
            print('''unknown command
                    try :
                    migrate    
                    backup
            ''')
        if os.path.exists(tmpdatapath):
                os.remove(tmpdatapath)
    except DongleError:
        sys.stdout=stdout
        if '-d' in sys.argv:
            print('dongle not connected')
        print(0) 
    except Exception as e:
        sys.stdout=stdout
        if '-d' in sys.argv:
            print(e)
        print(0)
if __name__ =='__main__':
    main()
    