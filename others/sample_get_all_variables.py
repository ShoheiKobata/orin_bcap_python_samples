# -*- coding:utf-8 -*-

# Sample program
# get all variable values and save csv

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap


import pybcapclient.bcapclient as bcapclient
import os
import time
import csv
import traceback
import tqdm

# set IP Address , Port number and Timeout of connected RC8
host = "192.168.0.1"
port = 5007
timeout = 2000

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

variable_names = ['I', 'F', 'D', 'V', 'P', 'J', 'T', 'S']

h_ctrl = 0
h_var_len = 0
h_var = 0

if not os.path.exists('data'):
    os.mkdir('data')

try:
    # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
    h_ctrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)
    print("Connect RC8")
    # get all variables
    for variable_name in variable_names:
        print('Start get values in type ' + variable_name)
        value_list = []
        variable_len_name = '@VAR_' + variable_name + '_LEN'
        csv_file_path = os.path.join('data', 'VAR_' + variable_name + '.csv')
        # Start timer
        start = time.time()

        h_var_len = m_bcapclient.controller_getvariable(h_ctrl, variable_len_name)
        h_var = m_bcapclient.controller_getvariable(h_ctrl, variable_name + '*')
        # get variable length
        var_len = m_bcapclient.variable_getvalue(h_var_len)
        # get all values
        for i in tqdm.tqdm(range(var_len)):
            m_bcapclient.variable_putid(h_var, i)
            value_list.append(m_bcapclient.variable_getvalue(h_var))
        # End for
        print('End get values in type ' + variable_name)
        print('Start write values csv in type ' + variable_name)
        with open(csv_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for i in tqdm.tqdm(range(len(value_list))):
                if(type(value_list[i]) is list):
                    row = [i] + value_list[i]
                else:
                    row = [i, value_list[i]]
                writer.writerow(row)
            # End for
        # End with
        print('End write values csv in type ' + variable_name)
        elapsed_time = time.time() - start
        print("elapsed_time:{0}".format(elapsed_time) + "[sec]")

except Exception as e:
    print('=== ERROR Description ===')
    print(traceback.format_exc())
    print(str(e))

# DisConnect
if(h_var != 0):
    m_bcapclient.variable_release(h_var)
    print("Release variable handle")
if(h_var_len != 0):
    m_bcapclient.variable_release(h_var_len)
    print("Release variable Length handle")
# End If
if(h_ctrl != 0):
    m_bcapclient.controller_disconnect(h_ctrl)
    print("Release Controller")
# End If
m_bcapclient.service_stop()
print("B-CAP service Stop")
