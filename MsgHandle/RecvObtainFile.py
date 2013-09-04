#coding=utf-8
_metaclass_ = type
from MsgHandle import MsgHandleInterface 
from GlobalData import ConfigData, CommonData

class RecvObtainFile(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvObtainFile,self).__init__() 
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetMediaPath()
    
    def HandleMsg(self,bufsize,session):
        "接收文件名,保存文件名"
        recvbuffer = session.sockfd.recv(bufsize)
        session.filename = self.__mediapath + "/auditserver/" + recvbuffer
        
        session.threadtype = CommonData.ThreadType.ACCETPNO
    
        showmsg = CommonData.MsgHandlec.SPARATE + "开始分发文件(" + recvbuffer + ")"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg)
        
        import SendDhPAndPubkey
        _sdh = SendDhPAndPubkey.SendDhPAndPubkey()
        _sdh.HandleMsg(0, session)
        