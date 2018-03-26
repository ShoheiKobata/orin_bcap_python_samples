# -*- coding:utf-8 -*-

#b-capを使用してI[1]の値を読み書きする。
#フォルダ構成はこのプログラム(01_ReadWrite.py)と同じ
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
#I[1]のオブジェクトを生成
IHandl=0
IHandl = m_bcapclient.controller_getvariable(hCtrl,"I1","")
#I[1]の値を読み込む
retI = m_bcapclient.variable_getvalue(IHandl)
print("Read Variable I[1] = %d" %retI)

#書き込む値をランダムに生成
newval = random.randint(0,99)
#I[1]に値を書き込む
m_bcapclient.variable_putvalue(IHandl,newval)
print("Write Variable :newval = %d" %newval)
#I[1]の値を読み込む
retI = m_bcapclient.variable_getvalue(IHandl)
print("Read Variable I[1] = %d" %retI)

#切断処理
if(IHandl != 0):
    m_bcapclient.variable_release(IHandl)
    print("Release I[1]")
#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
m_bcapclient.service_stop()
print("B-CAP service Stop")

