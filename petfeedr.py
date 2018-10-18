import l293d
import pyrebase
import time
import datetime
import keys

#INIT
firebase = pyrebase.initialize_app(keys.config)
db = firebase.database()

#APP
try:
    motor = l293d.DC(22, 18, 16)
    while True:
        current = db.child("feeder").child("motor").get().val()
        if current == True:
            print("Feedr On...")
            motor.clockwise(duration=3)
            currentTime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            db.child("feedings").push(currentTime)
            db.child("feeder").update({"motor": False})
        else:
            print("Feedr Off..")
        time.sleep(0.5)
finally:
    l293d.cleanup()
    print("Thank You For Choosing PetFeedr!")
