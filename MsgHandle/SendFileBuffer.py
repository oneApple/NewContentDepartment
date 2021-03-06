#coding=utf-8
_metaclass_ = type
from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum, ConfigData

class SendFileBuffer(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendFileBuffer,self).__init__()
    
    def handleFileBegin(self,bufsize,session):
        "第一次发送则打开文件"
        if not session.filename or session.filename != session.control.filename:
            session.filename = session.control.filename.decode("utf8")
        session.file = open(session.filename,"rb")
        import os
        session.totalbytes = os.path.getsize(session.filename)
        
        _filename = session.filename[-session.filename[::-1].index("/"):].encode("utf-8")
        showmsg = "开始发送文件(" + _filename + ")..."
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
    
    def HandleMsg(self,bufsize,session):
        if not session.currentbytes and session.threadtype != CommonData.ThreadType.CONNECTAP:
            _cfg = ConfigData.ConfigData()
            _dir = _cfg.GetMediaPath() + "/auditserver/" 
            recvbuffer = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
            session.control.filename = _dir + NetSocketFun.NetUnPackMsgBody(recvbuffer)[0]
        if not session.currentbytes:
            self.handleFileBegin(bufsize, session)
        _filebuffer = session.file.read(CommonData.MsgHandlec.FILEBLOCKSIZE)
        session.currentbytes += len(_filebuffer)
        msgbody = NetSocketFun.NetPackMsgBody([_filebuffer])
        if session.currentbytes == session.totalbytes:
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDFILEOVER,len(msgbody))
            session.file.close()
            session.currentbytes = 0
            
            _filename = session.filename[-session.filename[::-1].index("/"):].encode("utf-8")
            filesize = float(session.totalbytes) / (1024 * 1024)
            showmsg = "文件发送完毕:\n(1)文件名:" + _filename + "\n(2)文件大小（MB）:" + str(filesize)
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,showmsg,True)
        else:
            msghead = self.packetMsg(MagicNum.MsgTypec.SENDFILEBUFFER,len(msgbody))
        NetSocketFun.NetSocketSend(session.sockfd, msghead + msgbody)
        