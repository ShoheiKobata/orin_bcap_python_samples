# -*- coding:utf-8 -*-

#b-capを使用してRC8の内のプログラム(pro1.pcs)を操作する。
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
#Task(Pro1)のオブジェクトを生成
HTask = 0
HTask = m_bcapclient.controller_gettask(hCtrl,"Pro1","")

#Pro1を開始する
#mode  1:1サイクル起動 2:連続起動 3:1ステップ起動
mode = 3
hr = m_bcapclient.task_start(HTask,mode,"")

#切断処理
if(HTask != 0):
    m_bcapclient.task_release(HTask)
    print("Release Pro1")
#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
m_bcapclient.service_stop()
print("B-CAP service Stop")

