# -*- coding:utf-8 -*-

# Sample program
# GetSrvData command
# 

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import time

# refer: https://www.fa-manuals.denso-wave.com/en/usermanuals/000199/

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.101"
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
hRobot = m_bcapclient.controller_getrobot(hCtrl,'Arm')

DataNumbers = [1,2,4,5,7,8,17,18,19,20]
DataType =['CurrentMotorSpeed[rpm]','MotorAngle','Absolute motor current value','Motor torque command position','load factor','command value ','Tool tip speed(work coordinates)','Tool tip deviation(work coordinates)','Tool tip speed (tool coordinates)','Tool tip deviation (tool coordinates)']


# 
for i in range(len(DataNumbers)):
    print(DataType[i])
    for j in range(10):
        return_datas = m_bcapclient.robot_execute(hRobot,'GetSrvData',DataNumbers[i])
        print(return_datas)
        time.sleep(0.5)


# Disconnect
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
