from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
import imutils
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

def contadoresInterfaz(seatFree, seatOcuppied, tableFree, tableOcuppied, numTablesF, numTablesO):

    seatsFree.config(text = f"Seats Free: {seatFree}")
    seatsOcuppied.config(text = f"Seats Occupied: {seatOcuppied}")
    tablesFree.config(text = f"Tables Free: {tableFree} {numTablesF}")
    tablesOcuppied.config(text = f"Tables Occupied: {tableOcuppied} {numTablesO}")
    

def reproducir_video():

    global cap
    check, img = cap.read()
    if check:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        imgBN = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgTH = cv2.adaptiveThreshold(imgBN, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 15, 9)
        imgMedian = cv2.medianBlur(imgTH, 1)
        kernel = np.ones((3,3), np.int8)
        imgDil = cv2.dilate(imgMedian, kernel)
        
        seatF = 0
        seatO = 0

        for x, y, w, h in seat:
            rec = (x, y, w, h)
            espacio = imgDil[y:y+h, x:x+w]
            count = cv2.countNonZero(espacio)
            # cv2.putText(img, str(seat.index(rec))+ ', ' + str(occ[seat.index(rec)]) + ', ' + str(count), (x,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            # cv2.putText(img, 'Seat ' + str(seat.index(rec)+1), (x+10,y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (0,0,0), 2)
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            occ[seat.index(rec)] = 1
            if count < px:
                seatF = seatF + 1
                cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
                occ[seat.index(rec)] = 0
            else: 
                seatO = seatO + 1

        tableF = 0
        tableO = 0
        strTablesF = '['
        strTablesO = '['
        for x, y, w, h in tables:
            rec = (x, y, w, h)
            zeros = 0
            for j in table[tables.index(rec)]:
                if occ[j] == 0:
                    zeros += 1
            if zeros == len(table[tables.index(rec)]): 
                tableF = tableF + 1
                table_occ[tables.index(rec)] = 'Free'
                strTablesF = strTablesF + str(tables.index(rec)+1) + ' '
                #cv2.putText(img, 'Table '+ str(tables.index(rec)+1) + ': ' + str(table_occ[tables.index(rec)]), (300 * tables.index(rec) + 60, 680), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,0), 3)
                cv2.putText(img, 'Table ' + str(tables.index(rec)+1), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
            else:
                tableO = tableO + 1 
                table_occ[tables.index(rec)] = 'Full'
                strTablesO = strTablesO + str(tables.index(rec)+1) + ' '
                #cv2.putText(img, 'Table '+ str(tables.index(rec)+1) + ': ' + str(table_occ[tables.index(rec)]), (300 * tables.index(rec) + 60, 680), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255,0,0), 3)
                cv2.putText(img, 'Table ' + str(tables.index(rec)+1), (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

            # cv2.putText(img, str(tables.index(rec))+ ', ' + str(occ[tables.index(rec)]) + ', ' + str(count), (x,y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)
            # cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255), 2)
            # if table_occ[tables.index(rec)] == 'Free':
                # cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
        
        strTablesF = strTablesF[:-1]
        strTablesO = strTablesO[:-1]
        if len(strTablesF)>0: strTablesF=strTablesF+']'
        if len(strTablesO)>0: strTablesO=strTablesO+']'

        contadoresInterfaz(seatF,seatO,tableF,tableO, strTablesF, strTablesO)

        imagen = Image.fromarray(img)
        img1 = ImageTk.PhotoImage(image=imagen)
        lblVideo.configure(image=img1)
        lblVideo.image = img1
        lblVideo.after(10, reproducir_video)



#Video
cap = cv2.VideoCapture('prueba.mp4')

root = Tk()
root.title = "Procesamiento de Imagene - Tabajo Parcial"
#root.attributes('-fullscreen', True)

#Boton para empezar a reproducir el video
btnVisualizar = Button(root, text="Reproducir video", command=reproducir_video)
btnVisualizar.grid(column=0, row=1, padx=10, pady=5)

#Texto
seatsFree = Label(root)
seatsFree.grid(column=1, row = 0, columnspan=1)
seatsFree.config(fg='blue',font=("Arial", 18))

seatsOcuppied = Label(root)
seatsOcuppied.grid(column=2, row = 0, columnspan=1)
seatsOcuppied.config(fg='red',font=("Arial", 18))

tablesFree = Label(root)
tablesFree.grid(column=3, row = 0, columnspan=1)
tablesFree.config(fg='blue',font=("Arial", 18))

tablesOcuppied = Label(root)
tablesOcuppied.grid(column=4, row = 0, columnspan=1)
tablesOcuppied.config(fg='red',font=("Arial", 18))


#Contenedor de video
lblVideo = Label(root)
lblVideo.grid(column = 0, row=1, columnspan = 5)

root.mainloop()