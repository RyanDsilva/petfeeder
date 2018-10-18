import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

LED = 18
GPIO.setup(LED, GPIO.OUT)

try:
    while True:
        GPIO.output(LED, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED, GPIO.LOW)
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.output(LED, GPIO.LOW)
finally:
    GPIO.cleanup()

