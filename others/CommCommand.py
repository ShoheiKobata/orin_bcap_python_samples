# -*- coding:utf-8 -*-

# Sample program
# Comm command sample

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import ctypes
import time


def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000))


loopflg = True
ESC = 0x1B          # [ESC] virtual key code

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
port = 5007
timeout = 2000
# Set line number using Data Communication in RC8
# Operation path in RC8 : [F6 Setting] - [F5 Communication and Token] - [F3 Data Communication]
line_number = 4

# Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

# set Parameter
Name = ""
Provider = "CaoProv.DENSO.VRC"
Machine = ("localhost")
Option = ("")

# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect RC8")
hcom = m_bcapclient.controller_getextension(hCtrl, "Comm")

retComState = 0
while True:
    m_bcapclient.extension_execute(hcom,"open",line_number)
    time.sleep(1)
    retComState = m_bcapclient.extension_execute(hcom,"State",line_number)
    print("CommState  ",retComState)
    if retComState==2:
        break
    # End if
# End while

m_bcapclient.extension_execute(hcom,"clear",line_number)
retComInput=""
while loopflg:
    retComCount = 0
    retComCount = m_bcapclient.extension_execute(hcom,"count",line_number)
    if(retComCount>0):
        retComInput = m_bcapclient.extension_execute(hcom,"input",line_number)
        print(retComInput)
    # End if
    if getkey(ESC):  # If push the ESC key,Stop program 
        print("push the ESC key")
        # CommClose
        m_bcapclient.extension_execute(hcom,"close",line_number)
        loopflg = False
    # End if
# End while

# Disconnect
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
