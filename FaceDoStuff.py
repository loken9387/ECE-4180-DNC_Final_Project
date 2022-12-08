import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np 
import pickle
import RPi.GPIO as GPIO
from time import sleep
import threading
import time
import board
import busio
import adafruit_mpr121
from changeProfile import *

data_lock = threading.Lock()
lock_data = threading.Lock()

padOnOff = 0
var = 0
whoIs = 0

relay_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin, GPIO.OUT)
GPIO.output(relay_pin, GPIO.LOW)
sleep(.5)
GPIO.output(relay_pin, GPIO.HIGH)
sleep(.5)
GPIO.output(relay_pin, GPIO.LOW)
sleep(.5)
GPIO.output(relay_pin, GPIO.HIGH)

def somethingElse():
    with lock_data:
        if padOnOff == 1:
            print("I am running")
            GPIO.output(relay_pin, GPIO.HIGH)
    sleep(900)
    GPIO.output(relay_pin, GPIO.LOW)

def elseSomething():
    while True:
        with data_lock:
            if var == 1:
                dylan()
            if var == 2:
                najaah()
        sleep(300)

if __name__ == "__main__":
    with open('labels', 'rb') as f:
        dicti = pickle.load(f)
        f.close()

    camera = PiCamera()
    camera.rotation = 270
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(640, 480))


    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")

    font = cv2.FONT_HERSHEY_SIMPLEX

    thread1 = threading.Thread(target=elseSomething)
    thread2 = threading.Thread(target=somethingElse)
    #thread1.start()
    thread2.start()
    najaah()

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        frame = frame.array
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.5, minNeighbors = 5)
        for (x, y, w, h) in faces:
            roiGray = gray[y:y+h, x:x+w]

            id_, conf = recognizer.predict(roiGray)

            for name, value in dicti.items():
                if value == id_:
                    print(name)
                    print(padOnOff)
                    with data_lock:
                        if name == 'Dylan' and whoIs != 1:
                            dylan()
                            whoIs = 1
                            var = 1

            if conf < 70:
                with lock_data:
                    padOnOff = 1
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, name + str(conf), (x, y), font, 2, (0, 0 ,255), 2,cv2.LINE_AA)

            else:
                GPIO.output(relay_pin, GPIO.LOW)
                sleep(.01)
                with lock_data:
                    padOnOff = 0

        cv2.imshow('frame', frame)
        key = cv2.waitKey(1)

        rawCapture.truncate(0)

        if key == 27:
            break

    cv2.destroyAllWindows()
