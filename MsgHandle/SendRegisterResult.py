# -*- coding: UTF-8 -*-
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import MagicNum, CommonData
from DataBase import NOUserTable

class SendRegisterResult(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendRegisterResult,self).__init__()
    
    def verifyUser(self,name):
        "验证该用户是否已经被注册"
        _db = NOUserTable.NOUserTable()
        _db.Connect()
        _res = _db.searchUser(name)
        _db.CloseCon()
        return not _res
    
    def addNewCPUser(self,value):
        "添加新用户"
        _db = NOUserTable.NOUserTable()
        _db.Connect()
        _db.AddNewUser(value)
        _db.CloseCon()
    
    def HandleMsg(self,bufsize,session):
        "返回注册信息并保存用户名"
        _recvmsg = session.sockfd.recv(bufsize)
        _loginmsg = _recvmsg.split(CommonData.MsgHandlec.PADDING) + [MagicNum.CPUserTablec.UNACCEPT]
        _loginmsg
        if self.verifyUser(_loginmsg[0]) == False:
            restype = MagicNum.MsgTypec.REGISTERFAIL
            msghead = self.packetMsg(restype,0)
            session.sockfd.send(msghead)
        else:
            restype = MagicNum.MsgTypec.REGISTERSUCCESSMSG
            self.addNewCPUser(_loginmsg[:-2] + _loginmsg[-1:])
            session.name = _loginmsg[0]
            from CryptoAlgorithms import RsaKeyExchange
            _rke = RsaKeyExchange.RsaKeyExchange()
            _rke.WritePubkeyStr(session.name, _loginmsg[-2])
            msgbody = _rke.GetPubkeyStr("own")
            msghead = self.packetMsg(restype,len(msgbody))
            session.sockfd.send(msghead + msgbody.decode('gbk').encode("utf-8") )
