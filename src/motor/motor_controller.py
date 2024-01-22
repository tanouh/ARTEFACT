import motor_driver
import time

step_duration = .3

def start_motor():
        return motor_driver.MotorDriver()

def stop_motor(motor):
        motor.MotorStop(0)
        motor.MotorStop(1)

def set_speed(motor, new_speed):
        motor.set_speed_right(100*new_speed)
        motor.set_speed_left(100*new_speed)

def set_step_duration(duration):
        step_duration = duration

def move_forward(motor):
        motor.MotorRun(0, 'forward')
        motor.MotorRun(1, 'forward')

def move_backward(motor):
        motor.MotorRun(0, 'backward')
        motor.MotorRun(1, 'backward')
        time.sleep(.3)

def move_right_forward(motor):
        motor.MotorRun(1, 'forward')
        time.sleep(step_duration)

def move_left_forward(motor):
        motor.MotorRun(0, 'forward')
        time.sleep(step_duration)

def modify_speed(motor, new_speed):
    set_speed(motor, new_speed)
    time.sleep(step_duration)  # Optionally, wait for some duration to see the effect
    

def left(middle,motor):
        motor.set_speed_right((40+((middle)**2 *0.0025)))
        motor.set_speed_left(40)

def left_slow(middle,motor):
        motor.set_speed_right((25+((middle)**2 *0.005)))
        motor.set_speed_left(25)

def right(middle,motor):
        motor.set_speed_left((40+((middle)**2 *0.0025)))
        motor.set_speed_right(40)

def right_slow(middle,motor):
        motor.set_speed_left(25+((middle)**2 *0.005))
        motor.set_speed_right(25)

def move_right(motor, speed): 
        print(int(speed*1.25))
        motor.set_speed_left(int(speed*1.25)) # parameters? do not turn too quick
        motor.set_speed_right(speed) # hope to move right more
        move_forward(motor)

def move_left(motor, speed):
        print(int(speed*1.25))
        motor.set_speed_right(int(speed*1.25)) # parameters? do not turn too quick
        motor.set_speed_left(speed)
        move_forward(motor)

def turn_left(motor):
        motor.MotorRun(0, 'forward')
        motor.MotorRun(1, 'backward') # ou stop ? 
        time.sleep(.3)

def turn_right(motor):
        motor.MotorRun(0, 'backward') # ou stop ?
        motor.MotorRun(1, 'forward')
        time.sleep(.3)

def updateMotor(motor, direction, speed, duration):
        set_speed(motor, speed)
        
        if direction  == -1: # tourner a gauche
                print(" tourner a gauche ")
                turn_left(motor)  
                stop_motor(motor)
                time.sleep(0.5)
        
        elif direction == 1: # tourner a droite
                print(" tourner a droite ")
                turn_right(motor)
                stop_motor(motor)
                time.sleep(0.5)
 
        elif direction == -.2: # avancer vers la gauche
                print(" avancer vers la gauche ")
                move_left(motor, speed*100)
                time.sleep(duration)
                stop_motor(motor)
                time.sleep(0.5)

        elif direction == .2 :  # avancer vers la droite
                print(" avancer vers la droite ")
                move_right(motor, speed*100)
                time.sleep(duration)
                stop_motor(motor)
                time.sleep(0.5)

                
        elif direction == 0: # avancer tout droit
                print("demi-tour")
                move_backward(motor)
                stop_motor(motor) 
                time.sleep(.5)
        else : 
                stop_motor(motor) 
                time.sleep(0.5)       

        
                


