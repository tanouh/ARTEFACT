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
    
def turn_around(motor, orientation = turn_right):
        modify_speed(motor, 60) 
        orientation(motor)
        time.sleep(step)
        stop_motor(motor)

def adjusting_speed(target, motor):
        # modify_speed(motor, motor.speed * (target / 20))
        if target > 80 :
                modify_speed(motor, 60) # Si tres loin marcher plus vite
        else :
                modify_speed(motor, 30) # ??
        

def reach_target(target, motor):
        print("Avancer")

        modify_speed(motor, 45) # ??
        turn_left(motor)  # tourner a gauche avant d'avancer pour modifier la direction
        time.sleep(hstep)
        stop_motor(motor)

        if target > 80 :
                modify_speed(motor, 60) # Si tres loin marcher plus vite
        else :
                modify_speed(motor, 30) # ??
        
        move_forward(motor) # Avancer
        time.sleep(2*step)
        stop_motor(motor)
        time.sleep(hstep)

        # modify_speed(motor, 30)
        # turn_left(motor) # Tourner a gauche trop
        



# to do : 
# functions : 
#       - "speed up"
#       - "slow down"

# motor = start_motor()
# move_forward(motor)
# move_forward(motor)
# turn_left(motor)
# turn_right(motor)