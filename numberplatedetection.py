# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 22:42:25 2021

@author: Nirav
"""

import numpy as np
import cv2
import pytesseract 

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

cascade = cv2.CascadeClassifier("haarcascade_russian_plate_number.xml")

img = cv2.imread("img6_2.2.jpg")

img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
nplate = cascade.detectMultiScale(img_gray, 1.3, 5)

for (x,y,w,h) in nplate:
    print("hii")
    a,b = (int(0.02*img.shape[0]),int(0.025*img.shape[1]))
    plate = img[y+a:y+h-a, x+b:x+w-b, :]
    
    
    kernal = np.ones((1, 1), np.uint8)
    plate = cv2.dilate(plate, kernal, iterations=1)
    plate = cv2.erode(plate,kernal,iterations=1)
    plate_gray = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    (thresh, plate) = cv2.threshold(plate_gray,127,255,cv2.THRESH_BINARY)
    read = pytesseract.image_to_string(plate)
    print(read)
    read = ''.join(e for e in read if e.isalnum())
    print(read)
    cv2.rectangle(img, (x,y), (x+w, y+h), (51,51,255), 2)
    cv2.rectangle(img, (x,y-40), (x+w, y), (51,51,255),-1)
    cv2.putText(img, read ,(x,y-10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0))
    cv2.imshow('Plate',plate)
    
cv2.imshow('result',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
    
    