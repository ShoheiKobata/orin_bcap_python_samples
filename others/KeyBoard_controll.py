# -*- coding:utf-8 -*-

# This sample program is to control the robot with KeyBoard.
# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap
#
#

import pybcapclient.bcapclient as bcapclient

import random
import numpy as np
import ctypes


def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key) & 0x8000))


def main():
    flg = True
    ESC = 0x1B          # [ESC] virtual key code
    xp = 0x41  # a : x+
    xm = 0x53  # s : x-
    yp = 0x44  # d : y+
    ym = 0x46  # f : y-
    zp = 0x47  # g : z+
    zm = 0x48  # h : z-
    Rxp = 0x5A  # z : Rx+
    Rxm = 0x58  # x : Rx-
    Ryp = 0x43  # c : Ry+
    Rym = 0x56  # v : Ry-
    Rzp = 0x42  # b : Rz+
    Rzm = 0x4E  # n :Rz-

    # set IP Address , Port number and Timeout of connected RC8
    host = "192.168.0.2"
    port = 5007
    timeout = 2000
    # Handls
    hctrl = 0
    hrob = 0

    sumstate = np.zeros(7)
    target_pos = np.zeros(7)
    org_pos = np.zeros(7)

    bcap = bcapclient.BCAPClient(host, port, timeout)
    bcap.service_start("")
    print("Start b-cap service")

    Name = ""
    Provider = "CaoProv.DENSO.VRC"
    Machine = ("localhost")
    Option = ("")
    hctrl = bcap.controller_connect(Name, Provider, Machine, Option)
    print("Connect Ctrl")
    # Connect To arm
    hrob = bcap.controller_getrobot(hctrl, "Arm", "")
    print("Connect Robot")
    # Take Arm
    Command = "TakeArm"
    Param = [0, 0]
    bcap.robot_execute(hrob, Command, Param)
    print("Take Arm")
    # Motor On
    Command = "Motor"
    Param = [1, 0]
    bcap.robot_execute(hrob, Command, Param)
    print("Motor On")
    # Get CurPos
    Command = "CurPos"
    Param = ""
    tmp_cur_pos = bcap.robot_execute(hrob, Command, Param)
    print(type(tmp_cur_pos))
    print(tmp_cur_pos)
    org_pos = np.array(tmp_cur_pos[0:7])

    '''print("Origin Pos")
    print(org_pos)
    org_list = org_pos.tolist()
    origin_pos = org_pos
    print(origin_pos)

    while flg:

        #print(type(state.buttons))
        #print(state.buttons)
        sumstate = sumstate + arr_state
        target_pos = sumstate + origin_pos
        # FIX Rx,Ry,Fig
        target_pos[3:5] = origin_pos[3:5] #Rx,Ry
        target_pos[6] = origin_pos[6]     #Fig
        tlist = target_pos.tolist()
        print("tlist")
        print(tlist)
        POSEDATA = [tlist,"P","@P"]
        bcap.robot_move(hrob,1,POSEDATA,"")
        if getkey(ESC):     # If push the ESC key,program finish
            flg=False
        #End if
    #End while'''
    if hrob != 0:
        bcap.robot_release(hrob)
        hrob = 0
        print("Release Robot")
    # End if
    if hctrl != 0:
        bcap.controller_disconnect(hctrl)
        hctrl = 0
        print("Dissconnect Controller")
    bcap.service_stop()
    print("b-cap service Stop")

# End def Main


if __name__ == '__main__':
    main()
