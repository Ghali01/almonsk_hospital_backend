import win32com.client

__VID='14CD'
__PID='2536'
def getDevices():
    devices=[]
    wmi = win32com.client.GetObject ("winmgmts:")
    for usb in wmi.InstancesOf ("Win32_USBHub"):
        
        id:str=usb.DeviceID
        id=id.split('\\')[1]
        if 'VID' in id and 'PID' in id:
            id=id.replace('VID_','').replace('PID_','')
            id=id.split('&')
            vid=id[0]
            pid=id[1]
            devices.append({'vid':vid,'pid':pid,'description':usb.description})

    return devices
def checkOnUSBDongle():
    return True
    return len(list(filter(lambda it:it['pid']==__PID and it['vid']==__VID,getDevices())))>0
class DongleError(Exception):
    pass
if __name__=="__main__":
    print(getDevices())
    # print()