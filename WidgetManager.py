

class WidgetManager:
    def __init__(self):
        self.dc_widget = dict()

    # 注册控件
    def regWidget(self,sr_widName,ins_widget):
        if sr_widName not in self.dc_widget:
            self.dc_widget[sr_widName] = ins_widget
        else:
            raise Exception('控件 \'{}\' 已存在.'.format(sr_widName))

    # 根据名称获取控件
    def getWidgetByName(self,sr_widName):
        return self.dc_widget[sr_widName]




















