# -*- coding:utf-8 -*-

# check extension objects and command ()
# This program controls the electric hand in RC8.
# COBOTTA hand control is another command.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap


import pybcapclient.bcapclient as bcapclient
import time

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

# change Parameter [boardID,BoardType,ChannelNo]
h_ESC11_ctrl = m_bcapclient.controller_connect("", "CaoProv.DENSO.ESC11PCI","", "BoardID=0,BoardType=2,ChannelNo=0") #,@EventDisable=true")

print("CONNECT")
m_bcapclient.controller_execute(h_ESC11_ctrl, "MoveA", [10, 100])
print("Move1")
time.sleep(2)
m_bcapclient.controller_execute(h_ESC11_ctrl, "MoveA", [0, 100])
print("Move2")

if(h_ESC11_ctrl != 0):
    m_bcapclient.controller_disconnect(h_ESC11_ctrl)

m_bcapclient.service_stop()
