# -*- coding: UTF-8 -*-
_metaclass_ = type
from wx.lib.pubsub  import Publisher
import wx

from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum

class RecvRegisterSuccess(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvRegisterSuccess,self).__init__()
    
    def HandleMsg(self,bufsize,session):
        recvbuffer = session.sockfd.recv(bufsize)
        from CryptoAlgorithms import RsaKeyExchange
        _rke = RsaKeyExchange.RsaKeyExchange()
        _rke.WritePubkeyStr("auditserver",recvbuffer)
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.REGISTER_SWITCH,MagicNum.CPUserTablec.UNACCEPT)
        
