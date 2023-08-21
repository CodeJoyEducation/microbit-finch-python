"""
Library to use the Finch with MicroPython on the micro:bit v2.
README: https://github.com/CodeJoyEducation/microbit-finch-python
(c) 2023 CodeJoy - All rights reserved.
This work is licensed under the terms of the MIT license.  
For a copy, see <https://opensource.org/licenses/MIT>.
"""
from microbit import spi,sleep,accelerometer,compass,pin0,pin2,pin13,pin14,pin15,pin16,running_time,display,Image
from time import sleep_us
from math import pi,atan,atan2,sin,cos
class finch:
	readyToSend=False
	blr=0
	blg=0
	blb=0
	sd=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
	lsr=0
	@staticmethod
	def startFinch():
		"""Must be run before any other Finch commands. This initializes the Finch robot.
        """
		pin0.write_analog(0)
		pin2.write_digital(1)
		sleep(100)
		pin2.write_digital(0)
		sleep(2000)
		pin16.write_digital(1)
		spi.init(baudrate=1000000,bits=8,mode=0,sclk=pin13,mosi=pin15,miso=pin14)
		finch.readyToSend=True
		finch.stop()
		finch.resetEncoders()
		finch._sendCommand([0xD4])
		display.show(Image.HAPPY)
	@staticmethod
	def _capToBounds(value:int,min_value:int,max_value:int):
		"""(PRIVATE) Restrict a value between min and max values
        
        :param value: The value to constrain
        :param min_value: The minimum possible value
        :param max_value: The maximum possible value
        """
		return min(max(value,min_value),max_value)
	@staticmethod
	def _percentToByte(percent:int):
		"""(PRIVATE) Convert a percentage to a value between 0 and 255
        
        :param percent: The percentage to convert
        """
		return int(finch._capToBounds(percent,0,100)/100*255)
	@staticmethod
	def _sendCommand(cmdArray:list,fillerVal=0xFF):
		"""(PRIVATE) Send one command to the finch. Each command consists of
                16 spi writes. If less than 16 values are specified, additional filler
                values will be added.

        :param cmdArray: List containing all values to send
        :param fillerVal: value to use as filler (defaults to 0xFF)
        """
		if(len(cmdArray)>16): return
		t=0
		while not finch.readyToSend and t<25:
			sleep(10)
			t+=1
		if finch.readyToSend:
			finch.readyToSend=False
			sleep_us(500)
			pin16.write_analog(0)
			sleep_us(4)
			r=bytearray(16)
			m=bytearray(16)
			for i in range(16):
				try:
					v=cmdArray[i]
				except IndexError:
					v=fillerVal
				m[i]=v
			spi.write_readinto(m,r)
			sleep_us(100)
			finch.sd=r
			finch.lsr=running_time()
			sleep_us(4)
			pin16.write_digital(1)
			finch.readyToSend=True
	@staticmethod
	def _getSensors():
		"""(PRIVATE) Reads the value of the sensors. Resulting array contains:
                [Firmware version, nothing, distance msb, distance lsb, light left,
                light right, line left, line right, battery, enc3 left, enc2 left,
                enc1 left, enc3 right, enc2 right, enc1 right, Filler Value]
        """
		if running_time()-finch.lsr>10:
			finch._sendCommand([0xD4])
	@staticmethod
	def getDistance():
		"""Returns the value of the Finch distance sensor in centimeters
        """
		finch._getSensors()
		return round(((finch.sd[2]<<8|finch.sd[3])*0.0919))
	@staticmethod
	def _getPositionControlFlag():
		"""(PRIVATE) 1 if the finch is still moving, otherwise 0
        """
		finch._getSensors()
		return_val=0
		return_val=((finch.sd[6]&0x80)>>7)
		return return_val
	@staticmethod
	def stop():
		""" Stop all actions on the robot. This will stop the motors and turn off all LEDs.
        """
		finch._sendCommand([0xDF])
	@staticmethod
	def resetEncoders():
		""" Sets the value of the left and right encoders to zero.
        """
		finch._sendCommand([0xD5])
		sleep(100)
	@staticmethod
	def _sendAllLEDs(red:int,green:int,blue:int):
		"""(PRIVATE) Utility method to send the LED command to set all beak
            and tail LEDs at once. Only the tail LEDs will be set to the value
            specified. Beak LED will be set using the global variable.

            :param red: red intensity (0 - 255)
            :param green: green intensity (0 - 255)
            :param blue: blue intensity (0 - 255)
        """
		finch._sendCommand([0xD0,finch.blr,finch.blg,finch.blb,red,green,blue,red,green,blue,red,green,blue,red,green,blue])
	@staticmethod
	def _sendSingleLED(portNumber:int,red:int,green:int,blue:int):
		"""(PRIVATE) Send a command to set a single LED

            :param portNumber: Beak = 0, Tail = 1 - 4 (5 = ALL)
            :param red: red intensity (0 - 255)
            :param green: green intensity (0 - 255)
            :param blue: blue intensity (0 - 255)
        """
		finch._sendCommand([0xD3,portNumber,red,green,blue],0x00)
	@staticmethod
	def setBeak(red:int,green:int,blue:int):
		"""Set the beak LED color

            :param red: red intensity % (0 - 100)
            :param green: green intensity % (0 - 100)
            :param blue: blue intensity % (0 - 100)
        """
		finch.blr=finch._percentToByte(red)
		finch.blg=finch._percentToByte(green)
		finch.blb=finch._percentToByte(blue)
		finch._sendSingleLED(0,finch.blr,finch.blg,finch.blb)
	@staticmethod
	def setTail(port:int,red:int,green:int,blue:int):
		"""Set the LED color of the tail LEDs

            :param port: Tail LED port (1 - 4 or 5 for all)
            :param red: red intensity % (0 - 100)
            :param green: green intensity % (0 - 100)
            :param blue: blue intensity % (0 - 100)
        """
		if(port==5):
			finch._sendAllLEDs(finch._percentToByte(red),finch._percentToByte(green),finch._percentToByte(blue))
		elif(port>=1 and port<=4):
			finch._sendSingleLED(port,finch._percentToByte(red),finch._percentToByte(green),finch._percentToByte(blue))
	@staticmethod
	def _sendMotor(l_velocity:int,l_dist:int,r_velocity:int,r_dist:int):
		"""(PRIVATE) Send a command to move the finch motors

        :param l_velocity: left motor velocity
        :param l_dist: left motor distance (ticks)
        :param r_velocity: right motor velocity
        :param r_dist: right motor distance (ticks)
        """
		finch._sendCommand([0xD2,0xFF,l_velocity,(l_dist&0xFF0000)>>16,(l_dist&0x00FF00)>>8,(l_dist&0x0000FF),r_velocity,(r_dist&0xFF0000)>>16,(r_dist&0x00FF00)>>8,(r_dist&0x0000FF)])
	@staticmethod
	def _convertSpeed(speed:int):
		"""(PRIVATE) Convert a speed percentage to a value between -100 and 100

        :param speed: speed percentage (0 - 100%)
        """
		converted=round(abs(finch._capToBounds(speed,-100,100))*0.36)
		if converted!=0 and converted<3:converted=3
		raw=0
		if speed>=0:
			raw=0x80|converted
		else:
			raw=0x7F&converted
		return raw
	@staticmethod
	def stopMotors():
		finch._sendMotor(0,0,0,0)
	@staticmethod
	def setMove(direction:str,distance:int,speed:int=50):
		"""Moves the Finch forward or back for a given distance at a given speed
        
        :param direction: Direction to move. ("forward" or "backward")
        :param distance: Number of centimeters (cm) t0 move [10,000cm max]
        :param speed: Percentage of max speed to move the Finch (0 - 100)
        """
		velocity=0
		direction=direction.lower()
		distance=round(finch._capToBounds(distance,0,100000)*49.7)
		if distance==0: return
		if direction=='forward':
			velocity=finch._convertSpeed(speed)
		elif direction=='backward':
			velocity=finch._convertSpeed(-speed)
		else:
			raise ValueError('the direction input only accepts "forward" or "backward"')
		finch._sendMotor(velocity,distance,velocity,distance)
		sleep(50)
		while finch._getPositionControlFlag()==1:
			sleep(30)
		finch.stopMotors()
		sleep(100)
	@staticmethod
	def setTurn(direction:str,angle:int=90,speed:int=50):
		"""Turns the Finch left or right to a given angle at a given speed
        
        :param direction: Direction to turn. ("left" or "right")
        :param angle: Number of degrees to turn (360 * 1000 degrees max) [Default: 90]
        :param speed: Percentage of max speed to turn the Finch (0 - 100) [Default: 50]
        """
		l_speed=0
		r_speed=0
		direction=direction.lower()
		if direction=='left':
			l_speed=finch._convertSpeed(-speed)
			r_speed=finch._convertSpeed(speed)
		elif direction=='right':
			l_speed=finch._convertSpeed(speed)
			r_speed=finch._convertSpeed(-speed)
		else:
			raise ValueError('the direction input only accepts "left" or "right"')
		dist=round(4.335*finch._capToBounds(angle,0,360000))
		if(dist==0): return
		finch._sendMotor(l_speed,dist,r_speed,dist)
		sleep(50)
		while finch._getPositionControlFlag()==1:
			sleep(30)
		finch.stopMotors()
		sleep(100)
	@staticmethod
	def setMotors(l_speed:int=50,r_speed:int=50):
		"""Sets the Finch motors at the provided speeds
        
        :param l_speed: Left motor speed (-100 - 100) [Default: 50]
        :param r_speed: Right motor speed (-100 - 100) [Default: 50]
        """
		finch._sendMotor(finch._convertSpeed(l_speed),0,finch._convertSpeed(r_speed),0)
	@staticmethod
	def getLight(light:str):
		finch._getSensors()
		R=finch._percentToByte(finch.blr)
		G=finch._percentToByte(finch.blg)
		B=finch._percentToByte(finch.blb)
		raw_val=0
		correction=0
		if light=='right':
			raw_val=finch.sd[5]
			correction=6.40473070e-03*R+1.41015162e-02*G+5.05547817e-02*B+3.98301391e-04*R*G+4.41091223e-04*R*B+6.40756862e-04*G*B+-4.76971242e-06*R*G*B
		elif light=='left':
			raw_val=finch.sd[4]
			correction=1.06871493e-02*R+1.94526614e-02*G+6.12409825e-02*B+4.01343475e-04*R*G+4.25761981e-04*R*B+6.46091068e-04*G*B+-4.41056971e-06*R*G*B
		return round(finch._capToBounds(raw_val-round(correction),0,100))
	@staticmethod
	def getLine(side:str):
		"""Returns the value of either the left or right side line sensors
        
        :param line: Line sensor to read. ("left" or "right")
        """
		finch._getSensors()
		side=side.lower()
		return_val=0
		if side=='right':
			return_val=finch.sd[7]&0x7F
		elif side=='left':
			return_val=finch.sd[6]&0x7F
		else:
			raise ValueError('the line input only accepts "left" or "right"')
		return round(100-((return_val-6)*100/121))
	@staticmethod
	def getEncoder(side:str):
		"""Returns the number of rotations that the requested wheel has turned since the last reset
        
        :param encoder: Encoder to read. ()"left" or "right")
        """
		finch._getSensors()
		side=side.lower()
		return_val=0
		if side=='right':
			return_val=(finch.sd[12]<<16|finch.sd[13]<<8|finch.sd[14])
		elif side=='left':
			return_val=(finch.sd[9]<<16|finch.sd[10]<<8|finch.sd[11])
		else:
			raise ValueError('the encoder input only accepts "left" or "right"')
		if return_val>=0x800000:
			return_val=return_val|0xFF000000
		return round(return_val/792,1)
	@staticmethod
	def getBattery():
		"""Returns the value of the Finch battery in milliVolts
        Note: You may start to see strange behavior when the value is below 3373 mV
        """
		finch._getSensors()
		return round(9.37*(finch.sd[8]+320))
	@staticmethod
	def _getFinchAccel(dimension:str):
		"""(PRIVATE) Returns the value of the Finch accelerometer
        
        :param dimension: Dimension to read. ("x", "y", "z" or "strength")
        """
		dimension=dimension.lower()
		if dimension=='x'or dimension=='strength':
			return -accelerometer.get_x()
		elif dimension=='y'or dimension=='z':
			mbY=-accelerometer.get_y()
			mbZ=accelerometer.get_z()
			rad=40*pi/180
			if dimension=='y':
				return mbY*cos(rad)-mbZ*sin(rad)
			elif dimension=='z':
				return mbY*sin(rad)+mbZ*cos(rad)
		else:
			raise ValueError('the dimension input only accepts "x", "y", "z" or "strength"')
	@staticmethod
	def _getFinchMag(dimension:str):
		"""(PRIVATE) Returns the value of the Finch Magnetometer and reports it in finch reference frame
        
        :param dimension: Dimension to read. ("x", "y", "z" or "strength")
        """
		dimension=dimension.lower()
		if dimension=='x'or dimension=='strength':
			return -compass.get_x()
		elif dimension=='y'or dimension=='z':
			mbY=-compass.get_y()
			mbZ=-compass.get_z()
			rad=40*pi/180
			if dimension=='y':
				return mbY*cos(rad)+mbZ*sin(rad)
			elif dimension=='z':
				return mbZ*cos(rad)-mbY*sin(rad)
		else:
			raise ValueError('the dimension input only accepts "x", "y", "z" or "strength"')
	@staticmethod
	def getFinchAM(type:str,dimension:str):
		"""Returns the value of the Finch accelerometer or magnetometer
        
        :param type: Type of sensor to read. ("accelerometer" or "magnetometer")
        :param dimension: Dimension to read. ("x", "y", "z" or "strength")
        """
		type=type.lower()
		if(type=='accelerometer'):
			return round(finch._getFinchAccel(dimension)*0.00980665*10)/10
		elif(type=='magnetometer'):
			return round(finch._getFinchMag(dimension))
		else:
			raise ValueError('the type input only accepts "accelerometer" or "magnetometer"')
	@staticmethod
	def getFinchCompass():
		"""Returns the value of the Finch compass in degrees (relative to the Finch's beak)
        """
		ax=finch._getFinchAccel('x')
		ay=finch._getFinchAccel('y')
		az=finch._getFinchAccel('z')
		mx=finch._getFinchMag('x')
		my=finch._getFinchMag('y')
		mz=finch._getFinchMag('z')
		phi=atan(-ay/az)
		theta=atan(ax/(ay*sin(phi)+az*cos(phi)))
		xp=mx
		yp=my*cos(phi)-mz*sin(phi)
		zp=my*sin(phi)+mz*cos(phi)
		xpp=xp*cos(theta)+zp*sin(theta)
		return (round(180.0+((atan2(xpp,yp))*(180/pi)))+180)%360
	@staticmethod
	def isFinchOrientation(orientation:str):
		"""Returns a boolean value that indicates whether or not the Finch is in the given position.

        @param  orientation: finch orientation ("beakup", "beakdown", "tiltleft", "tiltright", "level", "upsidedown", "shake")
        """
		orientation=orientation.lower()
		threshold=800
		if orientation=='beakup':
			return finch._getFinchAccel('y')>threshold
		elif orientation=='beakdown':
			return finch._getFinchAccel('y')<-threshold
		elif orientation=='tiltleft':
			return finch._getFinchAccel('x')<-threshold
		elif orientation=='tiltright':
			return finch._getFinchAccel('x')>threshold
		elif orientation=='level':
			return finch._getFinchAccel('z')<-threshold
		elif orientation=='upsidedown':
			return finch._getFinchAccel('z')>threshold
		elif orientation=='shake':
			return accelerometer.is_gesture('shake')
		else:
			raise ValueError('the orientation input only accepts "beakup", "beakdown", "tiltleft", "tiltright", "level", "upsidedown", "shake"')
	@staticmethod
	def getFinchOrientations():
		"""Returns a list of all the Finch orientations that are true. ("beakup", "beakdown", "tiltleft", "tiltright", "level", "upsidedown", "shake")
        """
		orientations=['beakup','beakdown','tiltleft','tiltright','level','upsidedown','shake']
		return_list=[]
		for orientation in orientations:
			if finch.isFinchOrientation(orientation):
				return_list.append(orientation)
		return return_list