from time import sleep
import pigpio
import math
from xbox360controller import Xbox360Controller

class DifferentialDrive:
    def __init__(self):
        self.pi = pigpio.pi()

        # white input wire is connected to GPIO 12, 13 which will control the speed via PWM. Calibrate ESC
        self.L_ESC_GPIO = 12
        self.R_ESC_GPIO = 13

        # connect to pigpio and initialize
        self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1500)
        self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1500)

        # set drive coefficient (range of speed)
        self.DRIVE_COEFF = 50

    def run(self, x, y):
        if not self.pi.connected:
            print("not connected")
            exit()
        self.joystickToDiff(x, y, 0, 127, 1400, 1600)
        print("Done")
        
    def joystickToDiff(self, x, y, minJoystick, maxJoystick, minSpeed, maxSpeed):
        # If x and y are 0, no turn
        if x == 0 and y == 0:
            return (0, 0)

        # First Compute the angle in deg
        # First hypotenuse
        z = math.sqrt(x * x + y * y)

        # angle in radians
        rad = math.acos(math.fabs(x) / z)

        # and in degrees
        angle = rad * 180 / math.pi

        # Now angle indicates the measure of turn
        # Along a straight line, with an angle o, the turn co-efficient is same
        # this applies for angles between 0-90, with angle 0 the coeff is -1
        # with angle 45, the co-efficient is 0 and with angle 90, it is 1

        tcoeff = -1 + (angle / 90) * 2
        turn = tcoeff * math.fabs(math.fabs(y) - math.fabs(x))
        turn = round(turn * 100, 0) / 100

        # And max of y or x is the movement
        mov = max(math.fabs(y), math.fabs(x))

        # First and third quadrant
        if (x >= 0 and y >= 0) or (x < 0 and y < 0):
            rawLeft = mov
            rawRight = turn
        else:
            rawRight = mov
            rawLeft = turn

        # Reverse polarity
        if y < 0:
            rawLeft = 0 - rawLeft
            rawRight = 0 - rawRight

        # minJoystick, maxJoystick, minSpeed, maxSpeed
        # Map the values onto the defined range
        #rightOut = map(rawRight, minJoystick, maxJoystick, minSpeed, maxSpeed)
        #leftOut = map(rawLeft, minJoystick, maxJoystick, minSpeed, maxSpeed)

        #if (rightOut >= -1 or rightOut <=1) and (leftOut >= -1 or leftOut <=1):
        self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1500 + rawLeft * self.DRIVE_COEFF)
        self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1500 + rawRight * self.DRIVE_COEFF)

    def map(v, in_min, in_max, out_min, out_max):
        # Check that the value is at least in_min
        if v < in_min:
            v = in_min
        # Check that the value is at most in_max
        if v > in_max:
            v = in_max
        return (v - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

if __name__ == '__main__':
    DifferentialDrive().run()