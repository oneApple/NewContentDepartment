#coding=utf-8
_metaclass_ = type
from MsgHandle import MsgHandleInterface 
from NetCommunication import NetSocketFun
from GlobalData import ConfigData,CommonData

class RecvFilename(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvFilename,self).__init__() 
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetMediaPath()
    
    def createMediaDir(self,session):
        "创建媒体存放目录"
        import os 
        self.___ownPath = self.__mediapath + "/" + "auditserver"
        if not os.path.exists(self.___ownPath):
            if not os.path.exists(self.__mediapath):
                os.mkdir(self.__mediapath)
            os.mkdir(self.___ownPath)
    
    def HandleMsg(self,bufsize,session):
        "接收文件名，并打开文件准备写"
        recvbuffer = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        self.createMediaDir(session)
        session.filename = recvbuffer
        
        session.threadtype = CommonData.ThreadType.ACCEPTAP
        
        _localfilename = self.___ownPath + "/" + session.filename
        session.file = open(_localfilename.encode('utf-8'),"w")
        session.currentbytes = 0
    
        showmsg = "开始审核返回文件(" + recvbuffer + ")"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
        
        import SendDhPAndPubkey
        _sdh = SendDhPAndPubkey.SendDhPAndPubkey()
        _sdh.HandleMsg(0, session)
        