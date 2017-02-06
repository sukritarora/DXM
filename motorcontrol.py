import RPi.GPIO as GPIO

class Motor:
    direction = [(GPIO.HIGH, GPIO.LOW, GPIO.HIGH), (GPIO.LOW, GPIO.HIGH, GPIO.HIGH)] 
    def __init__ (self, pin_f, pin_b, pin_e):
        self.forward = pin_f
        self.backward = pin_b
        self.enable = pin_e

        GPIO.setup(self.forward, GPIO.OUT)
        GPIO.setup(self.backward, GPIO.OUT)
        GPIO.setup(self.enable, GPIO.OUT)

    def move (self, i):
        GPIO.output(self.forward, Motor.direction[i][0])
        GPIO.output(self.backward, Motor.direction[i][1])
        GPIO.output(self.enable, Motor.direction[i][2])

    def stop(self):
        GPIO.output(self.enable, GPIO.LOW)

    def done(self):
        GPIO.cleanup()


   
