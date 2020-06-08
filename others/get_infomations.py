# -*- coding:utf-8 -*-

# Sample program
# read and write value of IO using b-cap

# b-cap Lib URL 
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient

### refer: https://www.fa-manuals.denso-wave.com/en/usermanuals/000384/
SystemStatus = ["Reserved","Reserved","Reserved","Reserved","Reserved","Reserved","Reserved","Command processing complete","Reserved","Reserved","Robot is running (encoder level)","Robot is running (command level)","1 cycle complete","Manual mode or Teach check mode","Cal complete","Program start reset","Reserved","Reserved","When stop process is running","Protective Stop","Automatic robot run enabled","Emergency stop status","Reserved","Continue start allowed","Robot warning","Battery exhaustion warning","When an executable token is not set to the Teach Pendant in Auto Mode","Automatic mode","Robot initialization complete (in I/O standard or MiniIO dedicated mode) / Robot power On complete (in I/O compatible mode)","Servo On","Robot error","Robot in operation (program running)"]

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

### Controller System Infomation
ret = m_bcapclient.controller_execute(hCtrl,"SysInfo",0)
print("Serial No." + str(ret))
ret = m_bcapclient.controller_execute(hCtrl,"SysInfo",15)
if ret==-1:
    print("Encoder battery maintenance date: Maintenance date has passed")
else:
    print("Encoder battery maintenance date: Maintenance date has not arrived yet")
# End if

### Controller System States
ret = m_bcapclient.controller_execute(hCtrl,"SysState")
ret_bin = "{:032b}".format(ret) # Zero binding 32bit
print(ret_bin)
print(type(ret_bin))

for i,bit_data in enumerate(ret_bin):
    print(str(i) + SystemStatus[i] + "::" + str(bit_data))
# Disconnect
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
#End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
