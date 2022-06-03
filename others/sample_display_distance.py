# -*- coding:utf-8 -*-

# sample program
# This program is sample to display the moving distance.
# It displays the remaining moving distance as shown below.
'''
 x:  -7.91
 y: 117.11
 z: 109.82
 [######                        ]  22%
'''
# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import time
import math
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
name = ""
provider = "CaoProv.DENSO.VRC"
machine = "localhost"
option = "@IfNotMember"

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hctrl = m_bcapclient.controller_connect(name, provider, machine, option)
    print("Connect RC8")
    hrobot = m_bcapclient.controller_getrobot(hctrl, "Arm", "")

    start_pos = m_bcapclient.robot_execute(hrobot, "CurPos")
    cur_pos = m_bcapclient.robot_execute(hrobot, "CurPos")
    while True:
        time.sleep(0.008)
        if m_bcapclient.robot_execute(hrobot, "MotionComplete", [0, 0]):
            # Operation command is complete: VARIANT_TRUE,
            start_pos = m_bcapclient.robot_execute(hrobot, "CurPos")
            dest_pos = start_pos
        else:
            # Running, suspended, continue-stopped: VARIANT_FALSE
            dest_pos = m_bcapclient.robot_execute(hrobot, "DestPos")
        cur_pos = m_bcapclient.robot_execute(hrobot, "CurPos")

        # End if
        distance = [0, 0, 0]
        sum_distance = 0
        full_distance = [0, 0, 0]
        sum_full_distance = 0.00001
        for i in range(3):
            distance[i] = dest_pos[i] - cur_pos[i]
            full_distance[i] = dest_pos[i] - start_pos[i]
            sum_distance += distance[i] * distance[i]
            sum_full_distance += full_distance[i] * full_distance[i]
        # End for
        distance_len = math.sqrt(sum_distance)
        full_distance_len = math.sqrt(sum_full_distance)
        progress_dist = (full_distance_len - distance_len) / full_distance_len
        bar_dist = "#" * int(progress_dist * 30) + " " * (30 - int(progress_dist * 30))
        print(f" x:{distance[0]:7.2f} \n y:{distance[1]:7.2f} \n z:{distance[2]:7.2f} \n [{bar_dist}] {progress_dist*100:3.0f}% \n" + "\033[4A", end="")


except Exception as e:
    print('=== ERROR Description ===')
    if str(type(e)) == "<class 'pybcapclient.orinexception.ORiNException'>":
        print(e)
        errorcode_int = int(str(e))
        if errorcode_int < 0:
            errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
        else:
            errorcode_hex = hex(errorcode_int)
        print("Error Code : 0x" + str(errorcode_hex))
        error_description = m_bcapclient.controller_execute(hctrl, "GetErrorDescription", errorcode_int)
        print("Error Description : " + error_description)
    else:
        print(e)

except KeyboardInterrupt:
    print('interrupted! Ctrl + C')

finally:
    #  DisConnect
    if(hrobot != 0):
        m_bcapclient.robot_release(hrobot)
        print("Release Robot Handle")
    # End If
    if(hctrl != 0):
        m_bcapclient.controller_disconnect(hctrl)
        print("Release Controller")
    # End If
    m_bcapclient.service_stop()
    print("B-CAP service Stop")
