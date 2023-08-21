# Imports go at the top
from microbit import *
from finch import finch

finch.startFinch()
finch.stop()

line_threshold = 50 # Tweaking this value will change how sensitive the line following is and may vary depending on your line
turn_speed = 10 # Speed to turn at when a line is detected
forward_speed = 50 # Speed to move forward at when no line is detected
change_detected = True # Variable to control if the robot should move forward when no line is detected

left_speed = 0
right_speed = 0

current_right_speed = -1
current_left_speed = -1

go = False # Variable to control if the robot should be moving

while True:
    # Check if the button has been pressed and toggle the robot state
    if button_a.was_pressed():
        go = not go
        if(go):
            # If the robot is enabled, show an arrow
            display.show(Image.ARROW_S)
        else:
            # If the robot is disabled, show a skull
            display.show(Image.SKULL)
            change_detected = True

    # Only run the line following code if the robot is enabled
    if go:
        line_left = finch.getLine('left')
        line_right = finch.getLine('right')
        
        if finch.getDistance() <= 15:
            # Stop before running into something
            finch.setBeak(40,0,0)
            right_speed = 0
            left_speed = 0
        elif line_left < line_threshold:
            # Left sensor reads line
            finch.setBeak(50,40,0)
            left_speed = -turn_speed
            right_speed = turn_speed
        elif line_right < line_threshold:
            # Right sensor reads line
            finch.setBeak(50,40,0)
            left_speed = turn_speed
            right_speed = -turn_speed
        elif change_detected:
            # No sensors read line
            finch.setBeak(0,40,0)
            left_speed = forward_speed
            right_speed = forward_speed
            change_detected = False
            
        # Only update the motors if the speed has changed
        if left_speed != current_left_speed or right_speed != current_right_speed:
            finch.setMotors(left_speed, right_speed)
            change_detected = True
    
    # If robot is disabled stop everything
    else:
        if change_detected:
            finch.stop() # Stop the robot
            change_detected = False

    sleep(10) # Give the micro:bit a break