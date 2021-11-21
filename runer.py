import clr
clr.AddReference('System.Net.NetworkInformation')
from System.Net.NetworkInformation import  NetworkChange,NetworkAddressChangedEventHandler
from subprocess import Popen
import os
from PyQt5.QtWidgets import QMainWindow,QApplication
from  PyQt5.QtCore import   pyqtSignal
from ui.main import  Ui_Form
import sys
from utilities.network import pingOnServer,killAllServers
from threading import Thread
class MainWindow(QMainWindow,Ui_Form):
    serverSignal=pyqtSignal(int)
    isServerOn=False
    runServerOnBack=False
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        NetworkChange.NetworkAddressChanged += NetworkAddressChangedEventHandler(lambda a,b:self.networkChanged(a,b))
        self.serverButton.clicked.connect(self.onServerButtton)
        self.serverSignal.connect(self.onServerStatusChanged)
        self.serverButtonBack.setVisible(False)
        self.serverButtonBack.clicked.connect(self.runServerOnBackground)

        self.onLunchServer()
    def onLunchServer(self):
        if pingOnServer()==False:
            self.proc = Popen('hospital-server.exe',)
            self.serverStatus.setText('جاري تشغيل الخادم')
            Thread(target=lambda:self.checkingOnServer()).start()
            self.serverButton.setEnabled(False)
        else:
            self.isServerOn=True
            self.serverButton.setText('ايقاف تشغيل')
            self.serverSignal.emit(1)
            self.serverButton.setEnabled(True)
    
    def onServerButtton(self):
        if self.isServerOn:
            killAllServers()
            self.isServerOn=False
            self.serverButton.setText('تشغيل')
            self.serverSignal.emit(3)
            self.serverButtonBack.setVisible(False)

        else:
            killAllServers()
            self.proc = Popen('hospital-server.exe')
            Thread(target=lambda:self.checkingOnServer()).start()
            self.serverSignal.emit(2)
            self.serverButton.setEnabled(False)
    def networkChanged(self,a, b):
        print('changed')
        if self.isServerOn:
            killAllServers()
            self.proc = Popen('hospital-server.exe')
            self.serverSignal.emit(2)
            self.checkingOnServer()
    def checkingOnServer(self):
        if pingOnServer()==True:
            self.isServerOn=True
            self.serverButton.setText('ايقاف تشغيل')
            self.serverSignal.emit(1)
            self.serverButton.setEnabled(True)
            self.serverButtonBack.setVisible(True)
        else:
            self.isServerOn=False
            print('checking')
            self.checkingOnServer()
    def closeEvent(self,event):
        if not self.runServerOnBack:
            killAllServers()
    def runServerOnBackground(self):
        self.runServerOnBack=True
        self.close()
    def onServerStatusChanged(self,res):
        if res==1:
            self.serverStatus.setText('تم  تشغيل الخادم')
        elif res ==2:
            self.serverStatus.setText('جاري تشغيل الخادم')
        if res==3:
            self.serverStatus.setText('تم  ايقاف الخادم')
       


def main():
    app=QApplication(sys.argv)
    w=MainWindow()
    app.exec()

    global proc

if __name__=="__main__":
    main()