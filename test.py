# print("Computer Vision and Deep Learning in IoT")
# print("Farshid PirahanSiah")
# print("05.03.21")
import os
# for i in range(1,100):
#     if (i%3==0 and i%5==0):
#         print(str(i) + " =  3 and 5 ")    
#     elif (i%3==0):
#         print(str(i) + " = 3")
#     elif (i%5==0):
#         print(str(i) + " = 5")
#number=[1,2,3,4,5]
#print(list(filter(lambda number:number%2==0,number )))

import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):# 2 reduce noise: gaussian blur # 3 edge detection Canny
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)    
    blur=cv2.GaussianBlur(gray,(5,5),0)    
    low_threshold=50
    high_threshold=150
    canny=cv2.Canny(image,low_threshold,high_threshold)
    return canny

def region_of_interest(image):
    height=image.shape[0]
    polygons=np.array([ [ (200,height),(1100,height),(550,250)  ] ])
    mask=np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image

def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            #print(line) # x1,y1,x2,y2
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image
def make_coordinates(image,line_parameters):
    slope,intercept=line_parameters
    y1=image.shape[0]
    y2=int(y1*(3/5))
    x1=int( (y1-intercept)/slope)
    x2=int( (y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])



def average_slope_intercept(image,lines):
    left_fit=[]
    right_fit=[]
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters=np.polyfit((x1,x2),(y1,y2),1)
        slope=parameters[0]
        intercept=parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average=np.average(left_fit,axis=0)
    right_fit_average=np.average(right_fit,axis=0)
    left_line=make_coordinates(image,left_fit_average)
    right_line=make_coordinates(image,right_fit_average)
    return np.array([left_line,right_line])








image=cv2.imread('image/test_image.jpg')
#C:\code\Computer_Vison_IoT\Image\test_image.jpg
# 1 Gray
lane_image=np.copy(image)
canny_image= canny(lane_image)
# 4 select region
#plt.imshow(canny)
#plt.show()
cropped_image=region_of_interest(canny_image)
# 5 bitwise
#masked_image=cv2.bitwise_and(canny,roi)
# 6 Hough Transflorm

lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
#9
averaged_lines=average_slope_intercept(lane_image,lines)

line_image=display_lines(lane_image,averaged_lines)

combo_image=cv2.addWeighted(lane_image,0.8,line_image,1,1)


cv2.imshow('result',combo_image)
cv2.waitKey()








