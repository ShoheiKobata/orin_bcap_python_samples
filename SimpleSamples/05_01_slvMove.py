#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Sample program
# b-cap slave mode with controll IO
# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import time

import pybcapclient.bcapclient as bcapclient

# set IP Address , Port number and Timeout of connected Robot Controller (RC8,RC8A,COBOTTA,RC9)
host = "127.0.0.1"
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

# Move Initialize Position
Comp = 1
Pos_value = [0.0, 0.0, 90.0, 0.0, 90.0, 0.0]
Pose = [Pos_value, "J", "@E"]
m_bcapclient.robot_move(HRobot, Comp, Pose, "")
print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")


# Slave move: Change Send format
Command = "slvSendFormat"
Param = 0x0020  # Change the format to position and Hand IO(0x0020), Mini IO(0x0100)
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Slave move: Change return format
Command = "slvRecvFormat"
# Param = 0x0001  # Change the format to position
Param = 0x0014  # hex(10): timestamp, hex(4): [pose, joint]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Slave move: Change mode
Command = "slvChangeMode"
# Param = 0x001  # Type P, mode 0 (buffer the destination)
# Param = 0x201  # Type P, mode 2 (overwrite the destination)
Param = 0x202  # Type J, mode 2 (overwrite the joint)
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Send POS slvMove
Command = "slvMove"
LoopNum = 100
oldtime = 0
for num in range(LoopNum):
    Pos_value = [0.0 + num * 0.1, 0.0, 90.0, 0.0, 90.0, 0.0, 0, 0]  # Joint Type
    # Pos_value = [460.0 + num, 0.0, 779.9, 180.0, 0.0, 180.0, 5]   # Postion type
    # HandIO
    # IO[64]=On : 0x010000 , IO[64,65]=on 0x030000 ,IO[64-67]=On 0x0F0000 , IO[64-71]=On 0xFF0000
    # MiniIO
    # IO[24]=On : 0x01000000 , IO[24,25]=On : 0x03000000 IO[24-26]=On 0x0F000000 , IO[24-31]=On : 0xFF000000
    # MiniIO and Hand IO
    # [Pos_value,MiniIO,HandIO]
    send_data = [Pos_value, 0x70000000]
    ret = m_bcapclient.robot_execute(HRobot, Command, send_data)
    print("pos P,J:" + str(ret[1]))
for num in range(LoopNum):
    Pos_value = [0.0 + (LoopNum - num) * 0.1, 0.0, 90.0, 0.0, 90.0, 0.0, 0, 0]  # Joint Type
    # Pos_value = [460.0 + LoopNum - num, 0.0, 779.9, 180.0, 0.0, 180.0, 5]     # Position Type
    send_data = [Pos_value, 0x000000]
    ret = m_bcapclient.robot_execute(HRobot, Command, send_data)
    print("pos P,J:" + str(ret[1]))

# Slave move: Change mode
Command = "slvChangeMode"
Param = 0x000  # finish Slave Move
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Release Handle and Disconnect
Command = "slvChangeMode"
# Param = 0x001  # Type P, mode 0 (buffer the destination)
Param = 0x101  # Type P, mode 1 (overwrite the destination)
# Param = 0x102  # Type J, mode 1 (overwrite the joint)
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

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
