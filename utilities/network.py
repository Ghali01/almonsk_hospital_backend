from subprocess import check_output

def getIP():
    proc=check_output('arp -a').decode('utf-8')

    ip=proc[len('Interface: ')+2:proc.index('---')-1]
    return ip   


# if __name__=='__main__':
#     print(getIP())