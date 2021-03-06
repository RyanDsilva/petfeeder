import l293d
import pyrebase
import time
import datetime
import RPi.GPIO as GPIO
import smtplib
import INFO

# INIT

GPIO.setmode(GPIO.BOARD)
firebase = pyrebase.initialize_app(INFO.config)
db = firebase.database()

# creates SMTP session
s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
s.starttls()
# Authentication
s.login(INFO.senderEmail, INFO.senderPass)

# message to be sent
message = "You need to refill your PetFeedr storage tank!"

# APP


def rc_time(pin_to_circuit):
    count = 0

    # Output on the pin for
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)

    # Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count


try:
    motor = l293d.DC(22, 18, 16)
    while True:
        current = db.child("feeder").child("motor").get().val()
        if current == True:
            print("Feedr On...")
            motor.clockwise(duration=3)
            currentTime = datetime.datetime.fromtimestamp(
                time.time()).strftime('%Y-%m-%d %H:%M:%S')
            db.child("feedings").push(currentTime)
            db.child("feeder").update({"motor": False})
            if rc_time(7) < 2000:
                s.sendmail(INFO.senderEmail, INFO.recipientEmail, message)
                print("EMAIL SENT!")
        else:
            print("Feedr Off..")
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    l293d.cleanup()
    GPIO.cleanup()
    print("Thank You For Choosing PetFeedr!")
