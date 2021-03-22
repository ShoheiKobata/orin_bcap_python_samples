# -*- coding:utf-8 -*-

# This sample program is to control the robot with 3D mouse.
# b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap
#
# spacenavigator github URL
# https://github.com/johnhw/pyspacenavigator
#

import pyspacenavigator.spacenavigator as spacenavigator
import pybcapclient.bcapclient as bcapclient

import random
import numpy as np
import ctypes

def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))

def main():
    flg=True
    ESC = 0x1B          # [ESC] virtual key code
    
    ### set IP Address , Port number and Timeout of connected RC8
    host = "192.168.0.1"
    port = 5007
    timeout = 2000
    ### Handls
    hctrl=0
    hrob=0

    sumstate = np.zeros(7)
    target_pos = np.zeros(7)
    org_pos = np.zeros(7)
    success = spacenavigator.open()
    if success:
        bcap = bcapclient.BCAPClient(host,port,timeout)
        bcap.service_start("")
        print("Start b-cap service")

        Name = ""
        Provider="CaoProv.DENSO.VRC"
        Machine = ("localhost")
        Option = ("")
        hctrl = bcap.controller_connect(Name,Provider,Machine,Option)
        print("Connect Ctrl")
        #Connect To arm
        hrob = bcap.controller_getrobot(hctrl,"Arm","")
        print("Connect Robot")
        #Take Arm
        Command = "TakeArm"
        Param = [0,0]
        bcap.robot_execute(hrob,Command,Param)
        print("Take Arm")
        #Motor On
        Command = "Motor"
        Param = [1,0]
        bcap.robot_execute(hrob,Command,Param)
        print("Motor On")
        #Get CurPos
        Command = "CurPos"
        Param = ""
        tmp_cur_pos = bcap.robot_execute(hrob,Command,Param)
        org_pos = np.array(tmp_cur_pos[0:7])
        print("Origin Pos")
        print(org_pos)
        org_list = org_pos.tolist()

        origin_pos = org_pos
        print(origin_pos)

        while flg:
            state = spacenavigator.read()
            arr_state = np.array([state.x, state.y, state.z,state.pitch,-1*state.roll,-1*state.yaw,0])
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
        #End while
        if hrob != 0:
            bcap.robot_release(hrob)
            hrob = 0
            print("Release Robot")
        #End if
        if hctrl != 0:
            bcap.controller_disconnect(hctrl)
            hctrl = 0
            print("Dissconnect Controller")
        bcap.service_stop()
        print("b-cap service Stop")
    #End if
    else:
        print("Failed spacenavigator.Open() ")
    #End else
#End def Main

if __name__ == '__main__':
    main()