from digitalio import DigitalInOut, Direction, Pull#pylint: disable-msg=import-error
import board #pylint: disable-msg=import-error
import adafruit_tcs34725 #pylint: disable-msg=import-error
import servo #pylint: disable-msg=import-error
from analogio import AnalogIn #pylint: disable-msg=import-error
import busio #pylint: disable-msg=import-error
import pulseio #pylint: disable-msg=import-error
import time

# ✓ electromagnet
# ✓ color sensor
#  ✓ servo wiring
#    autonomous mode(will have to wait until it is constructed because we won't know the numbers)
#  ✓ wire mode switch
#    once built, limit potentiometers and scale them to the new range of what's physically possible for less broken servos and finer control
    #could be tricky with the servos meeting in the middle

#servos are a little unreliable

i2c = busio.I2C(board.SCL, board.SDA)#sets up i2c for the color sensor
sensor = adafruit_tcs34725.TCS34725(i2c)

red = DigitalInOut(board.D11)#red 
green = DigitalInOut(board.D12)#green
blue = DigitalInOut(board.D13)#blue
red.direction = Direction.OUTPUT
green.direction = Direction.OUTPUT
blue.direction = Direction.OUTPUT

mag = DigitalInOut(board.D3)#sets up the magnet
mag.direction = Direction.OUTPUT

btn = DigitalInOut(board.D2)#sets up the button
btn.direction = Direction.INPUT
btn.pull = Pull.UP

potpin1 = AnalogIn(board.A5)#sets up the potentiometers
potpin2 = AnalogIn(board.A4)
potpin3 = AnalogIn(board.A3)
potpin4 = AnalogIn(board.A2)

switch = DigitalInOut(board.D4)#sets up the switch
switch.direction = Direction.INPUT



pwm1 = pulseio.PWMOut(board.D8, frequency=50, duty_cycle=0)#set up the servos
pwm2 = pulseio.PWMOut(board.D9, frequency=50, duty_cycle=0)
pwm3 = pulseio.PWMOut(board.D10, frequency=50, duty_cycle=0)###
pwm4 = pulseio.PWMOut(board.D5, frequency=50, duty_cycle=0)
servo1 = servo.Servo(pwm1, min_pulse=500, max_pulse=2400)
servo2 = servo.Servo(pwm2, min_pulse=500, max_pulse=2400)
servo3 = servo.Servo(pwm3, min_pulse=500, max_pulse=2400)
servo4 = servo.Servo(pwm4, min_pulse=500, max_pulse=2400)


def mapp(x,in_min,in_max,out_min,out_max):
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min




def ledset():
    colors = sensor.color_rgb_bytes
    if max(colors)>29:
        spot = colors.index(max(colors))
    else:
        spot = -1
    
    #find prettier solution
    if spot == 0:
       red.value = True
       green.value = False
       blue.value = False
    elif spot == 1:
        green.value = True
        red.value = False
        blue.value = False
    elif spot == 2:
        blue.value = True
        red.value = False
        green.value = False
    else:
        blue.value = False
        red.value = False
        green.value = False
            
        

while True:
    mag.value = not btn.value
    
    print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
    if switch.value:
        servo1.angle = mapp(potpin1.value,0,65536,0,179)
        servo2.angle = mapp(potpin2.value,0,65536,0,179)
        servo3.angle = mapp(potpin3.value,0,65536,0,179)
        servo4.angle = mapp(potpin4.value,0,65536,0,179)
    else:
        pass
        #The automatic mode code will go here
    
    ledset()#set led colors using function ledset(color)
