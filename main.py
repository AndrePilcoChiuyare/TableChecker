import cv2
import pickle
import numpy as np

seat = []

with open('seats.pkl', 'rb') as file:
    seat = pickle.load(file)

tables = []
with open('tables.pkl', 'rb') as file:
    tables = pickle.load(file)

video = cv2.VideoCapture('prueba.mp4')
occ = [1] * len(seat)

table = [(0,1), (2,3,4,5), (6,7,8), (9,10,11,13)]
table_len = len(table)
table_occ = ['Free'] * table_len

px = 3600
while True:
    check, img = video.read()
    imgBN = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgTH = cv2.adaptiveThreshold(imgBN, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 9)
    imgMedian = cv2.medianBlur(imgTH, 1)
    kernel = np.ones((3,3), np.int8)
    imgDil = cv2.dilate(imgMedian, kernel)
    for x, y, w, h in seat:
        rec = (x, y, w, h)
        espacio = imgDil[y:y+h, x:x+w]
        count = cv2.countNonZero(espacio)

        cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
        occ[seat.index(rec)] = 1
        if count < px:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            occ[seat.index(rec)] = 0

    for x, y, w, h in tables:
        rec = (x, y, w, h)
        zeros = 0
        for j in table[tables.index(rec)]:
            if occ[j] == 0:
                zeros += 1
        if zeros == len(table[tables.index(rec)]): table_occ[tables.index(rec)] = 'Free'
        else: table_occ[tables.index(rec)] = 'Full'
        cv2.putText(img, 'Table '+ str(tables.index(rec)+1) + ': ' + str(table_occ[tables.index(rec)]), (300 * tables.index(rec) + 60, 680), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,255,255), 3)
        # cv2.putText(img, str(tables.index(rec))+ ', ' + str(occ[tables.index(rec)]) + ', ' + str(count), (x,y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
        cv2.putText(img, 'Table ' + str(tables.index(rec)+1), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,0,0), 2)
        # cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
        # if table_occ[tables.index(rec)] == 'Free':
            # cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

    cv2.imshow('video', img)
    # cv2.imshow('video TH', imgTH)
    # cv2.imshow('video Median', imgMedian)
    # cv2.imshow('video Dilatada', imgDil)
    cv2.waitKey(10)