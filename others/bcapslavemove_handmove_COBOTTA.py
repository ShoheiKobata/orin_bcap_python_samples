#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Sample program
# bcap communication and multithreaded sample
# One process moves and the other process gets the position.

# b-cap lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient
import threading
import time

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
        hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
        print("Sub :Connect " + Provider)
        hRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
        time.sleep(1)
        while not stop_event.wait(0.01):
            m_bcapclient.controller_execute(hCtrl, 'HandMoveA', [1, 100])
            m_bcapclient.controller_execute(hCtrl, 'HandMoveA', [29, 100])
            # ret = m_bcapclient.robot_execute(hRobot, "CurPos")
            # print('Sub :' + str(ret))

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
        hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)

        thread = threading.Thread(target=thread_proc, args=(stop_event, ))
        thread.start()

        # get Robot Object Handl
        HRobot = m_bcapclient.controller_getrobot(hCtrl, "Arm", "")
        print("Main:AddRobot")

        m_bcapclient.controller_execute(hCtrl, 'ClearError')

        # TakeArm
        Command = "TakeArm"
        Param = [0, 0]
        m_bcapclient.robot_execute(HRobot, Command, Param)
        print("Main:TakeArm")

        Command = "Motor"
        Param = [1, 0]
        m_bcapclient.robot_execute(HRobot, Command, Param)
        print("Motor on")
        # Move Initialize Position
        Comp = 1
        Pos_value = [0.0, 0.0, 90.0, 0.0, 90.0, 0.0]
        Pose = [Pos_value, "J", "@E"]
        m_bcapclient.robot_move(HRobot, Comp, Pose, "")
        print("Complete Move P,@E J(0.0, 0.0, 90.0, 0.0, 90.0, 0.0)")

        # Slave move: Change Send format
        Command = "slvSendFormat"
        # Change the format to position and Hand IO(0x0020), Mini IO(0x0100)
        Param = 0x0000
        m_bcapclient.robot_execute(HRobot, Command, Param)
        print("slvMove Format Change" + Command + ":" + str(Param))

        # Slave move: Change return format
        Command = "slvRecvFormat"
        # Param = 0x0001  # Change the format to position
        Param = 0x0014  # hex(10): timestamp, hex(4): [pose, joint]
        m_bcapclient.robot_execute(HRobot, Command, Param)
        print("slvMove Format Change" + Command + ":" + str(Param))

        # Slave move: Change mode
        Command = "slvChangeMode"
        # Param = 0x001  # Type P, mode 0 (buffer the destination)
        # Param = 0x201  # Type P, mode 2 (overwrite the destination)
        Param = 0x202  # Type J, mode 2 (overwrite the joint)
        m_bcapclient.robot_execute(HRobot, Command, Param)
        print("slvMove Format Change" + Command + ":" + str(Param))

        # Send POS slvMove
        Command = "slvMove"
        LoopNum = 300
        # oldtime = 0
        for num in range(LoopNum):
            Pos_value = [0.0 + num * 0.1, 0.0, 90.0, 0.0, 90.0, 0.0, 0, 0]  # Joint Type
            print(Pos_value)
            ret = m_bcapclient.robot_execute(HRobot, Command, Pos_value)
        for num in range(LoopNum):
            Pos_value = [0.0 + (LoopNum - num) * 0.1, 0.0, 90.0, 0.0, 90.0, 0.0, 0, 0]  # Joint Type
            ret = m_bcapclient.robot_execute(HRobot, Command, Pos_value)
            print("time:" + str(ret[0]))
            print("pos P,J:" + str(ret[1]))
        # Slave move: Change mode
        Command = "slvChangeMode"
        Param = 0x000  # finish Slave Move
        m_bcapclient.robot_execute(HRobot, Command, Param)
        print("slvMove Format Change" + Command + ":" + str(Param))

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
