# -*- coding:utf-8 -*-

# Sample program
# read values of All Integer types  Variables using b-cap

# b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import random

### set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
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

### get I[1] Object Handl
IHandl=0
IHandl = m_bcapclient.controller_getvariable(hCtrl,"I*","")
### Get System Variables "@VAR_I_LEN" Object Handl
VAR_I_Handl = 0
VAR_I_Handl = m_bcapclient.controller_getvariable(hCtrl,"@VAR_I_LEN","")

### Get System Variables "@VAR_I_LEN" Value
ret_I_Len = m_bcapclient.variable_getvalue(VAR_I_Handl)

for IDnum in range(ret_I_Len):
    ###Change ID Number I[*]
    m_bcapclient.variable_putid(IHandl,IDnum)    
    ### read value of I[*]
    retI = m_bcapclient.variable_getvalue(IHandl)
    print("Read Variable I[%d] = %d" %(IDnum,retI))

### Disconnect
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

