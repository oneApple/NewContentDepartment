# -*- coding: UTF-8 -*-
import wx,os
from wx.lib.pubsub  import Publisher

import ValidaDialog
import RegisterDialog
import MainFrame
from GlobalData import MagicNum, CommonData,ConfigData
from NetCommunication import NetConnect

class LoginDialog(ValidaDialog.ValidaDialog,object):
    def __init__(self,netconnect):
        super(LoginDialog,self).__init__("登录",MagicNum.ValidaDialogc.IMAGEBUTTON)
        self.CheckConfig()
        if not netconnect:
            self.__netconnect = NetConnect.NetConnect(self)
            if self.__netconnect.StartNetConnect() == MagicNum.NetConnectc.NOTCONNECT:
                self.setHeaderText("无法连接到服务器，请重新启动") 
        else :
            self.__netconnect = netconnect
        self.registerPublisher()
    
    def CheckConfig(self):
        try:
            cfg = ConfigData.ConfigData()
            pathmap = {cfg.GetDbPath():"数据库配置不正确",
               cfg.GetYVectorFilePath():"特征提取存放路径配置不正确",
               cfg.GetFfmpegPathAndArgs()[0]:"ffmpeg程序配置不正确",
               cfg.GetFfmpegPathAndArgs()[1]:"ffmpeg参数配置不正确",
               cfg.GetKeyPath():"密钥路径配置不正确",
               }
            for path in pathmap:
                if not os.path.exists(path):
                    self.setHeaderText(pathmap[path])
        except Exception,e:
            self.setHeaderText("配置文件不存在或路径错误")
            os.sys.exit()
    
    def registerPublisher(self):
        Publisher().subscribe(self.tryAgain, CommonData.ViewPublisherc.LOGIN_TRYAGAIN)    
        Publisher().subscribe(self.SwitchView, CommonData.ViewPublisherc.LOGIN_SWITCH)     
        
    def getTextLabel(self):
        _labelList = ["用户名", "密码"]
        return _labelList
    
    def getHeaderText(self):
        _text = """\
                   内 容 提 供 部 门\
                """
        return _text
    
    def SwitchView(self,msg):
        _inputlist = self.getInputText()
        _mainFrame = MainFrame.MyFrame(msg.data + (_inputlist[0],),self.__netconnect)
        _mainFrame.Run()
        self.Hide()
    
    def secondButtonFun(self):
        _inputlist = self.getInputText()
        self.__netconnect.ReqConnect(_inputlist[0], _inputlist[1])
            
    def registerButtonFun(self,event):
        self.Hide()
        _dlg = RegisterDialog.RegisterDialog(self.__netconnect,self)
        _dlg.Run()
        
        
if __name__=='__main__':
    app = wx.PySimpleApp()
    dlg = LoginDialog(None)
    dlg.Run()
    app.MainLoop()