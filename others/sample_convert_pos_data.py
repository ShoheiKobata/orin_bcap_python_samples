# -*- coding:utf-8 -*-

# sample program
# This program is to convert {Homogeneous Translation Type, position type, joint type} data into {Homogeneous Translation Type, position type, joint type} data to return.

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
option = "@IfNotMember"

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hctrl = m_bcapclient.controller_connect(name, provider, machine, option)
    print("Connect RC8")
    hrobot = m_bcapclient.controller_getrobot(hctrl, "Arm", "")

    base_joint_value = [0.0, 0.0, 90.0, 0.0, 90.0, 0.0]
    ret_position_data = m_bcapclient.robot_execute(hrobot, "J2P", [base_joint_value, "J"])
    print(f"J{base_joint_value} J2P P{ret_position_data}")
    ret_translation_data = m_bcapclient.robot_execute(hrobot, "P2T", [ret_position_data, "P"])
    print(f"P{ret_position_data} P2T T{ret_translation_data}")
    ret_joint_data = m_bcapclient.robot_execute(hrobot, "T2J", [ret_translation_data, "T"])
    print(f"P{ret_translation_data} P2T T{ret_joint_data}")

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
    #  DisConnect
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
