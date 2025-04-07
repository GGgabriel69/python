import cv2
import numpy as np

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

def avancer():
    GPIO.output(GPIO_PIN_DIR_D, False)
    GPIO.output(GPIO_PIN_DIR_G, False)
    GPIO.output(GPIO_PIN_VIT_D, True)
    GPIO.output(GPIO_PIN_VIT_G, True)

def tourner_gauche():
    GPIO.output(GPIO_PIN_DIR_D, False)
    GPIO.output(GPIO_PIN_DIR_G, False)
    GPIO.output(GPIO_PIN_VIT_D, True)
    GPIO.output(GPIO_PIN_VIT_G, False)

def tourner_droite():
    GPIO.output(GPIO_PIN_DIR_D, False)
    GPIO.output(GPIO_PIN_DIR_G, True)
    GPIO.output(GPIO_PIN_VIT_D, False)
    GPIO.output(GPIO_PIN_VIT_G, True)

def stop():
    GPIO.output(GPIO_PIN_VIT_D, False)
    GPIO.output(GPIO_PIN_VIT_G, False)

def detect_red_ball_on_frame(frame):
    if frame is None or frame.size == 0:
        return None, None

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Deux plages de rouge
    lower_red1 = np.array([0, 132, 255])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    gray = cv2.bitwise_and(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
                           cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), mask=mask)
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(gray_blurred, cv2.HOUGH_GRADIENT, 1, 20,
                               param1=50, param2=30, minRadius=10, maxRadius=400)

    if circles is not None:
        circles = np.uint16(np.around(circles[0, :]))
        return circles.tolist(), frame
    else:
        return None, frame

def draw_circles_on_frame(frame, circles):
    if frame is None or frame.size == 0:
        return
    if circles is not None:
        for x, y, r in circles:
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)  # center
    cv2.imshow("Detected Red Ball", frame)

# Capture vid�o
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Erreur: impossible d?ouvrir la cam�ra.")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Erreur de lecture cam�ra.")
            break

        circles, processed_frame = detect_red_ball_on_frame(frame)
        draw_circles_on_frame(processed_frame.copy(), circles)

        if circles:
            # Utiliser la premi�re balle d�tect�e
            x, y, r = circles[0]
            frame_center = frame.shape[1] // 2

            offset = x - frame_center

            tolerance = 70  # pixels de tol�rance pour �tre "au centre"
            if abs(offset) < tolerance:
                print("Balle au centre -> avancer")
                stop()
            elif offset < -tolerance:
                print("Balle � gauche -> tourner � gauche")
                tourner_gauche()
            elif offset > tolerance:
                print("Balle � droite -> tourner � droite")
                tourner_droite()
        else:
            print("Aucune balle d�tect�e -> stop")
            stop()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    GPIO.cleanup()