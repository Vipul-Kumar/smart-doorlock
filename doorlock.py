from flask import Flask,redirect
import os

app = Flask(__name__)
import RPi.GPIO as GPIO
import time

servo = 22

GPIO.setmode(GPIO.BOARD)

GPIO.setup(servo, GPIO.OUT)
# in servo motor,
# 1ms pulse for 0 degree (LEFT)
# 1.5ms pulse for 90 degree (MIDDLE)
# 2ms pulse for 180 degree (RIGHT)

# so for 50hz, one frequency is 20ms
# duty cycle for 0 degree = (1/20)*100 = 5%
# duty cycle for 90 degree = (1.5/20)*100 = 7.5%
# duty cycle for 180 degree = (2/20)*100 = 10%

p = GPIO.PWM(servo, 50)  # 50hz frequency

p.start(12.5)  # starting duty cycle ( it set the servo to 0 degree )
print(" About to run while loop")


def SetAngle(angle, servo, pwm):
    duty = angle / 18 + 2
    GPIO.output(servo, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1.2)
    GPIO.output(servo, False)
    pwm.ChangeDutyCycle(0)

@app.route('/')
def video():
    html_obj = '''
    <div>
	            <h2 style='font-size:120px;text-align:center; position:relative; top: 50px;'>Door Locked</h2>
             <div align="center">
                <p align:center;><iframe x style='float:bottom;position:relative;top:30px;height:500px; width:70%' src='http://192.168.0.27:8081/'></iframe></p>
                </div>
	            <p style='text-align:center;'>
		        <a style='font-size:100px; text-decoration:none; text-align:center; position:relative;top:100px;' href='/unlock'>Unlock</a><br><br>
				<a style='font-size:100px; text-decoration:none; text-align:center; position:relative;top:150px;' href='/lock'>Lock</a>
	            <p>
    </div>'''
    # return redirect("http://192.168.0.27:8081/", code=302)
    return html_obj


@app.route('/lock')
def lock():
    SetAngle(0, servo, p)
    time.sleep(1)
    html_obj = '''
    <div>
	            <h2 style='font-size:120px;text-align:center; position:relative; top: 50px;'>Door Locked</h2>
             <div align="center">
                <p align:center;><iframe x style='float:bottom;position:relative;top:30px;height:500px; width:70%' src='http://192.168.0.27:8081/'></iframe></p>
                </div>
	            <p style='text-align:center;'>
		        <a style='font-size:100px; text-decoration:none; text-align:center; position:relative;top:100px;' href='/unlock'>Unlock</a><br><br>
				<a style='font-size:100px; text-decoration:none; text-align:center; position:relative;top:150px;' href='/lock'>Lock</a>
	            <p>
    </div>'''
    # return redirect("http://192.168.0.27:8081/", code=302)
    return html_obj

@app.route('/unlock')
def unlock():
    SetAngle(180, servo, p)
    time.sleep(1)
    html_obj = '''
    <div>
	            <h2 style='font-size:120px;text-align:center; position:relative; top: 50px;'>Door Locked</h2>
             <div align="center">
                <p align:center;><iframe x style='float:bottom;position:relative;top:30px;height:500px; width:70%' src='http://192.168.0.27:8081/'></iframe></p>
                </div>
	            <p style='text-align:center;'>
		        <a style='font-size:100px; text-decoration:none; text-align:center; position:relative;top:100px;' href='/unlock'>Unlock</a><br><br>
				<a style='font-size:100px; text-decoration:none; text-align:center; position:relative;top:150px;' href='/lock'>Lock</a>
	            <p>
    </div>'''
    # return redirect("http://192.168.0.27:8081/", code=302)
    return html_obj
try:
    app.run(host='0.0.0.0', port=8090)
    print("server started on port 8090")
except KeyboardInterrupt:
    # SetAngle(180, servo, p)
    my_cmd = "sudo service motion stop"
    os.system(my_cmd)
    GPIO.cleanup()
