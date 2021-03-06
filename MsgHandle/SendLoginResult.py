# -*- coding: UTF-8 -*-
_metaclass_ = type

from NetCommunication import NetSocketFun
from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData
from DataBase import NOUserTable

class SendLoginResult(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendLoginResult,self).__init__()
    
    def verifyUser(self,name,psw):
        "验证用户名密码的正确性"
        _db = NOUserTable.NOUserTable()
        _db.Connect()
        _res = _db.VerifyNamePsw(name, psw)
        _db.CloseCon()
        return _res
    
    def HandleMsg(self,bufsize,session):
        "返回登录结果，并保存用户名"
        recvmsg = NetSocketFun.NetSocketRecv(session.sockfd,bufsize)
        _loginmsg = NetSocketFun.NetUnPackMsgBody(eval(recvmsg))[0]
        _res = self.verifyUser(_loginmsg[0], _loginmsg[1])
        if  _res != False:
            msgbody = NetSocketFun.NetPackMsgBody([str(_res)])
            msghead = self.packetMsg(MagicNum.MsgTypec.LOGINSUCCESS,len(msgbody))
            NetSocketFun.NetSocketSend(session.sockfd,msghead + msgbody)
            session.peername = _loginmsg[0]
            showmsg = session.peername + "登录成功"
        else:
            msghead = self.packetMsg(MagicNum.MsgTypec.LOGINFAIL,0)
            NetSocketFun.NetSocketSend(session.sockfd,msghead)
            showmsg = session.peername + "登录失败"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg,True)