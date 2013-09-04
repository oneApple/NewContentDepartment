# -*- coding: UTF-8 -*-
_metaclass_ = type
import os

from GlobalData import ConfigData, CommonData, MagicNum
from MsgHandle import MsgHandleInterface

class SendFileList(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendFileList,self).__init__()
        _cfg = ConfigData.ConfigData()
        self.mediaPath = _cfg.GetMediaPath() + "/auditserver"
    
    def HandleMsg(self,bufsize,session):
        try:
            _fileList = os.listdir(self.mediaPath) 
        except:
            _fileList = []
        _msgbody =  CommonData.MsgHandlec.PADDING.join(_fileList)
        _msghead = self.packetMsg(MagicNum.MsgTypec.SENDFILELIST, len(_msgbody))
        session.sockfd.send(_msghead + _msgbody)