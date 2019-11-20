import RPi.GPIO as GPIO
from time import sleep
from subprocess import check_output

Heading = 333

## Get C program output      ##   https://raspberrypi.stackexchange.com/questions/61197/read-c-output-in-python ##
## String to list of numbers ##   https://stackoverflow.com/questions/4289331/how-to-extract-numbers-from-a-string-in-python ##
x = check_output('./a.out', shell=True)
newstr = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in x)
nums = [float(i) for i in newstr.split()]
Nose = float(nums[0])
Tmeprature = int(nums[1])
print Nose

def SetAngle(angle):
	duty = angle /18 +2
	GPIO.output(11, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(11, False)
	pwm.ChangeDutyCycle(0)


GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm = GPIO.PWM(11, 50)
pwm.start(0)


SetAngle(75)
SetAngle(125)
SetAngle(90)
pwm.stop()
GPIO.cleanup()
