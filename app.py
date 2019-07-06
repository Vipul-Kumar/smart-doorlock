from flask import Flask,redirect, render_template
import os
import commands

app = Flask(__name__)
import RPi.GPIO as GPIO
import time

servo = 22

#GPIO.setmode(GPIO.BOARD)

#GPIO.setup(servo, GPIO.OUT)
# in servo motor,
# 1ms pulse for 0 degree (LEFT)
# 1.5ms pulse for 90 degree (MIDDLE)
# 2ms pulse for 180 degree (RIGHT)

# so for 50hz, one frequency is 20ms
# duty cycle for 0 degree = (1/20)*100 = 5%
# duty cycle for 90 degree = (1.5/20)*100 = 7.5%
# duty cycle for 180 degree = (2/20)*100 = 10%

#p = GPIO.PWM(servo, 50)  # 50hz frequency

#p.start(0)  # starting duty cycle ( it set the servo to 0 degree )
print("Server Ready!")
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo, GPIO.OUT)
pwm = GPIO.PWM(servo, 50)
pwm.start(0)
def SetAngle(angle, servo):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo, GPIO.OUT)
    pwm = GPIO.PWM(servo, 50)
    pwm.start(0)
    print("in setAngle Function with value = "+str(angle))
    print("Value of servo " + str(servo))
    duty = angle / 18 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1.2)
    GPIO.output(servo, False)
    #pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()

last_angle = 50

hostname = commands.getoutput('hostname -I')
web_cam_stream_url = 'http://'+hostname.strip()+':8081/'
homepage = 'http://'+hostname.strip()+'/'

@app.route('/')
def video():
    global last_angle
    global web_cam_stream_url
    with open('lock_status.txt','r') as f:
      status = f.read()
    
    print(web_cam_stream_url)
      
    print("in root node")
    return render_template('homepage.html', status = status, webcam_url = web_cam_stream_url)
    


@app.route('/lock')
def lock():
    global last_angle
    global homepage
    print("In lock fn")
    #SetAngle(0, servo)
    last_angle = 0
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(22, GPIO.OUT)
    pwm = GPIO.PWM(22, 50)
    pwm.start(2.5)
    #print("in setAngle Function with value = "+str(angle))
    #print("Value of servo " + str(servo))
    #duty = angle / 18 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(2.5)
    time.sleep(2)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()
    
    
    
    time.sleep(1)
    with open('lock_status.txt','w+') as f:
      f.write("Locked")
    return redirect(homepage, code=302)
    # return html_obj
    #return "Door Locked"

@app.route('/unlock')
def unlock():
    global last_angle
    global homepage
    print("in unlock fn")
    #SetAngle(180, servo)
    last_angle = 180
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo, GPIO.OUT)
    pwm = GPIO.PWM(servo, 50)
    pwm.start(12.5)
    #print("in setAngle Function with value = "+str(angle))
    #print("Value of servo " + str(servo))
    #duty = angle / 18 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(12.5)
    time.sleep(1.2)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)
    pwm.stop()    
    
    time.sleep(1)
    with open('lock_status.txt','w+') as f:
      f.write("Unlocked")
    return redirect(homepage, code=302)
    # return html_obj
    #return "Door Unlocked"
print("End Block")
with open('lock_status.txt','a+') as f:
      pass

GPIO.output(servo, False)
pwm.ChangeDutyCycle(0)
pwm.stop()
GPIO.cleanup()
if __name__ == '__main__':
   app.run()
#try:
 #   app.run(host='0.0.0.0', port=8091)
    #app.run(debug=True)
    #print("server started on port 8090")
#except KeyboardInterrupt:
    # SetAngle(180, servo, p)
 #   my_cmd = "sudo service motion stop"
  #  os.system(my_cmd)
#GPIO.cleanup()
