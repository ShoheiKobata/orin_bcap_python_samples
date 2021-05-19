#!/usr/bin/env python3
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

# set IP Address , Port number and Timeout of connected Robot Controller (RC8,RC8A,COBOTTA,RC9)
host = "192.168.0.1"
port = 5007
timeout = 2000

# set Parameter
# If you want to connect to RC9, please select "VRC9" as the provider name.
# If you want to connect to RC8, RC8A, or COBOTTA, select "VRC" as the provider name.
Name = ""
Provider = "CaoProv.DENSO.VRC"
# Provider = "CaoProv.DENSO.VRC9"
Machine = "localhost"
Option = ""

# Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect "+Provider)
# get task(pro1) Object Handl
HTask = 0
HTask = m_bcapclient.controller_gettask(hCtrl, "Pro1", "")

# Start pro1
# mode  1:One cycle execution, 2:Continuous execution, 3:Step forward
mode = 2
hr = m_bcapclient.task_start(HTask, mode, "")

while loopflg:
    # Status (VT_I4), 0:TASK_NON_EXISTENT, Task is not exist. , 1:TASK_SUSPEND, Hold-stopped , 2:TASK_READY, Ready , 3:TASK_RUN, Running , 4:TASK_STEPSTOP, Step-stopped
    TaskStatus = m_bcapclient.task_execute(HTask, "GetStatus")
    print("TaskStatus : ", TaskStatus)
    if(TaskStatus != 3):
        loopflg = False
    if getkey(ESC):  # If push the ESC key,task stop
        print("push the ESC key")
        # mode:: 0: Default stop, 1: Instant stop, 2: Step stop, 3: Cycle stop, 4: Initialized stop
        mode = 1
        hr = m_bcapclient.task_stop(HTask, mode, "")
        print("task stop")

# Disconnect
if(HTask != 0):
    m_bcapclient.task_release(HTask)
    print("Release Pro1")
# End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
