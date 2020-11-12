# -*- coding:utf-8 -*-

# Sample program
# Control of task(pro1.pcs) using b-cap

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import ctypes


def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000))


loopflg = True
ESC = 0x1B          # [ESC] virtual key code

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.38.12"
port = 5007
timeout = 2000

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
# get task(pro1) Object Handl
#HTask = 0
#HTask = m_bcapclient.controller_gettask(hCtrl, "pro2", "")

# Start pro1
# mode  1:One cycle execution, 2:Continuous execution, 3:Step forward
#mode = 1
# hr = m_bcapclient.task_start(HTask, mode, "")
#TaskStart = m_bcapclient.task_getvariable(HTask, "@START")
#hr = m_bcapclient.variable_putvalue(TaskStart, mode)

EmgHandle = m_bcapclient.controller_getvariable(hCtrl, "@EMERGENCY_STOP")

while loopflg:
    print(m_bcapclient.variable_getvalue(EmgHandle))

    if getkey(ESC):  # If push the ESC key,task stop
        print("push the ESC key")

# Disconnect
# if(HTask != 0):
#    m_bcapclient.task_release(HTask)
#    print("Release Pro1")
# End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
