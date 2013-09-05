# -*- coding: UTF-8 -*-
_metaclass_ = type
from wx.lib.pubsub  import Publisher
import wx

from MsgHandle import MsgHandleInterface
from GlobalData import CommonData

class RecvLoginSuccess(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(RecvLoginSuccess,self).__init__()
    
    def HandleMsg(self,bufsize,session):
        recvbuffer = session.sockfd.recv(bufsize)                                                                                       
        recvlist = recvbuffer.split(CommonData.MsgHandlec.PADDING)
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.LOGIN_SWITCH,recvlist)
        
