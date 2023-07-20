# -*- coding:utf-8 -*-

# test program
# Measure the program processing time.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

'''
for _ in range(10000):
    # read value of I[1]
    retI = m_bcapclient.variable_getvalue(IHandl)
result
process_time: 17.367063760757446[sec]

The communication speed is about 1.7 [msec] in our environment.
This result is for reference only.
'''

import pybcapclient.bcapclient as bcapclient
import time

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
# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect RC8")
# get I[1] Object Handl
IHandl = 0
IHandl = m_bcapclient.controller_getvariable(hCtrl, "I1", "")
start = time.time()
for _ in range(10000):
    # read value of I[1]
    retI = m_bcapclient.variable_getvalue(IHandl)
    # print("Read Variable I[1] = %d" % retI)
# End for
process_time = time.time() - start
print(f'process_time: {process_time}[sec]')
# Disconnect
if(IHandl != 0):
    m_bcapclient.variable_release(IHandl)
    print("Release I[1]")
# End if
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
