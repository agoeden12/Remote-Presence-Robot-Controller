from differential_drive import DifferentialDrive
from tank_drive import TankDrive
from xbox360controller import Xbox360Controller
import signal
from motor_controller import MotorControl


class RemotePresenceRobot:


    def __init__(self):
        pass



def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))


def on_button_released(button):
    print('Button {0} was released'.format(button.name))


def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))


if __name__ == "__main__":
    # rpr = RemotePresenceRobot()
    mc = MotorControl()
    dd = DifferentialDrive()
    try:
        with Xbox360Controller(0, axis_threshold=0.5) as controller:
            # Button A events
            # controller.button_a.when_pressed = on_button_pressed
            # controller.button_a.when_released = on_button_released

            # # Left and right axis move event
            # controller.axis_l.when_moved = on_axis_moved
            # controller.axis_r.when_moved = on_axis_moved
            
            while True:
                dd.run(controller.axis_l.y, controller.axis_r.x)
                #mc.run(controller.axis_l.y, controller.axis_r.x)
            
            
    except KeyboardInterrupt:
        dd.run(0, 0)
        #mc.run(0, 0)
        dd.pi.stop()
        #mc.pi.stop() # Disconnect pigpio.
        pass

