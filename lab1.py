import RPi.GPIO as GPIO
import time
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(27,GPIO.IN)

while True:
    GPIO.output(17,GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(17,GPIO.LOW)
    time.sleep(0.5)

    if GPIO.input(27) == GPIO.HIGH:
        print("bouton pas appuyé")
    else:
        print("bouton appuyé")
    time.sleep(1)

