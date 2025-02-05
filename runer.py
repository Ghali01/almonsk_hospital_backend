from PyQt5.QtGui import QIcon
import clr
clr.AddReference('System.Net.NetworkInformation')
from System.Net.NetworkInformation import  NetworkChange,NetworkAddressChangedEventHandler

from PyQt5.QtWidgets import QMainWindow,QApplication,QMessageBox,QFileDialog, QWidget
from  PyQt5.QtCore import   pyqtSignal
from ui.main import  Ui_Form
import sys
from utilities.network import pingOnServer,pingOnMySQL,killAllServers
from threading import Thread
import json
import os
from utilities.usb import checkOnUSBDongle
import ctypes 
import subprocess
def popen(cmd: str) -> str:
    """For pyinstaller -w"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd,startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    return process.stdout.read()
class MainWindow(QMainWindow,Ui_Form):
    serverSignal=pyqtSignal(int)
    dialogSignal=pyqtSignal(int)
    pingDbSignal=pyqtSignal(int)
    startMigratingSignal=pyqtSignal(str)
    stopServerSignal=pyqtSignal(str)
    runingServerSignal=pyqtSignal()
    databasePingrSignal=pyqtSignal(int)
    connect2SqliteFinshedSignal=pyqtSignal()
    connect2MysqlSignal=pyqtSignal(int)

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
        self.msqlPingBtn.clicked.connect(self.onPingMySqlBtn)
        self.dialogSignal.connect(self.dialogSlot)
        self.mysqlMigrateBtn.clicked.connect(self.onMigrateBtn)
        self.pingDbSignal.connect(self.pingDbSlot)
        self.startMigratingSignal.connect(self.startMigratingSlot)
        self.stopServerSignal.connect(self.stopServerSlot)
        self.runingServerSignal.connect(self.runingServerSlot)
        self.backupBtn.clicked.connect(self.onBackupBtn)
        self.importBtn.clicked.connect(self.onImportBtn)
        self.migrate2FlashBtn.clicked.connect(self.onMigrateToFlashBtn)
        self.hostLineEdit.setText('127.0.0.1')
        self.usernameLineEdit.setText('root'),
        self.passwordLineEdit.setText('')
        self.portSpinBox.setValue(3306)
        self.dbNameLlineEdit.setText('hospital')
        self.databasePingrSignal.connect(self.databasePingSlot)
        self.connect2sqlite.clicked.connect(self.connect2SqliteBtnSlot)
        self.connect2MysqlBtn.clicked.connect(self.connect2MysqlBtnSlot)
        self.connect2SqliteFinshedSignal.connect(self.connect2SqliteFinshedSlot)
        self.connect2MysqlSignal.connect(self.connect2MysqleSlot)
        self.serverButton.setEnabled(False)
        with open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'r') as dbSettingsFile:
            dbSettings=json.loads(dbSettingsFile.read())
            dbType=dbSettings['type']
            self.dbType=dbType
            if dbType=='mysql':
                print('ssws')
                self.tabWidget.setCurrentIndex(1)
                self.dbConncetSettings=dbSettings['default']                
                self.hostLineEdit.setText(self.dbConncetSettings['HOST'])
                self.usernameLineEdit.setText(self.dbConncetSettings['USER']),
                self.passwordLineEdit.setText(self.dbConncetSettings['PASSWORD'])
                self.portSpinBox.setValue(int(self.dbConncetSettings['PORT']))
                self.dbNameLlineEdit.setText(self.dbConncetSettings['NAME'])
            elif self.dbType=='sqlite':
                self.migrate2FlashBtn.setVisible(False)                        
                self.connect2sqlite.setVisible(False)                        
    
        Thread(target=self.onLunchServer).start()
    def killAllServers(self):
        killAllServers()
    def onLunchServer(self):
        try:
            if pingOnServer()==False:
                
                
                self.runServer()
            else:
                self.isServerOn=True
                self.serverButton.setText('ايقاف تشغيل')
                self.serverSignal.emit(1)
                self.serverButton.setEnabled(True)
        except:
            pass    
    def onServerButtton(self):
        if self.isServerOn:
            self.killAllServers()
            self.serverSignal.emit(3)

        else:
            self.killAllServers()
            Thread(target=self.runServer).start()
    def networkChanged(self,a, b):
        print('changed')
        if self.isServerOn:
            self.killAllServers()
            self.serverSignal.emit(3)
            self.runServer()
    def checkingOnServer(self):
        if pingOnServer()==True:
            self.serverSignal.emit(1)
        else:
            self.isServerOn=False
            # print('checking')
            self.checkingOnServer()
    def closeEvent(self,event):
        if not self.runServerOnBack:
            self.killAllServers()
    def runServerOnBackground(self):
        self.runServerOnBack=True
        self.close()
    def onServerStatusChanged(self,res):
        if res==1:
            self.serverButton.setText('ايقاف تشغيل')
            self.isServerOn=True
            self.serverButton.setEnabled(True)
            self.serverStatus.setText('تم  تشغيل الخادم')
            self.serverButtonBack.setVisible(True)
        elif res ==2:
            self.serverButton.setEnabled(False)
            self.serverStatus.setText('جاري تشغيل الخادم')
        if res==3:
            self.isServerOn=False
            self.serverButton.setEnabled(True)
            self.serverButton.setText('تشغيل')

            self.serverStatus.setText('تم  ايقاف الخادم')
            self.serverButtonBack.setVisible(False)
    def pingOnNewDB(self): 
        isConnected,time= pingOnMySQL(
            host=self.hostLineEdit.text(),
            user=self.usernameLineEdit.text(),
            password=self.passwordLineEdit.text(),
            port=self.portSpinBox.text()
        )
        if not isConnected:
            self.dialogSignal.emit(11)

        return isConnected,time
    def onPingMySqlBtn(self):
        isConnected,time=self.pingOnNewDB()
        if isConnected:
            self.pingDbSignal.emit(time)
            self.dialogSignal.emit(5)
    def onMigrateBtn(self):
        def migrate():
            
            if self.pingOnNewDB()[0]==True and self.pingOnCurrentDB()[0]==True:
                self.killAllServers()
                self.startMigratingSignal.emit('mysql')  
    
                settingsFile=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'r+')
                settingsFile.seek(0)
                settings=json.loads(settingsFile.read())
                settings['newDB']={
                            "ENGINE": "django.db.backends.mysql",
                            "HOST": self.hostLineEdit.text(),
                            "USER":self.usernameLineEdit.text(),
                            "PASSWORD":self.passwordLineEdit.text(),
                            "PORT":self.portSpinBox.text(),
                            "NAME":str(self.dbNameLlineEdit.text())
                    }
                settingsFile.truncate(0)
                settingsFile.seek(0)
                settingsFile.write(json.dumps(settings))
                settingsFile.close()
                resB=popen('db-management.exe migratetomysql')
                settingsFile=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'w')
            
                if int(resB.decode('utf-8'))==1:
                    
                    self.dialogSignal.emit(1)
                    settings['type']='mysql'
                    settings['default']=settings['newDB']
                
                else: 
                    self.dialogSignal.emit(3)
                del settings['newDB']
                settingsFile.write(json.dumps(settings))
                settingsFile.close()

                
        res=QMessageBox.question(self,'migratin','Do you want migrate to a mysql server',QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
        if res==QMessageBox.Yes:
            Thread(target=migrate).start()

    def dialogSlot(self,res):
        if res==1:
            
            dialiog=QMessageBox().information(self,'Migration succeeded','Migration finshed with succeeded',QMessageBox.Close,QMessageBox.Close)
            self.migrate2FlashBtn.setVisible(True)
            self.connect2sqlite.setVisible(True)                        

            self.dbType=='mysql'                        

        if res==2:
            
            dialiog=QMessageBox().critical(self,'Backup Error','Could not make backup to database',QMessageBox.Close,QMessageBox.Close)

        if res==3:
            dialiog=QMessageBox().critical(self,'Migrate Error','Could not Migrat to the new database',QMessageBox.Close,QMessageBox.Close)
        
        if res in (1,2,3):
            
            self.mysqlMigrateBtn.setText('migrate')
            self.mysqlMigrateBtn.setEnabled(True)
            self.runServer() 
        if res==4:
            dialiog=QMessageBox().critical(self,'Connection Error','Could not connect to database',QMessageBox.Close,QMessageBox.Close)
        if res==5:
            dialog=QMessageBox().information(self,'ping done','ping done sucssesfully')
        if res==6:
            dialog=QMessageBox().information(self,'export done','export done sucssesfully')
        if res==7:
            dialog=QMessageBox().critical(self,'export error','export finshed with error')
        if res in (6,7):
            
            self.backupBtn.setText('export')
            self.backupBtn.setEnabled(True)
   
        if res==8:
            dialog=QMessageBox().information(self,'import done','import done sucssesfully')
        if res==9:
            dialog=QMessageBox().critical(self,'import error','import finshed with error')
        if res in(8,9):
            self.importBtn.setText('import')
            self.importBtn.setEnabled(True)
        if res==10:    
            dialiog=QMessageBox().information(self,'Migration succeeded','Migration finshed with succeeded',QMessageBox.Close,QMessageBox.Close)
            self.dbType=='sqlite'                        
            self.migrate2FlashBtn.setText('migrate to local')
            self.migrate2FlashBtn.setEnabled(True)
            self.migrate2FlashBtn.setVisible(False)
            self.connect2sqlite.setVisible(False)                        

        if res==11:
            dialiog=QMessageBox().critical(self,'Connection Error','Could not connect to the new database',QMessageBox.Close,QMessageBox.Close)
        
    def pingDbSlot(self,time:float):
        self.labelPingTime.setText('%.2f' % time)
    def startMigratingSlot(self,type):
        print('migrateing')
        if type=='mysql':
            self.mysqlMigrateBtn.setText('migrateing')
            self.mysqlMigrateBtn.setEnabled(False)
        if type=='sqlite':
            self.migrate2FlashBtn.setText('migrateing')
            self.migrate2FlashBtn.setEnabled(False)
        self.serverSignal.emit(3)
        self.serverButton.setEnabled(False)
    def stopServerSlot(self,op):
        self.serverSignal.emit(3)
        self.serverButton.setEnabled(False)
        if op =="export":
            self.backupBtn.setText('exporting')
            self.backupBtn.setEnabled(False)
        if op =="import":
            self.importBtn.setText('importing')
            self.importBtn.setEnabled(False)
    def runServer(self):
        
        if (self.dbType=='mysql' and self.pingOnCurrentDB()[0]==True) or self.dbType=='sqlite':
            self.proc = subprocess.Popen('hospital-server.exe')
            # sleep(3)
          

            Thread(target=lambda:self.checkingOnServer()).start()
            self.runingServerSignal.emit()  
    def runingServerSlot(self): 
        self.serverStatus.setText('جاري تشغيل الخادم')
        self.serverButton.setEnabled(False)
   
    def pingOnCurrentDB(self):
        
        self.databasePingrSignal.emit(1)
        if self.dbType=='sqlite':
            return True,0
        isConnected,time=pingOnMySQL(
            host=self.dbConncetSettings['HOST'],
            user=self.dbConncetSettings['USER'],
            password=self.dbConncetSettings['PASSWORD'],
            port=self.dbConncetSettings['PORT']
        )
        
        if isConnected:    
            return True,time
        else:
            self.databasePingrSignal.emit(2)
            self.dialogSignal.emit(4)
            return False,0
    def onBackupBtn(self):
        fileName=str(QFileDialog.getSaveFileName(self,'Select Folder',filter='Database File (*.sqlite3)',options=QFileDialog.DontUseNativeDialog)[0])
        
        if fileName: 
            path='/'.join(fileName.split('/')[0:-1])
        
            fileName+='.sqlite3'if not fileName.endswith('.sqlite3') else ''
            # print(path)
            # print(fileName)
            def export():
       
                # path=str(QFileDialog.getExistingDirectory(self,'Select Folder',))

                self.killAllServers()
                self.stopServerSignal.emit('export')
                if self.pingOnCurrentDB():
                    file=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'r+')
                    settings=json.loads(file.read())
                    settings['export']={
                                "ENGINE": "django.db.backends.sqlite3", 
                                "NAME": fileName
                                }
                    file.truncate(0)
                    file.seek(0)
                    
                    file.write(json.dumps(settings))
                    file.close()
                    resB=popen(f"db-management.exe export2sqlite {path}")
                    if int(resB.decode('utf-8'))==1:
                        self.dialogSignal.emit(6)
                        
                    else:
                        self.dialogSignal.emit(7)
                    file=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'w')
                    del settings['export']
                    file.write(json.dumps(settings))
                    file.close()
                self.runServer()
            Thread(target=export).start()
    def onImportBtn(self):
        fileName=QFileDialog.getOpenFileName(self,'Select Database File',filter='Database File (*.sqlite3)',options=QFileDialog.DontUseNativeDialog)[0]
        if fileName:
            
            path = '/'.join(fileName.split('/')[0:-1])
        
            # print(path)
            # print(fileName)
            def importF():
                self.killAllServers()
                self.stopServerSignal.emit('import')
                if self.pingOnCurrentDB():
                    file=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'r+')
                    settings=json.loads(file.read())
                    settings['import']={
                                "ENGINE": "django.db.backends.sqlite3", 
                                "NAME": fileName
                                }
                    file.truncate(0)
                    file.seek(0)
                    file.write(json.dumps(settings))
                    file.close() 
                    resB=popen(f"db-management.exe importfromsqlite {path}")
                    if int(resB.decode('utf-8'))==1:
                        
                        self.dialogSignal.emit(8)
                    else:
                        self.dialogSignal.emit(9)
                    file=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'w')
                    del settings['import']
                    file.write(json.dumps(settings))
                    file.close() 
                self.runServer()
        Thread(target=importF).start()
    def onMigrateToFlashBtn(self): 
        def migrate():
            self.killAllServers()

            self.startMigratingSignal.emit('sqlite')
            if self.pingOnCurrentDB():    
                file=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'r+') 
                settings=json.loads(file.read())
                settings['newDB']={
                            "ENGINE": "django.db.backends.sqlite3", 
                            "NAME": "%APPDATA%/al-monsk server/db.sqlite3"
                            }
                file.truncate(0)
                file.seek(0)
                file.write(json.dumps(settings))
                file.close()
                resB=popen("db-management.exe migratetoflash")
                file=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'w') 
                if int(resB.decode('utf-8'))==1:
                    settings['type']='sqlite'
                    settings['default']=settings['newDB']
                    self.dialogSignal.emit(10)
                else:
                    self.dialogSignal.emit(3)

                del settings['newDB']
                file.write(json.dumps(settings))
                file.close()
            self.runServer()
        res=QMessageBox.question(self,'migratin','Do you want migrate to local',QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
    
        if res==QMessageBox.Yes:
            Thread(target=migrate).start()
    def databasePingSlot(self,res): 
        if res==1:
            self.serverButton.setEnabled(False)
            self.serverStatus.setText('جاري التحقق من قاعدة البيانات')
        elif res==2:
            self.serverButton.setEnabled(True)
            self.serverStatus.setText('')
    def connect2SqliteBtnSlot(self):
        self.connect2sqlite.setEnabled(False)
        self.connect2sqlite.setText('Connecting...')
        def migrate():
            self.killAllServers()
            self.startMigratingSignal.emit('sqlite')  
            settingsFile=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'r+')
            dbSettings=json.loads(settingsFile.read())
            dbSettings['newDB']={
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": "%APPDATA%/al-monsk server/db.sqlite3"
            }
            settingsFile.truncate(0)
            settingsFile.seek(0)
            settingsFile.write(json.dumps(dbSettings))
            
            settingsFile.close()
            resB=popen('db-management.exe migrate')
            if int(resB.decode('utf-8'))==1:
                dbSettings['type']='sqlite'
                self.dbType='sqlite'
                dbSettings['default']=dbSettings['newDB']
                self.connect2SqliteFinshedSignal.emit()
                self.runServer()          
            del dbSettings['newDB']
            settingsFile=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'w')
            settingsFile.write(json.dumps(dbSettings))

        Thread(target=migrate).start()
    def connect2MysqlBtnSlot(self):
        def migrate():
            if self.pingOnCurrentDB():
                self.killAllServers()
                self.connect2MysqlSignal.emit(1)

                self.startMigratingSignal.emit('mysql')  
                settingsFile=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'r+')
                dbSettings=json.loads(settingsFile.read())
                dbSettings['newDB']={
                                "ENGINE": "django.db.backends.mysql",
                                "HOST": self.hostLineEdit.text(),
                                "USER":self.usernameLineEdit.text(),
                                "PASSWORD":self.passwordLineEdit.text(),
                                "PORT":self.portSpinBox.text(),
                                "NAME":str(self.dbNameLlineEdit.text())
                        }
                settingsFile.truncate(0)
                settingsFile.seek(0)
                settingsFile.write(json.dumps(dbSettings))
                
                settingsFile.close()
                resB=popen('db-management.exe migrate')
                print(int(resB.decode('utf-8')))
                if int(resB.decode('utf-8'))==1:
                    dbSettings['type']='mysql'
                    self.dbType='mysql'
                    dbSettings['default']=dbSettings['newDB']
                    self.connect2MysqlSignal.emit(2)
                else:
                    self.connect2MysqlSignal.emit(3)
                self.runServer()          
                del dbSettings['newDB']
                settingsFile=open(os.path.expandvars('%APPDATA%/al-monsk server/db.json'),'w')
                settingsFile.write(json.dumps(dbSettings))
                settingsFile.close()

        Thread(target=migrate).start()
    def connect2SqliteFinshedSlot(self):
        self.connect2sqlite.setVisible(False)
        self.migrate2FlashBtn.setVisible(False)
        self.connect2sqlite.setEnabled(True)
        self.connect2sqlite.setText('Connect to sqlite')
        dialiog=QMessageBox().information(self,'Connection Succeeded','Connect finshed with succeeded',QMessageBox.Close,QMessageBox.Close)
    def connect2MysqleSlot(self,res):
        if res==1:
            self.connect2MysqlBtn.setText('Conneecting')
            self.connect2MysqlBtn.setEnabled(False)
        if res==2:
            dialiog=QMessageBox().information(self,'Connection Succeeded','Connect finshed with succeeded',QMessageBox.Close,QMessageBox.Close)
            self.connect2sqlite.setVisible(True)
            self.migrate2FlashBtn.setVisible(True)
            self.migrate2FlashBtn.setEnabled(True)
            self.migrate2FlashBtn.setText('migrate')
            self
        if res in (2,3):
            self.connect2MysqlBtn.setText('Conneect')
            self.connect2MysqlBtn.setEnabled(True)
            
            self.mysqlMigrateBtn.setText('migrate')
            self.mysqlMigrateBtn.setEnabled(True)
        
def main():
    myAppId=u'mega.almonsk.server.runer'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppId)
    app=QApplication(sys.argv)
    app.setWindowIcon(QIcon('app_icon.ico'))
    if checkOnUSBDongle():
        w=MainWindow()
        app.exec()
    else:
        d=QMessageBox.critical(None,'error','dongle not connected')
     

if __name__=="__main__":
    main()