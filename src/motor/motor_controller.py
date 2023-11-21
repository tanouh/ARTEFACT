import motor_driver
import time

step_duration = 1

def start_motor():
        return motor_driver.MotorDriver()

def stop_motor(motor):
        motor.MotorStop(0)
        motor.MotorStop(1)

def set_speed(motor, new_speed):
        motor.set_speed(new_speed)

def set_step_duration(duration):
        global step_duration
        step_duration = duration

(a1,b1)=(0,False)
def move_forward(motor):
        global a1
        global b1
        b1=True
        a1+=1
        motor.MotorRun(0, 'forward')
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)
        a1-=1
        if not b1:
                a1=0
        elif a1==0:
                b1=False
                stop_motor(motor)
        else:
                a1=0


def move_backward(motor):
        motor.MotorRun(0, 'backward')
        motor.MotorRun(1, 'backward')
        time.sleep(step_duration)
        stop_motor(motor)


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

# to do : 
# functions : 
#       - "speed up"
# #       - "slow down"
# if __name__ == '__main__':
#         motor = start_motor()
#         move_forward(motor)
#         turn_left(motor)
#         turn_right(motor)
#         stop_motor(motor)