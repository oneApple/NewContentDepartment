# -*- coding: UTF-8 -*-
import threading, socket

import NetThread
from GlobalData import MagicNum, ConfigData

_metaclass_ = type
class NetAcceptThread(threading.Thread):
    def __init__(self):
        super(NetAcceptThread,self).__init__()
        self.__runflag = True
        self.__threadlist = []
        
    def run(self):
        "监听，每当有一个新的连接请求则创建新的线程"
        self._listenfd = socket.socket()
        config = ConfigData.ConfigData()
        _listenAddress = config.GetLocalServerAddress()
        try:
            self._listenfd.bind((_listenAddress[0],int(_listenAddress[1])))
        except Exception,e:
            print e
            self._listenfd.close();
            return MagicNum.NetAcceptc.BINDERROR
        
        self._listenfd.listen(MagicNum.NetAcceptc.MAXLISTENNUM)
        while self.__runflag:
            c,addr = self._listenfd.accept()
            s = 'Got connect from:' + str(addr) + "\n"
            print s
            th = NetThread.NetThread(c.dup(),self,True)
            self.__threadlist.append(th)
            th.start()
            c.close()
        self._listenfd.close();
        
    def closeNetThread(self,th):
        th.stop()
        #th.join()
        self.__threadlist.remove(th)
            
    def stop(self):
        "关闭所有线程"
        while self.__threadlist:
            th = self.__threadlist[0]
            th.stop()
            #th.join()
            self.__threadlist.remove(th)
        self.__runflag = False
        
        