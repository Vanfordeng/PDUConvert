#!/usr/bin/env python
# _*_coding:utf-8_*_

import base
import re
import datetime

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

class Topdu(object):
    #COMMON方法
    # GSM 列奇偶(奇偶)索引值交换
    def odd_to_even(self, number):
        for x in range(len(number) - 1):
             if x % 2 != 0:
                 continue
             number[x], number[x + 1] = number[x + 1], number[x]
        return number

     # GSM 列表转换为字符串
    def list_to_string(self, lst):
        return "".join(str(x) for x in lst)

    #GSM将数字转换为pdu十六进制格式
    def number_to_pdu_hex(self,number):
        temp = hex(number)[2:]
        if len(temp) == 1:
            temp = "0" + temp
        return temp


    # GSM 字符串转换为16进制
    def string_to_hex(self, string, encoded="8-bit"):
        s_hex = ""
        # s = unicode(string, "UTF-8")
        for x in string:
            temp = hex(ord(x))[2:]
            if encoded == "8-bit":
                s_hex += temp
            elif encoded == "UCS2":
                if len(temp) == 2:
                  temp = "00" + temp
                s_hex += temp
        return s_hex

    #CDMA 将二进制字符转换为16进制
    def bin_to_hex(self,character):
        temp = int(character, base=2)
        return hex(temp)

    #CDMA 16进制，10进制,字符串转换为4位2进制
    def hex_to_4bin(self,string,base=10):
        bin_arr = []
        for y in string:
            bin_temp = bin(int(y, base=base))[2:]
            if len(bin_temp) < 4:
                bin_temp = "0" * (4 - len(bin_temp)) + bin_temp
            bin_arr.append(bin_temp)
        return bin_arr
    #CMDA字符串转换为7Bit并且去掉最高位
    def string_to_7bit_CDMA(self,s):
        s_bin = []
        for x in s:
            temp = hex(ord(x))[2:]
            s_bin_temp = ""
            for y in temp:
                bin_temp = bin(int(y, base=16))[2:]
                if len(bin_temp) < 4:
                    bin_temp = (4 - len(bin_temp)) * '0' + bin_temp
                s_bin_temp += bin_temp
            s_bin.append(s_bin_temp)
        for x in range(len(s_bin)):
            s_bin[x] = s_bin[x][1:]
        return s_bin

    #GSM字符串转换为7Bit的HEX编码
    def string_to_7bit(self,s):
        s_7bit = ""
        s_bin = self.string_to_7bit_CDMA(s)
        #编码机制转换
        for x in self.binStr_to_bin7bit(s_bin):
            temp = self.bin_to_hex(x)[2:]
            if len(temp) ==1:
                temp = "0"+ temp
            s_7bit += temp
        # print s_7bit.upper()
        return s_7bit.upper()

    # GSM将7位的字符串转换为7bit编码的7位二进制
    def binStr_to_bin7bit(self,s_bin):
        s_convert_bin = []
        if len(s_bin) ==0:
            return []
        if len(s_bin) ==1:
            return s_bin

        s_previous = s_bin[0]
        s_next = s_bin[1]
        index_bit = 1
        index_element = 1
        # print s_bin
        for x in range(len(s_bin) - 1):
            s_previous = s_next[-index_bit:] + s_previous
            s_convert_bin.append(s_previous)
            s_previous = s_next[:(7 - index_bit)]
            index_element +=1
            if index_element >=len(s_bin) and s_previous:
                s_previous = "0" * (8 - len(s_previous)) + s_previous
                s_convert_bin.append(s_previous)
                break
            if index_element >=len(s_bin):
                s_convert_bin.append(s_next)
                break
            s_next = s_bin[index_element]
            if index_bit == 7:
                index_bit = 1
                index_element +=1
                s_previous = s_next
                if index_element >= len(s_bin):
                    s_previous = "0" * (8 - len(s_previous)) + s_previous
                    s_convert_bin.append(s_previous)
                    break
                s_next = s_bin[index_element]
                continue
            index_bit += 1
        # print s_convert_bin
        return s_convert_bin

    #GSM判断传入字符串是否包含中文
    def contain_zh(self,word):
        word = word.decode()
        global zh_pattern
        match = zh_pattern.search(word)

        return match
    #CMDA 获取当前系统时间
    def get_time(self):
        return datetime.datetime.now().strftime('%y%m%d%H%M%S')

    # CDMA 将二进制字符串,切换为4位二进制数组
    def binString_to_4binArr(self,string):
        start = 0
        end = 4
        temp_4binArr =[]
        for x in range(len(string)):
            temp_4binArr.append(string[start:end])
            start += 4
            end += 4
            if start >=len(string):
                break
        return  temp_4binArr
    #CDMA 将4位2进制数组转换为16进制字符串
    def bin4_to_hexString(self,arr_temp):
        n = []
        for x in arr_temp:
            temp = self.bin_to_hex(x)
            n.append(temp[2:])
        return self.list_to_string(n)

    def int_to_8bin(self,integer):
        temp = bin(integer)[2:]
        if len(temp) < 8:
            temp = "0"* (8-len(temp)) + temp
        return temp
    def int_to_2Hex(self,integer):
        temp = hex(integer)[2:]
        if len(temp) == 1:
            temp = "0" + temp
        return temp

if __name__ == '__main__':
    topdu = Topdu()
    topdu.string_to_7bit("hello")
    print topdu.string_to_7bit_CDMA("hello")
    te = topdu.int_to_8bin(7)
    print te
    print topdu.bin_to_hex(te)

