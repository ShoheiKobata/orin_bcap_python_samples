# -*- coding:utf-8 -*-

'''
# Sample program
# get all variable values and save csv
# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

Start command
streamlit run robot_data_dashboard.py

'''


from operator import truediv
import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import time

import pybcapclient.bcapclient as bcapclient


class bcap_robot:
    # Handl
    mbcap = None
    h_ctrl = 0
    h_robot = 0
    h_task = 0
    h_var = 0

    # Set param
    Name = "rc"
    Provider = "CaoProv.DENSO.VRC"
    Machine = "localhost"
    Option = "@IfNotMember"
    timeout = 2000

    def __init__(self, host='192.168.0.1', port=5007):
        self.init_data = 0
        self.conect_flg = 0
        self.ifnotm = '@IfNotMember'
    # End init

    def connect(self, host='192.168.0.1', port=5007):
        res = ''
        try:
            if self.conect_flg == 0:
                # Connection processing of tcp communication
                print("Open Connection")
                self.mbcap = bcapclient.BCAPClient(host, port, self.timeout)
                # start b_cap Service
                print("Send SERVICE_START packet")
                self.mbcap.service_start("")

                # Connect to RC8 (RC8(VRC)provider)
                self.h_ctrl = self.mbcap.controller_connect(
                    self.Name, self.Provider, self.Machine, self.Option)
                print("Connect RC8")
                # get Robot Object Handl
                self.h_robot = self.mbcap.controller_getrobot(self.h_ctrl, "arm", self.ifnotm)
                self.h_var = self.mbcap.robot_getvariable(self.h_robot, "@Current_Position", self.ifnotm)
                res = 'connected'
                self.conect_flg = 1
        except Exception as e:
            print('=== ERROR Description ===')
            print(str(e))
            res = 'Error : ' + str(e)
        finally:
            return res

    def get_base_information(self):
        # get serial number
        ret_list = []
        serial = self.mbcap.controller_execute(self.h_ctrl, 'SysInfo', 0)
        ret_list.append(['シリアルNo', serial])

        robot_type = self.mbcap.robot_execute(self.h_robot, 'GetRobotTypeName')
        ret_list.append(['ロボット型式', robot_type])
        h_version = self.mbcap.controller_getvariable(self.h_ctrl, '@VERSION', self.ifnotm)
        version_str = self.mbcap.variable_getvalue(h_version)
        ret_list.append(['コントローラバージョン', version_str])
        ret_DataFrame = pd.DataFrame(ret_list, columns=['name', 'value'])

        return ret_DataFrame
    # End def

    def get_curpos(self):
        res = self.mbcap.robot_execute(self.h_robot, 'CurPos')
        print(res)
        return res
    # End def

    def disconnect(self):
        try:
            if(self.h_var != 0):
                self.mbcap.variable_release(self.h_var)
            # End if
            if(self.h_robot != 0):
                self.mbcap.robot_release(self.h_robot)
            # End if
            if(self.h_ctrl != 0):
                self.mbcap.controller_disconnect(self.h_ctrl)
            # End if
            self.mbcap.service_stop()
            res = 'disconnected'
        except Exception as e:
            print('=== ERROR Description ===')
            print(str(e))
            res = 'Error : ' + str(e)
        finally:
            return res
    # End def

    def __def__(self):
        try:
            self.disconnect()
            print("Close com port")
        except Exception as e:
            print("Error close com port")
            print(e)
    # End def


def main():

    if 'robot' not in st.session_state:
        st.session_state['robot'] = bcap_robot()

    # End if
    st.title('ロボットデータダッシュボード')
    st.header('接続先のロボットのIPアドレスを入力してください')
    # テキスト入力
    ip_add_str = st.text_input('IPアドレス', '192.168.0.1')
    # ボタン
    start_button = st.empty()
    if start_button.button('Start',key='start'):
        count = 0
        t = []
        x = []
        y = []
        z = []
        rx = []
        ry = []
        rz = []
        
        res = st.session_state['robot'].connect(ip_add_str, 5007)
        st.write(res)  # markdown
        st.subheader('接続先ロボット情報')  # サブヘッダー
        ret_DataFrame = st.session_state['robot'].get_base_information()
        st.table(ret_DataFrame)
        start_button.empty()
        # グラフを書き出すためのプレースホルダを用意する
        plot_area = st.empty()
        fig, axes = plt.subplots(3, 2)        
        if st.button('Stop', key='stop'):
            pass
        while True:
            # 現在のグラフを消去する
            for i in (0, 1, 2):
                for j in (0, 1):
                    axes[i][j].clear()
                # End for
            # End for
            # データを追加する
            pos_list = st.session_state['robot'].get_curpos()
            count = count + 1
            t.append(count)
            x.append(pos_list[0])
            y.append(pos_list[1])
            z.append(pos_list[2])
            rx.append(pos_list[3])
            ry.append(pos_list[4])
            rz.append(pos_list[5])
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
            # プレースホルダに書き出す
            plot_area.pyplot(fig)
            time.sleep(0.01)
            
        # End while

    # 選択肢をサイドバーに表示する場合
    #st.sidebar.selectbox('ラベル', ('選択肢1', '選択肢2', '選択肢3'))


if __name__ == '__main__':
    main()
