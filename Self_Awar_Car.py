import RPi.GPIO as GPIO
import time

#Set up GPIO mode - Do not edit this code

GPIO.setmode(GPIO.BCM) # BCM Pin references are being used
GPIO.setwarnings(False)

#Set up GPIO pins

motASpeed = 12
motADir = 5
motBSpeed = 13
motBDir = 6
trigger = 16
echo = 19

GPIO.setup(motASpeed,GPIO.OUT)
GPIO.setup(motADir,GPIO.OUT)
GPIO.setup(motBSpeed,GPIO.OUT)
GPIO.setup(motBDir,GPIO.OUT)
GPIO.setup(trigger,GPIO.OUT)
GPIO.setup(echo,GPIO.IN)
freq = 50
pwmMotA = GPIO.PWM(motASpeed,freq)
pwmMotB = GPIO.PWM(motBSpeed,freq)


def stop():
    """Turns the motors off, stopping the robot"""
    pwmMotA.ChangeDutyCycle(0)
    pwmMotB.ChangeDutyCycle(0)

def forward(A,B):
    """Causes the robot to drive forward in a straight line"""
    pwmMotA.ChangeDutyCycle(A)
    GPIO.output(motADir,1)
    pwmMotB.ChangeDutyCycle(B)
    GPIO.output(motBDir,1)
    
def backward(A,B):
    """Causes the robot to drive backward in a straight line"""
    # Your code here - use forward(A, B) as an example
    pwmMotA.ChangeDutyCycle(A)
    GPIO.output(motADir,0)
    pwmMotB.ChangeDutyCycle(B)
    GPIO.output(motBDir,0)
    
def right(A,B):
    """Causes the robot to keep turning to the right"""
    # Your code here - use forward(A, B) as an example
    pwmMotA.ChangeDutyCycle(A)
    GPIO.output(motADir,0)
    pwmMotB.ChangeDutyCycle(B)
    GPIO.output(motBDir,1)
def left(A,B):
    """Causes the robot to keep turning to the left"""
    # Your code here - use forward(A, B) as an example
    pwmMotA.ChangeDutyCycle(A)
    GPIO.output(motADir1)
    pwmMotB.ChangeDutyCycle(B)
    GPIO.output(motBDir,0)

def checkDistance():
    """Uses the ultrasonic sensor to check how far away objects are from the front of the robot"""
    # Set up GPIO outputs to shoot an ultrasonic pulse
    
    GPIO.output(trigger,False)      # Turn the sonic trigger off
    time.sleep(0.5)                  # Let module settle for half a second
    GPIO.output(trigger,True)          # Turn the sonic trigger on (emit a pulse)
    time.sleep(0.00001)                  # Sleep for 10 microseconds to send out a 10 microsecond pulse
    GPIO.output(trigger,False)      # Turn the sonic trigger off

    startTime = time.time()               # Record the start time
    while GPIO.input(echo)== False:     # Check if the echo pin has not received a pulse yet 
        startTime = time.time()            # Update the start time with the current time

    while GPIO.input(echo)==True:     # Check if the echo pin has received a pulse
        stopTime = time.time()             # Keep track of when the pulse returned

        
        if stopTime - startTime >= 0.04:     # Check if elapsed time is greater than 0.04 seconds - object is likely too close
            print("Hold it! You're too close for me to see.")
            stopTime = startTime         # Set stop time to start time
            break

    totTime = time.time()-startTime                  # Calculate total elapsed time from start to finish

    distance = 34326*totTime/2                 # Calculate the distance of the detected object

    
    return distance

def isNearObstacle(howNear):
    distance = checkDistance()                # Find distance of object using function from previous step
    print("isNearObstacle: " + str(distance))

    if howNear > distance:                 # Check if the obstacle is too close
        return True
    else:
        return False

def avoidObstacle(reverseTime, turnTime):
    # Back off a little
    print("Backwards")
    backward(70,70)                # You may need to experiment with backward() first to find good A and B values
    time.sleep(reverseTime)                # Reverse for a certain amount of time (in seconds)     
    stop()

    # Turn right
    print("Right")
    right(70,70)                   # You may need to experiment with right() first to find good A and B values
    # Find a time that causes for a 90 degree turn (requires some experimentation)
    time.sleep(turnTime)
    stop()

pwmMotA.start(0)
pwmMotB.start(0)

howNear = 15                        # The distance (in cm) an object must be for the robot to reverse and turn right      
reverseTime= 1                   # The time (in seconds) that the robot will reverse for
turnTime = 1                  # The time (in seconds) that the robot will turn right for

try:
    # Set trigger to False (Low)
    GPIO.output(trigger,False)

    # Allow module to settle
    time.sleep(0.1)

    # Repeat the next indented block forever
    while True:
        forward(50, 50)             # Experiment to find A and B values to make the robot go in a straight line
        time.sleep(0.01)             # Slight pause to let module settle
        if isNearObstacle(howNear):                    # Check if you are close to an obstacle using a function from step 5
            stop()
           # Avoid Obstacle - your robot should do a 90 degree turn - feel free to experiment with turnTime for this
            avoidObstacle(reverseTime,turnTime) 
### End of Step 6 ------------------------------------------------------------------------------------------------------
##
### If you press CTRL+C, cleanup and stop - do not edit
except KeyboardInterrupt:
    GPIO.cleanup()

