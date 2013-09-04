# -*- coding: UTF-8 -*-
_metaclass_ = type

import wx
from wx.lib.pubsub  import Publisher

class CommandInterface:
    def __init__(self,view):
        self.view = view
    
    def sendViewMsg(self,msgtype,msg):
        wx.CallAfter(Publisher().sendMessage,msgtype,msg)     
        
    def Excute(self):
        pass