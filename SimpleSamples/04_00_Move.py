# -*- coding:utf-8 -*-

# Send "Move" command to RC8

#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient

### set IP Address , Port number and Timeout of connected RC8
host = "127.0.0.1"
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
Machine = ("localhost")
Option = ("")

### Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
print("Connect RC8")
### get Robot Object Handl
HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
print("AddRobot")

### TakeArm
Command = "TakeArm"
Param = [0,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("TakeArm")

###Motor On
Command = "Motor"
Param = [1,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("Motor On")

###set ExtSpeed Speed,Accel,Decel
Command = "ExtSpeed"
Speed = 100
Accel = 100
Decel = 100
Param = [Speed,Accel,Decel]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("ExtSpeed")

### Set Parameters
#Interpolation
Comp=1
#PoseData
Pose = "@P P1"
m_bcapclient.robot_move(HRobot,Comp,Pose,"SPEED=F2,NEXT")
print("Complete Move P,@P P[1]")
Pose = [2,"P","@0"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@0 P[2]")

'''
position_Value = [210.0,0.0,260.0,180.0,0.0,180.0,261]
Pose = [position_Value,"P","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@E P(x,y,z,Rx,Ry,Rz,Fig)")
'''
###Motor Off
Command = "Motor"
Param = [0,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("Motor Off")

###Give Arm
Command = "GiveArm"
Param = None
m_bcapclient.robot_execute(HRobot,Command,Param)
print("GiveArm")

#Disconnect
if(HRobot != 0):
    m_bcapclient.robot_release(HRobot)
    print("Release Robot Object")
#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
