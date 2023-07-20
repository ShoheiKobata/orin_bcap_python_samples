# -*- coding:utf-8 -*-

# Sample programn
# This is a sample program that controls two robots with one program.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap


import pybcapclient.bcapclient as bcapclient

# set IP Address , Port number and Timeout of connected RC8
R1_ip_address = "192.168.0.1"
R1_port = 5007
R1_timeout = 2000

R2_ip_address = "192.168.0.2"
R2_port = 5007
R2_timeout = 2000

# Connection processing of tcp communication
R1_bcapclient = bcapclient.BCAPClient(R1_ip_address, R1_port, R1_timeout)
print("R1:Open Connection")
R2_bcapclient = bcapclient.BCAPClient(R2_ip_address, R2_port, R2_timeout)
print("R2:Open Connection")

# start b_cap Service
R1_bcapclient.service_start("")
print("R1:Send SERVICE_START packet")
R2_bcapclient.service_start("")
print("R2:Send SERVICE_START packet")

# set Parameter
Name = ""
Provider = "CaoProv.DENSO.VRC"
Machine = "localhost"
Option = ""

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    R1_hCtrl = R1_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("R1:Connect RC8")
    R2_hCtrl = R2_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("R2:Connect RC8")

    # Get Robot Handle
    R1_hRobot = R1_bcapclient.controller_getrobot(R1_hCtrl, "Arm", "")
    R2_hRobot = R2_bcapclient.controller_getrobot(R2_hCtrl, "Arm", "")

    # Take Arm
    Command = "TakeArm"
    Param = [0, 0]
    R1_bcapclient.robot_execute(R1_hRobot, Command, Param)
    print("R1:TakeArm")
    R2_bcapclient.robot_execute(R2_hRobot, Command, Param)
    print("R2:TakeArm")

    comp = 1
    joint_value = [0, 0, 90, 0, 90, 0]
    pose = [joint_value, "J", "@E"]
    print('R1:Move Start')
    R1_bcapclient.robot_move(R1_hRobot, comp, pose, "")
    print('R2:Move Start')
    R2_bcapclient.robot_move(R2_hRobot, comp, pose, "")

    joint_value = [-10, 0, 90, 0, 90, 0]
    pose = [joint_value, "J", "@E"]
    print('R1:Move Start')
    R1_bcapclient.robot_move(R1_hRobot, comp, pose, "Next")
    print('R2:Move Start')
    R2_bcapclient.robot_move(R2_hRobot, comp, pose, "")

    joint_value = [0, 0, 90, 0, 90, 0]
    pose = [joint_value, "J", "@E"]
    print('R1:Move Start')
    R1_bcapclient.robot_move(R1_hRobot, comp, pose, "")
    print('R2:Move Start')
    R2_bcapclient.robot_move(R2_hRobot, comp, pose, "")

    # Give Arm
    Command = "GiveArm"
    R1_bcapclient.robot_execute(R1_hRobot, Command, None)
    print("R1:GiveArm")
    R2_bcapclient.robot_execute(R2_hRobot, Command, None)
    print("R2:GiveArm")

except Exception as e:
    print('=== ERROR Description ===')
    print(str(e))

# DisConnect
if(R1_hRobot != 0):
    R1_bcapclient.robot_release(R1_hRobot)
    print("R1:Release Robot Handle")
# End If

if(R1_hCtrl != 0):
    R1_bcapclient.controller_disconnect(R1_hCtrl)
    print("R1:Release Controller")
# End If
R1_bcapclient.service_stop()
print("R1:B-CAP service Stop")
