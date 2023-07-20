#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Sample program
# this is sample program to get details of errors currently occurring in the controller.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient

# set IP Address , Port number and Timeout of connected Robot Controller (RC8,RC8A,COBOTTA,RC9)
host = "192.168.0.1"
port = 5007
timeout = 2000

# set Parameter
# If you want to connect to RC9, please select "VRC9" as the provider name.
# If you want to connect to RC8, RC8A, or COBOTTA, select "VRC" as the provider name.
Name = ""
Provider = "CaoProv.DENSO.VRC"
# Provider = "CaoProv.DENSO.VRC9"
Machine = "localhost"
Option = ""

# Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect " + Provider)


error_count = m_bcapclient.controller_execute(hCtrl, 'GetCurErrorCount')
print(f'error num :{error_count}')

print('[エラーコード (VT_I4),エラーメッセージ (VT_BSTR),サブコード (VT_I4),ファイルID+行番号 (VT_I4),プログラム名 (VT_BSTR),行番号 (VT_I4),ファイルID (VT_I4)]')
for i in range(error_count):
    print(m_bcapclient.controller_execute(hCtrl, 'GetCurErrorInfo', i))

# m_bcapclient.controller_execute(hCtrl, 'clearerror')
# print('error clear')

if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
