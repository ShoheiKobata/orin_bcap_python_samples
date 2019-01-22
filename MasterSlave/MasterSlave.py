#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# master Robot - COBOTTA
# slave Robot - COBOTTA or VS or VM
# 

import win32com.client
import time
import ctypes

### Config ###
MasterIpStr = "Server=192.168.0.1"
SlaveIpStr = "Server=192.168.0.2"

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

# Create CAOEngine
caoEng = win32com.client.Dispatch("CAO.CaoEngine")
caoWS = caoEng.Workspaces(0)

# Connect To RC8
m_ctrl = caoWS.AddController("","CaoProv.DENSO.RC8", "", MasterIpStr)
s_ctrl = caoWS.AddController("","CaoProv.DENSO.RC8", "", SlaveIpStr)

m_rob = m_ctrl.AddRobot("m_Arm")
s_rob = s_ctrl.AddRobot("s_Arm")

loop_flg = True
sync_flg = False
tmpio = True

s_rob.execute("TakeArm")
s_rob.execute("Motor",[1,0])
s_rob.execute("ExtSpeed",100)

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
    m_jnt = m_rob.execute("CurJnt")
    m_handPos = m_ctrl.execute("HandCurPos")
    posedata = [m_jnt,"J","@P"]
    # Check slave robot moving
    ret_motion_comp = s_rob.execute("MotionComplete",Param)

    '''
    # 
    if(abs(m_handPos-m_handPos_old) > 0.25):
        if((1 < m_handPos) and (m_handPos<28)):
            handFlg = True
        # End if
    # End if
    '''

    if sync_flg:
        if(ret_motion_comp==True):
           s_rob.execute("MotionSkip",[-1,3])
        posout =  "J" + str(m_jnt)
        s_outrange = s_rob.execute("OutRange",posout) 
        if(s_outrange==0):
            s_rob.move(1,posedata,"Next")
        
    '''
    # COBOTTA Hand move
    s_handpos = s_ctrl.execute("HandCurPos")
    if(handFlg == True):
        if((s_handpos-m_handPos)>0):
            s_hold = s_ctrl.execute("HandHoldState")
            if(s_hold==False):
                s_ctrl.execute("HandMoveAH",[m_handPos,100,6])
        else:
            s_ctrl.execute("HandMoveA",[m_handPos,100])
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

