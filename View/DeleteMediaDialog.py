# -*- coding: UTF-8 -*-

import wx, os
from DataBase import MediaTable
from GlobalData import ConfigData
   
class DeleteMediaDialog(wx.SingleChoiceDialog):
    def __init__(self,title):
        self.__type = type
        
        _cfg = ConfigData.ConfigData()
        self.__mediaPath = _cfg.GetMediaPath() + "/auditserver/"
        
        self.__userlist = self.getMediaList()
        
        super(DeleteMediaDialog,self).__init__(None,"选择文件",title,self.__userlist)
   
    def getMediaList(self):
        _db = MediaTable.MediaTable()
        _db.Connect()
        _res = _db.Search("select name from MediaTable")
        _db.CloseCon()
        _file = [m[0] for m in _res]
        try:
            return _file
        except:
            return []
   
    def secondButtonFun(self):
        _choice = self.GetStringSelection()
        
        _db = MediaTable.MediaTable()
        _db.Connect()
        _db.deleteMedia(_choice)
        _db.CloseCon()
        
        _path = self.__mediaPath + _choice
        try:
            os.remove(_path)
            if os.listdir(self.__mediaPath) == []:
                os.rmdir(self.__mediaPath)
        except:
            wx.MessageBox("该文件不存在","错误",wx.ICON_ERROR|wx.YES_DEFAULT)
        
    def firstButtonFun(self):
        pass
   
    def Run(self):
        _res = self.ShowModal()
        if _res == wx.ID_OK:
            self.secondButtonFun()
        elif _res == wx.ID_CANCEL:
            self.firstButtonFun()
        self.Destroy()
   
if __name__=='__main__':
    app = wx.App()
    f = DeleteMediaDialog("修改权限")
    f.Run()
    app.MainLoop()