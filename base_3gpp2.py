#!/usr/bin/env python
# _*_coding:utf-8_*_

# PDU拼接数据区（3GPP2)
pdu_ABCDEFGHIJKLMNOPQRSTU = ""
pud_LENGTH = ""

"""
(SMS_MSG_TYPE)
A:SMS Point-to-Point  点对点传输
"""
pud_A = "00"

"""
(Teleservice Identifier)
B:0×00, 表示uTeleserviceID字段
C:0×02, 字段长度，该长度必须为2，否则为错误的pdu信息
D:字段内容为：0×1002,十进制是4098,表示teleserviceid
"""
pdu_BCD = "00021002"

"""
(Address Parameters)
E:02  = PARAMETER_ID ,   这里表示源地址  Originating Address parameter, this field shall be set to ‘00000010’.
F:07  = PARAMETER_LEN， SMS message parameter length.
"""
pdu_EF="0207"
"""
G:被叫号码

00 00001011   00 第一个 0 = DIGIT_MODE，4-bit DTMF  第二个 0 = NUMBER_MODE
              00001011  1(十进制)  表示  后面紧跟了  一个 11 位的号码。
00 01  
10 00
00 01
00 10
01 00
00 01
10 01
00 11
00 01
00 11
01 01
00
    
1882093135
"""
pdu_G_phone = ""

"""
H：表示SMS_TL_BEARER_RPLY_OPT，具体使用意义尚不清楚。
"""
pdu_H = "06014C"

"""
I:0×08, 表示SMS_TL_BEARER_DATA字段（短信内容）
"""
pdu_I = "08"
"""
J:短信内容字段长度
"""
pdu_J = ""

"""
K:Mesage Id TAG
L:内容长度
"""
pdu_KL="0003"

"""
M:DELIVER 短信
N:Messag ID
O:HEADER_IND

10 1B B0  === 0001 0000 0001 1011 1011 0000
0001 表示 DELIVER 短信
0000 0001 1011 1011表示 message id, 与CMGS发送后上报的数据一致。
紧接后面的 0, 表示HEADER_IND
"""
pdu_MNO="200000"
"""
P:字段类型
Q：字段长度
R：短信编码，短信内容
102e8cbb
0001 0000 0010 1110 1000 1100   1011 1011
0001 0  =  MSG_ENCODING ：  表示 7-bit 编码，   00100  表示 16-bit  unicode 编码,  00000  表示 8-bit  编码
000 0010 1 -->  5 (十进制) = NUM_FIELDS ：表示后面有5个 7-bit 编码的数据 
110 1000  -->  0x68  （ASCII 码） ： h 
"""
pud_P ="01"
pud_Q = ""
pdu_R_content = ""

"""
S:时间戳字段标识
T:字段长度
U:字段内容 140901112631 4 YEAR，  09 MONTH,   01 DAY,  11 HOURS,  26 MINUTES,  31 SECONDS
"""
pdu_S ="03"
pdu_T = "06"
pdu_U = ""
