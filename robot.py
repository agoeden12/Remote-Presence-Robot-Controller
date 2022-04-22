from numpy import require
from differential_drive import DifferentialDrive
from tank_drive import TankDrive
from motor_controller import MotorControl

from xbox360controller import Xbox360Controller
import argparse as ap

class RemotePresenceRobot:

    def tank_drive(self):
        pass

    def differential_drive(self):
        pass

    def start_controls_socket(self):
        pass

    def shutoff(self):

        # Close socket

        if (self.drive == "differential"):
            self.differential_drive.pi.stop()
        else:
            self.tank_drive.pi.stop()
    
    def drive(self, controller=None):
        if (self.driveType == "differential"):
            self.drive = DifferentialDrive()
        else:
            self.drive = MotorControl() # Replace with tankdrive class

        if (controller == None):
            pass # get vals from socket
        else:
            self.drive.run(controller.axis_l.y, controller.axis_r.x)

    def __init__(self, driveStyle):
        self.driveType = driveStyle


if __name__ == "__main__":

    parser = ap.ArgumentParser()
    parser.add_argument("--no-drive", action="store_true", help="Run the websocket but not control the robot motors.")
    parser.add_argument("--drive-style", type=str, choices=["differential","tank"], required=True, help="Select the control style of the robot.")
    parser.add_argument("--manual-control", action="store_true", help="Run the robot with a controller connected to the robot.")

    args = parser.parse_args()

    rpr = RemotePresenceRobot(args.drive_style)
    rpr.start_controls_socket()

    if (not args.no_drive):
        if (args.manual_control):
            controller = Xbox360Controller(0, axis_threshold=0.5)
            rpr.drive(controller)

        else:
            rpr.drive()



    
    # rpr = RemotePresenceRobot()
    # dd = DifferentialDrive()
    # try:
    #     with Xbox360Controller(0, axis_threshold=0.5) as controller:
    #         # Button A events
    #         # controller.button_a.when_pressed = on_button_pressed
    #         # controller.button_a.when_released = on_button_released

    #         # # Left and right axis move event
    #         # controller.axis_l.when_moved = on_axis_moved
    #         # controller.axis_r.when_moved = on_axis_moved
            
    #         while True:
    #             dd.run(controller.axis_l.y, controller.axis_r.x)
    #             #mc.run(controller.axis_l.y, controller.axis_r.x)
            
            
    # except KeyboardInterrupt:
    #     dd.run(0, 0)
    #     #mc.run(0, 0)
    #     dd.pi.stop()
    #     #mc.pi.stop() # Disconnect pigpio.
    #     pass

