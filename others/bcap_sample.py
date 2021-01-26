# -*- coding:utf-8 -*-

# test program
# Get system variables in each object

import pybcapclient.bcapclient as bcapclient


class bcap:
    '''
        class of bcap
    '''
    # Handl
    m_bcap = None
    H_ctrl = None
    H_robot = None
    H_task = None
    H_Var = None

    # Set param
    Name = ""
    Provider = "CaoProv.DENSO.VRC"
    Machine = "localhost"
    Option = ""

    timeout = 2000

    def __init__(self, host, port):
        # Connection processing of tcp communication
        print("Open Connection")
        self.m_bcap = bcapclient.BCAPClient(host, port, self.timeout)
        # start b_cap Service
        print("Send SERVICE_START packet")
        self.m_bcap.service_start("")

        # Connect to RC8 (RC8(VRC)provider)
        self.H_ctrl = self.m_bcap.controller_connect(
            self.Name, self.Provider, self.Machine, self.Option)
        print("Connect RC8")
        # get Robot Object Handl
        self.H_robot = self.m_bcap.controller_getrobot(self.H_ctrl, "", "")
    # End init

    def __del__(self):
        # DisConnect
        if(self.H_robot != 0):
            self.m_bcap.robot_release(self.H_robot)
        # End If
        if(self.H_ctrl != 0):
            self.m_bcap.controller_disconnect(self.H_ctrl)
            print("Release Controller")
        # End If
        self.m_bcap.service_stop()
        print("B-CAP service Stop")
    # End __del__

    def readIO(self, port):
        port_str = "IO" + str(port)
        H_IO = self.m_bcap.controller_getvariable(self.H_ctrl, port_str, "")
        ret = self.m_bcap.variable_getvalue(H_IO)
        print("IO" + str(port) + "=" + str(ret))
        self.m_bcap.variable_release(H_IO)
    # End readIO

    def readCtrlValAll(self):
        var_name_list = self.m_bcap.controller_getvariablenames(
            self.H_ctrl, "")
        bstrName = ""
        bstrOpt = ""
        indexes = [i for i in var_name_list if "@" in i]
        for bstrName in indexes:
            Htemp = self.m_bcap.controller_getvariable(
                self.H_ctrl, bstrName, bstrOpt)
            ret = self.m_bcap.variable_getvalue(Htemp)
            print("Controller Class VariableName=" + bstrName)
            print(ret)
        # End for
    # End def readCtrlValAll

    def readRobotValAll(self):
        var_name_list = self.m_bcap.robot_getvariablenames(self.H_robot, "")
        print(var_name_list)
        bstrOpt = ""
        indexes = [i for i in var_name_list if "@" in i]
        for num in range(20):
            print("Robot Class VariableName=" + indexes[num])
            Htemp = self.m_bcap.robot_getvariable(
                self.H_robot, indexes[num], bstrOpt)
            ret = self.m_bcap.variable_getvalue(Htemp)
            print(ret)
    # End def readCtrlValAll
# End class


def main():

    # Set IP Address and port num
    host = "127.0.0.1"
    port = 5007

    robclient = bcap(host, port)

    robclient.readCtrlValAll()
    robclient.readRobotValAll()
    # robclient.readIO(128)

    del robclient
# End def main


if __name__ == "__main__":
    main()
# End
