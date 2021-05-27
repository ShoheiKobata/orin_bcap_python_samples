# -*- coding:utf-8 -*-

# test program
# palletcalspos in extension object class
# Pallet.CalcPos command reference https://www.fa-manuals.denso-wave.com/en/usermanuals/000402/

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient

# set IP Address , Port number and Timeout of connected RC8
host = "127.0.0.1"
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
    print(hCtrl)
    # Get extention pallet
    hext = m_bcapclient.controller_getextension(hCtrl, "Pallet", "")
    # Assign position indicating pallet four corner position P1 to aaa
    aaa = "P( 600, -100, 50, -180, 0, 180, 5 )"
    # ssign position indicating pallet four corner position P2 to bbb
    bbb = "P( 600, 100, 50, -180, 0, 180, 5 )"
    # Assign position indicating pallet four corner position P3 to ccc
    ccc = "P( 400, -100, 50, -180, 0, 180, 5 )"
    # Assign position indicating pallet four corner position P4 to ddd
    ddd = "P( 400, 100, 50, -180, 0, 180, 5 )"
    comandstr = "CalcPos"
    vntParam = [3, 5, 20, aaa, bbb, ccc, ddd, 2, 1]
    ret = m_bcapclient.extension_execute(hext, comandstr, vntParam)
    print(ret)


except Exception as e:
    print('=== ERROR Description ===')
    if str(type(e)) == "<class 'pybcapclient.orinexception.ORiNException'>":
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

# End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
