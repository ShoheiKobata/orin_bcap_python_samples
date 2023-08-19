import os
import sys

import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk
from logging import INFO, basicConfig, getLogger, NullHandler
import logging.handlers

import pyspacenavigator.spacenavigator as spacenavigator
from pyrobot import Robot

logger = getLogger(__name__)


class Application(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # logger settings
        logger.info('gui')

        # class
        self.device_is_opened = spacenavigator.open()
        self.rob = Robot()

        self.pack()
        self.master.geometry("500x600")
        self.master.title("3D Mouse Controll")
        self.master.protocol("WM_DELETE_WINDOW", self.delet_func)
        self.wid_height = 100
        self.wid_width = 500
        self._font = ('Helvetica', 14)
        self.is_running = False
        self.active_move = []
        [self.active_move.append(tk.BooleanVar(value=True)) for i in range(6)]
        self.rate_tomove = 10.0
        self.is_connect_rob = False

        self.frame_list = []
        # create frame
        self.frame_list.append(self.create_frame(self.master, "white"))
        self.frame_list.append(self.create_frame(self.master, "green"))
        self.frame_list.append(self.create_frame(self.master, "red"))
        # place frame position
        [self.frame_list[i].pack() for i in range(len(self.frame_list))]

        self.widget()
        self._timer_func()
    # End def init

    def widget(self):
        # top
        self.top_label = tk.Label(self.frame_list[0], text="接続先ロボットIPアドレスを入力してください", width=40, font=self._font)  # place top label into label[0]
        strvar = tk.StringVar(value='192.168.255.255')
        self.ip_add_txt = tk.Entry(self.frame_list[0], width=15, textvariable=strvar, font=self._font)
        rc_types = ('RC8', 'RC9')
        v = tk.StringVar()
        self.rc_comb = ttk.Combobox(self.frame_list[0], values=rc_types, justify=tk.CENTER, state='readonly', width=5, font=self._font)
        self.rc_comb.current(1)
        self.connct_btn = tk.Button(self.frame_list[0], text="Connect", command=self.connect_rc, font=self._font)
        self.top_label.grid(row=0, column=0, columnspan=3, padx=5, pady=7)
        self.ip_add_txt.grid(row=1, column=0, padx=5, pady=7)
        self.rc_comb.grid(row=1, column=1, padx=5, pady=7)
        self.connct_btn.grid(row=1, column=2, padx=5, pady=7)

        # main
        self.x_chk = tk.Checkbutton(self.frame_list[1], text='x', font=self._font, variable=self.active_move[0])
        self.x_chk.grid(row=0, column=0)
        self.y_chk = tk.Checkbutton(self.frame_list[1], text='y', font=self._font, variable=self.active_move[1])
        self.y_chk.grid(row=1, column=0)
        self.z_chk = tk.Checkbutton(self.frame_list[1], text='z', font=self._font, variable=self.active_move[2])
        self.z_chk.grid(row=2, column=0)
        self.rx_chk = tk.Checkbutton(self.frame_list[1], text='rx', font=self._font, variable=self.active_move[3])
        self.rx_chk.grid(row=3, column=0)
        self.ry_chk = tk.Checkbutton(self.frame_list[1], text='ry', font=self._font, variable=self.active_move[4])
        self.ry_chk.grid(row=4, column=0)
        self.rz_chk = tk.Checkbutton(self.frame_list[1], text='rz', font=self._font, variable=self.active_move[5])
        self.rz_chk.grid(row=5, column=0)

        self.all_active = tk.Button(self.frame_list[1], text="All", command=lambda: self.activate_func(-1), font=self._font) 
        self.trans_active = tk.Button(self.frame_list[1], text="XYZ", command=lambda: self.activate_func(1), font=self._font) 
        self.rot_active = tk.Button(self.frame_list[1], text="RxRyRz", command=lambda: self.activate_func(2), font=self._font) 
        self.scala_active = tk.Button(self.frame_list[1], text="XYZRz", command=lambda: self.activate_func(3), font=self._font) 
        self.start_btn = tk.Button(self.frame_list[1], text="Start", command=lambda: self.btn_fnc(True), font=self._font)
        self.stop_btn = tk.Button(self.frame_list[1], text="Stop", command=lambda: self.btn_fnc(False), font=self._font, state='disable')
        self.all_active.grid(row=0, column=1)
        self.trans_active.grid(row=1, column=1)
        self.rot_active.grid(row=2, column=1)
        self.scala_active.grid(row=3, column=1)
        self.start_btn.grid(row=4, column=1)
        self.stop_btn.grid(row=5, column=1)

        self.pos_tree = ttk.Treeview(self.frame_list[1], columns=(1, 2), show='headings', height=7)
        self.pos_tree.heading(1, text="name")
        self.pos_tree.heading(2, text="Value")
        self.pos_tree.insert(parent='', index=0, iid=0, values=('X', 0.0))
        self.pos_tree.insert(parent='', index=1, iid=1, values=('Y', 0.0))
        self.pos_tree.insert(parent='', index=2, iid=2, values=('Z', 0.0))
        self.pos_tree.insert(parent='', index=3, iid=3, values=('Rx', 0.0))
        self.pos_tree.insert(parent='', index=4, iid=4, values=('Ry', 0.0))
        self.pos_tree.insert(parent='', index=5, iid=5, values=('Rz', 0.0))
        self.pos_tree.insert(parent='', index=6, iid=6, values=('Fig', 0))
        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview")
        self.pos_tree.grid(row=0, column=2, rowspan=5)

        # bottom
        self.log = scrolledtext.ScrolledText(self.frame_list[2], state='disabled')
        self.log.pack(expand=True, fill='both', padx=10, pady=10)
        # last setting
        self.master.bind("<Configure>", self.resize_frame)
    # End def

    def _writelog(self, logtext=''):
        '''
        output log text in gui
        '''
        self.log['state'] = 'normal'
        self.log.insert(tk.END, '\n')
        self.log.insert(tk.END, logtext)
        self.log.see('end')
        self.log['state'] = 'disabled'
    # End def

    def create_frame(self, root, color):
        """
        create frame method
        """
        frame = tk.Frame(root, height=self.wid_height, width=self.wid_width, bg=color)
        return frame
    # End def

    def resize_frame(self, event):
        """
        change frame size method
        """
        # winfo_height、winfo_widthでmasterのウィンドウ情報を取得
        self.wid_height = self.master.winfo_height() / (len(self.frame_list) + 1)
        self.wid_width = (self.master.winfo_width())
        # フレームの高さと幅を再設定します。
        for i in range(len(self.frame_list)):
            if i == 1:
                self.frame_list[i].config(height=self.wid_height * 2, width=self.wid_width)
            else:
                self.frame_list[i].config(height=self.wid_height, width=self.wid_width)
        # [self.frame_list[i].config(height=self.wid_height, width=self.wid_width) for i in range(len(self.frame_list))]
        #print("Windowサイズは", self.wid_height, "x", self.wid_width)
        #print(f'ip:{self.ip_add_txt.get()}, rc_type:{self.rc_comb.get()}')
        #self._writelog(f'ip:{self.ip_add_txt.get()}, rc_type:{self.rc_comb.get()}')
    # End def

    def connect_rc(self):
        ip_str = self.ip_add_txt.get()
        rc_type = self.rc_comb.get()
        self.is_connect_rob = self.rob.connect(ip=ip_str, rc_type=rc_type, name='3dmousectrl')
        if self.is_connect_rob:
            self._writelog('sucess connect')
            rob_info = self.rob.get_base_info()
            self._writelog('Serial No.' + rob_info[0])
            self._writelog('Robot Type.' + rob_info[1])
            self._writelog('VRC Ver.' + rob_info[2])
    # End def

    def activate_func(self, patern=-1):
        if patern == -1:
            [self.active_move[i].set(True) for i in range(6)]
        elif patern == 1:
            [self.active_move[i].set(True) for i in [0, 1, 2]]
            [self.active_move[i].set(False) for i in [3, 4, 5]]
        elif patern == 2:
            [self.active_move[i].set(False) for i in [0, 1, 2]]
            [self.active_move[i].set(True) for i in [3, 4, 5]]
        elif patern == 3:
            [self.active_move[i].set(True) for i in [0, 1, 2, 5]]
            [self.active_move[i].set(False) for i in [3, 4]]
        else:
            pass
        # End if

    def btn_fnc(self, flg=False):
        if flg:
            self.rob.standby_on()
            self.start_btn['state'] = 'disable'
            self.stop_btn['state'] = 'normal'
            self.is_running = flg
        else:
            self.is_running = flg
            self.start_btn['state'] = 'normal'
            self.stop_btn['state'] = 'disable'
            self.rob.standby_off()
        # End if
    # End def

    def _timer_func(self):
        interval_msec = 100
        if self.is_running:
            deviation = []
            state = spacenavigator.read()
            state_list = [state.x * self.rate_tomove, state.y * self.rate_tomove, state.z * self.rate_tomove,
                          state.pitch, -1 * state.roll, -1 * state.yaw]
            for i in range(6):
                if self.active_move[i].get():
                    deviation.append(state_list[i])
                else:
                    deviation.append(0)
                # End if
            # End for
            logger.info(deviation)
            self.rob.moveto(deviation=deviation)
        # End if
        if self.is_connect_rob:
            monitor_data = self.rob.moniter_data()
            mode = monitor_data[0]
            pos = monitor_data[1]
            for i in range(len(pos)):
                temp = self.pos_tree.item(i, 'values')
                self.pos_tree.item(i, values=(temp[0], pos[i]))
            # End for
        # End if
        self.master.after(interval_msec, self._timer_func)
    # End def

    def delet_func(self):
        logger.info('finish')
        self.master.quit()
        self.master.destroy()
    # End def
# End class


def main():
    # logger setting
    log_dir = os.path.join(os.path.dirname(sys.argv[0]), "log")
    os.makedirs(log_dir, exist_ok=True)
    formatter = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    log_file_path = os.path.join(os.path.dirname(sys.argv[0]), "log", "mainlog.log")
    basicConfig(level=INFO, format=formatter)
    h = logging.handlers.RotatingFileHandler(log_file_path, maxBytes=100000, backupCount=5)
    formatter = "%(asctime)s:%(levelname)s:%(name)s:%(message)s"
    h.setFormatter(logging.Formatter(formatter))
    logger.addHandler(h)
    logger.info('start App')

    win = tk.Tk()
    app = Application(master=win)
    app.mainloop()


if __name__ == "__main__":
    main()
