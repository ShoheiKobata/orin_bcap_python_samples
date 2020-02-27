# -*- coding:utf-8 -*-

# Sample program
# read and write value of Global Variables using b-cap
# I(Integer),F(Sigle Precision Real Number),D(Double Precision Real Number),
# P(Position),S(String)

# b-cap lib URL
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

# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect RC8")

# get I[1] Object Handl
IHandl = 0
IHandl = m_bcapclient.controller_getvariable(hCtrl, "I1", "")
# read value of I[1]
retI = m_bcapclient.variable_getvalue(IHandl)
print("Read Variable I[1] = %d" % retI)
# Generate random value
newval = retI + 1
# write value of I[1]
m_bcapclient.variable_putvalue(IHandl, newval)
print("Write Variable :newval = %d" % newval)
# read value of I[1]
retI = m_bcapclient.variable_getvalue(IHandl)
print("Read Variable I[1] = %d" % retI)

# get F[1] Object Handl
FHandl = 0
FHandl = m_bcapclient.controller_getvariable(hCtrl, "F1", "")
# read value of F[1]
retF = m_bcapclient.variable_getvalue(FHandl)
print("Read Variable F[1] = ", retF)
# Generate random value
newval = retF + 1.1
# write value of F[1]
m_bcapclient.variable_putvalue(FHandl, newval)
print("Write Variable :newval =", newval)
# read value of F[1]
retF = m_bcapclient.variable_getvalue(FHandl)
print("Read Variable F[1] =", retF)

# get D[1] Object Handl
DHandl = 0
DHandl = m_bcapclient.controller_getvariable(hCtrl, "D1", "")
# read value of D[1]
retD = m_bcapclient.variable_getvalue(DHandl)
print("Read Variable D[1] = ", retD)
# Generate random value
newval = retD + 1.1
# write value of D[1]
m_bcapclient.variable_putvalue(DHandl, newval)
print("Write Variable :newval =", newval)
# read value of D[1]
retD = m_bcapclient.variable_getvalue(DHandl)
print("Read Variable D[1] =", retD)

# get P[1] Object Handl
PHandl = 0
PHandl = m_bcapclient.controller_getvariable(hCtrl, "P1", "")
# read value of P[1]
retP = m_bcapclient.variable_getvalue(PHandl)
print("Read Variable P[1] = ", retP)
# Generate random value
newval = [x + y for (x, y) in zip(retP, [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 0])]
# write value of P[1]
m_bcapclient.variable_putvalue(PHandl, newval)
print("Write Variable :newval =", newval)
# read value of P[1]
retP = m_bcapclient.variable_getvalue(PHandl)
print("Read Variable P[1] =", retP)

# get S[1] Object Handl
SHandl = 0
SHandl = m_bcapclient.controller_getvariable(hCtrl, "S1", "")
# read value of S[1]
retS = m_bcapclient.variable_getvalue(SHandl)
print("Read Variable S[1] = ", retS)
# Generate random value
newval = retS + "hoge"
# write value of S[1]
m_bcapclient.variable_putvalue(SHandl, newval)
print("Write Variable :newval =", newval)
# read value of S[1]
retS = m_bcapclient.variable_getvalue(SHandl)
print("Read Variable S[1] =", retS)

# Disconnect
if(IHandl != 0):
    m_bcapclient.variable_release(IHandl)
    print("Release I[1]")
if(FHandl != 0):
    m_bcapclient.variable_release(FHandl)
    print("Release F[1]")
if(DHandl != 0):
    m_bcapclient.variable_release(DHandl)
    print("Release D[1]")
if(PHandl != 0):
    m_bcapclient.variable_release(PHandl)
    print("Release P[1]")
if(SHandl != 0):
    m_bcapclient.variable_release(SHandl)
    print("Release S[1]")

if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
