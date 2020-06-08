# -*- coding:utf-8 -*-

# test program
# check the ForceParam command

# b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import random

### set IP Address , Port number and Timeout of connected RC8
host = "127.0.0.1"
port = 5007
timeout = 2000

### Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host,port,timeout)
print("Open Connection")

### start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

### set Parameter
Name = ""
Provider="CaoProv.DENSO.VRC"
Machine = "localhost"
Option = ""

### Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
print("Connect RC8")
try:
    ### get robot handle
    hRobot = m_bcapclient.controller_getrobot(hCtrl,"Arm","")
    m_bcapclient.robot_execute(hRobot,"TakeArm",[0,0])

    ### set Force Parameter
    CtrlNum = 1  # 力制御番号
    Coordinates = 1 #座標系
    Force = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6] #力
    PosEralw = [1.3, 1.4, 1.5, 1.6, 1.7, 1.8] #位置偏差許容    default:[100,100,100,10,10,10]
    Spring = [3.7, 3.8, 3.9, 4.0, 4.1, 4.2]  #柔らかさ  default:100[%]
    Mass = [3.1, 3.2, 3.3, 3.4, 3.5, 3.6] #慣性 default:[100,100,100,100,100,100]
    Damp = [2.5, 2.6, 2.7, 2.8, 2.9, 3.0] #粘性 default:100[%]
    CurLmt = [100,100,100,100,100,100] # 電流制限値 default:[100,100,100,100,100,100]
    Offset = [0,0,0,0,0,0] # オフセット値   default:[0,0,0,0,0,0]
    Eralw = [1.9, 2.0, 2.1, 2.2, 2.3, 2.4] #各軸偏差許容    default:[10,10,10,10,10,10]
    lMode = 0 # 速度制御モード　将来の予約領域です0を設定してください。
    Rate = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2] #制御割合 default:[0,0,0,0,0,0]
    SpMax = 5.5 #最大並進速度  default:10[mm/s]
    RSpMax = 5.6 #最大回転速度  default:10[deg/s]
    
    Param = [CtrlNum,Coordinates,Force,PosEralw,Spring,Mass,Damp,CurLmt,Offset,Eralw,lMode,Rate,SpMax,RSpMax]

    m_bcapclient.robot_execute(hRobot,"ForceParam",Param)
except Exception as e:
    print('=== エラー内容 ===')
#    print( 'type:' + str(type(e)))
#    print('args:' + str(e.args))
    print(str(e))

m_bcapclient.robot_execute(hRobot,"GiveArm")

### Disconnect

#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
m_bcapclient.service_stop()
print("B-CAP service Stop")

