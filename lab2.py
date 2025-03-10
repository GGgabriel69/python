from flask import Flask, request, jsonify
import RPi.GPIO as GPIO

#configurer le GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

app = Flask(__name__, static_folder='static')

@app.route('/button_state', methods=['GET'])
def button_state():
    state = GPIO.input(27)  #lire l'état du bouton
    return jsonify({"button_pressed":bool(state)}), 200

@app.route('/led_on', methods=['POST'])
def led_on():
    data = request.get_json()
    if data['state'] == 'on':
        GPIO.output(17, GPIO.HIGH)  #allume led
    else: 
        GPIO.output(17, GPIO.LOW)  #allume led
    return "état changé"


    #test 1


if __name__ == '__main__':
    try:
       app.run(host='0.0.0.0')
    except KeyboardInterrupt:
       GPIO.cleanup()   #nettoyer le GPIo à la fin