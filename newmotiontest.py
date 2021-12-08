import RPi.GPIO as GPIO
from gpiozero import MotionSensor
import time
from time import sleep
from picamera import PiCamera

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

L1 = 26
L2 = 13
L3 = 1
L4 = 6

C1 = 24
C2 = 16
C3 = 23
C4 = 25

GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.setup(L3, GPIO.OUT)
GPIO.setup(L4, GPIO.OUT)

GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 

real_pass = ["1", "2", "3", "A", "4"]
password_arr = []
pass_counter = 0
passIsCorrect = False

def password(line, characters):
    global pass_counter
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        password_arr.append(characters[0])
        #print(pass_counter)
        pass_counter += 1
        sleep(0.15)
    elif(GPIO.input(C2) == 1):
        password_arr.append(characters[1])
        #print(pass_counter)
        pass_counter += 1
        sleep(0.15)
    elif(GPIO.input(C3) == 1):
        password_arr.append(characters[2])
        #print(pass_counter)
        pass_counter += 1
        sleep(0.15)
    elif(GPIO.input(C4) == 1):
        password_arr.append(characters[3])
        #print(pass_counter)
        pass_counter += 1
        sleep(0.15)
    GPIO.output(line, GPIO.LOW)

camera = PiCamera()

LED = 21
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, False)

BuzzerPin = 8

GPIO.setup(BuzzerPin, GPIO.OUT)
GPIO.output(BuzzerPin, False)

pir = MotionSensor(27)
counter = 0
# start = time.time()
# end = time.time()
imgCounter = 1
while True:
    pir.wait_for_motion()    
    start = time.time()
    print("motion detected")
    #camera.capture('image' + str(imgCounter) + '.jpg')
    while not passIsCorrect:
        
        camera.capture('image' + str(imgCounter) + '.jpg')
        while True:
    #         print("Motion Detected")
            #camera.capture('image.jpg')
            end = time.time()
            #print(counter)
            counter += 1
            
            if (end - start > 3):
                GPIO.output(LED, True)
                
            if (end - start > 20):
                GPIO.output(BuzzerPin, True)
                
            password(L1, ["1","2","3","A"])
            password(L2, ["4","5","6","B"])
            password(L3, ["7","8","9","C"])
            password(L4, ["*","0","#","D"])
            sleep(0.1)
            if pass_counter == 5:
                break
        
        if password_arr == real_pass:
            passIsCorrect = True
            break

    #             else:
    #                 passIsCorrect = False
    #                 print("was not correct")
        print(password_arr)
        password_arr.clear()
        pass_counter = 0
        #print(password_arr)
        sleep(0.2)
        imgCounter += 1
        
    print("password was correct")
    GPIO.output(BuzzerPin, False)
    GPIO.output(LED, False)
    sleep(30)
    passIsCorrect = False
    password_arr.clear()
    #     time.sleep(0.

