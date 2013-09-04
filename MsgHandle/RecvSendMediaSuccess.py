# -*- coding: UTF-8 -*-
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData
from DataBase import MediaTable

class RecvSendMediaSuccess(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvSendMediaSuccess,self).__init__()
    
    def HandleMsg(self,bufsize,session):
        "收到接收成功以后，改变状态为接受"
        _filename = session.filename[-session.filename[::-1].index("/"):].encode("utf-8")
        if session.threadtype == CommonData.ThreadType.ACCETPNO:
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, CommonData.MsgHandlec.SPARATE + "运营商端接收文件("+ _filename +")及参数成功")
            return
        
        _db = MediaTable.MediaTable()
        _db.Connect()
        _db.AlterMedia("status", MagicNum.MediaTablec.ACCEPT,session.filename.decode("utf-8"))
        _db.CloseCon()
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, CommonData.MsgHandlec.SPARATE + "服务端接收文件("+ _filename +")及参数成功")
