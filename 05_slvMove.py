# -*- coding:utf-8 -*-

#b-capを使用して slave Move でロボットを動作させる

#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient

#接続先RC8 の　IPアドレス、ポート、タイムアウトの設定
host = "10.6.228.192"
port = 5007
timeout = 2000

#TCP通信の接続処理
m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
print("Open Connection")

#b_cap Service を開始する
m_bcapclient.service_start("")
print("Send SERVICE_START packet")


Name = ""
Provider="CaoProv.DENSO.VRC"
Machine = ("localhost")
Option = ("")

#RC8との接続処理 (RC8(VRC)プロバイダ)
hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
print("Connect RC8")
#robotハンドル取得
HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
print("AddRobot")

#軸の制御権を取得
Command = "TakeArm"
Param = [0,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("TakeArm")

#Motor On
Command = "Motor"
Param = [1,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("Motor On")

#初期位置に移動
Comp=1
Pos_value = [0.0 , 0.0 , 90.0 , 0.0 , 90.0 , 0.0]
Pose = [Pos_value,"J","@E"]
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")

# Slave move: Change return format
Command = "slvRecvFormat"
# Param = 0x0001  # Change the format to position
Param = 0x0014  # hex(10): timestamp, hex(1): [pose, joint]
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Slave move: Change mode
Command = "slvChangeMode"
# Param = 0x001  # Type P, mode 0 (buffer the destination)  
Param = 0x101  # Type P, mode 1 (overwrite the destination)  
# Param = 0x102  # Type J, mode 1 (overwrite the joint)  
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

# Send POS slvMove
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

# Slave move: Change mode
Command = "slvChangeMode"  
Param = 0x000  # finish Slave Move  
m_bcapclient.robot_execute(HRobot, Command, Param)
print("slvMove Format Change" + Command + ":" + str(Param))

#Release Handle and Disconnect
if HRobot != 0:
    m_bcapclient.robot_release(HRobot)
    print("Release Robot")
if hCtrl != 0:
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")

#b-cap service stop
m_bcapclient.service_stop()
print("b-cap service Stop")

del m_bcapclient
print("Finish")