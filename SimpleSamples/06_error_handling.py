#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# A sample program for bCAP error handling.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
from pybcapclient.orinexception import ORiNException

# set IP Address , Port number and Timeout of connected Robot Controller (RC8,RC8A,COBOTTA,RC9)
host = "192.168.0.1"
port = 5007
timeout = 2000

# set Parameter
# If you want to connect to RC9, COBOTTA Pro, please select "VRC9" as the provider name.
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
print("Connect " + Provider)
# get I[1] Object Handl
HInt1 = m_bcapclient.controller_getvariable(hCtrl, "I1")
try:
    # A type mismatch error occurs in the robot controller.
    m_bcapclient.variable_putvalue(HInt1, [0, 0, 90, 0, 90, 0])
    # aa = 1 / 0  # non ORiN error occurred
except ORiNException as e:
    print('catch ORiN Exception in Robot Controller')
    errorcode_int = int(str(e))
    if errorcode_int < 0:
        errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
    else:
        errorcode_hex = hex(errorcode_int)
    # End if
    print("Error Code : 0x" + str(errorcode_hex))
    error_description = m_bcapclient.controller_execute(hCtrl, "GetErrorDescription", errorcode_int)
    print("Error Description : " + error_description)
except Exception as e:
    print(' non ORiN error occurred')
    print(e)

# Disconnect
if (HInt1 != 0):
    m_bcapclient.variable_release(HInt1)
    print("Release I1 Object")
# End If
if (hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
