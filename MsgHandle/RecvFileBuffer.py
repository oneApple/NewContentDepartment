# -*- coding: UTF-8 -*-

_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum,CommonData

class RecvFileBuffer(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvFileBuffer,self).__init__() 
        
    def HandleMsg(self,bufsize,session):
        if not session.currentbytes:
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,"开始接收文件(" + session.filename + ") ...")
        recvbuffer = session.sockfd.recv(bufsize)
        session.currentbytes += len(recvbuffer)
        session.file.write(recvbuffer)
        msghead = self.packetMsg(MagicNum.MsgTypec.REQFILEBUFFER, 0)
        session.sockfd.send(msghead)