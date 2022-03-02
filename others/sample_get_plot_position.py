#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Sample program
# get and plot robot position data

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import itertools
from matplotlib import pyplot as plt
from matplotlib import animation

import pybcapclient.bcapclient as bcapclient


class bcap_robot:
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

    def __init__(self, host='192.168.0.1', port=5007):
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
        self.H_Var = self.m_bcap.robot_getvariable(self.H_robot, "@Current_Position")
    # End init

    def get_curpos(self):
        res = self.m_bcap.variable_getvalue(self.H_Var)
        return res
    # End def

    def disconnect(self):
        if(self.H_Var != 0):
            self.m_bcap.variable_release(self.H_Var)
        # End if
        if(self.H_robot != 0):
            self.m_bcap.robot_release(self.H_robot)
        # End if
        if(self.H_ctrl != 0):
            self.m_bcap.controller_disconnect(self.H_ctrl)
        # End if
        self.m_bcap.service_stop()
        print("disconnect")
    # End def

    def __def__(self):
        try:
            self.disconnect()
            print("Close com port")
        except Exception as e:
            print("Error close com port")
            print(e)
    # End def

    def _update(self, frame, t, x, y, z, rx, ry, rz, axes):
        """グラフを更新するための関数"""
        # 現在のグラフを消去する
        for i in (0, 1, 2):
            for j in (0, 1):
                axes[i][j].clear()
        pos_values = self.get_curpos()
        # データを更新 (追加) する
        t.append(frame)
        x.append(pos_values[0])
        y.append(pos_values[1])
        z.append(pos_values[2])
        rx.append(pos_values[3])
        ry.append(pos_values[4])
        rz.append(pos_values[5])
        axes[0][0].plot(t, x, color='black')
        axes[1][0].plot(t, y, color='black')
        axes[2][0].plot(t, z, color='black')
        axes[0][1].plot(t, rx, color='black')
        axes[1][1].plot(t, ry, color='black')
        axes[2][1].plot(t, rz, color='black')

        # 100個以上のデータは削除する (FIFO)
        if len(t) >= 100:
            del t[0]
            del x[0]
            del y[0]
            del z[0]
            del rx[0]
            del ry[0]
            del rz[0]


def main():

    robot = bcap_robot('192.168.0.1', 5007)
    # 描画領域
    fig, axes = plt.subplots(3, 2)
    # 描画するデータ
    t = []
    x = []
    y = []
    z = []
    rx = []
    ry = []
    rz = []

    try:
        params = {
            'fig': fig,
            'func': robot._update,  # グラフを更新する関数
            'fargs': (t, x, y, z, rx, ry, rz, axes),  # 関数の引数 (フレーム番号を除く)
            'interval': 500,  # 更新間隔 (ミリ秒)
            'frames': itertools.count(0, 0.5),  # フレーム番号を無限に生成するイテレータ
        }
        anime = animation.FuncAnimation(**params)

        # グラフを表示する
        plt.show()

    except KeyboardInterrupt:
        print('finish')
        plt.close()
        print('plt close')


if __name__ == '__main__':
    main()
