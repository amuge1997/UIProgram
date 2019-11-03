# Task4.py Task5.py Task6.py

try:
    from SBLIB.SB_qFramePure.SlotManager import SlotManager
except:
    from SlotManager import SlotManager

from PyQt5.QtCore import QThread,pyqtSignal
from datetime import datetime
import os,shutil,time


class SignalManager:
    signal_state = pyqtSignal(str,str)
    signal_clear = pyqtSignal()
    def __init__(self):
        self.signal_state.connect(self.setState)
        self.signal_clear.connect(self.textClear)
    def setState(self,sr,color):
        wid_state = self.inst_QT.getWidgetByName('t5state')
        wid_state.setStyleSheet("color:{}".format(color))
        wid_state.setText(sr)
    def textClear(self):
        wid_file = self.inst_QT.getWidgetByName('t5file')
        wid_path1 = self.inst_QT.getWidgetByName('t5path1')
        wid_path2 = self.inst_QT.getWidgetByName('t5path2')
        wid_path3 = self.inst_QT.getWidgetByName('t5path3')
        wid_file.setText('')
        wid_path1.setText('')
        wid_path2.setText('')
        wid_path3.setText('')

class Task5(SlotManager,SignalManager,QThread):
    def __init__(self,inst_QT):
        QThread.__init__(self)
        SlotManager.__init__(self)
        SignalManager.__init__(self)
        self.inst_QT = inst_QT
        self.regSlot('t5slot',it_mode=1)

    def cmdOutput(self, sr):
        print('>>> {}'.format(sr))

    def run(self):
        wid_file = self.inst_QT.getWidgetByName('t5file')
        wid_path1 = self.inst_QT.getWidgetByName('t5path1')
        wid_path2 = self.inst_QT.getWidgetByName('t5path2')
        wid_path3 = self.inst_QT.getWidgetByName('t5path3')

        while True:
            time.sleep(0.5)

            ret,para = self.getSignalFromSlot('t5slot')
            if ret is not False:
                try:
                    sr_file = wid_file.toPlainText().replace('file:///', '')
                    sr_path1 = wid_path1.toPlainText().replace('file:///', '')
                    sr_path2 = wid_path2.toPlainText().replace('file:///', '')
                    sr_path3 = wid_path3.toPlainText().replace('file:///', '')
                    ls_paths = [sr_path1,sr_path2,sr_path3]

                    sr_pyinstaller = 'pyinstaller'
                    sr_curPath = os.getcwd()
                    sr_conCmd = 'cd {}\\src && {} -F '.format(sr_curPath,sr_pyinstaller)

                    sr_resultDir = '{}\\src\\dist'.format(os.getcwd())
                    sr_openDirCmd = 'start explorer {}'.format(sr_resultDir)

                    sr_specDir = '{}\\src\\'.format(os.getcwd())

                    if os.path.isfile(sr_file):
                        if '.py' in sr_file:
                            sr_src = sr_file
                            sr_datatime = datetime.strftime(datetime.now(), '_%y-%m-%d-%H-%M-%S')
                            sr_dst = sr_file[:-3] + sr_datatime + '.py'
                            shutil.copy(sr_src, sr_dst)

                            sr_specFileName = os.path.split(sr_src)[1][:-3]+sr_datatime+'.spec'
                            sr_specAbsPath = os.path.join(sr_specDir,sr_specFileName)

                            self.signal_state.emit('State', 'black')
                            sr_conCmd += '{} '.format(sr_dst)
                            for path in ls_paths:
                                if os.path.isdir(path):
                                    sr_conCmd += '-p {} '.format(path)
                            self.signal_state.emit('Wait...','blue')
                            self.cmdOutput('Start building!')
                            self.cmdOutput(sr_conCmd)
                            self.cmdOutput(sr_openDirCmd)
                            os.popen(sr_conCmd).read()
                            os.remove(sr_dst)
                            os.remove(sr_specAbsPath)

                            sr_fileName = os.path.split(sr_dst)[1].replace('.py','.exe')
                            sr_exePath = os.path.join(sr_resultDir,sr_fileName)
                            if os.path.isfile(sr_exePath):
                                self.signal_state.emit('Completed !', 'green')
                                os.popen(sr_openDirCmd).read()
                                self.cmdOutput('Completed!')
                            else:
                                self.signal_state.emit('Failure !', 'red')
                                self.cmdOutput('failure!')
                            self.signal_clear.emit()
                        else:
                            self.signal_state.emit('Illegal File Type!', 'red')
                except Exception as e:
                    self.cmdOutput('发生错误: {}'.format(e))
                    self.signal_state.emit('Error !', 'red')

                self.startListenMode1Slot('t5slot')




























