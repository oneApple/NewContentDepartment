# -*- coding: UTF-8 -*-

import wx, os, random
from GlobalData import ConfigData
from Command import DataHandleCmd
   
class SetSamplingParamsDialog(wx.Dialog):
    "获取采样参数并进行采样"
    def __init__(self,view):        
        wx.Dialog.__init__(self, None, -1, "设置采样参数")
        self.__sclist = []
        self.__view = view
        self.getFrameNum()
        
        self.__topSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.createStatic("\n选 择 采 样 参 数\n")
        self.createSpinCtrl()
        self.createButton("提交")
        
        self.SetSizer(self.__topSizer)
        self.__topSizer.Fit(self)
    
    def createButton(self,label):
        _Bt = wx.Button(self,-1,label)
        self.Bind(wx.EVT_BUTTON, self.buttonCmd, _Bt)
        self.__topSizer.Add(_Bt,0,wx.ALIGN_RIGHT)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def createStatic(self,label):
        _text = wx.StaticText(self,-1,label)
        self.__topSizer.Add(_text,0,wx.ALIGN_CENTER)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def getFrameNum(self):
        "获取目录下文件数即帧的数目"
        _cfg = ConfigData.ConfigData()
        _dir = self.__view.filename
        _filename = _dir[-_dir[::-1].index("/"):_dir.index(".")]
        _mediadir = _cfg.GetYVectorFilePath() + _filename
        self.__framenum = sum([len(files) for root,dirs,files in os.walk(_mediadir)])
    
    def createSpinCtrl(self):
        _labelList = [" A 组 组 数   "," A组帧间隔 "," B 组 组 数   "," B组帧间隔 "]
        _maxnumList = [self.__framenum,1,self.__framenum,1]
        
        for _label,_maxnum in zip(_labelList,_maxnumList):
            self.createSingleSpinCtrl(_label,_maxnum)
    
    def createSingleSpinCtrl(self,label,maxnum):
        _hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        _label = wx.StaticText(self,-1,label)
        _sc = wx.SpinCtrl(self, -1,size = (100,30))
        _sc.SetRange(1,maxnum)
        _sc.SetValue(1) 
        self.Bind(wx.EVT_SPINCTRL, self.OnScrollChanged,_sc)
        
        _hbox.Add(_label,0,wx.ALIGN_CENTER)
        _hbox.Add(_sc,0,wx.EXPAND)
        
        self.__sclist.append(_sc)
        self.__topSizer.Add(_hbox,0,wx.EXPAND)
        self.__topSizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    
    def OnScrollChanged(self,event):
        _spin = event.GetEventObject()
        if _spin == self.__sclist[0]:
            _value = self.getGroupLen(_spin.GetValue(), self.__framenum / _spin.GetValue())
            self.__sclist[1].SetRange(1,_value)
            self.__sclist[1].SetValue(1)
        elif _spin == self.__sclist[2]:
            _value = self.getGroupLen(_spin.GetValue(), self.__framenum / _spin.GetValue())
            self.__sclist[3].SetRange(1,_value)
            self.__sclist[3].SetValue(1)
    
    def getGroupLen(self,gt,glen):
        "获取分组长度(参数X),_glen是每组的帧数目"
        _glen = glen - 1
        _x = 1
        while _glen >= 2:
            _glen = _glen / 2
            _x += 1
        if (self.__framenum / gt - 1) < 2 ** _x:
            _x -= 1
        return _x
    
    def getSamplingParams(self):
        _valueList = []
        for _value in self.__sclist:
            _valueList.append(_value.GetValue())
        aparams = [self.__framenum,_valueList[0],_valueList[1],random.random(),random.uniform(3.5699456,4.0)]
        bparams = [self.__framenum,_valueList[2],_valueList[3],random.random(),random.uniform(3.5699456,4.0)]
        return aparams,bparams
    
    def buttonCmd(self,event):
        _cmd = DataHandleCmd.DataHandleCmd(self.__view,*self.getSamplingParams())
        _cmd.Excute()
        self.Destroy()
    
    def Run(self):
        self.Center()
        self.ShowModal()
        
if __name__=='__main__': 
    app = wx.App()
    s = SetSamplingParamsDialog("采样参数设置")
    s.Run()
    app.MainLoop()