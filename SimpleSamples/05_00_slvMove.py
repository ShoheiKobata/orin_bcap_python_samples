# -*- coding:utf-8 -*-

# Sample program
<<<<<<< HEAD
# b-cap slave mode

# b-cap Lib URL
=======
# b-cap slave mode 

#b-cap Lib URL 
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient

<<<<<<< HEAD
# set IP Address , Port number and Timeout of connected RC8
=======
### set IP Address , Port number and Timeout of connected RC8
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
host = "192.168.0.1"
port = 5007
timeout = 2000

<<<<<<< HEAD
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
Param = 0x0000  # Change the format to position
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Slave move: Change return format
=======
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

### Motor On
Command = "Motor"
Param = [1,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("Motor On")

### Move Initialize Position
Comp=1
Pos_value = [0.0 , 0.0 , 90.0 , 0.0 , 90.0 , 0.0]
Pose = [Pos_value,"J","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")

### Slave move: Change return format
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
Command = "slvRecvFormat"
# Param = 0x0001  # Change the format to position
Param = 0x0014  # hex(10): timestamp, hex(1): [pose, joint]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

<<<<<<< HEAD
# Slave move: Change mode
Command = "slvChangeMode"
# Param = 0x001  # Type P, mode 0 (buffer the destination)
# Param = 0x201  # Type P, mode 1 (overwrite the destination)
Param = 0x202  # Type J, mode 1 (overwrite the joint)
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Send POS slvMove
Command = "slvMove"
LoopNum = 50
for num in range(LoopNum):
    Pos_value = [0.0 + num * 0.05, 0.0, 90.0, 0.0, 90.0, 0.0, 0, 0]
    # Pos_value = [460.0 + num, 0.0, 779.9, 180.0, 0.0, 180.0, 5]
    ret = m_bcapclient.robot_execute(HRobot, Command, Pos_value)
    # print(ret)
    print("time:" + str(ret[0]))
    print("pos P,J:" + str(ret[1]))
for num in range(LoopNum):
    Pos_value = [0.0 + (LoopNum - num) * 0.05, 0.0, 90.0, 0.0, 90.0, 0.0, 0, 0]
    # Pos_value = [460.0 + LoopNum - num, 0.0, 779.9, 180.0, 0.0, 180.0, 5]
    ret = m_bcapclient.robot_execute(HRobot, Command, Pos_value)
    # print(ret)
    print("time:" + str(ret[0]))
    print("pos P,J:" + str(ret[1]))

# Slave move: Change mode
Command = "slvChangeMode"
Param = 0x000  # finish Slave Move
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Release Handle and Disconnect
=======
### Slave move: Change mode
Command = "slvChangeMode"
# Param = 0x001  # Type P, mode 0 (buffer the destination)  
Param = 0x101  # Type P, mode 1 (overwrite the destination)  
# Param = 0x102  # Type J, mode 1 (overwrite the joint)  
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

### Send POS slvMove
Command = "slvMove"
LoopNum = 100
for num in range(LoopNum):
    Pos_value = [255.0 + num ,0.0, 535.5 , 180.0 , 0.0 , 180.0 , 5]
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    #print(ret)
    print("time:" + str(ret[0]))
    print("pos P,J:" + str(ret[1]))
for num in range(LoopNum):
    Pos_value = [255.0 + LoopNum - num , 0.0, 535.5 , 180.0 , 0.0 , 180.0 , 5]
    ret = m_bcapclient.robot_execute(HRobot,Command,Pos_value)
    #print(ret)
    print("time:" + str(ret[0]))
    print("pos P,J:" + str(ret[1]))

### Slave move: Change mode
Command = "slvChangeMode"  
Param = 0x000  # finish Slave Move  
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

### Release Handle and Disconnect
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
if HRobot != 0:
    m_bcapclient.robot_release(HRobot)
    print("Release Robot")
if hCtrl != 0:
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")

<<<<<<< HEAD
# b-cap service stop
=======
### b-cap service stop
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
m_bcapclient.service_stop()
print("b-cap service Stop")

del m_bcapclient
print("Finish")
