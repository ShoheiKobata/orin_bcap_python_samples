# -*- coding:utf-8 -*-

#b-capを使用してRC8の内のプログラム(pro1.pcs)を操作する。
#フォルダ構成はこのプログラム(03_Task.py)と同じ
#ディレクトリにbCAPClientのpythonファイル3つが存在すること
#bcapclient.py , orinexception.py , variant.py
#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import bcapclient
import random

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

HRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
print("AddRobot")

#
Command = "TakeArm"
Param = [0,0]
m_bcapclient.robot_execute(HRobot,Command,Param)
print("TakeArm")
#
Comp=1
Pose = "@P P1"
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@P P[1]")
Pose = "@P P2"
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@P P[2]")
Pose = "@P P3"
m_bcapclient.robot_move(HRobot,Comp,Pose,"")
print("Complete Move P,@P P[3]")

Command = "GiveArm"
Param = None
m_bcapclient.robot_execute(HRobot,Command,Param)
print("GiveArm")

#切断処理
if(HRobot != 0):
    m_bcapclient.robot_release(HRobot)
    print("Release Pro1")
#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
m_bcapclient.service_stop()
print("B-CAP service Stop")

