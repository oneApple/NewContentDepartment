# -*- coding: UTF-8 -*-

_metaclass_ = type
from NetCommunication import NetSocketFun

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum,CommonData
from NetCommunication import NetSocketFun


class RecvAllFile(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvAllFile,self).__init__() 
        
    def HandleMsg(self,bufsize,session):
        recvbuffer = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        session.file.write(recvbuffer)
        session.file.close()
        if session.threadtype == CommonData.ThreadType.ACCETPNO:
            msghead = self.packetMsg(MagicNum.MsgTypec.REQAGROUP, 0)
        elif session.threadtype == CommonData.ThreadType.ACCEPTAP:
            msghead = self.packetMsg(MagicNum.MsgTypec.REQCGROUP, 0)
        showmsg = "文件接收完毕:\n(1)文件名:" + session.filename + "\n(2)文件大小:" + str(session.currentbytes + bufsize)
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)
        NetSocketFun.NetSocketSend(session.sockfd,msghead)
        session.currentbytes = 0

