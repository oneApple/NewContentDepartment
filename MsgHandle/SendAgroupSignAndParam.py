# -*- coding: UTF-8 -*-
_metaclass_ = type

from MsgHandle import MsgHandleInterface
from GlobalData import CommonData, MagicNum, ConfigData
from DataBase import MediaTable
from CryptoAlgorithms import Rsa, HashBySha1

class SendAgroupSignAndParam(MsgHandleInterface.MsgHandleInterface,object):
    def __init__(self):
        super(SendAgroupSignAndParam,self).__init__()
        _cfg = ConfigData.ConfigData()
        self.__mediapath = _cfg.GetMediaPath()
    
    def APgetAgroupHashAndParam(self,session):
        "得到数据库中存放的A组参数和hash"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _dir = session.filename
        _filename =  _dir[-_dir[::-1].index("/"):]
        _res = _db.searchMedia(_filename.decode("utf-8"))
        return _res[0][1:3]
    
    def deltempFile(self,session):
        import os
        _cfg = ConfigData.ConfigData()
        _mediapath = _cfg.GetYVectorFilePath()
        _media = _mediapath + "out.ts" 
        os.remove(_media)
        _dir = _mediapath + session.filename[:session.filename.index(".")]
        for root, dirs, files in os.walk(_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            os.rmdir(root)  
    
    def getFrameNum(self,filename):
        "获取目录下文件数即帧的数目"
        print filename
        import os
        _cfg = ConfigData.ConfigData()
        _dirname = _cfg.GetYVectorFilePath() + filename[:filename.index(".")]
        _framenum = sum([len(files) for root,dirs,files in os.walk(_dirname)])
        return str(_framenum)
    
    def NOgetAgroupHashAndParam(self,session):
        "得到数据库中存放的A组参数和hash"
        _db = MediaTable.MediaTable()
        _db.Connect()
        _dir = session.filename
        _filename =  _dir[-_dir[::-1].index("/"):]
        _res = _db.searchMedia(_filename.decode("utf-8"))
        
        showmsg = "正在采样 ..."
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
        from VideoSampling import ExecuteFfmpeg,GetVideoSampling
        _meidaPath = self.__mediapath + "/auditserver/" + _dir[-_dir[::-1].index("/"):]
        _efm = ExecuteFfmpeg.ExecuteFfmpeg(_meidaPath)
        _efm.Run()
        _efm.WaitForProcess()
        
        import os
        showmsg = CommonData.MsgHandlec.SPARATE +"采样完成:\n(1)总帧数：" + self.getFrameNum(_dir[-_dir[::-1].index("/"):]) + \
                  "\n(2)文件大小(byte)：" + str(os.path.getsize(_meidaPath))
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, showmsg)
        
        _sparam = _res[0][1].split(CommonData.MsgHandlec.PADDING)
        import string
        _iparam = [string.atoi(s) for s in _sparam[:3]] + [string.atof(s) for s in _sparam[3:]]
        
        _cgvs = GetVideoSampling.GetVideoSampling(_filename[:_filename.index(".")],*_iparam)
        try:
            self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, CommonData.MsgHandlec.SPARATE + "Ａ组采样过程:")
            return _res[0][1],CommonData.MsgHandlec.PADDING.join(_cgvs.GetSampling())
        except:
            return _res[0][1],CommonData.MsgHandlec.PADDING.join("")
    
    def packMsgBody(self,session):
        "将会话密钥与A组参数用公钥加密，将采样hash用私钥加密（签名）"
        if session.threadtype == CommonData.ThreadType.CONNECTAP:
            _agroup = self.APgetAgroupHashAndParam(session)
        elif session.threadtype == CommonData.ThreadType.ACCETPNO:
            _agroup = self.NOgetAgroupHashAndParam(session)
            self.deltempFile(session)
                      
        _cfd = ConfigData.ConfigData()
        _rsa = Rsa.Rsa(_cfd.GetKeyPath())
        _plaintext = str(session.sessionkey) + CommonData.MsgHandlec.PADDING + _agroup[0]
        _pubkeyMsg = _rsa.EncryptByPubkey(_plaintext.encode("ascii"), session.peername)
        
        _hbs = HashBySha1.HashBySha1()
        _sign = _rsa.SignByPrikey(_hbs.GetHash(_agroup[1].encode("ascii"),MagicNum.HashBySha1c.HEXADECIMAL))
        _msgbody = _pubkeyMsg + CommonData.MsgHandlec.PADDING \
                              + _sign + CommonData.MsgHandlec.PADDING + _agroup[1].encode("ascii")
        showmsg = "发送采样结果：\n(1)A组参数:\n(帧总数,分组参数,帧间隔位数,混沌初值,分支参数)\n(".decode("utf8") + \
                  ",".join(_agroup[0].split(CommonData.MsgHandlec.PADDING)) + \
                  ")\n(2)A组采样:".decode("utf8") + _agroup[1] + "\n(3)A组采样签名：".decode("utf8") + _sign 
        showmsg += "\nCP用AP的公钥加密采样参数A"
        showmsg += "\nCP用其私钥加密比特串承诺值"
        showmsg += "\nCP发送加密的A组参数和加密的比特串承诺值，以及公钥加密TID发送给AP"
        self.sendViewMsg(CommonData.ViewPublisherc.MAINFRAME_APPENDTEXT, CommonData.MsgHandlec.SPARATE + showmsg)
        return _msgbody
    
    def HandleMsg(self,bufsize,session):
        msgbody = self.packMsgBody(session)
        msghead = self.packetMsg(MagicNum.MsgTypec.SENDAGROUP,len(msgbody))
        session.sockfd.send(msghead + msgbody)
        
if __name__ == "__main__":
    pass    
        