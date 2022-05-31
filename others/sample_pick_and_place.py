# -*- coding:utf-8 -*-

# sample program
# This program is "pick and place" moving by cobotta

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap


import pybcapclient.bcapclient as bcapclient


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
name = ""
provider = "CaoProv.DENSO.VRC"
machine = "localhost"
option = "@IfNotMember"

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hctrl = m_bcapclient.controller_connect(name, provider, machine, option)
    print("Connect RC8")
    # Get Robot Handle
    hrobot = m_bcapclient.controller_getrobot(hctrl, "Arm", "@IfNotMember")
    # TakeArm
    command = "TakeArm"
    Param = [0, 0]
    m_bcapclient.robot_execute(hrobot, command, Param)
    print("TakeArm")

    command = "ExtSpeed"
    speed = 50
    accel = 25
    decel = 25
    m_bcapclient.robot_execute(hrobot, command, [speed, accel, decel])
    print(f"Set External Speed {[speed, accel, decel]}")

    Pose = "@P J(0,0,90,0,90,0)"
    opt = ""
    m_bcapclient.robot_move(hrobot, 1, Pose, opt)
    print("Moved initial position")

    pick_position = [177, -90, 120, 180, 0, 180, 261]
    place_position = [177, 90, 120, 180, 0, 180, 261]

    print("Picking motion")
    print("Approach")
    pose_base = [pick_position, "P"]
    pose_len = [30.0, "", "@P"]
    lcomp = 1  # 1=PTP, 2=CP
    m_bcapclient.robot_execute(hrobot, "Approach", [lcomp, pose_base, pose_len])

    print("Move")
    lcomp = 2
    pose = [pick_position, "@E", "P"]
    m_bcapclient.robot_move(hrobot, lcomp, pose)

    print("COBOTTA Hand Move (Chuck) , **not electric hand")
    dblpos = 5.0
    sngspeed = 100
    dblforce = 10.0
    m_bcapclient.controller_execute(hctrl, "HandMoveAH", [dblpos, sngspeed, dblforce])

    print("Depart")
    lcomp = 2  # 1=PTP, 2=CP
    pose_len = [30.0, "", "@P"]
    m_bcapclient.robot_execute(hrobot, "Depart", [lcomp, pose_len])

    print("Place motion")
    print("Approach")
    pose_base = [place_position, "P"]
    pose_len = [30.0, "", "@P"]
    lcomp = 1  # 1=PTP, 2=CP
    m_bcapclient.robot_execute(hrobot, "Approach", [lcomp, pose_base, pose_len])

    print("Move")
    lcomp = 2
    pose = [place_position, "@E", "P"]
    m_bcapclient.robot_move(hrobot, lcomp, pose)

    print("COBOTTA Hand Move (UnChuck) , **not electric hand")
    dblpos = 30.0
    sngspeed = 100
    m_bcapclient.controller_execute(hctrl, "HandMoveA", [dblpos, sngspeed])

    print("Depart")
    lcomp = 2  # 1=PTP, 2=CP
    pose_len = [30.0, "", "@P"]
    m_bcapclient.robot_execute(hrobot, "Depart", [lcomp, pose_len])

    Pose = "@P J(0,0,90,0,90,0)"
    opt = ""
    m_bcapclient.robot_move(hrobot, 1, Pose, opt)
    print("Moved initial position")


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
        error_description = m_bcapclient.controller_execute(hctrl, "GetErrorDescription", errorcode_int)
        print("Error Description : " + error_description)
    else:
        print(e)

finally:
    #  GiveArm
    command = "GiveArm"
    m_bcapclient.robot_execute(hrobot, command, None)
    print("GiveArm")

    #  DisConnect
    if(hrobot != 0):
        m_bcapclient.robot_release(hrobot)
        print("Release Robot Handle")
    # End If
    if(hctrl != 0):
        m_bcapclient.controller_disconnect(hctrl)
        print("Release Controller")
    # End If
    m_bcapclient.service_stop()
    print("B-CAP service Stop")
