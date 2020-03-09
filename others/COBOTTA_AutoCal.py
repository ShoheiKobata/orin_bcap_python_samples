# -*- coding:utf-8 -*-

# COBOTTA
# AutoCAL sequence

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import random
import time

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
Machine = "localhost"
Option = ""

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("Connect RC8")
    # Get Robot Handle
    hRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")

    # Error Clear
    errorcnt = m_bcapclient.controller_execute(hCtrl, "GetCurErrorCount")
    if errorcnt > 0:
        print("Error count : " + str(errorcnt))
        m_bcapclient.robot_execute(hRobot, "ManualResetPreparation")
        print("executed ManualResetPreparation")
        m_bcapclient.controller_execute(hCtrl, "ClearError")
        print("executed ClearError")

    m_bcapclient.robot_execute(hRobot, "AutoCal", "")
    print("executed autocal")
    m_bcapclient.robot_execute(hRobot, "ManualResetPreparation")
    print("executed ManualResetPreparation")
    m_bcapclient.robot_execute(hRobot, "MotionPreparation", "")
    print("executed MotionPreparation")
    m_bcapclient.robot_execute(hRobot, "TakeArm")
    m_bcapclient.robot_execute(hRobot, "ExtSpeed", 100)
    m_bcapclient.robot_move(hRobot, 1, "@P J(0,0,90,0,90,0)")


except Exception as e:
    print('=== ERROR Description ===')
    if str(type(e)) == "<class 'pybcapclient.orinexception.ORiNException'>":
        print(e)
        errorcode_int = int(str(e))
        if errorcode_int < 0:
            errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
        else:
            errorcode_hex = hex(errorcode_int)
        print("Error Code : 0x" + str(errorcode_hex))
        error_description = m_bcapclient.controller_execute(
            hCtrl, "GetErrorDescription", errorcode_int)
        print("Error Description : " + error_description)
    else:
        print(e)

finally:
    # DisConnect
    if(hRobot != 0):
        m_bcapclient.robot_release(hRobot)
        print("Release Robot Handle")
    # End If
    if(hCtrl != 0):
        m_bcapclient.controller_disconnect(hCtrl)
        print("Release Controller")
    # End If
    m_bcapclient.service_stop()
    print("B-CAP service Stop")
