#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" Sample project io viewer

This program can monitor the IO status of the robot controller.
This program can change the IO state of the robot controller.
In addition, IO commands can also be executed using pseudo input settings.
The part to be developed is commented as #TODO.

"""
import re
import time
from pybcapclient.bcapclient import BCAPClient
from pybcapclient.orinexception import ORiNException
import customtkinter

FONT_TYPE = "meiryo"


class IoViewerApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # robot
        self.bcap = None
        self.h_ctrl = 0
        self.h_io_mode = 0
        self.h_io = 0
        self.rob_type = ''
        self.rc_serial_no = ''
        self.ifnotm = '@IfNotMember'
        # メンバー変数の設定
        self.fonts = (FONT_TYPE, 15)
        self.after_id = 0
        # フォームサイズ設定
        self.geometry("800x600")
        self.title("IO Viewer")

        self.io_btn_list = []
        # フォームのセットアップをする
        self.setup_form()
    # End def

    def setup_form(self):
        # CustomTkinter setting form design
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # resize setting
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # top frame connect
        self.connect_frame = customtkinter.CTkFrame(master=self)
        self.connect_frame.grid_columnconfigure(0, weight=1)
        self.connect_frame.grid(row=0, column=0, padx=1, pady=5, sticky="ew")
        self.con_top_label = customtkinter.CTkLabel(self.connect_frame, text='Connect to', font=(FONT_TYPE, 20))
        self.con_top_label.grid(row=0, column=0, padx=20, sticky="w")
        self.iptextbox = customtkinter.CTkEntry(master=self.connect_frame, placeholder_text="192.168.0.1", width=120, font=self.fonts)
        self.iptextbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.rc_type_cb = customtkinter.CTkComboBox(self.connect_frame, values=["RC8", "RC9"])
        self.rc_type_cb.set("RC8")
        self.rc_type_cb.grid(row=1, column=1, padx=10, pady=(0, 10))
        self.con_btn = customtkinter.CTkButton(master=self.connect_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.con_btn_select_callback, text="Connect", font=self.fonts, hover=False)
        self.con_btn.grid(row=1, column=2, padx=10, pady=(0, 10))

        # middle frame robot info view
        self.robinfo_frame = customtkinter.CTkFrame(master=self)
        self.robinfo_frame.grid_rowconfigure(1, weight=1)
        self.robinfo_frame.grid_columnconfigure(0, weight=1)
        self.robinfo_frame.grid(row=1, column=0, padx=1, pady=5, sticky="ew")
        self.rob_top_label = customtkinter.CTkLabel(self.robinfo_frame, text='robot info', font=(FONT_TYPE, 20))
        self.rob_top_label.grid(row=0, column=0, padx=5, sticky="w")
        self.robinfo_txt = customtkinter.CTkLabel(self.robinfo_frame, text='', font=(FONT_TYPE, 15))
        self.robinfo_txt.grid(row=1, column=0, padx=5, sticky="w")

        # botom frame IO View and controll
        self.io_top_label = customtkinter.CTkLabel(self, text='IO VIEW AND CONTROL', font=(FONT_TYPE, 20))
        self.io_top_label.grid(row=2, column=0, padx=1, sticky="ew")
        self.io_frame = customtkinter.CTkFrame(master=self)
        self.io_frame.grid_rowconfigure(0, weight=1)
        self.io_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.io_frame.grid(row=3, column=0, padx=1, pady=5, sticky="nsew")

    # End def

    def create_io_table(self, frame, start_port, end_port):
        for i, port_no in enumerate(range(start_port, end_port + 1)):
            self.bcap.variable_putid(self.h_io, port_no)
            io_state = self.bcap.variable_getvalue(self.h_io)
            fg_color = 'gray'
            if io_state is True:
                fg_color = 'green'
            list_index = len(self.io_btn_list)
            btn_txt = 'IO[' + str(port_no) + ']'
            self.io_btn_list.append([customtkinter.CTkButton(master=frame, fg_color=fg_color, text=btn_txt, width=10, height=10, corner_radius=5, hover=False), btn_txt])  # , command=lambda: self.io_btn_callback(list_index, port_no)
            self.io_btn_list[list_index][0].bind('<Button-1>', self.io_btn_callback_bind)
            self.io_btn_list[list_index][0].grid(row=i, column=0, sticky="ew")
        # End for
    # End def

    def create_io_frame(self, io_mode):
        io_mode_str = ''
        if io_mode == 0:
            io_mode_str = 'Mini IO mode'
            mini_io_in = [0, 15]
            mini_io_out = [16, 31]
            hand_io_in = [48, 55]
            hand_io_out = [64, 71]
        elif io_mode == 1:
            io_mode_str = 'Standard Mode'
            # TODO change IO Area Standard Mode
        elif io_mode == 2:
            io_mode_str = 'RC3 Compatible Mode'
            # TODO change IO Area RC3 Compatible Mode
        elif io_mode == 3:
            io_mode_str = 'All user I/O Mode'
            # TODO change IO Area All user I/O Mode
        else:
            mini_io_in = [0, 15]
            mini_io_out = [16, 31]
            hand_io_in = [48, 55]
            hand_io_out = [64, 71]
        # End if
        self.io_top_label.configure(text='IO VIEW AND CONTROL | IO Mode : ' + io_mode_str)

        mini_io_in_frame = customtkinter.CTkFrame(master=self.io_frame)
        mini_io_in_frame.grid_columnconfigure(0, weight=1)
        mini_io_in_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.create_io_table(mini_io_in_frame, mini_io_in[0], mini_io_in[1])
        mini_out_in_frame = customtkinter.CTkFrame(master=self.io_frame)
        mini_out_in_frame.grid_columnconfigure(0, weight=1)
        mini_out_in_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        self.create_io_table(mini_out_in_frame, mini_io_out[0], mini_io_out[1])
        hand_io_in_frame = customtkinter.CTkFrame(master=self.io_frame)
        hand_io_in_frame.grid_columnconfigure(0, weight=1)
        hand_io_in_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")
        self.create_io_table(hand_io_in_frame, hand_io_in[0], hand_io_in[1])
        hand_out_in_frame = customtkinter.CTkFrame(master=self.io_frame)
        hand_out_in_frame.grid_columnconfigure(0, weight=1)
        hand_out_in_frame.grid(row=0, column=3, padx=5, pady=5, sticky="nsew")
        self.create_io_table(hand_out_in_frame, hand_io_out[0], hand_io_out[1])

    def switch_event(self):
        print("switch toggled, current value:", self.switch_var.get())

    def io_btn_callback_bind(self, event):
        btn_txt = event.widget['text']
        for data in self.io_btn_list:
            if btn_txt in data:
                break
        # End for
        idx = self.io_btn_list.index(data)
        io_port_str = ''.join(re.findall('[0-9]', btn_txt))
        io_port_int = int(io_port_str)
        print(io_port_int)
        target_btn = self.io_btn_list[idx][0]
        try:
            if target_btn.cget('fg_color') == 'green':
                self.bcap.variable_putid(self.h_io, io_port_int)
                self.bcap.variable_putvalue(self.h_io, False)
                target_btn.configure(fg_color='gray')
            else:
                self.bcap.variable_putid(self.h_io, io_port_int)
                self.bcap.variable_putvalue(self.h_io, True)
                target_btn.configure(fg_color='green')
        except ORiNException as e:
            print('ORiN Error')
            self._orin_error_handling(e)
    # End def

    def io_btn_callback(self, list_index, port):
        print(list_index, port)

    def con_btn_select_callback(self):
        if self.con_btn.cget('text') == 'Connect':
            connected, io_mode = self.rc_connect()
            if connected is True:
                self.con_btn.configure(text='Disconnect', fg_color='green')
                self.con_btn.configure(fg_color='green')
                self.create_io_frame(io_mode=io_mode)
                self.update_func()
        else:
            self.after_cancel(self.after_id)
            time.sleep(0.1)
            self.rc_disconnect()
            self.con_btn.configure(text='Connect', fg_color='gray30')

    def rc_connect(self):
        ret_bool = False
        io_mode = -1
        try:
            self.bcap = BCAPClient(host=self.iptextbox.get(), port=5007, timeout=2000)
            if self.rc_type_cb.get() == 'RC8':
                provider_name = 'CaoProv.DENSO.VRC'
            else:
                provider_name = 'CaoProv.DENSO.VRC9'
            # End if
            self.bcap.service_start('')
            self.h_ctrl = self.bcap.controller_connect(name='io_view', provider=provider_name, machine='localhost', option=self.ifnotm)
            self.h_rob = self.bcap.controller_getrobot(self.h_ctrl, 'Arm', self.ifnotm)
            self.rc_serial_no = self.bcap.controller_execute(self.h_ctrl, 'SysInfo', 0)
            self.rob_type = self.bcap.robot_execute(self.h_rob, 'RobInfo', 1)
            self.h_io_mode = self.bcap.controller_getvariable(self.h_ctrl, '@IO_ALLOC_MODE', self.ifnotm)
            io_mode = self.bcap.variable_getvalue(self.h_io_mode)
            self.robinfo_txt.configure(text=' Serial No.' + self.rc_serial_no + '\n Robot Type: ' + self.rob_type)
            self.h_io = self.bcap.controller_getvariable(self.h_ctrl, 'IO*', self.ifnotm)
        except ORiNException as e:
            print('ORiN Error')
            self._orin_error_handling(e)
        except Exception as e:
            print('non ORiN Error')
            print(e)
        else:
            ret_bool = True
        finally:
            return ret_bool, io_mode
    # End def

    def rc_disconnect(self):
        if self.h_rob != 0:
            self.bcap.robot_release(self.h_rob)
            self.h_rob = 0
        if self.h_io_mode != 0:
            self.bcap.variable_release(self.h_io_mode)
            self.h_io_mode = 0
        if self.h_ctrl != 0:
            self.bcap.controller_disconnect(self.h_ctrl)
            self.h_ctrl = 0
        self.bcap.service_stop()
        del self.bcap
    # End def

    def update_func(self):
        # update io state from robot controler interval
        update_interval = 10
        self.after_id = self.after(update_interval, self.update_func)
        target_id = int(self.after_id[6:]) % len(self.io_btn_list)
        target_brn = self.io_btn_list[target_id][0]
        io_port_str = ''.join(re.findall('[0-9]', self.io_btn_list[target_id][1]))
        io_port_int = int(io_port_str)
        self.bcap.variable_putid(self.h_io, io_port_int)
        if (self.bcap.variable_getvalue(self.h_io)) is True:
            target_brn.configure(fg_color='green')
        else:
            target_brn.configure(fg_color='gray')
        # End if
    # End def

    def _orin_error_handling(self, e):
        errorcode_int = int(str(e))
        if errorcode_int < 0:
            errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
        else:
            errorcode_hex = hex(errorcode_int)
        # End if
        print("Error Code : 0x" + str(errorcode_hex))
        error_description = self.bcap.controller_execute(self.h_ctrl, "GetErrorDescription", errorcode_int)
        print("Error Description : " + error_description)
    # End def
# End class


def main():
    app = IoViewerApp()
    app.mainloop()


if __name__ == "__main__":
    main()
