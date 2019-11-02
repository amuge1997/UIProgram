try:
    from PyQt5.QtWidgets import *
    from ui2a3 import ui2a3

    try:
        from SBLIB.SB_qFramePure.WidgetManager import WidgetManager
    except:
        from WidgetManager import WidgetManager

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




















