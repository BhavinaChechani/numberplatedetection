# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 23:49:25 2021

@author: Nirav
"""

#task 2.2
#Implement the contour detection code for rectangular license plate (day 4 and 5)
#team B

import cv2
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
# Reading image file
image = cv2.imread('img6_2.2.jpg')
dst=cv2.getPerspectiveTransform(image,dst)

image = imutils.resize(image, width=500)

# Display the original image
cv2.imshow("Original Image", image)
cv2.waitKey(0)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Grayscale Conversion", gray)
cv2.waitKey(0)

gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imshow("Bilateral Filter", gray)
cv2.waitKey(0)

# Finding Edges
edged = cv2.Canny(gray, 140, 200)
cv2.imshow("Canny Edges", edged)
cv2.waitKey(0)

# Finding contours
cnts, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# Creating copy of original image
img1 = image.copy()
cv2.drawContours(img1, cnts, -1, (0,255,0), 3)
cv2.imshow("All Contours", img1)
cv2.waitKey(0)

cnts=sorted(cnts, key = cv2.contourArea, reverse = True)[:20]
PlateCnt = None

img2 = image.copy()
cv2.drawContours(img2, cnts, -1, (0,255,0), 3)
cv2.imshow("20 Contours", img2)
cv2.waitKey(0)

for contour in cnts:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        hull = cv2.convexHull(approx, returnPoints=False)
        print(hull)
        if len(hull) == 4:  #the contour with 4 corners
            PlateCnt = approx #approx Number Plate Contour
            print("hii")
            print(PlateCnt)

            x, y, w, h = cv2.boundingRect(contour)
            new_img = gray[y:y + h, x:x + w]
            cv2.imwrite('image1.png',new_img)
            break


cv2.drawContours(image, [PlateCnt], -1, (0, 255, 0), 3)
cv2.imshow("Final Image With Number Plate Detected", image)
cv2.waitKey(0)

cv2.imshow("Cropped Image ",new_img)

text = pytesseract.image_to_string(new_img,config='--psm 6')
text=''.join(e for e in text if e.isalnum())
print("Number is :", text)

cv2.waitKey(0)
cv2.destroyAllWindows()