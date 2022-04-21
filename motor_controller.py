from time import sleep
import pigpio


# IMPORTANT: run 'sudo pigpiod' prior to running script
# range 1100 - 1900 \\ 1500 == stop \\ 1100 - 1500 backwards \\ 1500 - 1900 forwards
class MotorControl:

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

    def run(self, speed, turn):
        if not self.pi.connected:
            print("not connected")
            exit()
        
        print("Speed: {0} | Turn: {1}".format(speed, turn))
        self.set_Turn(speed, turn)
        print("run done")



    def test_run(self):
        if not self.pi.connected:
            print("not connected")
            exit()
        try:
            # launch program
            print('this ran')
            while True:
                # logic should follow: if not receive input command within a second, then stop(), else execute input command
                # accept commands through UDP socket. For now we hard code commands to test out
                self.set_Turn(.1, 0)
                # (speed, turn)

        # force stop program -- doesn't need to be from keyboard interrupt but from controller
        except KeyboardInterrupt:
            print('this stopped')
            self.set_Turn(0, 0)
            self.pi.stop() # Disconnect pigpio.

    def set_Turn(self, speed, turn):
        # no turn (forwards & backwards)
        # speed value given from from -1 to 1
        # directional value from -1 to 1
        if turn == 0:
            print('no turn')
            self.set_Drive(speed, 1, 1)
        # turn right
        if turn > 0:
            # right go backwards, left move forwards at same speed
            # speed will determine forward or backwards drive
            print('turn right')
            self.set_Drive(speed, 1, -1)
        # turn left
        if turn < 0:
            print('turn left')
            self.set_Drive(speed, -1, 1)

        print("set_Turn done")

    def set_Drive(self, speed, L, R):
        # stop
        if speed == 0:
            self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1500)
            self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1500)

        # move forwards
        elif speed > 0:
            if L == -1:
                # if we're turning left
                self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1450 + L * speed * self.DRIVE_COEFF)
                self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1550 + R * speed * self.DRIVE_COEFF)
            elif R == -1:
                # if we're turning right
                # print('now this should run')
                # print('this is L: ', L * speed * self.DRIVE_COEFF, '\nthis is R: ', R * speed * self.DRIVE_COEFF)
                # self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1550)
                # self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1450)
                self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1550 + L * speed * self.DRIVE_COEFF)
                self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1450 + R * speed * self.DRIVE_COEFF)
            else:
                # no turning, just move forwards
                self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1550 + L * speed * self.DRIVE_COEFF)
                self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1550 + R * speed * self.DRIVE_COEFF)


        # move backwards. as speed moves closer from 0 to -1 we want backwards speed to increase
        else:
            # turning left backwards (reverse of above) since speed is negative, will cancel out -1 value of L allowing it to accelerate.
            # R will continue to accelerate in opposite direction
            # now we want left to move forwards and right to move backwards
            if L == -1:
                self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1550 + L * speed * self.DRIVE_COEFF)
                self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1450 + R * speed * self.DRIVE_COEFF)
            elif R == -1:
                # turning right backwards -- left moves backwards, right forwards
                self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1450 + L * speed * self.DRIVE_COEFF)
                self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1550 + R * speed * self.DRIVE_COEFF)
            else:
                # no turning, just move backwards
                self.pi.set_servo_pulsewidth(self.L_ESC_GPIO, 1450 + L * speed * self.DRIVE_COEFF)
                self.pi.set_servo_pulsewidth(self.R_ESC_GPIO, 1450 + R * speed * self.DRIVE_COEFF)


if __name__ == '__main__':
    MotorControl().run()