#
#
# from PyQt5.QtCore import QThread, pyqtSignal
# class SignalSlot(QThread):
#     signal_setTextOupt = pyqtSignal(str)
#     signal_setTextLabl = pyqtSignal(str, str)
#     def __init__(self):
#         QThread.__init__(self)
#         self.signal_setTextOupt.connect(self.setTextEidt)
#         self.signal_setTextLabl.connect(self.setTextLabe)
#     def setTextEidt(self, sr):
#         wid_textOupt = self.inst_QT.textOupt
#         wid_textOupt.setStyleSheet("font-family:KaiTi;font-size:20px")
#         wid_textOupt.setText(sr)
#     def setTextLabe(self, sr, color):
#         wid_textOupt = self.inst_QT.label
#         wid_textOupt.setStyleSheet("color:{}".format(color))
#         wid_textOupt.setText(sr)
#
# import queue, threading
# class TaskParent:
#     def __init__(self):
#         self.que = queue.Queue()
#         self.lc = threading.Lock()
#         self.bl_listen = True
#
#     def slot(self):
#         if self.bl_listen:
#             self.lc.acquire()
#             self.que.put({})
#             self.lc.release()
#             self.bl_listen = False
#     def startListen(self):
#         self.bl_listen = True
#     def getSignal(self):
#         self.lc.acquire()
#         ret = self.que.get() if not self.que.empty() else False
#         self.lc.release()
#         return ret
#     def cmdOutput(self, sr):
#         print('>>> {}'.format(sr))


try:
    from PyQt5.QtWidgets import *
    # from ui import ui
    # from ui2 import ui2
    # from ui3 import ui3
    from ui2a3 import ui2a3

    try:
        from SBLIB.SB_qFramePure.WidgetManager import WidgetManager
    except:
        from WidgetManager import WidgetManager

    # from Task1 import Task1
    # from Task2 import Task2
    from Task4 import Task4
    from Task5 import Task5
    from Task6 import Task6
    import sys
except Exception as e:
    print(e)
    input()

class Main(QMainWindow,WidgetManager,ui2a3):
    def __init__(self):
        # noinspection PyArgumentList
        QMainWindow.__init__(self)
        self.setupUi(self)

        WidgetManager.__init__(self)

        self.setFixedSize(self.width(), self.height())

        # self.Task1 = Task1(self)
        # self.rc_inpu.textChanged.connect(self.Task1.slot)
        # self.Task1.start()

        # self.Task2 = Task2(self)
        # self.pc_submit.clicked.connect(self.Task2.slot)
        # self.Task2.start()

        self.regWidget(sr_widName='t4input',ins_widget=self.rc_inpu)
        self.regWidget(sr_widName='t4output',ins_widget=self.rc_oupt)
        self.regWidget(sr_widName='t4state',ins_widget=self.rc_state)

        self.regWidget(sr_widName='t5submit',ins_widget=self.pc_submit)
        self.regWidget(sr_widName='t5state',ins_widget=self.pc_state)
        self.regWidget(sr_widName='t5path1', ins_widget=self.pc_pathInpt1)
        self.regWidget(sr_widName='t5path2', ins_widget=self.pc_pathInpt2)
        self.regWidget(sr_widName='t5path3', ins_widget=self.pc_pathInpt3)
        self.regWidget(sr_widName='t5file',ins_widget=self.pc_fileInpt)

        self.regWidget('output', self.bk_textOupt)
        self.regWidget('addPopEdit',self.bk_addPopEdit)
        self.regWidget('addBtn', self.bk_addBtn)
        self.regWidget('popBtn', self.bk_popBtn)
        self.regWidget('saveBtn', self.bk_saveBtn)
        self.regWidget('unpackBtn', self.bk_upackBtn)
        self.regWidget('timelabel',self.bk_time)


        self.Task4 = Task4(self)
        self.Task5 = Task5(self)
        self.Task6 = Task6(self)

        self.rc_inpu.textChanged.connect(self.Task4.getSlot('t4slot'))

        self.pc_submit.clicked.connect(self.Task5.getSlot('t5slot'))

        self.bk_saveBtn.clicked.connect(self.Task6.getSlot('t6SaveStart'))
        self.bk_addBtn.clicked.connect(self.Task6.getSlot('t6Add'))
        self.bk_popBtn.clicked.connect(self.Task6.getSlot('t6Pop'))
        self.bk_upackBtn.clicked.connect(self.Task6.getSlot('t6UnpackStart'))

        self.Task4.start()
        self.Task5.start()
        self.Task6.start()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)

        main = Main()
        main.show()

        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        input()




















