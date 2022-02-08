# coding:utf-8


# COBOTTA Sample program
# Get COBOTTA Mecha Button States
# ### The 'GetMechaButtonState', 'ClearMechaButtonState' command can be used with COBOTTA version 1.13 or later.

# b-cap Lib URL
# https://github.com/DENSORobot/orin_bcap

import pybcapclient.bcapclient as bcapclient


def main():
    # set IP Address , Port number and Timeout of connected RC8
    host = '192.168.0.1'
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

    try:
        # Connect to RC8 (RC8(VRC)provider) , Get Controller Handle
        hCtrl = m_bcapclient.controller_connect(Name, Provider, Machine, Option)

    except Exception as e:
        print(e)
    finally:
        m_bcapclient.service_stop()
        print("B-CAP service Stop")
# End def


if __name__ == "__main__":
    main()	
