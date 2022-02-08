#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Send "Move" command to RC8
# When this program is executed, the motor is turned on, the external speed is set to 10%, and the "Move"

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient

# set IP Address , Port number and Timeout of connected Robot Controller (RC8,RC8A,COBOTTA,RC9)
host = "192.168.0.1"
port = 5007
timeout = 2000

# set Parameter
# If you want to connect to RC9, please select "VRC9" as the provider name.
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
# get Robot Object Handl
HRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
print("AddRobot")

# TakeArm
Command = "TakeArm"
Param = [0, 0]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("TakeArm")

# Motor On
Command = "Motor"
Param = [1, 0]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("Motor On")

# set ExtSpeed Speed,Accel,Decel
Command = "ExtSpeed"
Speed = 10
Accel = 10
Decel = 10
Param = [Speed, Accel, Decel]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("ExtSpeed")

# Set Parameters
# Interpolation
Comp = 1
# PoseData (string)
Pose = "@P P1"
m_bcapclient.robot_move(HRobot, Comp, Pose, "SPEED=F2,NEXT")
print("Complete Move P,@P P[1]")

# PoseData (array [Index , Variavletype , Pass])
Pose = [2, "P", "@0"]
m_bcapclient.robot_move(HRobot, Comp, Pose, "")
print("Complete Move P,@0 P[2]")

'''Comment out because the Motion Range is different for robots
#PoseData (array [Raw value , Variavletype , Pass])
position_Value = [210.0,0.0,260.0,180.0,0.0,180.0,261]
Pose = [position_Value,"P","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@E P(x,y,z,Rx,Ry,Rz,Fig)")
'''
# Motor Off
Command = "Motor"
Param = [0, 0]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("Motor Off")

# Give Arm
Command = "GiveArm"
Param = None
m_bcapclient.robot_execute(HRobot, Command, Param)
print("GiveArm")

# Disconnect
if(HRobot != 0):
    m_bcapclient.robot_release(HRobot)
    print("Release Robot Object")
# End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
