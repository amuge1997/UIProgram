# Task4.py Task5.py Task6.py

try:
    from SBLIB.SB_qFramePure.SlotManager import SlotManager
except:
    from SlotManager import SlotManager

import json,os,shutil,hashlib,time,threading
from PyQt5.QtCore import pyqtSignal,QThread

def check_issave(func):
    def wrap(self,path):
        path=os.path.abspath(path)
        for one in self.SavePaths:
            isEqu=True
            for i,j in zip(one,path):
                if i in ['\\','/'] and j in ['\\','/']:
                    continue
                if i!=j:
                    isEqu=False
                    break
            if isEqu:
                raise Exception("路径 '{}' 存在路径保护列表中".format(path))
        func(self,path)
        return
    return wrap


class oss_class:
    def __init__(self):
        self.SavePaths=[]
    def append(self,path:str):
        self.SavePaths.append(os.path.abspath(path))
    @check_issave
    def rmtree(self,path:str):
        shutil.rmtree(path)
    @check_issave
    def remove(self,path:str):
        os.remove(path)


class FileClass:
    SplitSym='%lhk%'
    def __init__(self,fname):
        self.Fname=fname
        self.Name,self.Hash,self.Mtime=fname.split(self.SplitSym)


class SignalManager:
    signal_saveBtn = pyqtSignal(str)
    signal_output = pyqtSignal(str)
    signal_timeLabel = pyqtSignal(str)

    def __init__(self):
        self.signal_output.connect(self.f1)
        self.signal_saveBtn.connect(self.f2)
        self.signal_timeLabel.connect(self.f3)

    def f1(self,sr):
        self.wid_output.setText(sr)
    def f2(self,sr):
        self.wid_saveBtn.setText(sr)
    def f3(self,sr):
        self.wid_tLabel.setText(sr)

