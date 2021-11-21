from waitress import serve
from utilities.network import getIP
   
def main():
    from hospital.wsgi import application
    port=58967
    print(getIP()+":"+str(port))
    serve(application,host='0.0.0.0',port=port)

if __name__=='__main__':
    main()