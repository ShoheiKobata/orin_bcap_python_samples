#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Sample program
# bcap communication and multithreaded sample
# One process moves and the other process gets the position.

# b-cap lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import threading

# set IP Address , Port number and Timeout of connected Robot Controller (RC8,RC8A,COBOTTA,RC9)
HOST = "192.168.0.1"
PORT = 5007
TIMEOUT = 2000


def thread_proc(stop_event):
    # def thread_proc(stop_event, m_bcapclient):
    m_bcapclient = bcapclient.BCAPClient(HOST, PORT, TIMEOUT)
    print("Main:Open Connection")
    # start b_cap Service
    m_bcapclient.service_start("")
    print("Main:Send SERVICE_START packet")

    Name = "sub_process"
    Provider = "CaoProv.DENSO.VRC"
    Machine = "localhost"
    Option = ""

    try:
        # Connect to RC8 (RC8(VRC)provider)
        hCtrl = m_bcapclient.controller_connect(
            Name, Provider, Machine, Option)
        print("Sub :Connect " + Provider)
        hRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")

        while not stop_event.wait(0.01):
            ret = m_bcapclient.robot_execute(hRobot, "CurPos")
            print('Sub :' + str(ret))

    except Exception as e:
        print(e)

    finally:
        if(hRobot != 0):
            m_bcapclient.robot_release(hRobot)
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
            print("Sub :Release Controller")


def main_proc():
    stop_event = threading.Event()

    # set Parameter
    # If you want to connect to RC9, please select "VRC9" as the provider name.
    # If you want to connect to RC8, RC8A, or COBOTTA, select "VRC" as the provider name.
    Name = "mainprocess"
    Provider = "CaoProv.DENSO.VRC"
    Machine = "localhost"
    Option = ""

    # Connection processing of tcp communication
    m_bcapclient = bcapclient.BCAPClient(HOST, PORT, TIMEOUT)
    print("Main:Open Connection")

    # start b_cap Service
    m_bcapclient.service_start("")
    print("Main:Send SERVICE_START packet")

    try:
        # Connect to RC8 (RC8(VRC)provider)
        hCtrl = m_bcapclient.controller_connect(
            Name, Provider, Machine, Option)

        thread = threading.Thread(
            # target=thread_proc, args=(stop_event, m_bcapclient,))
            target=thread_proc, args=(stop_event, ))
        thread.start()

        # get Robot Object Handl
        HRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
        print("Main:AddRobot")

        # TakeArm
        Command = "TakeArm"
        Param = [0, 0]
        m_bcapclient.robot_execute(HRobot, Command, Param)
        print("Main:TakeArm")

        # Interpolation
        Comp = 1
        # PoseData (string)
        Pose = "@P P1"
        m_bcapclient.robot_move(HRobot, Comp, Pose, "")
        print("Main:Complete Move P,@P P[1]")
        Pose = "@P P2"
        m_bcapclient.robot_move(HRobot, Comp, Pose, "")
        print("Main:Complete Move P,@P P[2]")
        Pose = "@P P3"
        m_bcapclient.robot_move(HRobot, Comp, Pose, "")
        print("Main:Complete Move P,@P P[3]")

        # Give Arm
        Command = "GiveArm"
        Param = None
        m_bcapclient.robot_execute(HRobot, Command, Param)
        print("Main:GiveArm")

    except Exception as e:
        print(e)

    finally:
        if not (thread is None):
            stop_event.set()
            thread.join()
        # Disconnect
        if(HRobot != 0):
            m_bcapclient.robot_release(HRobot)
            print("Main:Release Robot Object")
        # End If
        if(hCtrl != 0):
            m_bcapclient.controller_disconnect(hCtrl)
            print("Main:Release Controller")
        # End If
        m_bcapclient.service_stop()
        print("Main:B-CAP service Stop")


if __name__ == "__main__":
    main_proc()
