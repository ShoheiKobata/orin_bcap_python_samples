# -*- coding:utf-8 -*-

# COBOTTA
# Vaccum

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import random
import time
import csv
import os

import pybcapclient.bcapclient as bcapclient

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
port = 5007
timeout = 2000

# test datas


ret = []


def vacuum_load_check(sngPower, interval, loadtime):

    filename = str(sngPower) + "%_interval" + str(interval) + \
        "ms_LoadTime" + str(loadtime) + "ms.csv"

    f = open(os.path.join("data", filename), 'w')
    writer = csv.writer(f, lineterminator='\n')
    header = ["Time(s)", "HandCurPressure[kPa]", "HandCurLoad[%]"]
    writer.writerow(header)

    # f = open(os.path.join("data", filename), 'w')
    # writer = csv.writer(f, lineterminator='\n')
    # header = ["Time(ms)", "HandCurPressure[kPa]", "HandCurLoad[%]"]

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
        hCtrl = m_bcapclient.controller_connect(
            Name, Provider, Machine, Option)
        print("Connect RC8")
        # Get Robot Handle
        hRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
        print("Get Arm Handle")

        param = [sngPower, True]
        m_bcapclient.controller_execute(hCtrl, "HandMoveVH", param)
        strat_time = time.time()
        Interval_Stime = time.time()
        flg_load = True
        # for i in range(20):
        while True:
            if interval > 0:
                interval_time = time.time() - Interval_Stime
                if flg_load is True:
                    if loadtime < interval_time:
                        m_bcapclient.controller_execute(hCtrl, "HandStop")
                        Interval_Stime = time.time()
                        flg_load = False
                    else:
                        pass
                    # End if
                else:
                    if interval < interval_time:
                        m_bcapclient.controller_execute(
                            hCtrl, "HandMoveVH", param)
                        Interval_Stime = time.time()
                        flg_load = True
                    # End if
                # End if
            # End if

            time.sleep(0.3)
            retPressure = m_bcapclient.controller_execute(
                hCtrl, "HandCurPressure")
            retLoad = m_bcapclient.controller_execute(hCtrl, "HandCurLoad")
            elapsed_time = time.time() - strat_time
            row = [elapsed_time, retPressure, retLoad]

            print(row)
            # ret.append(row)
            writer.writerow(row)
            if retLoad > 100:
                break
            # End if
            # if elapsed_time > 600:
                # break
            # End if
            errorcnt = m_bcapclient.controller_execute(
                hCtrl, "GetCurErrorCount")
            if errorcnt > 0:
                break
            # End if
        # End while

        m_bcapclient.controller_execute(hCtrl, "HandStop")
        print("HandStop")

        strat_time = time.time()
        while True:
            time.sleep(0.5)
            retPressure = m_bcapclient.controller_execute(
                hCtrl, "HandCurPressure")
            retLoad = m_bcapclient.controller_execute(hCtrl, "HandCurLoad")
            elapsed_time = time.time() - strat_time
            row = [elapsed_time, retPressure, retLoad]
            print(row)
            # ret.append(row)
            writer.writerow(row)

            if elapsed_time > 600:
                break
            # End if
        # End while

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
            error_description = m_bcapclient.controller_execute(
                hCtrl, "GetErrorDescription", errorcode_int)
            print("Error Description : " + error_description)
        else:
            print(e)

    finally:

        while True:
            time.sleep(0.5)
            retPressure = m_bcapclient.controller_execute(
                hCtrl, "HandCurPressure")
            retLoad = m_bcapclient.controller_execute(hCtrl, "HandCurLoad")
            elapsed_time = time.time() - strat_time
            row = [elapsed_time, retPressure, retLoad]
            print(row)
            # ret.append(row)
            writer.writerow(row)

            if retLoad < 40:
                break
            # End if
        # End while

        m_bcapclient.controller_execute(hCtrl, "ClearError")

        # DisConnect
        if(hRobot != 0):
            m_bcapclient.robot_release(hRobot)
            print("Release Robot Handle")
        # End If
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
            print("Release Controller")
        # End If
        m_bcapclient.service_stop()
        print("B-CAP service Stop")

        # f = open(os.path.join("data", filename), 'w')
        # writer = csv.writer(f, lineterminator='\n')
        # header = ["Time(s)", "HandCurPressure[kPa]", "HandCurLoad[%]"]
        # writer.writerow(header)
        # writer.writerows(ret)
        f.close()


def main():

    # for power in range(100, 20, -10):
    #    vacuum_load_check(power, 0, 0)
    # End for
    for interval in range(5, 15, 5):
        for load in range(5, 15, 5):
            for power in range(100, 80, -10):
                vacuum_load_check(power, interval, load)
            # End for
        # Endfor
    # Endfor


if __name__ == '__main__':
    main()
