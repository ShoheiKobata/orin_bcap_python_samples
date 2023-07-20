# -*- coding:utf-8 -*-

# This sample program changes the robot settings(Parameters) related to robot motion.

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
Name = ""
Provider = "CaoProv.DENSO.VRC"
Machine = "localhost"
Option = ""

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("Connect RC8")
    # Get Robot Handle
    hRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")

    '''
    set payload
     CaoRobot::Execute( “PayLoad” ) コマンド ( <Payload>[,<Gravity>[,<Inertia>]] )
    < Payload > : [in]先端負荷質量[g] [VT_I4]
    < Gravity > : [in]負荷重心位置 [V 型]
    引数省略時は0 ベクトル（V(0,0,0)）として扱われます．
    < Inertia > : [in]負荷重心イナーシャ [V 型]
    引数省略時は0 ベクトル（V(0,0,0)）として扱われます．
    戻り値 : なし
    '''
    payload = 1000
    gravity = [0.0, 0.0, 100.0]
    inertia = [0.0, 0.0, 0.0]
    m_bcapclient.robot_execute(hRobot, 'PayLoad', [payload, gravity, inertia])

    '''
    CaoRobot::Execute( “SpeedMode” ) コマンド
    SpeedMode ( <Mode> )
    < Mode > : [in]モード [VT_I4]
    0:無効
    1:PTP のみ有効
    2:CP のみ有効
    3:PTP,CP 共に有効
    戻り値 : なし
    '''
    m_bcapclient.robot_execute(hRobot, 'SpeedMode', 1)

    '''
    CaoRobot::Execute( “HighPathAccuracy” ) コマンド
    HighPathAccuracy ( <True/False> )
    < True/False > : [in]有効／無効 [VT_I4]
    有効:True（0 以外）
    無効:False（0）
    戻り値 : なし
    '''
    m_bcapclient.robot_execute(hRobot, 'HighPathAccuracy', True)

    '''
    CaoRobot::Execute( “GrvOffset” ) コマンド
    GrvOffset ( <True/False> )
    < True/False > : [in]有効／無効 [VT_I4]
    有効:True（0 以外）
    無効:False（0）
    戻り値 : なし
    '''
    m_bcapclient.robot_execute(hRobot, 'GrvOffset”', True)


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
        error_description = m_bcapclient.controller_execute(
            hCtrl, "GetErrorDescription", errorcode_int)
        print("Error Description : " + error_description)
    else:
        print(e)

finally:
    # DisConnect
    if(hRobot != 0):
        m_bcapclient.robot_release(hRobot)
        print("Release Robot Handle")
    # End If
    if(hCtrl != 0):
        m_bcapclient.controller_disconnect(hCtrl)
        print("Release Controller")
    # End If
    m_bcapclient.service_stop()
    print("B-CAP service Stop")
