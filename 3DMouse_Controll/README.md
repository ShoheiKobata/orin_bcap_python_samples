# 3DMouse_controll

Use the 3D mouse to move the robot.  

## Description  

By reflecting the movement amount of the 3D mouse on the robot, you can intuitively operate the robot.  
You can change the operation method such as straight ahead, straight ahead + rotation.  
In the program, Ry, Rz, Fig are fixed.  

## Requirement

python=3.* 

## Usage

- You should edit config of IP Address (host) in line 26 .  
    ```python:3DMouse_controll.py
    host = "192.168.0.2"
    port = 5007
    timeout = 2000
    ```

## Reference

- b-cap library:  
https://github.com/DENSORobot/orin_bcap  

- spacenavigator library:
Implements a simple interface to the 6 DoF 3Dconnexion [Space Navigator](http://www.3dconnexion.co.uk/products/spacemouse/spacenavigator.html) device.  
Requires [pywinusb](https://pypi.python.org/pypi/pywinusb/) to access HID data -- this is Windows only.  
