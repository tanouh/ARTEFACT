import motor_driver
import time

step_duration = 0.3
step = 0.2
hstep = 0.1
vhstep = 0.05

def start_motor():
        return motor_driver.MotorDriver()

def stop_motor(motor):
        motor.MotorStop(0)
        motor.MotorStop(1)

def set_speed(motor, new_speed):
        motor.set_speed_right(new_speed)
        motor.set_speed_left(new_speed)

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

def turn_right(motor):
        motor.MotorRun(0, 'backward') # ou stop ?
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)

def move_right_forward(motor):
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)

def move_left_forward(motor):
        motor.MotorRun(0, 'forward')
        time.sleep(step_duration)

def modify_speed(motor, new_speed):
    set_speed(motor, new_speed)
    time.sleep(step_duration)  # Optionally, wait for some duration to see the effect
    
def turn_around(motor,   orientation = turn_right):
        modify_speed(motor, 60) 
        orientation(motor)
        time.sleep(step)
        stop_motor(motor)

def left(middle,motor):
        motor.set_speed_right((70+(abs(middle)*0.1))/2)
        motor.set_speed_left(70/2)
        print('gauche')

def left_slow(middle,motor):
        motor.set_speed_right((35+(abs(middle)*0.05))/2)
        motor.set_speed_left(35/2)

def right(middle,motor):
        motor.set_speed_left((70+(abs(middle)*0.1))/2)
        motor.set_speed_right(70/2)
        print('droite')

def right_slow(middle,motor):
        motor.set_speed_left((35+(abs(middle)*0.05))/2)
        motor.set_speed_right(35/2)

