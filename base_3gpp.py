#!/usr/bin/env python
# _*_coding:utf-8_*_

# PDU拼接数据区（3GPP)
pdu_ABCDEFGHIJKLM = ""
pud_LENGTH = ""
# AB
"""
A：短信息中心地址长度，2位十六进制数(1字节)。
B：短信息中心号码类型，2位十六进制数。
"""
pdu_AB = "0891"  # 08 SMSC地址信息的长度 共8个八位字节(包括91),91 SMSC地址格式(TON/NPI) 用国际格式号码(在前面加‘+’)

# C
"""
C：短信息中心号码，B+C的长度将由A中的数据决定。
"""
pdu_C_smsc = ""

# DEFG
"""
D：文件头字节，2位十六进制数。
E：信息类型，2位十六进制数。
F：被叫号码长度，2位十六进制数。
G：被叫号码类型，2位十六进制数，取值同B
"""
pdu_DEFG = "11000D91"  # 11 基本参数(TP-MTI/VFP) 发送，TP-VP用相对格式, 00 消息基准值(TP-MR) 0,0D 目标地址数字个数 共13个十进制数(不包括91和‘F’),91 目标地址格式(TON/NPI) 用国际格式号码(在前面加‘+’)
# H
"""
H：被叫号码，长度由F中的数据决定。
"""
pdu_H_phone = ""
# I
"""
00 协议标识(TP-PID) 是普通GSM类型，点到点方式
"""
pdu_I = "00"  # 00 协议标识(TP-PID) 是普通GSM类型，点到点方式

# J
"""
J：数据编码方案，2位十六进制数。
"""
pdu_J_decoded = ""
# K
"""
K：有效期，2位十六进制数。
"""
pud_K = "00"
# L
"""
L：用户数据长度，2位十六进制数
"""
pdu_L = ""

# M
"""
M：用户数据，其长度由L中的数据决定。J中设定采用UCS2编码，这里是中英文的Unicode字符。
"""
pdu_M_content = ""