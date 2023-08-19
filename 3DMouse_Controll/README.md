# 3DMouse_controll

Use the 3D mouse to move the robot.  


# DEMO

![app_demo](https://github.com/ShoheiKobata/orin_bcap_python_samples/assets/33975299/842ba822-b6de-4f81-8bec-c48eba1dd71f)

While the robot is moving, the 3D mouse is being operated.


## Description  

By reflecting the movement amount of the 3D mouse on the robot, you can intuitively operate the robot.  
You can change the operation method such as straight ahead, straight ahead + rotation.  


## Requirement

python=3.* 
pywinusb==0.4.2

## Installation

```
pip install pywinusb
```

## Usage

```
git clone https://github.com/ShoheiKobata/orin_bcap_python_samples.git
cd orin_bcap_python_samples/3DMouse_Controll
python 3D_mouse_controll_gui.py 
```

## Reference

- b-cap library:  
https://github.com/DENSORobot/orin_bcap  

- spacenavigator library:
Implements a simple interface to the 6 DoF 3Dconnexion [Space Navigator](http://www.3dconnexion.co.uk/products/spacemouse/spacenavigator.html) device.  
Requires [pywinusb](https://pypi.python.org/pypi/pywinusb/) to access HID data -- this is Windows only.  
