# Finch Robot 2.0 (by Birdbrain) Library for micro:bit v2

Library to use the [BirdBrain](https://www.birdbraintechnologies.com/) [Finch Robot 2.0](https://www.birdbraintechnologies.com/products/finch-robot-2-0/) with [MicroPython on the micro:bit v2](https://python.microbit.org/v/3).

**Translated from the MakeCode library for MicroPython on the micro:bit v2 by [CodeJoy](https://codejoy.org)**

_____

## Important notes:
* This is similar in syntax to the original MakeCode library. However, there are some differences due to language differences and some thing I wanted to change for consistency.
   * [Original Birdbrain MakeCode library for the Finch Robot](https://github.com/BirdBrainTechnologies/pxt-finch) (MIT License)
* **IMPORTANT**: This library was built and tested using the micro:bit v2. It is unlikely to function properly on the micro:bit v1 due to memory constraints.**
_____
## Adding the library

In the [micro:bit Python Editor](https://python.microbit.org/):
1. Select the "Project" tab on the menu on the left side of interface
2. Click the "Create file" button
3. Name the file "hummingbird.py" and click the "Create" button
4. Copy the content of the [finch.py file from this github repo](finch.py)
7. Click back over to the main.py and import the new library by adding the line below under the `from microbit import *` line:
  * `from finch import finch`

Now just check out the documentation below to see how to use the library in your code!

_____
## API Reference

_Note: There are a number of other methods in the module. However, then are intended for internal use and not for library consumption, so they are not documented here. Those methods all begin with an underscore "\_"._

---
### startFinch()
This initialization method must be run after all your imports at the top of your python script and after your have imported the Hummingbird library.
```
    from microbit import *
    from finch import finch
    # ... any other needed libraries ...

    finch.startFinch()
    finch.stop() # If you find the finch is not stopping after a reset add this line after finch.startFinch()

    # ... the rest of your code ...
```
---
### getDistance()
Returns the value of the Finch distance sensor in centimeters

`finch.getDistance()`

```
    # Get the value of the distance sensor and assign it to a variable named "distance"
    distance = finch.getDistance()
```

---
### stop()
Stop all actions on the robot. This will stop the motors and turn off all LEDs.

`finch.stop()`

```
    # Stop the finch and turn off all the LEDs
    finch.stop()
```

---
### resetEncoders()
Sets the value of the left and right encoders to zero.

`finch.resetEncoders()`

```
    # Reset the finch's motor encoders to 0
    finch.resetEncoders()
```

---
### getEncoder(side)
Returns the number of rotations that the requested wheel has turned since the last reset

Note: This number only increases. Backward rotations still add to the total value just like a car's odometer.

`finch.getEncoder(side)`

This method has 1 argument
* side: The specific encoder to read. ("left" or "right")

```
    # Get the value of the left side motor encoder
    finch.getEncoder('left')
```

---
### setBeak(red, green, blue)
Set the beak LED color.

`finch.setBeak(red, green, blue)`

This method has 3 arguments:
* `red`: red intensity percentage (0 - 100)
* `green`: green intensity percentage (0 - 100)
* `blue`: blue intensity percentage (0 - 100)

```
    # Set the beak color to yellow
    finch.setBeak(100, 80, 0)
```

---
### setTail(port, red, green, blue)
Set one or all of the tail LED color(s).

`finch.setTail(port, red, green, blue)`

This method has 4 arguments:
* `port`: port number (1-4) to set or 5 for all 4
* `red`: red intensity percentage (0 - 100)
* `green`: green intensity percentage (0 - 100)
* `blue`: blue intensity percentage (0 - 100)

```
    # Set each of the tail LEDs to a different color
    finch.setTail(1, 100, 0, 0) # Red
    finch.setTail(2, 0, 100, 0) # Green
    finch.setTail(3, 0, 0, 100) # Blue
    finch.setTail(4, 100, 0, 100) # Purple
```

---
### stopMotors()
Stop both motors.

`finch.stopMotors()`

```
    # Stop the Finch's movement
    finch.stopMotors()
```

---
### setMotors(l_speed, r_speed)
Sets the Finch motors at the provided speeds. 
Note: Negative speeds turn the motors in reverse.

`finch.setMotors(l_speed, r_speed)`

This method has 2 arguments        
* `l_speed`: Left motor speed (-100 - 100) [Default: 50]
* `r_speed`: Right motor speed (-100 - 100) [Default: 50]

```
    # Setting the left motor to 60% and the right motor to 40% causes the finch to start a wide turn to the right.
    finch.setMotors(60, 40)
```

---
### setMove(direction, distance, speed)
Moves the Finch forward or back for a given distance at a given speed

`finch.setMove(direction, distance, speed)`

This method has 3 arguments        
* `direction`: Direction to move. ("forward" or "backward")
* `distance`: Number of centimeters (cm) to move [10,000cm max]
* `speed`: Percentage of max speed to move the Finch (0 - 100) [50% is the default]


```
    # Move the Finch 100cm forward at 80% speed, then pause for 1 second and move the finch 50cm backward at 40% speed
    finch.setMove('forward', 100, 80)
    sleep(1000)
    finch.setMove('backward', 50, 40)
```

---
### setTurn(direction, angle, speed)
Turns the Finch left or right to a given angle at a given speed.

`finch.setTurn(direction, angle, speed)`

This method has 3 arguments        
* `direction`: Direction to turn. ("left" or "right")
* `angle`: Number degrees to turn (360000 degrees max) [Default: 90]
* `speed`: Percentage of max speed to turn the Finch (0 - 100) [Default: 50]

```
    # Turn the find 45 degrees to the right at 60% speed
    finch.setTurn('right', 45, 60)
```

---
### getLine(side)
Returns the value of either the left or right side line sensors.

_Note: You should practice with your desired materials. Depending on how you have setup your surface you will receive different values when the sensor reads or does not read the line. We have found that black electrical tape makes a very effective line._

A sample of code for a line sensing robot is available in the examples folder.

`finch.getLine(side)`

This method has 1 argument
* side: Line sensor to read. ("left" or "right")

```
    # Get the value of the left side line sensor
    finch.getLine('left')
```

---
### getBattery()
Returns the value of the Finch battery in milliVolts

_Note: You may start to see strange behavior when the value is below 3373 mV_

`finch.getBattery()`

```
    # Get the battery voltage and assign it to the variable "batVolts"
    batVolts = finch.getBattery()
```

---
### getFinchAM(type, dimension)
Returns the value of the Finch accelerometer or magnetometer.

_Note: The return value takes into account the position of the micro:bit when the finch is sitting level._

`finch.getFinchAM(type, dimension)`

This method has 2 arguments:
* `type`: Type of sensor to read. ("accelerometer" or "magnetometer")
* `dimension`: Dimension to read. ("x", "y", "z" or "strength")

```
    # Get the value of the x dimension from the accelerometer
    finch.getFinchAM('accelerometer', 'x')
```

---
### getFinchCompass()
Returns the value of the Finch compass in degrees (relative to the Finch's beak)

_Note: The return value takes into account the position of the micro:bit when the finch is sitting level and adjusts if the finch is moved._

`finch.getFinchCompass()`

```
    # Get the value of the compass relative to the finch's beak
    finch.getCompass()
```

---
### isFinchOrientation(orientation)
Returns a boolean value (True or False) that indicates whether or not the Finch is in the given position.

`finch.isFinchOrientation(orientation)`

This method has 1 argument:
* `orientation`:  finch orientation ("beakup", "beakdown", "tiltleft", "tiltright", "level", "upsidedown", "shake")

```
    # See if the finch is upside down
    finch.isFinchOrientation('upsidedown')
```

---
### getFinchOrientations()
Returns a list of all the Finch orientations that are true. ("beakup", "beakdown", "tiltleft", "tiltright", "level", "upsidedown", "shake")

_Note: There is a code sample using this method in the examples folder_

`finch.getFinchOrientations()`

```
    # Get a list of current orientations for the finch and assign it to the variable named finchIs
    finchIs = finch.getFinchOrientations()
```

---

## Sample Code:

Several samples of code are available in the [examples folder](examples/) of this repository

---

## License
```
Copyright 2023 CodeJoy

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the “Software”), to deal in the
Software without restriction, including without limitation the rights to use, 
copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```