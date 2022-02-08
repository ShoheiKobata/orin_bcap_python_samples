# -*- coding:utf-8 -*-

# Sample program
# exec SyncTimeMove And SyncMove with Cooperative Control Function
#

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import time


def main():

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
        # Get Robot Handle
        hMasterRobot = m_bcapclient.controller_getrobot(hCtrl, "Master", "ID=0")
        hSlaveRobot = m_bcapclient.controller_getrobot(hCtrl, "Slave", "ID=1")
        print('Get Robot obj')

        # TakeArm
        m_bcapclient.robot_execute(hMasterRobot, "TakeArm")
        m_bcapclient.robot_execute(hSlaveRobot, "TakeArm")
        print('takeArm')

        # SyncTime Move
        m_bcapclient.robot_execute(hMasterRobot, "SyncTimeStart")
        m_bcapclient.robot_move(hMasterRobot, 1, "@P J(0,0,90,0,90,0)")
        print('Move Master J(0,0,90,0,90,0)')
        time.sleep(2)  # To verify that the Move command does not work
        m_bcapclient.robot_move(hSlaveRobot, 1, "@P J(10,0,90,0,90,0)")
        print('Move Slave J(10,0,90,0,90,0)')
        time.sleep(1)  # To verify that the Move command does not work
        print('Set Move Pos')
        print('Start Move')
        m_bcapclient.robot_execute(hMasterRobot, 'SyncTimeEnd', 0)
        print('Move Finish')

        # SyncTime Move
        m_bcapclient.robot_execute(hMasterRobot, "SyncTimeStart")
        m_bcapclient.robot_move(hMasterRobot, 1, "@P J(10,0,90,0,90,0)")
        m_bcapclient.robot_move(hSlaveRobot, 1, "@P J(0,0,90,0,90,0)")
        print('Set Move Pos')
        print('Start Move')
        m_bcapclient.robot_execute(hMasterRobot, 'SyncTimeEnd', 0)

        # SyncMove
        m_bcapclient.robot_execute(hMasterRobot, "SyncMoveStart", 1)
        m_bcapclient.robot_move(hMasterRobot, 2, "@E J(0,0,90,0,90,0)")
        print('Start SyncMove Follower = Slave Robot')
        m_bcapclient.robot_execute(hMasterRobot, 'SyncMoveEnd', 0)

        # SyncMove
        m_bcapclient.robot_execute(hSlaveRobot, "SyncMoveStart", 0)
        m_bcapclient.robot_move(hSlaveRobot, 2, "@E J(0,0,90,0,90,0)")
        print('Start SyncMove Follower = Master Robot')
        m_bcapclient.robot_execute(hSlaveRobot, 'SyncMoveEnd', 0)

        m_bcapclient.robot_execute(hMasterRobot, "GiveArm")
        m_bcapclient.robot_execute(hSlaveRobot, "GiveArm")
        print('Give Arm')

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
        # DisConnect
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
            print("Release Controller")
        # End If
        m_bcapclient.service_stop()
        print("B-CAP service Stop")


if __name__ == '__main__':
    main()
