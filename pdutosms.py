#!/usr/bin/env python
# _*_coding:utf-8_*_

from smstopdu import Topdu
import re

class Tosms(object):

    """
    分解PDU编码字符串方法
    """

    #获取PDU编码中字符"F"出现的位置获取索引
    def get_F_number(self,string,index = 1):
        """
        index:0 表示第一个F出现的位置
        index:1表示第二个F出现的位置
        """
        index_temp  = string.find("F")
        index1_temp = string.find("F",index_temp +1)
        l = (index_temp,index1_temp)
        return l[index]

    #获取3gpp PDU编码中的编码字段
    def get_pdu_encoded(self,index,string):
        return  string[index+4:index+6]

    #获取3gpp PDU编码中的短信中心号码字段
    def get_pdu_smsc(self,index,string):
        return string[4:index+2]

    #获取3gpp PDU编码中的电话号码字段
    def get_pdu_phone(self,index,string):
        return string[string.find("0D91")+4:index+2]

    #获取3gpp PDU编码中的短信内容字段
    def get_pdu_content(self,index,string):
        return string[index+10:]

    #将ucs2 16进制数据转换为字符串数据
    def ucs2_hex_to_string(self,string):
        s = ""
        lst = re.findall(r'.{4}',string)
        for h in lst:
            s += unichr(int(h,base=16))
        return s
    #将utf-8 16进制数据转换为字符串数据
    def utf8_hex_to_string(self,string):
        s = ""
        lst = re.findall(r'.{2}',string)
        for h in lst:
            s += chr(int(h,base=16))
        return s

if __name__ == '__main__':
    s = "0891683108200805F011000D91683145603016F100000004D4F29C0E"
    s1 = "0500039B0402003300305143FF0C4F59989D00330033002E003300335143FF0C000A30106D4191CF52694F593011000A56FD5185901A7528003300330030002E00350033004D300256DE00430058004C004C67E5660E7EC63002000A30105957991052694F593011000A0034004798DE4EAB00310038595799104F59003200395206949F3002000A000A2605"
    tosms = Tosms()
    topdu = Topdu()
    # print hex_to_string(s)
    # print chr(int("75",base=16))
    # print bin(7)
    # print bin(5)
    print "----------------------------------"
    print tosms.get_F_number(s1,0)
    print tosms.get_F_number(s1)
    encoded =  tosms.get_pdu_encoded(tosms.get_F_number(s1),s1)
    smsc =  tosms.get_pdu_smsc(tosms.get_F_number(s1,0),s1)
    phone =  tosms.get_pdu_phone(tosms.get_F_number(s1),s1)
    content =  tosms.get_pdu_content(tosms.get_F_number(s1),s1)
    print "1111111111111",content
    print tosms.ucs2_hex_to_string(s1)
    print topdu.list_to_string(topdu.odd_to_even(list(smsc)))[:-1]
    print topdu.list_to_string(topdu.odd_to_even(list(phone)))[:-1]
    print encoded
    print "----------------------------------"