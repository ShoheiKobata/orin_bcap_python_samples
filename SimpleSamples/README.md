# Simple Samples

a simple robot operation program using b-cap communication.  

## Description  

XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx

## Usage

- You should edit config of IP Address.  

b-cap library:  
https://github.com/DENSORobot/orin_bcap  

python=3.*

## Reference

Reference of the commands used in the sample program.

------------------------

### TakeArm

CaoRobot::Execute("TakeArm")

This command corresponds to TAKEARM instruction of PacScript language.

Syntax `TakeArm([<ArmGroup> [,<Keep>]])`

- ArmGroup
  - Arm group number (VT_I4)
  - 0 to 31 (0 by default) (0 is an Armgroup that includes robot joints only and does not include any Extended-joints)
- Keep
  - Default value (VT_I4)
  - 0: Set the internal speed to 100, the current tool number to 0, and the current work number to 0.
  - 1: Keep the current internal speed, the current tool number and the current work number without change.
  - (0 by default) ※If Keep option is not specified, the internal speed, the current tool number and the current work number are initialized to 100, 0 and 0, respectively.
- Return value
  - None

------------------------

### Motor

CaoRobot::Execute("Motor")

Turn ON/OFF the motor.

Syntax `Motor(<State> [,<NoWait>])`

- State
  - Motor status (VT_I4)
  - 0: Motor OFF
  - 1: Motor ON
- NoWait
  - Completion wait (VT_I4)
  - 0:Wait for completion (default)
  - 1: Do not wait for completion
- Return value
  - None

------------------------

### ExtSpeed

CaoRobot::Execute("ExtSpeed")

Set the external speed, external acceleration, and external deceleration.

Syntax `ExtSpeed ( <Speed> [,<Accel> [,<Decel>]] )`

- Speed
  - External speed (VT_R4)
- Accel
  - External acceleration (VT_R4)
  - -1 : Keep the current setting (Not change the current setting)
  - -2 : `(External speed)*(External speed) / 100`
  - "-2" is entered if it is omitted.
- Decel
  - External deceleration (VT_R4)
  - -1 : Keep the current setting (Not change the current setting)
  - -2 : `(External speed)*(External speed) / 100`
  - "-2" is entered if it is omitted.
- Return value
  - None

------------------------

### Move

CaoRobot::Move

Move the robot to the specified coordinates.

Syntax `Move <lComp:LONG >, <vntPose:POSEDATA> [,<vntPose:POSEDATA>…] [, < bstrOpt:BSTR>]`

- lComp
  - Interpolation 1:MOVE P,... , 2:MOVE L,... , 3:MOVE C,... , 4:MOVE S,...
- vntPose
  - Pose data (POSEDATA type)
- bstrOpt
  - Motion option `[SPEED=n][,ACCEL=n][,DECEL=n][,TIME=n][,NEXT]`
    - SPEED (S): Specify the movement speed. The meaning is the same as the SPEED statement.
    - ACCEL: Specify the acceleration. The meaning is the same as the ACCEL statement.
    - DECEL: Specify the deceleration. The meaning is the same as the DECEL statement.
    - TIME: Specify the time to activate the motion.
    - NEXT: Asynchronous execution option.

#### POSEDATA

In RC8 provider, "POSEDATA " is defined so that the pose data type and vector type data of DENSO robots can be handled by VARIANT type variables.

POSEDATA type (VARIANT)

1. VT_BSTR : `"[<Pass>] [<Variable type>]<Index> [<ExJnt>]"` or `"[<Pass>] [<Variable type>](<Element 1>,<Element 2>,...) [<ExJnt>]"`
2. VT_VARIANT|VT_ARRAY : `(<Value>[,<Variable type>[,<Path>[, <ExJnt>]]])`
   1. `<Value>` : `<Index:VT_R4>` or `<Raw value:VT_R4|VT_ARRAY>`
   2. `<Variable type>` : P, T, J, V type with VT_I4 or VT_BSTR specified (default = P)
   3. `<Pass>` : @P, @E, @0, @Value with VT_I4 or VT_BSTR specified (default = @0)
   4. `<ExtJnt>` : `<Extended-joints option:VT_VARIANT|VT_ARRAY>` (default = None)

- Pass
  |Mark|@P|@E|@0|@Value:n|None|
  |:-:|:--|:--|:--|:--|:--|
  |VT_BSTR|"@P"|"@E"|"@0"|"@n"|""|
  |VT_I4|-1|-2|0|n|0|

- Variable type
  |Mark|P|T|J|V|None|
  |:-:|:--|:--|:--|:--|:--|
  |VT_BSTR|"P"|"T"|"J"|"V"|""|
  |VT_I4|0|1|2|3|-1|

- Index : Value:VT_R4
- Element n : Value:VT_R4

- examples
  1. `@P P[1]` in PacScript
     1. `"@P P1"` in python
     2. `[1,"P","@P"]` in python
     3. `[1,0,-1]` in python
  2. `@E J(0,0,90,0,90,0)` in PacScript
     1. `"@E J(0,0,90,0,90,0)"` in python
     2. `[[0,0,90,0,90,0],"J","@E"]` in python
     3. `[[0,0,90,0,90,0],2,-2]` in python

------------------------

