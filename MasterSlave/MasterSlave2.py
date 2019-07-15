#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Master Slave System program using b-cap slave motion
# Other commands can not be executed during b-cap slave mode. So if you want to move the hand, you will get another robot handler.

# master Robot - COBOTTA
# slave Robot - COBOTTA or VS or VM
# 

import pybcapclient.bcapclient as bcap
import time
import ctypes

### Config ###
MasterIpStr = "192.168.0.1"
SlaveIpStr = "192.168.0.2"
port = 5007
timeout = 2000
##############

def getkey(key):
    return(bool(ctypes.windll.user32.GetAsyncKeyState(key)&0x8000))
# End def

def printlist():
    print("[ESC] : Close Application")
    print("[1] : Start Synchro Mode")
    print("[2] : End Synchro Mode")
# End def

ESC = 0x1B          # Virtual key code of [ESC] key
key_1 = 0X31        # Virtual key code of [1] key
key_2 = 0X32        # Virtual key code of [2] key

### Connection processing of tcp communication
m_bcapclient = bcap.BCAPClient(MasterIpStr,port,timeout)
s_bcapclient = bcap.BCAPClient(SlaveIpStr,port,timeout)
print("Open Connection")

### start b_cap Service
m_bcapclient.service_start("")
s_bcapclient.service_start("")
print("Send SERVICE_START packet")

### set Parameter
Name = ""
Provider="CaoProv.DENSO.VRC"
Machine = ("localhost")
Option = ("")

# Connect To RC8
m_hctrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
s_hctrl = s_bcapclient.controller_connect(Name,Provider,Machine,Option)

m_hrob = m_bcapclient.controller_getrobot(m_hctrl,"m_Arm")
s_hrob = s_bcapclient.controller_getrobot(s_hctrl,"s_Arm")

loop_flg = True
sync_flg = False
tmpio = True

s_bcapclient.robot_execute(s_hrob,"TakeArm",[0,0])
s_bcapclient.robot_execute(s_hrob,"Motor",[1,0])
s_bcapclient.robot_execute(s_hrob,"ExtSpeed",100)

print("Connect and Init OK")
print("[ESC] : Close Application")
print("[1] : Start Synchro Mode")
print("[2] : End Synchro Mode")
print("=====Synchro Off=====")

Param = [-1,1]
ret = 0
handFlg = False
m_handPos_old = 0.0

while loop_flg:
    handFlg = False
    start = time.time()

    # Get Master Robot Datas
    m_jnt = m_bcapclient.robot_execute(m_hrob,"CurJnt")
    m_handPos = m_bcapclient.controller_execute(m_hctrl,"HandCurPos")
    posedata = [m_jnt,"J","@P"]
    # Check slave robot moving
    ret_motion_comp = s_bcapclient.robot_execute(s_hrob,"MotionComplete",Param)

    '''
    # COBOTTA Hand check dist
    if(abs(m_handPos-m_handPos_old) > 0.25):
        if((1 < m_handPos) and (m_handPos<28)):
            handFlg = True
        # End if
    # End if
    '''
    if sync_flg:
        if(ret_motion_comp==True):
           s_bcapclient.robot_execute(s_hrob,"MotionSkip",[-1,3])
        posout =  "J(" + ', '.join(map(str, m_jnt)) + ")"
        print(posout)
        s_outrange = s_bcapclient.robot_execute(s_hrob,"OutRange",posout) 
        if(s_outrange==0):
            s_bcapclient.robot_move(s_hrob,1,posedata,"Next")
        
   '''
    # COBOTTA Hand move
    s_handpos = s_bcapclient.controller_execute(s_hctrl,"HandCurPos")
    if(handFlg == True):
        if((s_handpos-m_handPos)>0):
            s_hold = s_bcapclient.controller_execute(s_hctrl,"HandHoldState")
            if(s_hold==False):
                s_bcapclient.controller_execute(s_hctrl,"HandMoveAH",[m_handPos,100,6])
        else:
            s_bcapclient.controller_execute(s_hctrl,"HandMoveA",[m_handPos,100])
        m_handPos_old = m_handPos
    '''

    if getkey(ESC):
        loop_flg = False
        print("=====Finish Application=====")
    if getkey(key_1):
        if sync_flg==False:
            sync_flg = True
            print("=====Synchro On=====")
            printlist()
    if getkey(key_2):
        if sync_flg==True:      
            sync_flg = False
            print("=====Synchro Off=====")
            printlist()

'''
    elapsed_time = time.time() - start
    print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")
    if(elapsed_time < 0.004):
        print("===================================")
'''
    #End If
#End while

###Give Arm 
s_bcapclient.robot_execute(s_hrob,"GiveArm")

###DisConnect
if(m_hrob != 0):
    m_bcapclient.robot_release(m_hrob)
if(s_hrob != 0):
    s_bcapclient.robot_release(s_hrob)
if(m_hctrl != 0):
    m_bcapclient.controller_disconnect(m_hctrl)
if(s_hctrl != 0):
    s_bcapclient.controller_disconnect(s_hctrl)

m_bcapclient.service_stop()
s_bcapclient.service_stop()
# End Application