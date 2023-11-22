import motor_driver
import time

step_duration = 0.1

def start_motor():
        return motor_driver.MotorDriver()

def stop_motor(motor):
        motor.MotorStop(0)
        motor.MotorStop(1)

def set_speed(motor, new_speed):
        motor.set_speed(new_speed)

def set_step_duration(duration):
        step_duration = duration

def move_forward(motor):
        motor.MotorRun(0, 'forward')
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)

def move_backward(motor):
        motor.MotorRun(0, 'backward')
        motor.MotorRun(1, 'backward')
        time.sleep(step_duration)

def turn_left(motor):
        motor.MotorRun(0, 'forward')
        motor.MotorRun(1, 'backward') # ou stop ? 
        time.sleep(step_duration)
        stop_motor(motor)

def turn_right(motor):
        motor.MotorRun(0, 'backward') # ou stop ?
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)
        stop_motor(motor)


def move_right_forward(motor):
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)
        stop_motor(motor)

def move_left_forward(motor):
        motor.MotorRun(0, 'forward')
        time.sleep(step_duration)
        stop_motor(motor)


# to do : 
# functions : 
#       - "speed up"
#       - "slow down"

# motor = start_motor()
# move_forward(motor)
# move_forward(motor)
# turn_left(motor)
# turn_right(motor)