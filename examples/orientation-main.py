# Imports go at the top
from microbit import *
from finch import finch
import speech


finch.startFinch()
finch.stop()

while True:
    orientation = finch.getFinchOrientations()
    # print(orientation)
    # print('Direction: ',finch.getFinchCompass())
    if 'upsidedown' in orientation:
        finch.setBeak(100,0,0)
        speech.say('help!')
    elif 'beakup' in orientation:
        finch.setBeak(100,80,0)
    elif 'level' in orientation:
        finch.setBeak(60,60,60)
    else:
        finch.setBeak(0,0,0)

    sleep(10)