#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Sample program
# b-cap slave mode
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

# Set path point
target_joint = []
for i in range(500):
    target_joint.append([i * 0.05, 0.0, 90.0, 0.0, 90.0, 0.0, 0.0, 0.0])

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

# ClearError
Command = "ClearError"
Param = None
m_bcapclient.controller_execute(hCtrl, Command, Param)

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

# Move Initialize Position
Comp = 1
Pos_value = [0.0, 0.0, 90.0, 0.0, 90.0, 0.0]
Pose = [Pos_value, "J", "@E"]
m_bcapclient.robot_move(HRobot, Comp, Pose, "")
print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")

# Check CheckVirtualFence
for i in range(500):
    ret = m_bcapclient.robot_execute(HRobot, 'CheckVirtualFence', 'J(' + str(target_joint[i])[1:-1] + ')')
    if ret != 0:
        raise ValueError("Check CheckVirtualFence!")


# Slave move: Change Send format
Command = "slvSendFormat"
Param = 0x0000  # Change the format to position
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Slave move: Change return format
Command = "slvRecvFormat"
Param = 0x0001  # Change the format to position
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Slave move: Change mode
Command = "slvChangeMode"
# mode 2 (Synchronous - with waiting time, Number of buffer 3(Buffering data is always used)) , Type J
Param = 0x202
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Send POS slvMove
Command = "slvMove"
LoopNum = 500
for num in range(LoopNum):
    Pos_value = target_joint[num]
    ret = m_bcapclient.robot_execute(HRobot, Command, Pos_value)
    # print(num)
for num in range(LoopNum):
    Pos_value = target_joint[LoopNum - 1 - num]
    ret = m_bcapclient.robot_execute(HRobot, Command, Pos_value)

# Slave move: Change mode
Command = "slvChangeMode"
Param = 0x000  # finish Slave Move
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Motor Off
Command = "Motor"
Param = [0, 0]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("Motor Off")

# GiveArm
Command = "GiveArm"
Param = None
m_bcapclient.robot_execute(HRobot, Command, Param)
print("TakeArm")

# Release Handle and Disconnect
if HRobot != 0:
    m_bcapclient.robot_release(HRobot)
    print("Release Robot")
if hCtrl != 0:
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")

# b-cap service stop
m_bcapclient.service_stop()
print("b-cap service Stop")

del m_bcapclient
print("Finish")
