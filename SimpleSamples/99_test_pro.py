#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Sample program
# read and write value of Global Variables using b-cap
# I(Integer),F(Sigle Precision Real Number),D(Double Precision Real Number),
# P(Position),S(String)

# b-cap lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import time

# set IP Address , Port number and Timeout of connected Robot Controller (RC8,RC8A,COBOTTA,RC9)
host = "192.168.0.1"
port = 5007
timeout = 2000

# Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

Name = ""
Provider = "CaoProv.DENSO.VRC"
# Provider = "CaoProv.DENSO.VRC9"
Machine = "localhost"
Option = "@IfNotMember"
# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect ")
print(m_bcapclient.controller_getname(hCtrl))

for i in range(5):
    time.sleep(1)
    print(i)
