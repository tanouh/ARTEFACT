import motor_driver
import time

step_duration = 0.2

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

(a2,b2)=(0,False)
def move_backward(motor):
        global a2
        global b2
        b2=True
        a2+=1
        motor.MotorRun(0, 'backward')
        motor.MotorRun(1, 'backward')
        time.sleep(step_duration)
        a2-=1
        if not b2:
                a2=0
        elif a2==0:
                b3=False
                stop_motor(motor)
        else:
                a2=0

(a3,b3)=(0,False)
def turn_left(motor):
        global a3
        global b3
        b3=True
        a3+=1
        motor.MotorRun(0, 'forward')
        motor.MotorRun(1, 'backward') # ou stop ? 
        time.sleep(step_duration)
        a3-=1
        if not b3:
                a3=0
        elif a3==0:
                b3=False
                stop_motor(motor)
        else:
                a3=0

(a4,b4)=(0,False)
def turn_right(motor):
        global a4
        global b4
        b4=True
        a4+=1
        motor.MotorRun(0, 'backward') # ou stop ?
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)
        a4-=1
        if not b4:
                a4=0
        elif a4==0:
                b4=False
                stop_motor(motor)
        else:
                a4=0

(a5,b5)=(0,False)
def move_right_forward(motor):
        global a5
        global b5
        b5=True
        a5+=1
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)
        a5-=1
        if not b5:
                a5=0
        elif a5==0:
                b5=False
                stop_motor(motor)
        else:
                a5=0

(a6,b6)=(0,False)
def move_left_forward(motor):
        global a6
        global b6
        b6=True
        a6+=1
        motor.MotorRun(0, 'forward')
        time.sleep(step_duration)
        a6-=1
        if not b6:
                a6=0
        elif a6==0:
                b6=False
                stop_motor(motor)
        else:
                a6=0

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