# -*- coding:utf-8 -*-

# COBOTTA
# Vaccum

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import random
import time
import csv
import os

import pybcapclient.bcapclient as bcapclient

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.5"
port = 5007
timeout = 2000

# test datas

sngPower = 100
Interval = 0
loadtime = 10
ret = []

filename = str(sngPower) + "%_interval" + str(Interval) + \
    "ms_LoadTime" + str(loadtime) + "ms"

# f = open(os.path.join("data", filename), 'w')
# writer = csv.writer(f, lineterminator='\n')
# header = ["Time(ms)", "HandCurPressure[kPa]", "HandCurLoad[%]"]

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
    print("Get Arm Handle")

    param = [sngPower, True]
    m_bcapclient.controller_execute(hCtrl, "HandMoveVH", param)
    strat_time = time.time()
    # for i in range(20):
    while True:
        time.sleep(0.5)
        retPressure = m_bcapclient.controller_execute(hCtrl, "HandCurPressure")
        retLoad = m_bcapclient.controller_execute(hCtrl, "HandCurLoad")
        elapsed_time = time.time() - strat_time
        row = [elapsed_time, retPressure, retLoad]

        print(row)
        ret.append(row)
        if retLoad > 100:
            break
        # End if
        if elapsed_time > 600:
            break
        # End if
    m_bcapclient.controller_execute(hCtrl, "HandStop")
    print("HandStop")
    while True:
        time.sleep(0.5)
        retPressure = m_bcapclient.controller_execute(hCtrl, "HandCurPressure")
        retLoad = m_bcapclient.controller_execute(hCtrl, "HandCurLoad")
        elapsed_time = time.time() - strat_time
        row = [elapsed_time, retPressure, retLoad]
        print(row)
        ret.append(row)

        if elapsed_time > 600:
            break
        # End if

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

    f = open(os.path.join("data", filename), 'w')
    writer = csv.writer(f, lineterminator='\n')
    header = ["Time(s)", "HandCurPressure[kPa]", "HandCurLoad[%]"]
    writer.writerows(ret)
    f.close()
