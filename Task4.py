# Task4.py Task5.py Task6.py

try:
    from SBLIB.SB_qFramePure.SlotManager import SlotManager
except:
    from SlotManager import SlotManager

from PyQt5.QtCore import QThread,pyqtSignal
from aip import AipOcr
import filetype, os,time

class SignalManager():
    signal_setTextOupt = pyqtSignal(str)
    signal_setTextLabl = pyqtSignal(str, str)
    def __init__(self):
        self.signal_setTextOupt.connect(self.setTextEidt)
        self.signal_setTextLabl.connect(self.setTextLabe)
    def setTextEidt(self,sr):
        wid_textOupt = self.ins_QT.getWidgetByName('t4output')
        wid_textOupt.setStyleSheet("font-family:KaiTi;font-size:20px")
        wid_textOupt.setText(sr)
    def setTextLabe(self,sr,color):
        wid_textOupt = self.ins_QT.getWidgetByName('t4state')
        wid_textOupt.setStyleSheet("color:{}".format(color))
        wid_textOupt.setText(sr)

class Task4(SlotManager,SignalManager,QThread):
    def __init__(self,ins_QT):
        self.ins_QT = ins_QT
        QThread.__init__(self)
        SignalManager.__init__(self)
        SlotManager.__init__(self)

        self.regSlot('t4slot')

    def run(self):
        wid_textEdit = self.ins_QT.getWidgetByName('t4input')
        while True:
            time.sleep(0.5)

            ret,para = self.getSignalFromSlot('t4slot')
            if ret is not False:
                try:
                    sr_filePath = wid_textEdit.toPlainText().replace('file:///', '')
                    bl_isCorrectType = False
                    if os.path.isfile(sr_filePath):
                        self.signal_setTextLabl.emit('Please Wait...', 'blue')
                        us_ret = filetype.guess(sr_filePath)
                        if us_ret is not None:
                            if us_ret.extension in ['jpg','png']:
                                bl_isCorrectType = True
                                self.recognition(sr_filePath)
                        elif '.ui' in sr_filePath:
                            bl_isCorrectType = True
                            self.qtuiToPyui(sr_filePath)
                        if not bl_isCorrectType:
                            self.signal_setTextLabl.emit('Illegal File Type!', 'red')
                            self.cmdOutput('Illegal File Type!')
                except Exception as e:
                    self.signal_setTextLabl.emit('Error !', 'red')
                    self.cmdOutput(e)
                self.startListenMode1Slot('t4slot')

    def recognition(self,sr_filePath):
        self.cmdOutput('Recognition')
        api_id = "14465241"
        api_key = "fUNo9FrKLGxdbLoB3X9UwECC"
        api_sec = "ktfCmRZUO54iW199jYaglkT2wVBTRDbX"
        ins_client = AipOcr(api_id, api_key, api_sec)  # 客户端对象
        try:
            with open(sr_filePath, 'rb') as f:
                ins_img = f.read()
                ins_ret = ins_client.basicGeneral(ins_img, {})
                sr_ret = ''
                for ele in ins_ret["words_result"]:
                    sr_ret += '{}\n'.format(ele["words"])
                self.signal_setTextOupt.emit(sr_ret)
                self.signal_setTextLabl.emit('Success !','green')
        except Exception as e:
            self.signal_setTextLabl.emit('Error !', 'red')
            self.cmdOutput(e)

    def qtuiToPyui(self,sr_filePath):
        self.cmdOutput('QtuiToPyui')
        sr_src = sr_filePath
        sr_dst = 'C:\\Users\Administrator\Desktop\\{}'.format(os.path.split(sr_src)[1].replace('.ui','.py'))
        sr_pyuic = '{}/src/pyuic5.exe'.format(os.getcwd())
        sr_cmd = '{} {} -o {}'.format(sr_pyuic,sr_src,sr_dst)
        os.popen(sr_cmd)
        self.signal_setTextLabl.emit('Success !', 'green')

    def cmdOutput(self, sr):
        print('>>> {}'.format(sr))