class Task6(SignalManager,SlotManager,QThread):
    def __init__(self,inst_QT):
        SlotManager.__init__(self)
        QThread.__init__(self)
        SignalManager.__init__(self)
        self.inst_QT = inst_QT

        self.regSlot('t6Add')
        self.regSlot('t6Pop')
        self.regSlot('t6SaveStart')
        self.regSlot('t6UnpackStart')

        self.wid_saveBtn = self.inst_QT.getWidgetByName('saveBtn')
        self.wid_upackBtn = self.inst_QT.getWidgetByName('unpackBtn')
        self.wid_addBtn = self.inst_QT.getWidgetByName('addBtn')
        self.wid_popBtn = self.inst_QT.getWidgetByName('popBtn')
        self.wid_addPopEdit = self.inst_QT.getWidgetByName('addPopEdit')
        self.wid_output = self.inst_QT.getWidgetByName('output')
        self.wid_tLabel = self.inst_QT.getWidgetByName('timelabel')

        self.bl_saveThreadFlag = False
        self.th_saveThread = QThread()
        self.th_saveThread.run = self.saveThreadFunc
        self.th_saveThread.start()

        self.bl_upackThreadFlag = False
        self.th_upackThread = QThread()
        self.th_upackThread.run = self.unpackThreadFunc

        self.lc_saveUpackLock = threading.Lock()


        self.SaveOriDir = 'F:\\ALL_CODE_BK\\备份程序版本4\\Save'
        self.DataJson = 'F:\\ALL_CODE_BK\\备份程序版本4\\NeedSave.json'
        self.UnpackDir = 'F:\\ALL_CODE_BK\\备份程序版本4\\SaveUnpack'

        with open(self.DataJson) as f:
            ls = json.load(f)
            sr = ''
            for i in ls:
                sr += '{}\n'.format(i)
            self.signal_output.emit(sr)

    def run(self):
        while True:
            time.sleep(0.5)

            ret,para = self.getSignalFromSlot('t6Add')
            if ret:
                self.cmdOutput('add press')
                self.addPressFunc()
                self.startListenMode1Slot('t6Add')

            ret,para = self.getSignalFromSlot('t6Pop')
            if ret:
                self.cmdOutput('pop press')
                self.popPressFunc()
                self.startListenMode1Slot('t6Pop')

            ret,para = self.getSignalFromSlot('t6SaveStart')
            if ret:
                self.cmdOutput('save press')
                if self.bl_saveThreadFlag:
                    self.cmdOutput('save stop')
                    self.bl_saveThreadFlag = False
                    self.signal_saveBtn.emit('备份')
                else:
                    self.cmdOutput('save start')
                    self.bl_saveThreadFlag = True
                    self.signal_saveBtn.emit('停止')
                self.startListenMode1Slot('t6SaveStart')

            ret,para = self.getSignalFromSlot('t6UnpackStart')
            if ret:
                self.cmdOutput('unpack press')
                self.th_upackThread.start()
                self.startListenMode1Slot('t6UnpackStart')

    def saveThreadFunc(self):
        while True:
            while self.bl_saveThreadFlag:
                if self.lc_saveUpackLock.acquire(timeout=1.5):
                    try:
                        self.save_program_run()
                    except Exception as e:
                        self.cmdOutput('ERROR: save error: {}'.format(e))
                    self.lc_saveUpackLock.release()
                else:
                    self.cmdOutput('save cant acquire lock !')
                time.sleep(5)

    def unpackThreadFunc(self):

        def upackLabelThread():
            it_time = 0
            while True:
                sr = '解压用时: {}秒'.format(str(it_time))
                self.signal_timeLabel.emit(sr)
                time.sleep(1)
                it_time += 1

        if not self.bl_upackThreadFlag:
            if self.lc_saveUpackLock.acquire(timeout=10):
                self.bl_upackThreadFlag = True
                self.cmdOutput('unpacking ...')
                th_tLabelThread = QThread()
                th_tLabelThread.run = upackLabelThread
                th_tLabelThread.start()
                try:
                    self.unpack()
                except Exception as e:
                    self.cmdOutput('ERROR: unpack error: {}'.format(e))
                th_tLabelThread.terminate()
                self.cmdOutput('unpack complete !')
                self.bl_upackThreadFlag = False
                self.lc_saveUpackLock.release()
            else:
                self.cmdOutput('unpack cant acquire lock !')

    def addPressFunc(self):
        sr_path = self.wid_addPopEdit.toPlainText().replace('file:///', '')
        self.cmdOutput('want to add {}'.format(sr_path))
        if os.path.isdir(sr_path):
            sr_path = os.path.abspath(sr_path)
            bl_changeFlag = False
            with open(self.DataJson, 'r') as f:
                ls_paths = json.load(f)
                if sr_path not in ls_paths:
                    ls_paths.append(sr_path)
                    bl_changeFlag = True
            self.cmdOutput(str(ls_paths))
            if bl_changeFlag:
                with open(self.DataJson, 'w') as f:
                    json.dump(ls_paths, f)
                sr_out = ''
                for i in ls_paths:
                    sr_out += '{}\n'.format(str(i))
                self.signal_output.emit(sr_out)
        else:
            print('cant add this path .')

    def popPressFunc(self):
        sr_path = self.wid_addPopEdit.toPlainText().replace('file:///', '')
        self.cmdOutput('want to pop {}'.format(sr_path))
        if os.path.isdir(sr_path):
            sr_path = os.path.abspath(sr_path)
            bl_changeFlag = False
            with open(self.DataJson, 'r') as f:
                ls_paths = json.load(f)
                if sr_path in ls_paths:
                    ls_paths.remove(sr_path)
                    bl_changeFlag = True
            self.cmdOutput(str(ls_paths))
            if bl_changeFlag:
                with open(self.DataJson, 'w') as f:
                    json.dump(ls_paths, f)
                sr_out = ''
                for i in ls_paths:
                    sr_out += '{}\n'.format(str(i))
                self.signal_output.emit(sr_out)
        else:
            print('cant add this path .')

    '''
    save_program_run 中有个bug,
    如果两个及以上需保存目录路径是同一个目录的子目录，
    那么当一个目录路径 DirPath 被移除时，其被保存目录文件不会被移除，
    除非有着与 DirPath 相同父目录的需保存目录路径都被移除
    '''

    # 运行备份主程序
    def save_program_run(self):
        self.Time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        with open(self.DataJson) as f:
            self.NeedOriDirs = json.load(f)

        self.oss = oss_class()  # 安全删除
        for oneNeedOriDir in self.NeedOriDirs:
            self.oss.append(oneNeedOriDir)

        Dirs = []
        for oneNeedOriDir in self.NeedOriDirs:
            dName, ldName = os.path.split(oneNeedOriDir)

            dNameMD5 = ''
            for s in dName:
                if s in [':', '\\', '/']:
                    continue
                else:
                    dNameMD5 += s
            Dirs.append(dNameMD5)

            if not os.path.exists(os.path.join(self.SaveOriDir, dNameMD5)):
                os.mkdir(os.path.join(self.SaveOriDir, dNameMD5))
            oneNeedOriDirSavePath = os.path.join(self.SaveOriDir, dNameMD5, ldName)
            if not os.path.exists(oneNeedOriDirSavePath):
                os.mkdir(oneNeedOriDirSavePath)

            for NThisDir, NSubDirs, NFiles in os.walk(oneNeedOriDir):  # 递归更新
                tPath = NThisDir[len(oneNeedOriDir):]
                SThisDir = oneNeedOriDirSavePath + tPath
                self.update_dirs(NThisDir, SThisDir)  # 更新子目录
                self.update_files(NThisDir, SThisDir)  # 更新子文件

        # 删除Save目录中无关的子目录
        ThisDir, SubDirs, Files = next(os.walk(self.SaveOriDir))
        NeedPop = set(SubDirs).difference(Dirs)
        for needPop in NeedPop:
            pPath = os.path.join(ThisDir, needPop)
            self.oss.rmtree(pPath)
            self.ShowText("need pop dir:  {}".format(pPath))
    # 更新子目录
    def update_dirs(self,NThisDir,SThisDir):
        NThisDir, NSubDirs, NFiles = next(os.walk(NThisDir))
        SThisDir, SSubDirs, SFiles = next(os.walk(SThisDir))

        NeedAdd = set(NSubDirs).difference(SSubDirs)
        NeedPop = set(SSubDirs).difference(NSubDirs)

        for needadd in NeedAdd:
            sPath=os.path.join(SThisDir,needadd)
            os.mkdir(sPath)
            self.ShowText("need add dir:  {}".format(sPath))
        for needpop in NeedPop:
            pPath = os.path.join(SThisDir, needpop)
            self.oss.rmtree(pPath)
            self.ShowText("need pop dir:  {}".format(pPath))
    # 更新子文件
    def update_files(self,NThisDir,SThisDir):
        NThisDir, NSubDirs, NFiles = next(os.walk(NThisDir))
        SThisDir, SSubDirs, SFiles = next(os.walk(SThisDir))

        SFilesObjs = [FileClass(f) for f in SFiles]
        SFilesNames = [f.Name for f in SFilesObjs]

        NeedAdd = set(NFiles).difference(SFilesNames)
        NeedPop = set(SFilesNames).difference(NFiles)
        BothFil = set(NFiles) - NeedAdd

        SplitSym = FileClass.SplitSym
        # 1. 保持同名文件同步
        BothFil=list(filter(lambda obj:True if obj.Name in BothFil else False,SFilesObjs))
        for oneobj in BothFil:
            npath = os.path.join(NThisDir, oneobj.Name)
            mtime = str(os.stat(npath).st_mtime)
            if oneobj.Mtime != mtime:
                with open(npath, 'rb') as f:
                    md5 = hashlib.md5(f.read()).hexdigest()
                abspath = os.path.join(SThisDir,oneobj.Fname)
                if md5 != oneobj.Hash:
                    self.oss.remove(abspath)
                    spath = '{}\\{}{}{}{}{}'.format(SThisDir,oneobj.Name,SplitSym,oneobj.Hash,SplitSym,mtime)
                    shutil.copyfile(npath, spath)
                    self.ShowText(f"file hash update:  {abspath}")
                else:
                    srcpath = abspath
                    dstpath='{}\\{}{}{}{}{}'.format(SThisDir,oneobj.Name,SplitSym,oneobj.Hash,SplitSym,mtime)
                    os.rename(srcpath, dstpath)
                    self.ShowText(f"file time update:  {srcpath}")

        # 2.增加未备份文件
        for fileName in NeedAdd:
            npath=os.path.join(NThisDir,fileName)
            with open(npath, 'rb') as f:
                md5 = hashlib.md5(f.read()).hexdigest()
                mtime = os.stat(npath).st_mtime
                spath='{}\\{}{}{}{}{}'.format(SThisDir,fileName,SplitSym,md5,SplitSym,mtime)
                shutil.copyfile(npath, spath)
                self.ShowText(f"need add file:  {npath}")

        # 3.删除多余文件
        for oneobj in SFilesObjs:
            if oneobj.Name in NeedPop:
                rmpath = os.path.join(SThisDir,oneobj.Fname)
                self.oss.remove(rmpath)
                self.ShowText(f"need pop file:  {rmpath}")
    # 去掉路径字符串中的冒号
    def get_pathstr(self,path):
        return path[:1] + path[2:]
    # 输出
    def ShowText(self,text,isn=True,istime=True):
        oupstr=''
        if isn:
            oupstr+='\n'
        if istime:
            oupstr+=f'{self.Time} '
        oupstr+=f'{text}'
        print(oupstr)

    # 解压程序
    def unpack(self):
        SplitSym = FileClass.SplitSym

        UnPackPath = self.UnpackDir
        if os.path.exists(UnPackPath):
            print('\n{}目录 已经存在'.format(UnPackPath))
            return False

        try:
            shutil.copytree(self.SaveOriDir,UnPackPath)
            for ThisDir,SubDirs,Files in os.walk(UnPackPath):
                for file in Files:
                    src='{}/{}'.format(ThisDir,file)
                    dst='{}/{}'.format(ThisDir,file.split(SplitSym)[0])
                    os.rename(src,dst)
            return True
        except:
            self.oss.rmtree(UnPackPath)
            return False

    def cmdOutput(self, sr):
        print('>>> {}'.format(sr))

# if __name__ == '__main__':
#     cla=Task6()
#     cla.main_program_run()
#     #cla.unpack()













