# -*- coding:utf-8 -*-

# Sample program
# Sysinfo and Sysstate command

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import time
import pybcapclient.bcapclient as bcapclient

# this is sample program to use evp command
# EVP Project data needs to be created in advance

EVPProjectFile = "emg"

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


h_EVP2_Ctrl = m_bcapclient.controller_connect("", "CaoProv.DENSO.EVP2", "", "project= " + EVPProjectFile)
data_names = ['ModelID', 'RobotPoint', 'PixelPoint', 'Decode Result', 'SubRegionCheckResult', 'InterferenceCheck', 'InterferenceArea', 'RegionID', 'WorkDatas']
for i in range(10):
    t1 = time.time()
    print(f"count : {i}")
    rets = m_bcapclient.controller_execute(h_EVP2_Ctrl, 'run')
    work_count = rets[0]
    print(f"Work Count : {work_count}")
    if work_count > 0:
        print('work Datas')
        for work_data in rets[1]:
            for data_name, data in zip(data_names, work_data):
                print(f"{data_name}:{data}")
            # End for
        # End for
        print(f"FeederAction :{rets[2]}")
        print(f"PartLoadEvaluatorCoverRates :{rets[3]}")
        print(f"ConfirmExistence :{rets[4]}")
    # End if
    # 処理後の時刻
    t2 = time.time()
    elapsed_time = t2 - t1
    print(f"経過時間:{elapsed_time}[sec]")


# Disconnect
if(hCtrl != 0):
    m_bcapclient.controller_disconnect(hCtrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
