# -*- coding:utf-8 -*-

# sample program
# This program is a sample program to run a manual reset for RC9 and COBOTTAPRO.

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
provider = "CaoProv.DENSO.VRC9"
machine = "localhost"
option = "@IfNotMember"

try:
    # Connect to RC9  , Get Controller Handle
    hctrl = m_bcapclient.controller_connect(name, provider, machine, option)
    print("Connect RC9")
    sto_state_value = m_bcapclient.controller_execute(hctrl, 'StoState')
    print(f'sto state is {sto_state_value}')
    if sto_state_value:
        m_bcapclient.controller_execute(hctrl, "ManualReset")
        print('execute Manual Reset')
    # End if
    sto_state_value = m_bcapclient.controller_execute(hctrl, 'StoState')
    print(f'sto state is {sto_state_value}')

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
    if hctrl != 0:
        m_bcapclient.controller_disconnect(hctrl)
        print("Release Controller")
    # End If
    m_bcapclient.service_stop()
    print("B-CAP service Stop")
