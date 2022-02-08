# -*- coding:utf-8 -*-

# This is a sample program to move after checking whether the target position is within the Motion Range.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import ctypes


def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000))
# End def


ESC = 0x1B          # Virtual key code of [ESC] key
key_1 = 0X31        # Virtual key code of [1] key
key_2 = 0X32        # Virtual key code of [2] key

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
    # TakeArm
    Command = "TakeArm"
    Param = [0, 0]
    m_bcapclient.robot_execute(hRobot, Command, Param)
    print("TakeArm")

    TargetPos = [300, 0, 400, 180, 0, 180, 5]
    strTargetPos = str(TargetPos)
    Pose = "P(" + strTargetPos[1:-1] + ")"
    ret = m_bcapclient.robot_execute(hRobot, "OutRange", Pose)
    print(ret)
    if ret == 0:
        strPose = "@P " + Pose
        m_bcapclient.robot_move(hRobot, 1, strPose)
    # End If

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
