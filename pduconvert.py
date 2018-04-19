#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
author:Dengqihong
data:2018_03_13
"""

import sys
import wx
from smstopdu import Topdu
from pdutosms import Tosms
import base_3gpp as b3
import base_3gpp2 as b32
from ui import PDUConvertUI

reload(sys)
sys.setdefaultencoding('utf-8')

class SMSC(object):
    CD = {"CMCC":"+8613800280500",
          "CU":"+8613010811500",
          "CT":""}

    SH = {"CMCC":"+8613800210500",
          "CU":"+8613010314500",
          "CT":""}

    ADDRESS = {"CD":CD,"SH":SH}

PDU_encoded = {
    "7-bit":"00",
    "8-bit":"04",
    "UCS2":"08"
}

class PDUConvert(PDUConvertUI):
    def __init__(self,parent,title):
        super(PDUConvert,self).__init__(parent,title = title)
        self.topdu = Topdu()
        self.tosms = Tosms()
        #Common 数据区
        self._local = ""
        self._smsc = ""
        self._phone = ""
        self._encoded =""
        self._content = ""
        self._cur_opeartion = ""
        #初始化---------------------------------------------------------
        #初始化区域
        self._local = self.combox1.GetValue()
        #初始化短信中心号码
        self.cur_address = SMSC.ADDRESS["CD"]
        self._cur_opeartion = "CMCC"
        self.txt_SMSC.SetValue(self.cur_address[self._cur_opeartion])
        self._smsc = self.txt_SMSC.GetValue()
        #初始化电话号码
        self._phone = self.txt_Phone.GetValue()
        #初始化编码
        self._encoded = self.rb_encoded.GetStringSelection()
        #初始化短信内容
        self._content = self.txt_Content.GetValue()
        # ---------------------------------------------------------

    #获取区域
    def OnCombo(self,event):
        obj = event.GetEventObject()
        str_temp = obj.GetStringSelection()
        if str_temp == "成都":
            self._local = self.combox1.GetValue()
            self.cur_address= SMSC.ADDRESS["CD"]
            self.txt_SMSC.SetValue(self.cur_address.get(self._cur_opeartion))
        else:
            self._local = self.combox1.GetValue()
            self.cur_address = SMSC.ADDRESS["SH"]
            self.txt_SMSC.SetValue(self.cur_address.get(self._cur_opeartion))
    #获取运营商
    def OnRadioGroup(self,event):
        obj = event.GetEventObject()
        self.txt_SMSC.SetValue(self.cur_address.get("CMCC","Null"))
        if obj.GetId() == 11:
            self._smsc = self.cur_address.get("CMCC","Null")
            self._cur_opeartion="CMCC"
            self.txt_SMSC.SetValue(self._smsc)
        elif obj.GetId() == 12:
            self._smsc = self.cur_address.get("CU","Null")
            self._cur_opeartion = "CU"
            self.txt_SMSC.SetValue(self._smsc)
        elif obj.GetId() == 13:
            self._smsc = self.cur_address.get("CT", "Null")
            self._cur_opeartion = "CT"
            self.txt_SMSC.SetValue(self._smsc)
        self._smsc = self.txt_SMSC.GetValue()

    #运营商输入事件
    def OnSMSCTextEnter(self,event):
        obj = event.GetEventObject()
        self._smsc = obj.GetValue()

    #获取电话号码
    def OnPhoneTextEnter(self,event):
        obj = event.GetEventObject()
        self._phone = obj.GetValue()
    #获取编码
    def OnRadioBox(self,event):
        self._encoded = self.rb_encoded.GetStringSelection()
    #获取内容
    def OnContentTextEnter(self,event):
        obj = event.GetEventObject()
        self._content = obj.GetValue()

    #生成PDU--button事件
    def OnBtnGenerate(self,event):

        print "self._local:",self._local
        print "self._smsc:",self._smsc
        print "self._phone:",self._phone
        print "self._encoded:",self._encoded
        print "self._content:",self._content
        print "self._cur_opeartion:",self._cur_opeartion
        print "------------------分隔符---------------"

        if self._cur_opeartion != "CT":
            #PDU短信中心号码
            if "F" not in self._smsc:
                _smsc_temp = self._smsc[1:] + "F"
                b3.pdu_C_smsc = self.topdu.list_to_string(self.topdu.odd_to_even(list(_smsc_temp)))

            #PDU电话号码
            if "F" not in self._phone:
                _phone_temp = self._phone[1:] + "F"
                b3.pdu_H_phone = self.topdu.list_to_string(self.topdu.odd_to_even(list(_phone_temp)))
            # print b3.pdu_H_phone

            #PDU短信内容

            if self.topdu.contain_zh(self._content) and (self._encoded == "7-bit" or self._encoded == "8-bit"):
                dlg = wx.MessageDialog(self, "7-bit/8-bit不支持中文", "错误类型", wx.OK)
                dlg.ShowModal()

            if self._encoded == "7-bit":
                b3.pdu_M_content = self.topdu.string_to_7bit(self._content)
                b3.pdu_J_decoded = PDU_encoded[self._encoded]
            elif self._encoded == "8-bit":
                b3.pdu_M_content = self.topdu.string_to_hex(self._content,encoded="8-bit")
                b3.pdu_J_decoded = PDU_encoded[self._encoded]
            elif self._encoded == "UCS2":
                b3.pdu_M_content = self.topdu.string_to_hex(self._content,encoded="UCS2")
                b3.pdu_J_decoded = PDU_encoded[self._encoded]
            else:
                b3.pdu_M_content = ""
                b3.pdu_J_decoded = ""

            #PDU用户信息长度
            b3.pdu_L = self.topdu.number_to_pdu_hex(len(b3.pdu_M_content)/2).upper()
            if self._encoded == "7-bit":
                b3.pdu_L = self.topdu.number_to_pdu_hex(len(self.topdu.string_to_7bit_CDMA(self._content))).upper()

            #整理pdu_ABCDEFGHIJKLM 和pud_LENGTH
            b3.pud_LENGTH =b3.pdu_DEFG +b3.pdu_H_phone+b3.pdu_I+b3.pdu_J_decoded+b3.pud_K+b3.pdu_L+b3.pdu_M_content
            b3.pdu_ABCDEFGHIJKLM = b3.pdu_AB + b3.pdu_C_smsc + b3.pud_LENGTH
            pdu_length = str(len(b3.pud_LENGTH)/2)

            self.txt_PDUdata.SetValue("AT+CMGS=%s" % pdu_length + "\r\n" +
                                      "AT+CMGW=%s" % pdu_length + "\r\n" +
                                      b3.pdu_ABCDEFGHIJKLM.upper())

        if self._cur_opeartion == "CT":

            if self.topdu.contain_zh(self._content) and (self._encoded == "7-bit" or self._encoded == "8-bit"):
                dlg = wx.MessageDialog(self, "7-bit/8-bit不支持中文", "错误类型", wx.OK)
                dlg.ShowModal()

            # CDMA PDU电话号码
            if "+86" in self._phone:
                self._phone = self._phone[3:] #处理能够被CDMA处理的电话号码格式

            bin_A_phone = '0000001011'
            bin_B_phone = self.topdu.list_to_string(self.topdu.hex_to_4bin(self._phone))  #处理电话号码
            bin_End_phone = bin_A_phone + bin_B_phone + "00"
            b32.pdu_G_phone = self.topdu.bin4_to_hexString(self.topdu.binString_to_4binArr(bin_End_phone)).upper()

            #CDMA PDU短信内容
            bin_A_content_encoded = "00010"  #00010表示7-bit编码
            bin_7bit_arr = self.topdu.string_to_7bit_CDMA(self._content)
            bin_B_content_length = self.topdu.int_to_8bin(len(bin_7bit_arr))
            bin_C_content = self.topdu.list_to_string(bin_7bit_arr)
            bin_End_content = bin_A_content_encoded + bin_B_content_length + bin_C_content

            #给二进制内容不足4位的补0
            if len(bin_End_content)%8 != 0:
                bin_End_content = bin_End_content + "0" * (8-len(bin_End_content)%8)
            # if (len(bin_End_content)-13)%7 != 0:
            #     bin_End_content = bin_End_content + "0" * (7-(len(bin_End_content)-13)%7)

            b32.pdu_R_content = self.topdu.bin4_to_hexString(self.topdu.binString_to_4binArr(bin_End_content)).upper()
            b32.pud_Q = self.topdu.int_to_2Hex(len(b32.pdu_R_content)/2)
            #处理时间戳
            b32.pdu_U = self.topdu.get_time()

            #处理PDU数据长度
            b32.pud_LENGTH = b32.pdu_KL + b32.pdu_MNO + b32.pud_P + b32.pud_Q + b32.pdu_R_content + b32.pdu_S + b32.pdu_T + b32.pdu_U
            b32.pdu_J = self.topdu.int_to_2Hex(len(b32.pud_LENGTH) / 2)
            b32.pdu_ABCDEFGHIJKLMNOPQRSTU = b32.pud_A + b32.pdu_BCD + b32.pdu_EF +b32.pdu_G_phone + b32.pdu_H + b32.pdu_I +b32.pdu_J + b32.pud_LENGTH
            pdu_length = str(len(b32.pdu_ABCDEFGHIJKLMNOPQRSTU) / 2)
            self.txt_PDUdata.SetValue("AT+CMGS=%s" % pdu_length + "\r\n" +
                                      "AT+CMGW=%s" % pdu_length + "\r\n" +
                                       b32.pdu_ABCDEFGHIJKLMNOPQRSTU.upper())
    # 解析PDU--button事件
    def OnBtnRestore(self,event):
        # self.txt_Content.SetValue("")
        if self.txt_PDUdata.GetValue().startswith("AT+CMGS="):
            self.SetValue(self._smsc,self._phone,self._encoded,self._content)

        if self.txt_PDUdata.GetValue().startswith("0891"):
            self._content = self.txt_PDUdata.GetValue()
            encoded_temp = self.tosms.get_pdu_encoded(self.tosms.get_F_number(self._content),self._content)
            print "encoded_temp:", encoded_temp
            self._encoded = list(PDU_encoded.keys())[list(PDU_encoded.values()).index(encoded_temp)]

            smsc = self.tosms.get_pdu_smsc(self.tosms.get_F_number(self._content, 0), self._content)
            self._smsc = self.topdu.list_to_string(self.topdu.odd_to_even(list(smsc)))[2:-1]
            phone = self.tosms.get_pdu_phone(self.tosms.get_F_number(self._content), self._content)
            self._phone = self.topdu.list_to_string(self.topdu.odd_to_even(list(phone)))[2:-1]
            content = self.tosms.get_pdu_content(self.tosms.get_F_number(self._content),self._content)
            if self._encoded == "8-bit":
                self._content = self.tosms.utf8_hex_to_string(content)
            elif self._encoded == "UCS2":
                self._content = self.tosms.ucs2_hex_to_string(content)
            elif self._encoded == "7-bit":
                pass
            else:
                pass
            self.SetValue(self._smsc, self._phone, self._encoded, self._content)

        else:
            self._content = self.txt_PDUdata.GetValue()
            self._content = self.tosms.ucs2_hex_to_string(self._content)
            self.txt_Content.SetValue(self._content)

    def SetValue(self,smsc="",phone="",encoded="",content=""):
        self.txt_Content.SetValue("短信中心号码：%s " % smsc + "\r\n" +
                                  "电话号码：%s " % phone + "\r\n" +
                                  "编码：%s " % encoded + "\r\n" +
                                  "短信内容：%s " % content + "\r\n")

if __name__ == '__main__':
    app = wx.App()
    frame = PDUConvert(None,"PDUConvert 0.1")
    frame.SetMaxSize((400,600))
    app.MainLoop()