# -*- coding:utf-8 -*-

# Temp program , check command

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
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
# get Robot Object Handl
HRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
print("AddRobot")

Command = "CurExtSpd"
Param = ""
ret = m_bcapclient.robot_execute(HRobot, Command, Param)
print(ret)

# Disconnect
if(HRobot != 0):
    m_bcapclient.robot_release(HRobot)
    print("Release Robot Object")
# End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
