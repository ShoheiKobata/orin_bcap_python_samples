# -*- coding:utf-8 -*-

# check extension objects and command ()
# This program controls the electric hand in RC8.
# COBOTTA hand control is another command.

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
# get extension Object Handl
hExtension = m_bcapclient.controller_getextension(hCtrl, "Hand0", "")
print("Add Extension Hand")

# Get electric hand position Hand[0].CurPos
ret = m_bcapclient.extension_execute(hExtension, "CurPos")
print("electric hand pos = ", ret)

# Move electric hand  Hand[0].chuck 0
m_bcapclient.extension_execute(hExtension, "Chuck", 0)
print("electric hand moved")

# Get electric hand position Hand[0].CurPos
ret = m_bcapclient.extension_execute(hExtension, "CurPos")
print("electric hand pos = ", ret)

# Disconnect
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
