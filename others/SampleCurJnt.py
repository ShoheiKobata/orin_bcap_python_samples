# -*- coding:utf-8 -*-

# Sample program
# get values of position,speed and torque using b-cap

# b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import random
import time

### set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
port = 5007
timeout = 2000

### Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
print("Open Connection")

### start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

### set Parameter
Name = ""
Provider="CaoProv.DENSO.VRC"
Machine = "localhost"
Option = ""

try:
    ### Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
    print("Connect RC8")
    ### Get Robot Handle
    hRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")

    ### Start timer
    start = time.time()

    for i in range(0,1001):
        ### Get Position
        ret = m_bcapclient.robot_execute(hRobot,"CurJnt")
        print("CurJnt")
        print(ret)
        ret = m_bcapclient.robot_execute(hRobot,"CurPos")
        print("CurPos")
        print(ret)
        ### get torque
        ret = m_bcapclient.robot_execute(hRobot,"GetSrvData",4)
        print("Get torque")
        print(ret)
        ### get speed
        ret = m_bcapclient.robot_execute(hRobot,"GetSrvData",17)
        print("Get Speed (Tool tip speed (work coordinates and position 3 component only))")
        print(ret)
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")

except Exception as e:
    print('=== ERROR Description ===')
#    print( 'type:' + str(type(e)))
#    print('args:' + str(e.args))
    print(str(e))

#DisConnect
if(hRobot != 0):
    m_bcapclient.robot_release(hRobot)
    print("Release Robot Handle")
#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
m_bcapclient.service_stop()
print("B-CAP service Stop")