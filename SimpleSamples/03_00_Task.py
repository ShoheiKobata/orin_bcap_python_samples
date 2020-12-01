# -*- coding:utf-8 -*-

# Sample program
# Control of task(pro1.pcs) using b-cap

<<<<<<< HEAD
# b-cap Lib URL
=======
#b-cap Lib URL 
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient


<<<<<<< HEAD
# set IP Address , Port number and Timeout of connected RC8
host = "127.0.0.1"
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
Machine = ("localhost")
Option = ("")

# Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
print("Connect RC8")
# get task(pro1) Object Handl
HTask = 0
HTask = m_bcapclient.controller_gettask(hCtrl, "Pro1", "")

# Start pro1
# mode  1:One cycle execution, 2:Continuous execution, 3:Step forward
mode = 1
hr = m_bcapclient.task_start(HTask, mode, "")
=======
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
Machine = ("localhost")
Option = ("")

### Connect to RC8 (RC8(VRC)provider)
hCtrl = m_bcapclient.controller_connect(Name,Provider,Machine,Option)
print("Connect RC8")
### get task(pro1) Object Handl
HTask = 0
HTask = m_bcapclient.controller_gettask(hCtrl,"Pro1","")

#Start pro1
#mode  1:One cycle execution, 2:Continuous execution, 3:Step forward
mode = 1
hr = m_bcapclient.task_start(HTask,mode,"")
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc

# Disconnect
if(HTask != 0):
    m_bcapclient.task_release(HTask)
    print("Release Pro1")
<<<<<<< HEAD
# End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
=======
#End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
>>>>>>> 410caa0f0e32954f7ce606cad2b859196c3598bc
m_bcapclient.service_stop()
print("B-CAP service Stop")
