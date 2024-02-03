#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" Robot Modile

    Robot communication module for drawing_demo_app.

"""

import os
import sys
import threading
import time
import traceback
from pybcapclient.bcapclient import BCAPClient
from pybcapclient.orinexception import ORiNException
from logging import INFO, basicConfig, getLogger, NullHandler


class Robot():

    # App param
    rc_is_connected = False
    app_is_running = False
    # Drawing state
    work_str = ''
    draw_line_len = 0
    draw_point_len = 0
    draw_point_no = 0
    draw_line_no = 0
    draw_start_pos = [0, 0]
    draw_end_pos = [0, 0]

    # set logger
    _logger = getLogger(__name__)
    _logger.addHandler(NullHandler())
    _logger.setLevel(INFO)
    _logger.propagate = True
    _logger.info('init img tool')

    # Handl
    bcap = None
    h_ctrl = 0
    h_robot = 0
    h_task = 0
    h_var = 0
    initial_pos = 'J(0,0,90,0,90,0)'
    drawing_pose = [0, 180, 0, 180, 261]

    # spline_datas
    spline_data_len = 0
    play_spline_no = 0

    ctrllog_header = ['[No.]', '[J1 - 指令値]', '[J1 - エンコーダ値]', '[J1 - 電流値]', '[J1 - 負荷率]', '[J2 - 指令値]', '[J2 - エンコーダ値]', '[J2 - 電流値]', '[J2 - 負荷率]', '[J3 - 指令値]', '[J3 - エンコーダ値]', '[J3 - 電流値]', '[J3 - 負荷率]', '[J4 - 指令値]', '[J4 - エンコーダ値]', '[J4 - 電流値]', '[J4 - 負荷率]', '[J5 - 指令値]', '[J5 - エンコーダ値]', '[J5 - 電流値]', '[J5 - 負荷率]', '[J6 - 指令値]', '[J6 - エンコーダ値]', '[J6 - 電流値]', '[J6 - 負荷率]', '[J7 - 指令値]', '[J7 - エンコーダ値]', '[J7 - 電流値]', '[J7 - 負荷率]', '[J8 - 指令値]', '[J8 - エンコーダ値]', '[J8 - 電流値]', '[J8 - 負荷率]', '[ユーザデータ]', '[プログラム管理番号]', '[ファイル名]', '[行番号]', '[コントローラ起動時からのカウンタ]', '[ツール番号]', '[ワーク番号]', '[X - 指令値]', '[Y - 指令値]', '[Z - 指令値]', '[RX - 指令値]', '[RY - 指令値]', '[RZ - 指令値]', '[FIG - 指令値]', '[X - エンコーダ値]', '[Y - エンコーダ値]', '[Z - エンコーダ値]', '[RX - エンコーダ値]', '[RY - エンコーダ値]', '[RZ - エンコーダ値]', '[FIG - エンコーダ値]', '[X - 力覚センサー値]', '[Y - 力覚センサー値]', '[Z - 力覚センサー値]', '[RX - 力覚センサー値]', '[RY - 力覚センサー値]', '[RZ - 力覚センサー値]', '[移動量X - 指令値]', '[移動量Y - 指令値]', '[移動量Z - 指令値]', '[移動量RX - 指令値]', '[移動量RY - 指令値]', '[移動量RZ - 指令値]', '[移動量X - エンコーダ値]', '[移動量Y - エンコーダ値]', '[移動量Z - エンコーダ値]', '[移動量RX - エンコーダ値]', '[移動量RY - エンコーダ値]', '[移動量RZ - エンコーダ値]', '[力制御機能有効]']

    def __init__(self):
        self.init_data = 0
        self.rc_is_connected = False
        self.ifnotm = '@IfNotMember'
        self.thread = None
        self.path1 = os.path.abspath(sys.argv[0])
        self.base_dir = os.path.dirname(self.path1)
    # End init

    def connect(self, host='192.168.0.1', port=5007):
        res = ''
        try:
            if self.rc_is_connected is False:
                # Connection processing of tcp communication
                self.bcap = BCAPClient(host, port, 2000)
                # start b_cap Service
                self.bcap.service_start("")
                # Connect to RC8 (RC8(VRC)provider)
                self.h_ctrl = self.bcap.controller_connect('DrawLineDemo_rc', 'CaoProv.DENSO.VRC', 'localhost', self.ifnotm)
                # get Robot Object Handl
                self.h_robot = self.bcap.controller_getrobot(self.h_ctrl, "arm", self.ifnotm)
                work2 = self.bcap.robot_execute(self.h_robot, 'ConvertPoswork', ['P(73,10,0,0,0,0)', 1, 0])
                work3 = self.bcap.robot_execute(self.h_robot, 'ConvertPoswork', ['P(80,175,0,0,0,0)', 1, 0])
                str_work2 = str(work2)
                str_work3 = str(work3)
                self.bcap.robot_execute(self.h_robot, 'TakeArm', [0, 0])
                self.bcap.robot_execute(self.h_robot, 'SetWorkDef', [2, 'P(' + str_work2[1:-1] + ')'])
                self.bcap.robot_execute(self.h_robot, 'SetWorkDef', [3, 'P(' + str_work3[1:-1] + ')'])
                self.bcap.robot_execute(self.h_robot, 'GiveArm')
                self._logger.info('write work2 : ' + str_work2)
                self._logger.info('write work3 : ' + str_work3)
                res = 'connected'

        except Exception as e:
            self._error_handling(e)
            res = 'Error : ' + str(e)
        finally:
            self._logger.info('')
            return res
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

    def get_pos(self):
        ret_pos = self.bcap.robot_execute(self.h_robot, 'CurPos', '')
        return ret_pos
    # End def

    def start_drawing(self, line_datas, work_str, rate):
        """
        Start line drawing function

        Args:
            line_datas: list
                [
                    [x1,y1],[x2,y2],[].....
                    [x1,y1],[x2,y2],[].....
                    ......
                ]
            work_str: str
                setting work coordinate number
                Work2: portraite work
                Work3: handwrite work
        Returns:
            none
        """
        dir = os.path.join(self.base_dir, 'robot_log')
        self.work_str = work_str
        if not os.path.exists(dir):
            os.makedirs(dir)
        self.app_is_running = True
        try:
            self.bcap.robot_execute(self.h_robot, 'TakeArm', [0, 0])
            self.bcap.robot_change(self.h_robot, 'Tool1')
            self.bcap.robot_change(self.h_robot, work_str)
            self.bcap.robot_execute(self.h_robot, 'Motor', [1, 0])
            self.bcap.robot_execute(self.h_robot, 'ClearLog', '')
            self.bcap.robot_execute(self.h_robot, 'StartLog', '')
            self.thread = threading.Thread(target=self._loop_drawing, args=(line_datas, rate))
            self.thread.start()
        except Exception as e:
            self._error_handling(e)
            self.app_is_running = False

    def _loop_drawing(self, line_datas, rate):
        """
        line drawing function
        This function is intended to run in a separate thread from the main thread.

        Args:
            line_datas: list
                [
                    [x1,y1],[x2,y2],[].....
                    [x1,y1],[x2,y2],[].....
                    ......
                ]
        Returns:
            none
        """
        write_data = []
        self.draw_line_len = len(line_datas)
        time_s = time.time()
        try:
            for line_no, line_data in enumerate(line_datas):
                self.draw_point_len = len(line_data)
                self.draw_line_no = line_no
                for i, point_xy in enumerate(line_data):
                    self.draw_point_no = i
                    # resize
                    point_xy = list(map(lambda n: n * rate, point_xy))
                    # convert
                    point_robot = point_xy + self.drawing_pose
                    str_pos = str(point_robot)
                    pose_data = 'P(' + str_pos[1:-1] + ')'
                    # print(pose_data)
                    if i == 0:
                        self.bcap.robot_execute(self.h_robot, 'Approach', [1, pose_data, '@P 10'])
                    # End if
                    self.bcap.robot_move(self.h_robot, 2, '@P ' + pose_data)
                    write_data.append([line_no, i, time.time() - time_s] + point_robot + [])
                # End for
                self.bcap.robot_execute(self.h_robot, 'Depart', [2, '@P 10'])
            # End for
            self.bcap.robot_move(self.h_robot, 1, '@E ' + self.initial_pos)
            self.bcap.robot_execute(self.h_robot, 'Motor', [0, 0])
            # Get log datas
            self.bcap.robot_execute(self.h_robot, 'StopLog', '')
            elasped_time = time.time() - time_s
            self._logger.info('elasped time =' + str(elasped_time) + '[sec]')
        except Exception as e:
            self._error_handling(e)
        finally:
            self.app_is_running = False
            self.bcap.robot_execute(self.h_robot, 'GiveArm')
            self._logger.info('GiveArm')
            self.work_str = ''
            self.draw_line_len = 0
            self.draw_point_len = 0
            self.draw_point_no = 0
            self.draw_line_no = 0
        # End finally
    # End def

    def move_to_init(self):
        try:
            self.bcap.controller_execute(self.h_ctrl, 'ClearError', None)
            self.bcap.robot_execute(self.h_robot, 'TakeArm', [0, 0])
            self.bcap.robot_execute(self.h_robot, 'Motor', [1, 0])
            self.bcap.robot_execute(self.h_robot, 'Depart', [2, '@P 10'])
            self.bcap.robot_move(self.h_robot, 1, '@P ' + self.initial_pos)
        except Exception as e:
            self._error_handling(e)
        finally:
            self.bcap.robot_execute(self.h_robot, 'Motor', [0, 0])
            self.bcap.robot_execute(self.h_robot, 'GiveArm')

    def __call__(self) -> None:
        print('robot : start call')

    def disconnect(self):
        try:
            if self.h_robot != 0:
                self.bcap.robot_release(self.h_robot)
                self.h_robot = 0
            # End if
            if self.h_ctrl != 0:
                self.bcap.controller_disconnect(self.h_ctrl)
                self.h_ctrl = 0
            # End if
            self.bcap.service_stop()
            res = 'disconnected'
            self.rc_is_connected = False
        except Exception as e:
            self._error_handling(e)
            res = 'Error : ' + str(e)
        finally:
            return res
    # End def

    def __def__(self):
        try:
            self.app_is_running = False
            self.disconnect()
            print("robot : Close com port")
        except Exception as e:
            print("Error close com port")
            print(e)
    # End def

    def _error_handling(self, e):
        type_, value, traceback_ = sys.exc_info()
        err_trace = traceback.format_exception(type_, value, traceback_)
        self._logger.error(err_trace)
        if (type(e) is ORiNException) and (self.h_ctrl != 0):
            print('catch ORiN Exception in Robot Controller')
            errorcode_int = int(str(e))
            if errorcode_int < 0:
                errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
            else:
                errorcode_hex = hex(errorcode_int)
            # End if
            error_description = self.bcap.controller_execute(self.h_ctrl, "GetErrorDescription", errorcode_int)
            self._logger.error('ORiN Error , Error code: 0x' + str(errorcode_hex) + ', Error Description: ' + error_description)
            print("Error Description : " + error_description)
            print("Error Code : 0x" + str(errorcode_hex))
        else:
            self._logger.error(str(type(e)) + ' : ' + str(e))
        # End if
    # End def


def main():
    # Setting logger
    logger = getLogger(__name__)
    os.makedirs(os.path.join(os.path.dirname(sys.argv[0]), "log"), exist_ok=True)
    basicConfig(level=INFO, filename=os.path.join(os.path.dirname(sys.argv[0]), "log", "pyrobot.log"), format="%(asctime)s:%(levelname)s:%(message)s ")
    logger.info('handwritewin rogs')
    # test programs
    record = Robot()
    record.connect(host='192.168.0.1', port=5007)


if __name__ == '__main__':
    main()
