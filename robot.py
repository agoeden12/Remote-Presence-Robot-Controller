from differential_drive import DifferentialDrive
from tank_drive import TankDrive
from motor_controller import MotorControl

from xbox360controller import Xbox360Controller
import argparse as ap
import asyncio
import websockets
import json

class RemotePresenceRobot:

    async def start_controls_socket(self):
        async with websockets.serve(self.drive_with_socket, "localhost", 8765):
            await asyncio.Future()

    def shutdown(self):
        if (self.drive):
            self.drive.pi.stop()
    
    async def drive_with_socket(self, websocket, path):
        async for message in websocket:
            response = json.loads(message)  # Expecting JSON array with [speed, steering]
            print(response)
            self.drive.run(response[0], response[1])

    def drive_with_controller(self, controller):
        self.drive.run(controller.axis_l.y, controller.axis_r.x)

    def __init__(self, driveStyle, noDrive = False):
        self.driveType = driveStyle
        self.noDrive = noDrive
 
        if (self.driveType == "differential"):
            self.drive = DifferentialDrive()
        else:
            self.drive = MotorControl() # Replace with tankdrive class


if __name__ == "__main__":

    parser = ap.ArgumentParser()
    parser.add_argument("--no-drive", action="store_true", help="Run the websocket but not control the robot motors.")
    parser.add_argument("--drive-style", type=str, choices=["differential","tank"], default="differential", help="Select the control style of the robot.")
    parser.add_argument("--manual-control", action="store_true", help="Run the robot with a controller connected to the robot.")

    args = parser.parse_args()

    rpr = RemotePresenceRobot(args.drive_style, args.no_drive)

    try:
        if (args.manual_control):
            pass
            # controller = Xbox360Controller(0, axis_threshold=0.5)
            # rpr.drive_with_controller(controller)'
        else:
            asyncio.run(rpr.start_controls_socket())
    except KeyboardInterrupt:
        rpr.shutdown()
