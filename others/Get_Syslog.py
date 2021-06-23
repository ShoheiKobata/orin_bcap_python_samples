# -*- coding:utf-8 -*-

# Temp program , check command

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import os
import csv
import time
import datetime
import tqdm

import pybcapclient.bcapclient as bcap


class Robot_communicatio():

    def __init__(self, IPadd):
        self.strIP = IPadd

    def connect(self):
        self.port = 5007
        self.timeout = 2000
        try:
            bcapclient = bcap.BCAPClient(self.strIP, self.port, self.timeout)
            self.mbcapclient = bcapclient
            print("TCP Connect")
            self.mbcapclient.service_start("")
            # set Parameter
            Name = ""
            Provider = "CaoProv.DENSO.VRC"
            Machine = ("localhost")
            Option = ("")
            self.hctrl = self.mbcapclient.controller_connect(
                Name, Provider, Machine, Option)

            self.hrobot = self.mbcapclient.controller_getrobot(self.hctrl, "")

            print("Connect RC8")
            return True
        except Exception as e:
            print("Error Connect RC8")
            print(e)

            return False
    # End def

    def start_get_syslog(self):
        self.mbcapclient.robot_execute(self.hrobot, "ClearLog")
        self.mbcapclient.robot_execute(self.hrobot, "StartLog")
        print("Start Log")

    def stop_get_syslog(self):
        self.mbcapclient.robot_execute(self.hrobot, "StopLog")
        print("Stop Log")

    def get_syslog_datas(self):
        log_max = self.mbcapclient.robot_execute(self.hrobot, "GetLogCount")
        ret_datas = []
        print("get log data")
        print("Log Number " + str(log_max))
        for i in tqdm.tqdm(range(log_max)):
            ret_data = self.mbcapclient.robot_execute(
                self.hrobot, "GetLogRecord", i)
            param = "J("+str(ret_data[1+4*0])+","+str(ret_data[1+4*1])+","+str(ret_data[1+4*2])+","+str(
                ret_data[1+4*3])+","+str(ret_data[1+4*4])+","+str(ret_data[1+4*5])+")"
            posedata = self.mbcapclient.robot_execute(
                self.hrobot, "J2P", param)
            ret_data.extend(posedata)
            ret_datas.append(ret_data)

        # End for
        return ret_datas

    def disconnect(self):
        if(self.hctrl != 0):
            self.mbcapclient.controller_disconnect(self.hctrl)
        self.mbcapclient.service_stop()
        print("disconnect")

    def __def__(self):
        try:
            self.disconnect()
            print("Close com port")
        except Exception as e:
            print("Error close com port")
            print(e)
    # End def


def main():

    RC1 = Robot_communicatio("192.168.0.1")
    RC2 = Robot_communicatio("192.168.0.2")

    ret = False
    ret = RC1.connect()
    print('Connect 192.168.0.1 : ' + str(ret))
    ret = RC2.connect()
    print('Connect 192.168.0.2 : ' + str(ret))

    # RC1.start_get_syslog()
    # RC2.start_get_syslog()
    #print('Start SysLog')
    #start_time = time.time()
    # while True:
    #    process_time = time.time() - start_time
    #    if(process_time > 10):
    #        print(" ")
    #        break
    #    else:
    #        print("\r"+"DelayTime : " + str(process_time), end='')
    # End if
    # End while

    RC1.stop_get_syslog()
    RC2.stop_get_syslog()

    RC1_syslog_datas = RC1.get_syslog_datas()
    RC2_syslog_datas = RC2.get_syslog_datas()

    SAVE_DIR = "Data"
    if not os.path.exists(SAVE_DIR):
        # ディレクトリが存在しない場合、ディレクトリを作成する
        os.makedirs(SAVE_DIR)
    HEADER_LINE = ["[J1 - 指令値]", "[J1 - エンコーダ値]", "[J1 - 電流値]", "[J1 - 負荷率]", "[J2 - 指令値]", "[J2 - エンコーダ値]", "[J2 - 電流値]", "[J2 - 負荷率]", "[J3 - 指令値]", "[J3 - エンコーダ値]", "[J3 - 電流値]", "[J3 - 負荷率]", "[J4 - 指令値]", "[J4 - エンコーダ値]", "[J4 - 電流値]", "[J4 - 負荷率]", "[J5 - 指令値]", "[J5 - エンコーダ値]",
                   "[J5 - 電流値]", "[J5 - 負荷率]", "[J6 - 指令値]", "[J6 - エンコーダ値]", "[J6 - 電流値]", "[J6 - 負荷率]", "[J7 - 指令値]", "[J7 - エンコーダ値]", "[J7 - 電流値]", "[J7 - 負荷率]", "[J8 - 指令値]", "[J8 - エンコーダ値]", "[J8 - 電流値]", "[J8 - 負荷率]", "[ユーザデータ]", "[プログラム管理番号]", "[ファイル名]", "[行番号]", "[コントローラ起動時からのカウンタ]", "[ツール番号]", "[ワーク番号]", "[X]", "[Y]", "[Z]", "[Rx]", "[Ry]", "[Rz]", "[Fig]"]
    now = datetime.datetime.now()

    filename = 'syslog1_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
    f = open(os.path.join(SAVE_DIR, filename),
             'w', encoding='shift_jis', newline='')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(HEADER_LINE)
    writer.writerows(RC1_syslog_datas)
    f.close()
    filename = 'syslog2_' + now.strftime('%Y%m%d_%H%M%S') + '.csv'
    f = open(os.path.join(SAVE_DIR, filename),
             'w', encoding='shift_jis', newline='')
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(HEADER_LINE)
    writer.writerows(RC2_syslog_datas)
    f.close()


if __name__ == "__main__":
    main()
