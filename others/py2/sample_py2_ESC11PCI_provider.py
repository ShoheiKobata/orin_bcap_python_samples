# -*- coding:utf-8 -*-

# check extension objects and command ()
# This program controls the electric hand in RC8.
# COBOTTA hand control is another command.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap


import bcapclient as bcapclient
import time
import os

# プロキシ設定を無視する。
if os.environ.get("https_proxy"):
    del os.environ["https_proxy"]
if os.environ.get("http_proxy"):
    del os.environ["http_proxy"]

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
port = 5007
timeout = 2000

h_ESC11_ctrl = 0
try:
    # Connection processing of tcp communication
    m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
    print "Open Connection"

    # start b_cap Service
    m_bcapclient.service_start(option="")
    print "Send SERVICE_START packet"

    # set Parameter
    Name = ""
    Provider = "CaoProv.DENSO.VRC"
    Machine = ("localhost")
    Option = ("")

    h_ESC11_ctrl = m_bcapclient.controller_connect("", "CaoProv.DENSO.ESC11PCI", "", "BoardID=0,BoardType=2,ChannelNo=0")
    print "Connect Controller"
    m_bcapclient.controller_execute(h_ESC11_ctrl, "MoveA", [10, 100])
    print "Move 1"
    time.sleep(2)   
    m_bcapclient.controller_execute(h_ESC11_ctrl, "MoveA", [0, 100])
    print "Move 2"
    
except Exception as e:
    print 'error'
    print e

if(h_ESC11_ctrl != 0):
    m_bcapclient.controller_disconnect(h_ESC11_ctrl)

m_bcapclient.service_stop()
