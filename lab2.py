from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

#GPIO
import RPi.GPIO as GPIO
GPIO_PIN_DIR_D = 27
GPIO_PIN_DIR_G= 17
GPIO_PIN_VIT_D = 22
GPIO_PIN_VIT_G = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN_DIR_D, GPIO.OUT)
GPIO.setup(GPIO_PIN_DIR_G, GPIO.OUT)
GPIO.setup(GPIO_PIN_VIT_D, GPIO.OUT)
GPIO.setup(GPIO_PIN_VIT_G, GPIO.OUT)


#Flask
app = Flask(__name__)
CORS(app)
#Flask page d'accueil
@app.route('/')
def index():
    return render_template('index.html')
 
 #Flask allumer eteindre DEL
@app.route('/del', methods=['POST'])
def modif_vitesse_direction():
        isDirDOn = request.json['isDirDOn']
        if isDirDOn:
            GPIO.output(GPIO_PIN_DIR_D, GPIO.HIGH)
        else:
            GPIO.output(GPIO_PIN_DIR_D, GPIO.LOW)
        
        isDirGOn = request.json['isDirGOn']
        if isDirGOn:
            GPIO.output(GPIO_PIN_DIR_G, GPIO.HIGH)
        else:
            GPIO.output(GPIO_PIN_DIR_G, GPIO.LOW)

        isVitDOn = request.json['isVitDOn']
        if isVitDOn:
            GPIO.output(GPIO_PIN_VIT_D, GPIO.HIGH)
        else:
            GPIO.output(GPIO_PIN_VIT_D, GPIO.LOW)

        isVitGOn = request.json['isVitGOn']
        if isVitGOn:
            GPIO.output(GPIO_PIN_VIT_G, GPIO.HIGH)
        else:
            GPIO.output(GPIO_PIN_VIT_G, GPIO.LOW)
        return jsonify({'message': 'directions et vitesses updated successfully'})

#Flask lire bouton
@app.route('/bouton', methods=['GET'])
def lire_bouton():
    isButton1On = True if GPIO.input(GPIO_PIN_BUTTON) else False
    return jsonify({'isButton1On': isButton1On})

if __name__ == '__main__':
    app.run(host='0.0.0.0')
