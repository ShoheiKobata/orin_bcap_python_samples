# -*- coding:utf-8 -*-

#b-capを使用してIO[128]の値を読み書きする。
#フォルダ構成はこのプログラム(02_IOReadWrite.py)と同じ
#ディレクトリにbCAPClientのpythonファイル3つが存在すること
#bcapclient.py , orinexception.py , variant.py
#b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import bcapclient

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
#IO128のオブジェクトを生成
IOHandl = 0
IOHandl = m_bcapclient.controller_getvariable(hCtrl,"IO128","")
#IO128の値を読み込む
retIO = m_bcapclient.variable_getvalue(IOHandl)
print("Read Variable IO128 = %s" %retIO)

#書き込む値は今の状態と反対にする
newval = not(retIO)
#IO128に値を書き込む
m_bcapclient.variable_putvalue(IOHandl,newval)
print("Write Variable :newval = %s" %newval)
#IO128の値を読み込む
retIO = m_bcapclient.variable_getvalue(IOHandl)
print("Read Variable IO128 = %s" %retIO)

#切断処理
if(IOHandl != 0):
    m_bcapclient.variable_release(IOHandl)
    print("Release IO128")
#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
