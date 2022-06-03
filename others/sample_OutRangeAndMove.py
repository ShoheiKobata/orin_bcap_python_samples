# -*- coding:utf-8 -*-

# This is a sample program to move after checking whether the target position is within the Motion Range.

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
name = ""
provider = "CaoProv.DENSO.VRC"
machine = "localhost"
option = ""

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hctrl = m_bcapclient.controller_connect(name, provider, machine, option)
    print("Connect RC8")
    # Get Robot Handle
    hrobot = m_bcapclient.controller_getrobot(hctrl, "Arm", "")
    # TakeArm
    command = "TakeArm"
    arm_group = 0
    keep = 0
    m_bcapclient.robot_execute(hrobot, command, [arm_group, keep])
    print("TakeArm")

    targetpos_value = [300, 0, 400, 180, 0, 180, 5]
    pose = [targetpos_value, "P"]
    tool_def = -1
    work_def = -1
    ret = m_bcapclient.robot_execute(hrobot, "OutRange", [pose, tool_def, work_def])
    print(ret)
    if ret == 0:
        lcomp = 1
        pose_data = [targetpos_value, "P", "@E"]
        m_bcapclient.robot_move(hrobot, lcomp, pose_data)
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
        error_description = m_bcapclient.controller_execute(hctrl, "GetErrorDescription", errorcode_int)
        print("Error Description : " + error_description)
    else:
        print(e)

finally:
    m_bcapclient.robot_execute(hrobot, "GiveArm", None)
    # DisConnect
    if(hrobot != 0):
        m_bcapclient.robot_release(hrobot)
        print("Release Robot Handle")
    # End If
    if(hctrl != 0):
        m_bcapclient.controller_disconnect(hctrl)
        print("Release Controller")
    # End If
    m_bcapclient.service_stop()
    print("B-CAP service Stop")
