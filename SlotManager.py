import queue,threading

class SlotManager:
    def __init__(self):
        self.dc_slot = {}

    # 注册信号槽
    def regSlot(self,sr_slotName,it_mode = 1):
        if sr_slotName not in self.dc_slot:
            if it_mode == 1:
                self.dc_slot[sr_slotName] = {
                    'mode':1,
                    'emit':False,
                    'para':None,
                    'lock':threading.Lock(),
                    'listen':True
                }
            elif it_mode == 2:
                self.dc_slot[sr_slotName] = {
                    'mode':2,
                    'queue':queue.Queue(),
                    'lock':threading.Lock()
                }
        else:
            raise Exception('信号槽 \'{}\'已存在'.format(sr_slotName))

    # 获取信号槽
    def getSlot(self,sr_slotName):
        if sr_slotName not in self.dc_slot:
            raise Exception('没有该信号槽: {}'.format(sr_slotName))

        def f(*args):
            slot = self.dc_slot[sr_slotName]
            mode = slot['mode']
            lock = slot['lock']
            if mode == 1:
                lock.acquire()
                if slot['listen']:
                    slot['emit'] = True
                    slot['para'] = args
                    slot['listen'] = False
                lock.release()
            elif mode == 2:
                lock.acquire()
                slot['queue'].put(args)
                lock.release()
        return f

    # 开启模式1信号槽的监听
    def startListenMode1Slot(self,sr_slotName):
        if sr_slotName not in self.dc_slot:
            raise Exception('没有该信号槽: {}'.format(sr_slotName))
        mode = self.dc_slot[sr_slotName]['mode']
        if mode == 1:
            self.dc_slot[sr_slotName]['listen'] = True

    # 从信号槽中获取信号
    def getSignalFromSlot(self,sr_slotName):
        if sr_slotName not in self.dc_slot:
            raise Exception('没有该信号槽: {}'.format(sr_slotName))

        slot = self.dc_slot[sr_slotName]
        mode = slot['mode']
        if mode == 1:
            if slot['emit']:
                slot['emit'] = False
                return True,slot['para']
            else:
                return False,None
        elif mode == 2:
            lock = slot['lock']
            que = slot['queue']
            lock.acquire()
            if not que.empty():
                ret = True,que.get()
            else:
                ret = False,None
            lock.release()
            return ret





























