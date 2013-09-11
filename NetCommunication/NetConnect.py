# -*- coding: UTF-8 -*-
import socket, struct

import NetThread
from CryptoAlgorithms import RsaKeyExchange
from GlobalData import CommonData, ConfigData, MagicNum


_metaclass_ = type
class NetConnect:
    def __init__(self,view):
        self.__Sockfd = socket.socket()
        self.view = view  
    
    def ChangeView(self,view):
        self.view = view    
        
    def ReqConnect(self,name,psw):
        "请求登录"
        _msgbody = MagicNum.UserTypec.CPUSER + CommonData.MsgHandlec.PADDING + name + CommonData.MsgHandlec.PADDING + psw
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQLOGINMSG,len(_msgbody))
        self.__Sockfd.send(_msghead + _msgbody)
    
    def ReqRegister(self,name,psw,ip,port):
        "请求注册"
        _rke = RsaKeyExchange.RsaKeyExchange()
        _rke.GenerateRsaKey()
        _pkeystr = _rke.GetPubkeyStr("own")
        _msgbody = name + CommonData.MsgHandlec.PADDING + \
                   psw + CommonData.MsgHandlec.PADDING + \
                   ip + CommonData.MsgHandlec.PADDING + \
                   port + CommonData.MsgHandlec.PADDING + \
                   _pkeystr
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQREGISTERMSG,len(_msgbody))
        self.__Sockfd.send(_msghead + _msgbody.decode('gbk').encode("utf-8"))
        
    def ReqAudit(self,filename):
        "请求审核" 
        self.filename = filename
        _msgbody = filename[-filename[::-1].index("/"):].encode("utf-8")
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQAUDITMSG, len(_msgbody))
        self.__Sockfd.send(_msghead + _msgbody)
        
        import wx
        from wx.lib.pubsub  import Publisher
        wx.CallAfter(Publisher().sendMessage,CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT,["请求审核文件(" + _msgbody + ")".encode("utf8"),False])
        
    def StartNetConnect(self):
        "连接服务器并开启网络线程"
        config = ConfigData.ConfigData()
        _auditAddress = config.GetAuditServerAddress()
        try:
            self.__Sockfd.connect((_auditAddress[0],int(_auditAddress[1])))
        except:
            return MagicNum.NetConnectc.NOTCONNECT
        self.__netThread = NetThread.NetThread(self.__Sockfd.dup(),self,CommonData.ThreadType.CONNECTAP)
        self.__netThread.setDaemon(True)
        self.__netThread.start()
        
    def StopNetConnect(self):
        "发送关闭消息并关闭网络线程"
        _msghead = struct.pack(CommonData.MsgHandlec.MSGHEADTYPE,MagicNum.MsgTypec.REQCLOSEMSG, 0)
        self.__Sockfd.send(_msghead)
        self.__netThread.stop()
        #放在主线程主执行
        
if __name__=='__main__':
    filename = "/home/keym/视频/小伙.mpg"
    _msgbody = filename[-filename[::-1].index("/"):].encode("utf-8")
