# -*- coding:utf-8 -*-

# sample program
# Get File Object and edit program(test_pro.pcs) in RC8

# b-cap Lib URL
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

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("Connect RC8")
    # Get file names
    filenames = m_bcapclient.controller_getfilenames(hCtrl, "")
    print("Files in RC8 : " + str(filenames))
    hFile = m_bcapclient.controller_getfile(hCtrl, "test_pro.pcs", "@Create=1")
    file_val = m_bcapclient.file_getvalue(hFile)
    # preview in file text
    # print(file_val)
    title_line = "'!TITLE " + '"test_pro"\n'
    write_str = title_line + 'Sub Main\n    TakeArm Keep = 0\n    move p,@p p[1]\n    move p,@p p[2]\n    move p,@p p[3]\nEnd Sub'
    # write text
    # m_bcapclient.file_putvalue(hFile,write_str)
    # test commands
    # ret = m_bcapclient.file_getdatecreated(hFile) # crate date time "yyyy-mm-dd HH:MM:SS"
    # ret = m_bcapclient.file_getdatelastmodified(hFile) # Last modified date time "yyyy-mm-dd HH:MM:SS"
    # ret = m_bcapclient.file_getdatelastaccessed(hFile) # Last access date time "yyyy-mm-dd HH:MM:SS"
    # ret = m_bcapclient.file_getpath(hFile) # get file path
    # ret = m_bcapclient.file_getsize(hFile) # get file size (byte)
    # ret = m_bcapclient.file_getattribute(hFile)
    # ret = m_bcapclient.file_getname(hFile) # get file name
    # print(ret)

except Exception as e:
    print('=== ERROR Description ===')
    # print( 'type:' + str(type(e)))
    # print('args:' + str(e.args))
    if str(type(e)) == "<class 'pybcapclient.orinexception.ORiNException'>":
        errorcode_int = int(str(e))
        if errorcode_int < 0:
            errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
        else:
            errorcode_hex = hex(errorcode_int)
        print("Error Code : 0x" + str(errorcode_hex))
        error_description = m_bcapclient.controller_execute(
            hCtrl, "GetErrorDescription", errorcode_int)
        print("Error Description : " + error_description)
    else:
        print(e)

# DisConnect
if(hFile != 0):
    m_bcapclient.file_release(hFile)
    print("Release File")
# End If
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
