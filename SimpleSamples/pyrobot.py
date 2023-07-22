#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""Robot module

This is a sample program for a class module that group robot processing when creating an application.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

"""

import os
import sys
import traceback
from pybcapclient.bcapclient import BCAPClient
from pybcapclient.orinexception import ORiNException

from logging import INFO, basicConfig, getLogger
logger = getLogger(__name__)


class Robot():
    """Robot Class for Application

    Robot class for applications. You may develop functions and variables needed for your application.

    Attributes:

    """

    # bcap handle
    bcap = None
    h_ctrl = 0
    h_rob = 0

    # option_str
    ifnotm = '@IfNotMember'

    def __init__(self) -> None:
        pass
    # End def

    def connect(self, ip='192.168.0.1', rc_type='RC9', name='_'):
        """connect

        Function to start communication with the robot controller

        Args:
            ip (str): IP Address ("XXX.XXX.XXX.XXX") of robot controller
            rc_type (str): Robot cotroller type  RC8 or RC9
            name (str): name, arbitrary string
        """
        ret = False
        try:
            if rc_type == 'RC8':
                provider = 'CaoProv.DENSO.VRC'
            elif rc_type == 'RC9':
                provider = 'CaoProv.DENSO.VRC9'
            else:
                raise ValueError('rc_type value error')
            self.bcap = BCAPClient(host=ip, port=5007, timeout=2000)
            logger.info('connect robot')
            self.bcap.service_start('')
            self.h_ctrl = self.bcap.controller_connect(name + '_App', provider, 'localhost', self.ifnotm)
            logger.info('Connected RC')
            self.h_rob = self.bcap.controller_getrobot(self.h_ctrl, 'arm', self.ifnotm)
            self.h_mode = self.bcap.controller_getvariable(self.h_ctrl, '@Mode', self.ifnotm)
        except Exception as e:
            self._error_handling(e)
            ret = False
        else:
            ret = True
        return ret
    # End def

    def get_base_info(self):
        """get base information

        get basic information about connectded controller and robot

        Args:
            None
        Returns:
            list: [serial, robot_type, vrc_version]
            serial: str
            robot_type: str
            vrc_version: str
        """
        serial = self.bcap.controller_execute(self.h_ctrl, 'SysInfo', 0)
        robot_type = self.bcap.robot_execute(self.h_rob, 'GetRobotTypeName')
        h_version = self.bcap.controller_getvariable(self.h_ctrl, '@VERSION', self.ifnotm)
        vrc_version = self.bcap.variable_getvalue(h_version)
        return [serial, robot_type, vrc_version]
    # End def

    def save_all_pacscript(self, save_dir='', first=True, handle_parent=0):
        """save pacscript files

        Save the program in the robot controller to the PC.

        Args:
            save_dir: str
                Directory where programs is saved
        """
        try:
            os.makedirs(save_dir, exist_ok=True)
            h_files = []
            if first:
                file_names = self.bcap.controller_getfilenames(self.h_ctrl)
                for file_name in file_names:
                    h_files.append(self.bcap.controller_getfile(self.h_ctrl, file_name, self.ifnotm))
            else:
                file_names = self.bcap.file_getfilenames(handle_parent)
                for file_name in file_names:
                    h_files.append(self.bcap.file_getfile(handle_parent, file_name, self.ifnotm))
            # End for
            for h_file in h_files:
                file_name = self.bcap.file_getname(h_file)
                if (file_name.find('.lst') > 0):
                    continue
                if (file_name.find('\\') > 0):
                    print(file_name)
                    child_dir = os.path.join(save_dir, file_name)
                    self.save_all_pacscript(save_dir=child_dir, first=False, handle_parent=h_file)
                else:
                    data = self.bcap.file_getvalue(h_file)
                    f = open(os.path.join(save_dir, file_name), 'w', encoding='shift-jis', newline='')
                    f.write(data)
                    f.close()
                # End if
            # End for
        except Exception as e:
            self._error_handling(e)

    def err_func(self):
        try:
            h_int = self.bcap.controller_getvariable(self.h_ctrl, 'I1')
            self.bcap.variable_putvalue(h_int, [0, 0, 90, 0, 90, 0])
        except Exception as e:
            self._error_handling(e)
    # End def

    def disconnect(self):
        if self.h_rob != 0:
            self.bcap.robot_release(self.h_rob)
            self.h_rob = 0
        if self.h_ctrl != 0:
            self.bcap.controller_disconnect(self.h_ctrl)
            self.h_ctrl = 0
        if self.bcap is not None:
            self.bcap.service_stop()
            print("b-cap service Stop")
            del self.bcap
        # End if
        print("Finish")
    # End if

    def _error_handling(self, e):
        type_, value, traceback_ = sys.exc_info()
        err_trace = traceback.format_exception(type_, value, traceback_)
        print(err_trace)
        logger.error(err_trace)
        if (type(e) == ORiNException) and (self.h_ctrl != 0):
            print('catch ORiN Exception in Robot Controller')
            errorcode_int = int(str(e))
            if errorcode_int < 0:
                errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
            else:
                errorcode_hex = hex(errorcode_int)
            # End if
            print("Error Code : 0x" + str(errorcode_hex))
            error_description = self.bcap.controller_execute(self.h_ctrl, "GetErrorDescription", errorcode_int)
            print("Error Description : " + error_description)
            logger.error('ORiN Error , Error code: 0x' + str(errorcode_hex) + ', Error Description: ' + error_description)
        else:
            print(type(e))
            print(e)
            logger.error(str(type(e)) + ' : ' + str(e))
        # End if
    # End def

    def __del__(self):
        self.disconnect()
    # End def
# End class


def main():
    os.makedirs(os.path.join(os.path.dirname(sys.argv[0]), "log"), exist_ok=True)
    basicConfig(level=INFO, filename=os.path.join(os.path.dirname(sys.argv[0]), "log", "server.log"), format="%(asctime)s:%(levelname)s:%(message)s ")
    logger.info('rob lib rogs')
    rob = Robot()
    connected = rob.connect(ip='127.0.0.1', rc_type='RC8', name='sample')
    if connected:
        info = rob.get_base_info()
        save_dir = '_'.join(info)
        save_dir = save_dir.replace('.', '_')
        rob.save_all_pacscript(save_dir=save_dir, first=True)
        rob.err_func()
    # End if


if __name__ == '__main__':
    main()
