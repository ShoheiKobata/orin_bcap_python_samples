# MasterSlave

MasterSlave.py can build a master-slave system using b-cap communication.  

## Description  

The master uses the COBOTTA.  
6 axis robot like VS, VM, COBOTTA can be used for the slave.  
By moving the master by direct teaching, you can move the slave freely.  

## Requirement

python=3.* 

## Usage

1. You should edit config of IP Address in in line 13,14 in MasterSlave.py.

    ```python:MasterSlave.py
    MasterIpStr = "Server=192.168.0.1"
    SlaveIpStr = "Server=192.168.0.2"
    ```
2. When you start the program, the following wording will be printed on the command line.  

    ```
    Connect and Init OK
    [ESC] : Close Application
    [1] : Start Synchro Mode
    [2] : End Synchro Mode
    =====Synchro Off=====
    ```
3. Robots are not synchronized at startup. Press the 1 key to synchronize the robot. When you press the 2 key, the robot will end synchronization. Press the ESC key to exit the application.

## Comment

If the slave robot is operated jittery, please change the command motionskip,motioncomplete.  

b-cap library:  
https://github.com/DENSORobot/orin_bcap  

python=3.*
