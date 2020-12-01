# -*- coding:utf-8 -*-

# test program
# Search all over the error code

<<<<<<< HEAD
# b-cap Lib URL
=======
# b-cap Lib URL 
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
# https://github.com/DENSORobot/orin_bcap

import random
import time

import pybcapclient.bcapclient as bcapclient

<<<<<<< HEAD
# set IP Address , Port number and Timeout of connected RC8
=======
### set IP Address , Port number and Timeout of connected RC8
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
host = "127.0.0.1"
port = 5007
timeout = 2000

<<<<<<< HEAD
# Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

# set Parameter
Name = ""
Provider = "CaoProv.DENSO.VRC"
=======
### Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
print("Open Connection")

### start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

### set Parameter
Name = ""
Provider="CaoProv.DENSO.VRC"
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
Machine = "localhost"
Option = ""


<<<<<<< HEAD
# Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect RC8")
print(hCtrl)
# Get Robot Handle
errorcode = 0  # min = -2139095039 ## MAX = -2055208192  -2145382381
=======
### Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
print("Connect RC8")
print(hCtrl)
### Get Robot Handle
errorcode = 0 ## min = -2139095039 ## MAX = -2055208192  -2145382381
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
code_min = -2145382381
code_max = -2055208192
maxerrordisc = ""
maxerrorcode = ""
maxlen = 0
<<<<<<< HEAD
for errorcode in range(code_min, code_max):
    try:
        strDescription = m_bcapclient.controller_execute(
            hCtrl, "GetErrorDescription", errorcode)
        # if(strDescription != "未定義エラーです。"):
        print(format(errorcode & 0xffffffff, 'x'))
        # print(strDescription)
        if(maxlen < len(strDescription)):
            maxlen = len(strDescription)
            maxerrorcode = format(errorcode & 0xffffffff, 'x')
=======
for errorcode in range(code_min,code_max):
    try:
        strDescription = m_bcapclient.controller_execute(hCtrl,"GetErrorDescription",errorcode)
        #if(strDescription != "未定義エラーです。"):
        print(format(errorcode& 0xffffffff,'x'))
            # print(strDescription)
        if(maxlen < len(strDescription)):
            maxlen = len(strDescription)
            maxerrorcode = format(errorcode& 0xffffffff,'x')
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
            maxerrordisc = strDescription
    except Exception as e:
        print('=== ERROR Description ===')
        if str(type(e)) == "<class 'pybcapclient.orinexception.ORiNException'>":
            errorcode_int = int(str(e))
            if errorcode_int < 0:
<<<<<<< HEAD
                errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
            else:
                errorcode_hex = hex(errorcode_int)
            print("Error Code : 0x" + str(errorcode_hex))
            error_description = m_bcapclient.controller_execute(
                hCtrl, "GetErrorDescription", errorcode_int)
            print("Error Description : " + error_description)
        else:
            print(e)
# End for
=======
                errorcode_hex = format(errorcode_int & 0xffffffff,'x')
            else:
                errorcode_hex = hex(errorcode_int)
            print("Error Code : 0x" + str(errorcode_hex))
            error_description = m_bcapclient.controller_execute(hCtrl,"GetErrorDescription",errorcode_int)
            print("Error Description : " + error_description)
        else:
            print(e)
# End for 
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
print(maxerrordisc)
print(maxerrorcode)
print(maxlen)

<<<<<<< HEAD
# End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
=======
#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
m_bcapclient.service_stop()
print("B-CAP service Stop")
