# -*- coding:utf-8 -*-

# sample program
# This program is sample of pacScript's coordinate transformation command.

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

    reference_pos_value = [170, 50, 260, 180, 10, 135, 261]
    offset_pos_vaue = [10, 0, 0, 0, 0, 0, -1]
    pn1 = [reference_pos_value, "P"]
    # pn2 = [offset_pos_vaue, "P"]
    pn2 = "P(" + str(offset_pos_vaue)[1:-1] + ")"
    print(f"base:{pn1}")
    print(f"offset:{pn2}")
    devh_calc_res = m_bcapclient.robot_execute(hrobot, "DevH", [pn1, pn2])
    print(f"result devh:{devh_calc_res}")
    dev_calc_res = m_bcapclient.robot_execute(hrobot, "Dev", [pn1, pn2])
    print(f"result dev :{dev_calc_res}")

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
