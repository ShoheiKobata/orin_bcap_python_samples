# -*- coding:utf-8 -*-

'''
# Sample program
# get all variable values and save csv
# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

Start command
streamlit run robot_data_dashboard.py

'''

import sys
import traceback
import enum
from math import fabs
import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import time
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

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
                self.h_i = self.mbcap.controller_getvariable(self.h_ctrl, 'I*', self.ifnotm)
                self.h_f = self.mbcap.controller_getvariable(self.h_ctrl, 'F*', self.ifnotm)
                self.h_d = self.mbcap.controller_getvariable(self.h_ctrl, 'D*', self.ifnotm)
                self.h_v = self.mbcap.controller_getvariable(self.h_ctrl, 'V*', self.ifnotm)
                self.h_j = self.mbcap.controller_getvariable(self.h_ctrl, 'J*', self.ifnotm)
                self.h_p = self.mbcap.controller_getvariable(self.h_ctrl, 'P*', self.ifnotm)
                self.h_t = self.mbcap.controller_getvariable(self.h_ctrl, 'T*', self.ifnotm)
                self.h_s = self.mbcap.controller_getvariable(self.h_ctrl, 'S*', self.ifnotm)
                self.h_extsp = self.mbcap.robot_getvariable(self.h_robot, '@EXTSPEED', self.ifnotm)
                res = 'connected'
                self.conect_flg = 1
        except Exception as e:
            print('=== ERROR Description ===')
            print(str(e))
            res = 'Error : ' + str(e)
        finally:
            return res

    def get_base_information(self):
        ret_DataFrame = None
        try:
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
        except Exception as e:
            self._error_handle(e)
        finally:
            return ret_DataFrame
    # End def

    def _change_str_pose(self, value_type, data):
        str_tmp = str(data)
        ret_str = value_type + '(' + str_tmp[1:-1] + ')'
        return ret_str
    # End def

    def move_func(self, mode, dist_len, flg):
        # ['各軸', 'X-Y', 'Tool']
        if mode == '各軸':
            rob_location = self.mbcap.robot_execute(self.h_robot, 'CurJnt', '')
            rob_location = rob_location[:7]
            dist_location = [n + m * dist_len for n, m in zip(rob_location, flg)]
            pose = [dist_location, 'J', '@P']
        elif mode == 'X-Y':
            rob_location = self.mbcap.robot_execute(self.h_robot, 'CurPos')
            pose1 = self._change_str_pose('P', rob_location)
            dist_location = [n * dist_len for n in flg]
            pose2 = self._change_str_pose('P', dist_location)
            ret_dev = self.mbcap.robot_execute(self.h_robot, 'Dev', [pose1, pose2])
            pose = [ret_dev, 'P', '@P']
        else:
            rob_location = self.mbcap.robot_execute(self.h_robot, 'CurPos')
            pose1 = self._change_str_pose('P', rob_location)
            dist_location = [n * dist_len for n in flg]
            pose2 = self._change_str_pose('P', dist_location)
            ret_dev = self.mbcap.robot_execute(self.h_robot, 'DevH', [pose1, pose2])
            pose = [ret_dev, 'P', '@P']
        # End if
        self.mbcap.robot_execute(self.h_robot, 'TakeArm', [0, 0])
        self.mbcap.robot_move(self.h_robot, 2, pose, 'NEXT')
        self.mbcap.robot_execute(self.h_robot, 'GiveArm')
    # End def

    def get_value_len(self, value_type):
        """
        グローバル変数のサイズを返します。
        value_type :str
            変数の型を文字列で入力します。(S,V,I, ....)
        """
        ret = None
        value_len_name = '@VAR_' + value_type + '_LEN'
        h_val_len = self.mbcap.controller_getvariable(self.h_ctrl, value_len_name, self.ifnotm)
        ret = self.mbcap.variable_getvalue(h_val_len)
        self.mbcap.variable_release(h_val_len)
        return ret
    # End def

    def get_value(self, value_type, index):
        ret = None
        """
        グローバル変数の値を返します。

        value_type : str
            変数の型を文字列で指定 (S,I,T,...)
        index : int
            取得する変数のインデックス番号を指定
        """
        if value_type == 'I':
            self.mbcap.variable_putid(self.h_i, index)
            ret = self.mbcap.variable_getvalue(self.h_i)
        elif value_type == 'F':
            self.mbcap.variable_putid(self.h_f, index)
            ret = self.mbcap.variable_getvalue(self.h_f)
        elif value_type == 'D':
            self.mbcap.variable_putid(self.h_d, index)
            ret = self.mbcap.variable_getvalue(self.h_d)
        elif value_type == 'V':
            self.mbcap.variable_putid(self.h_v, index)
            ret = self.mbcap.variable_getvalue(self.h_v)
        elif value_type == 'J':
            self.mbcap.variable_putid(self.h_j, index)
            ret = self.mbcap.variable_getvalue(self.h_j)
        elif value_type == 'P':
            self.mbcap.variable_putid(self.h_p, index)
            ret = self.mbcap.variable_getvalue(self.h_p)
        elif value_type == 'T':
            self.mbcap.variable_putid(self.h_t, index)
            ret = self.mbcap.variable_getvalue(self.h_t)
        elif value_type == 'S':
            self.mbcap.variable_putid(self.h_s, index)
            ret = self.mbcap.variable_getvalue(self.h_s)
        else:
            ret = 0
        # End if
        return ret
    # End def

    def put_value(self, value_type, index, newval):
        if value_type == 'I':
            self.mbcap.variable_putid(self.h_i, index)
            self.mbcap.variable_putvalue(self.h_i, newval)
        elif value_type == 'F':
            self.mbcap.variable_putid(self.h_f, index)
            self.mbcap.variable_putvalue(self.h_f, newval)
        elif value_type == 'D':
            self.mbcap.variable_putid(self.h_d, index)
            self.mbcap.variable_putvalue(self.h_d, newval)
        elif value_type == 'V':
            self.mbcap.variable_putid(self.h_v, index)
            self.mbcap.variable_putvalue(self.h_v, newval)
        elif value_type == 'J':
            self.mbcap.variable_putid(self.h_j, index)
            self.mbcap.variable_putvalue(self.h_j, newval)
        elif value_type == 'P':
            self.mbcap.variable_putid(self.h_p, index)
            self.mbcap.variable_putvalue(self.h_p, newval)
        elif value_type == 'T':
            self.mbcap.variable_putid(self.h_t, index)
            self.mbcap.variable_putvalue(self.h_t, newval)
        elif value_type == 'S':
            self.mbcap.variable_putid(self.h_s, index)
            self.mbcap.variable_putvalue(self.h_s, newval)
        else:
            pass
        # End if
    # End def

    def get_tasknames(self):
        ret = self.mbcap.controller_gettasknames(self.h_ctrl, '')
        return ret
    # End def

    def get_file_value(self, filename):
        h_file = self.mbcap.controller_getfile(self.h_ctrl, filename, self.ifnotm)
        ret = self.mbcap.file_getvalue(h_file)
        self.mbcap.file_release(h_file)
        return ret
    # End def

    def rewrite_file_value(self, filename, data):
        h_file = self.mbcap.controller_getfile(self.h_ctrl, filename, self.ifnotm)
        self.mbcap.file_putvalue(h_file, data)
    # End def

    def get_curpos(self):
        res = None
        try:
            res = self.mbcap.robot_execute(self.h_robot, 'CurPos')
        except Exception as e:
            self._error_handle(e)
        finally:
            return res
    # End def

    def set_extSpeed(self, ext_sp_val):
        """
        外部速度をセットします。
        失敗した場合、false,成功したらtrueを返します。
        """
        ret = False
        try:
            self.mbcap.robot_execute(self.h_robot, 'ExtSpeed', ext_sp_val)
            ret = True
        except Exception as e:
            ret = False
            self._error_handle(e)
        finally:
            return ret

    def get_extSpeed(self):
        """
        現在の外部速度を取得します。
        """
        ret = 0.1
        try:
            ret = self.mbcap.variable_getvalue(self.h_extsp)
        except Exception as e:
            self._error_handle(e)
        finally:
            return ret

    def _error_handle(self, e):
        """
        エラー処理に使う関数。エラー内容からロボットの場合はロボットのエラーコードを出力。
        その他のエラーの場合はそのまま出力します。

        使用例
        --------------------------
        try:
            処理
        exception Exception as e:
            self._error_handle
        finally:
            処理
        """
        print('=== ERROR Description ===')
        print(traceback.format_exc())
        if str(type(e)) == "<class 'pybcapclient.orinexception.ORiNException'>":
            print(e)
            errorcode_int = int(str(e))
            if errorcode_int < 0:
                errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
            else:
                errorcode_hex = hex(errorcode_int)
            print("Error Code : 0x" + str(errorcode_hex))
            error_description = self.mbcap.controller_execute(self.h_ctrl, "GetErrorDescription", errorcode_int)
            print("Error Description : " + error_description)
        else:
            print(e)

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

    # オブジェクトを毎回読み込みを避けるため
    if 'robot' not in st.session_state:
        st.session_state['robot'] = bcap_robot()
    if 'start_flg' not in st.session_state:
        st.session_state['start_flg'] = False
    # End if
    st.title('ロボットコントローラボード')
    st.sidebar.header('接続先のロボットのIPアドレスを入力してください')
    # テキスト入力
    ip_add_str = st.sidebar.text_input('IPアドレス', '192.168.0.1')
    # ボタン
    start_button = st.sidebar.empty()
    select_boad_type = st.sidebar.radio('モードを選択してください。', ('robot_control', 'program_edit', 'variable_edit', 'position_monitor'))

    if not st.session_state['start_flg']:
        st.session_state['start_flg'] = start_button.button('Start', key='start')
    else:
        st.session_state['start_flg'] = not(start_button.button('Stop', key='start'))

    if st.session_state['start_flg']:
        res = st.session_state['robot'].connect(ip_add_str, 5007)
        st.write(res)  # markdown
        st.subheader('接続先ロボット情報')  # サブヘッダー
        ret_DataFrame = st.session_state['robot'].get_base_information()
        st.table(ret_DataFrame)
        if select_boad_type == 'robot_control':
            st.subheader('ロボットを操作します。')
            ret_ext_val = st.session_state['robot'].get_extSpeed()
            ExtSpeed = st.slider(label='extenal Speed', min_value=0.1, max_value=100.0, value=ret_ext_val)
            st.session_state['robot'].set_extSpeed(ExtSpeed)
            colA, colB = st.columns(2)
            with colA:
                control_mode_list = ['各軸', 'X-Y', 'Tool']
                control_mode = st.selectbox('動作モード', control_mode_list)
            with colB:
                dist_len = 0.0
                dist_len = st.number_input('動作距離', 0.0, 10.0, 0.0, step=0.1)
            move_label = []
            move_flg = [0, 0, 0, 0, 0, 0]
            if control_mode == '各軸':
                move_label = ['J' + str(i) for i in range(1, 7)]
            else:
                move_label = ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz']
            # End if

            # カラムを追加する
            col1, col2, col3 = st.columns(3)
            with col1:
                for i in range(6):
                    if st.button('-' + str(move_label[i]), key='m_' + str(i)):
                        move_flg[i] -= 1
            with col2:
                for i in range(6):
                    st.text(' ' + str(move_label[i]) + '  ')
            with col3:
                for i in range(6):
                    if st.button('+' + str(move_label[i]), key='p_' + str(i)):
                        move_flg[i] += 1

            if sum(move_flg) != 0:
                st.session_state['robot'].move_func(control_mode, dist_len, move_flg)

        elif select_boad_type == 'program_edit':
            select_program = ''
            select_list_programs = st.session_state['robot'].get_tasknames()
            select_program = st.selectbox('編集するプログラムを選択する', select_list_programs)
            if select_program != '':
                ret_file_val = st.session_state['robot'].get_file_value(select_program + '.pcs')
                new_text = st.text_area('Ctrl + Enter でコントローラへ書き込みます。', height=300, value=ret_file_val)
                st.session_state['robot'].rewrite_file_value(select_program + '.pcs', new_text)

        elif select_boad_type == 'variable_edit':
            select_list_variable = ['I', 'F', 'D', 'V', 'P', 'J', 'T', 'S']
            select_variable = st.sidebar.selectbox('編集する', select_list_variable)

            val_len = st.session_state['robot'].get_value_len(select_variable)
            val_data = []
            val_index = []
            val_columns = []
            if select_variable == 'V':
                val_columns = ['X', 'Y', 'Z', 'Use']
            elif select_variable == 'P':
                val_columns = ['X', 'Y', 'Z', 'Rx', 'Ry', 'Rz', 'Fig', 'Use']
            elif select_variable == 'J':
                val_columns = ['J1', 'J2', 'J3', 'J4', 'J5', 'J6', 'J7', 'J8', 'Use']
            elif select_variable == 'T':
                val_columns = ['X', 'Y', 'Z', 'Ox', 'Oy', 'Oz', 'Ax', 'Ay', 'Az', 'Fig', 'Use']
            else:
                val_columns = ['value', 'Use']
            # End if

            for index in range(val_len):
                data = st.session_state['robot'].get_value(select_variable, index)
                if type(data) is list:
                    val_data.append(data + [''])
                else:
                    val_data.append([data, ''])
                val_index.append(select_variable + str(index))
                df = pd.DataFrame(val_data, index=val_index, columns=val_columns)
            # End for
            # st.write(df)
            # st.table(df)
            gb = GridOptionsBuilder.from_dataframe(df, editable=True)
            grid = AgGrid(df, gridOptions=gb.build(), fit_columns_on_grid_load=True, updateMode=GridUpdateMode.VALUE_CHANGED)
            # 修正が反映される
            st.dataframe(grid['data'])

            if st.button('Write', key='Write to controller variable'):
                write_count = st.empty()
                bar = st.progress(0)
                max_len = len(grid['data'].values.tolist())
                for i, data in enumerate(grid['data'].values.tolist()):
                    if(len(data) == 2):
                        new_val = data[0]
                    else:
                        new_val = data[:-1]
                    # End if
                    st.session_state['robot'].put_value(select_variable, i, new_val)
                    write_count.text(f'count {i + 1}')
                    bar.progress((i + 1) / max_len)
                # End for
                st.write('write')
            # End if

        elif select_boad_type == 'position_monitor':
            count = 0
            t = []
            x = []
            y = []
            z = []
            rx = []
            ry = []
            rz = []

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
        else:
            pass
        # End if
    # End if


if __name__ == '__main__':
    main()
