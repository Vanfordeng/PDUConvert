#!/usr/bin/env python
# _*_coding:utf-8_*_

import wx
import win32api
"""
author:Dengqihong
data:2018_03_13
"""
class PDUConvertUI(wx.Frame):
    def __init__(self,parent,title):
        super(PDUConvertUI,self).__init__(parent,title = title,size=(400,600))
        exeName = win32api.GetModuleFileName(win32api.GetModuleHandle(None))
        icon = wx.Icon(exeName,wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon)
        # self.SetIcon(wx.Icon(name="pduconvert.ico", type=wx.BITMAP_TYPE_ICO))
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox_total = wx.BoxSizer(wx.VERTICAL)

        #SMSC
        staticbox1 = wx.StaticBox(panel,wx.ID_ANY,"短信息中心")
        sbsizer1 = wx.StaticBoxSizer(staticbox1,wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.choices = ["成都","上海"]
        self.combox1 = wx.ComboBox(panel,wx.ID_ANY,value=self.choices[0],size =(120,30),choices = self.choices)
        hbox1.Add(self.combox1,0,wx.ALIGN_CENTER_HORIZONTAL,5)
        self.combox1.GetStringSelection()
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.rb1 = wx.RadioButton(panel,11,label="中国移动",style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(panel,12,label="中国联通")
        self.rb3 = wx.RadioButton(panel,13,label="中国电信")
        hbox2.Add(self.rb1,0,wx.Centre)
        hbox2.Add(self.rb2,0,wx.Centre)
        hbox2.Add(self.rb3,0,wx.Centre)
        self.txt_SMSC = wx.TextCtrl(panel,wx.ID_ANY,size =(180,25),style = wx.ALIGN_LEFT)

        #Phone Number
        staticbox2 = wx.StaticBox(panel,wx.ID_ANY,"电话号码")
        sbsizer2 = wx.StaticBoxSizer(staticbox2,wx.HORIZONTAL)
        self.txt_Phone = wx.TextCtrl(panel,wx.ID_ANY,value="+86",size=(180,25),style = wx.ALIGN_LEFT)

        #Encoded
        # staticbox3 = wx.StaticBox(panel,wx.ID_ANY,"编码")
        # sbsizer3 = wx.StaticBoxSizer(staticbox3,wx.HORIZONTAL)
        # self.rb_encoded1 = wx.RadioButton(panel,21,label="7-bit",style=wx.RB_GROUP)
        # self.rb_encoded2 = wx.RadioButton(panel,22,label="8-bit")
        # self.rb_encoded3 = wx.RadioButton(panel,33,label="USC2")
        self.encoded = ["7-bit","8-bit","UCS2"]
        self.rb_encoded = wx.RadioBox(panel,label = "编码",choices = self.encoded,majorDimension=1,style = wx.RA_SPECIFY_ROWS)

        #Conent
        staticbox4 = wx.StaticBox(panel,wx.ID_ANY,"短信内容")
        sbsizer4 = wx.StaticBoxSizer(staticbox4,wx.HORIZONTAL)
        self.txt_Content = wx.TextCtrl(panel,wx.ID_ANY,size =(400,100),style = wx.TE_MULTILINE)

        #PDU Data
        staticbox5 = wx.StaticBox(panel,wx.ID_ANY,"PDU数据")
        sbsizer5 = wx.StaticBoxSizer(staticbox5,wx.HORIZONTAL)
        self.txt_PDUdata = wx.TextCtrl(panel,wx.ID_ANY,size =(400,100),style = wx.TE_MULTILINE)
        font = wx.Font(9, wx.DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.txt_PDUdata.SetFont(font)

        #按钮（生成数据包）,(还原数据包）
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_generate = wx.Button(panel,wx.ID_ANY,label ="生成数据包")
        self.btn_restore = wx.Button(panel,wx.ID_ANY,label ="还原数据包")
        hbox3.Add((40,0))
        hbox3.Add(self.btn_generate,0,wx.Centre,10)
        hbox3.Add((60, 0))
        hbox3.Add(self.btn_restore,0,wx.Centre,10)

        #事件绑定：
        self.combox1.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        self.Bind(wx.EVT_RADIOBUTTON,self.OnRadioGroup)
        self.rb_encoded.Bind(wx.EVT_RADIOBOX,self.OnRadioBox)
        self.txt_Content.Bind(wx.EVT_TEXT,self.OnContentTextEnter)
        self.txt_Phone.Bind(wx.EVT_TEXT,self.OnPhoneTextEnter)
        self.btn_generate.Bind(wx.EVT_BUTTON,self.OnBtnGenerate)
        self.btn_restore.Bind(wx.EVT_BUTTON,self.OnBtnRestore)
        self.txt_SMSC.Bind(wx.EVT_TEXT,self.OnSMSCTextEnter)

        #sbsizer，StaticBoxSizer 添加Sizer
        sbsizer1.Add(hbox1,0,wx.Centre,5)
        sbsizer1.Add(hbox2,0,wx.Centre,5)
        sbsizer1.Add((10,10))
        sbsizer1.Add(self.txt_SMSC,0,wx.Centre,5)
        sbsizer2.Add(self.txt_Phone,0,wx.Centre,5)
        # sbsizer3.Add(self.rb_encoded1,0,wx.Centre)
        # sbsizer3.Add((18,10))
        # sbsizer3.Add(self.rb_encoded2,0,wx.Centre)
        # sbsizer3.Add((22,10))
        # sbsizer3.Add(self.rb_encoded3,0,wx.Centre)
        sbsizer4.Add(self.txt_Content,0,wx.Centre,5)
        sbsizer5.Add(self.txt_PDUdata,0,wx.Centre,5)

        #vbox_total添加sizer
        vbox_total.Add((10,10))
        vbox_total.Add(sbsizer1,0,wx.Centre,5)
        vbox_total.Add(sbsizer2,0,wx.Centre,5)
        vbox_total.Add(self.rb_encoded,0,wx.Centre,5)
        vbox_total.Add(sbsizer4,0,wx.Centre,5)
        vbox_total.Add(sbsizer5,0,wx.Centre,5)
        vbox_total.Add((0,20))
        vbox_total.Add(hbox3,0,wx.Centre,5)

        #panel 添加Sizer
        panel.SetSizer(vbox_total)
        self.Centre()
        self.Show()

    def OnCombo(self,event):
        pass

    def OnRadioGroup(self,event):
        pass

    def OnRadioBox(self,event):
        pass

    def OnBtnGenerate(self,event):
        pass

    def OnBtnRestore(self,event):
        pass

    def OnContentTextEnter(self,event):
        pass

    def OnPhoneTextEnter(self,event):
        pass

    def OnSMSCTextEnter(self,event):
        pass

if __name__ == '__main__':
    app = wx.App()
    frame = PDUConvertUI(None,"PDUConvert 0.1")
    frame.SetMaxSize((400,600))
    app.MainLoop()
