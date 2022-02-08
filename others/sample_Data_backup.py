# -*- coding:utf-8 -*-

# This is a sample program that acquires various data of the robot.
# You can get all the variables and program informations.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import os
import pybcapclient.bcapclient as bcapclient
import csv

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
port = 5007
timeout = 2000

# Create save folder
folder_path = "variables"
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
folder_path = "PacScript"
if not os.path.exists(folder_path):
    os.mkdir(folder_path)


def save_csvfile(folder_path, datas):
    dirname = os.path.dirname(folder_path)
    os.makedirs(dirname, exist_ok=True)
    try:
        with open(folder_path, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(datas)
        print('save data' + folder_path)
    except Exception as e:
        print("ERROR in csv process")
        print(e)
# End def


def save_pacfile(folder_path, datas):
    dirname = os.path.dirname(folder_path)
    os.makedirs(dirname, exist_ok=True)
    print(folder_path)
    try:
        f = open(folder_path, 'w')
        f.write(datas)
        f.close()
        print('save data' + folder_path)
    except Exception as e:
        print("ERROR in Pacfile save process")
        print(e)
# End def


# Connection processing of tcp communication
m_bcapclient = bcapclient.BCAPClient(host, port, timeout)
print("Open Connection")

# start b_cap Service
m_bcapclient.service_start("")
print("Send SERVICE_START packet")

# set Parameter
Name = ""
Provider = "CaoProv.DENSO.VRC"
Machine = "localhost"
Option = ""

variable_names = ['I*', 'F*', 'D*', 'V*', 'P*', 'J*', 'T*', 'S*']
variable_len_names = ['@VAR_I_LEN', '@VAR_F_LEN', '@VAR_D_LEN', '@VAR_V_LEN', '@VAR_P_LEN', '@VAR_J_LEN', '@VAR_T_LEN', '@VAR_S_LEN']
variable_file_names = ['Var_I.csv', 'Var_F.csv', 'Var_D.csv', 'Var_V.csv', 'Var_P.csv', 'Var_J.csv', 'Var_T.csv', 'Var_S.csv']

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("Connect RC8")
    # save variables
    save_folder_path = "variables"
    for var_type, var_len, var_filename in zip(variable_names, variable_len_names, variable_file_names):
        hvar_type = m_bcapclient.controller_getvariable(hCtrl, var_type)
        hvar_len = m_bcapclient.controller_getvariable(hCtrl, var_len)
        ret_var_len = m_bcapclient.variable_getvalue(hvar_len)
        ret_values = []
        for id_num in range(ret_var_len):
            m_bcapclient.variable_putid(hvar_type, id_num)
            ret_data = m_bcapclient.variable_getvalue(hvar_type)
            if not isinstance(ret_data, list):
                ret_data = [ret_data]
            ret_values.append(ret_data)
        save_path = os.path.join(save_folder_path, var_filename)
        save_csvfile(save_path, ret_values)
    #
    #
    # save PacScript
    save_folder_path = 'PacScript\\'
    path_names = m_bcapclient.controller_getfilenames(hCtrl)
    for path_name in path_names:
        if '.' in path_name:
            print('file')
            hfile = m_bcapclient.controller_getfile(hCtrl, path_name)
            file_value = m_bcapclient.file_getvalue(hfile)
            save_pacfile(save_folder_path + path_name, file_value)
        else:
            path_name = path_name + '\\'
            print('folder')
            hfile = m_bcapclient.controller_getfile(hCtrl, path_name)
            dir_files = m_bcapclient.file_getfilenames(hfile)
            for dir_file in dir_files:
                if '.' in dir_file:
                    dir_file_path = path_name + dir_file
                    hdir_file = m_bcapclient.controller_getfile(hCtrl, dir_file_path)
                    file_value = m_bcapclient.file_getvalue(hdir_file)
                    save_pacfile(save_folder_path + dir_file_path, file_value)
                # End if
                m_bcapclient.file_release(hdir_file)
        m_bcapclient.file_release(hfile)

except Exception as e:
    print('=== ERROR Description ===')
    if str(type(e)) == "<class 'pybcapclient.orinexception.ORiNException'>":
        print(e)
        errorcode_int = int(str(e))
        if errorcode_int < 0:
            errorcode_hex = format(errorcode_int & 0xffffffff, 'x')
        else:
            errorcode_hex = hex(errorcode_int)
        print("Error Code : 0x" + str(errorcode_hex))
        error_description = m_bcapclient.controller_execute(
            hCtrl, "GetErrorDescription", errorcode_int)
        print("Error Description : " + error_description)
    else:
        print(e)

finally:
    # DisConnect
    if(hCtrl != 0):
        m_bcapclient.controller_disconnect(hCtrl)
        print("Release Controller")
    # End If
    m_bcapclient.service_stop()
    print("B-CAP service Stop")
