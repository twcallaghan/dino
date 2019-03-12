import cv2
import numpy as np
import time

#############################################

# CURRENTLY WORKING ENOUGH TO THE POINT THAT I AM ATTEMPTING INTEGRATION WITH DINOSTART

#############################################

# capturing video through webcam
cap = cv2.VideoCapture(0)
starttime = time.time()
heights = []
avgavailable = False
contourbool = False
while (1):
    _, img = cap.read()

    # converting frame(img i.e BGR) to HSV (hue-saturation-value)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # defining the range of red color
    #red_lower = np.array([136, 87, 111], np.uint8)
    #red_upper = np.array([180, 255, 255], np.uint8)

    #orange_lower = np.array([255, 127, 80], np.uint8)
    #orange_upper = np.array([255, 195, 0], np.uint8)
    '''
    # defining the Range of Blue color
    blue_lower = np.array([99, 115, 150], np.uint8)
    blue_upper = np.array([110, 255, 255], np.uint8)
    '''
    # defining the Range of yellow color
    yellow_lower = np.array([22, 60, 200], np.uint8)
    yellow_upper = np.array([60, 255, 255], np.uint8)

    # finding the range of red,blue and yellow color in the image
    #red = cv2.inRange(hsv, red_lower, red_upper)
    #orange = cv2.inRange(hsv, orange_lower, orange_upper)
    #blue = cv2.inRange(hsv, blue_lower, blue_upper)
    yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), "uint8")

    #red = cv2.dilate(red, kernal)
    #res = cv2.bitwise_and(img, img, mask=red)

    #orange = cv2.dilate(orange, kernal)
    #res1 = cv2.bitwise_and(img, img, mask=orange)

    #blue = cv2.dilate(blue, kernal)
    #res1 = cv2.bitwise_and(img, img, mask=blue)

    yellow = cv2.dilate(yellow, kernal)
    res2 = cv2.bitwise_and(img, img, mask=yellow)

    # Tracking the Red Color
    #(_, contours, hierarchy) = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    '''
    for pic, contour in enumerate(contours):
        endtime = time.time()
        area = cv2.contourArea(contour)
        avgavailable = False
        global contourbool
        contourbool = False
        if endtime - starttime > 5:
            if (area > 600):
                global y
                x, y, w, h = cv2.boundingRect(contour)
                contourbool = True
                #if y < 150:
                    #print 'mouth?'
                #    break
                #else:
                    #print y
                heights.append(y)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, "RED color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
                #print y
            if len(heights) % 40 == 0:
                print 'I NOW HAVE ENOUGH POINTS: GO!'
                a = 0
                totalheight = 0
                avgheight = 0.0
                for height in heights:
                    totalheight += heights[a]
                    a += 1
                    avgheight = totalheight/a
                #print 'average height ' + str(avgheight)
                avgavailable = True

            if avgavailable == True and contourbool == True and y > avgheight + 75:
                print 'duck'
                print 'y ' + str(y)
                print 'average height ' + str(avgheight)
            if avgavailable == True and contourbool == True and  y < avgheight - 75:
                print 'jump'
                print 'y ' + str(y)
                print 'average height ' + str(avgheight)10
    '''
    # Tracking the yellow Color
    (_, contours, hierarchy) = cv2.findContours(yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (area > 7500):
            contourbool = True
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "yellow  color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
            heights.append(y)
            #print y
        if len(heights) % 75 == 0 and len(heights) != 0:
            print 'I NOW HAVE ENOUGH POINTS: GO!'
            a = 0
            totalheight = 0
            avgheight = 0
            for height in heights:
                totalheight += heights[a]
                a += 1
                avgheight = totalheight / a
            avgavailable = True
        if avgavailable == True and contourbool == True and y > avgheight + 75:
            print 'duck'
            print 'y ' + str(y)
            print 'average height ' + str(avgheight)
        if avgavailable == True and contourbool == True and y < avgheight - 75:
            print 'jump'
            print 'y ' + str(y)
            print 'average height ' + str(avgheight)
    cv2.imshow("Color Tracking", img)
    # cv2.imshow("red",res)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        break