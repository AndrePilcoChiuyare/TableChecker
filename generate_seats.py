import cv2
import pickle

img = cv2.imread('table.jpg')

seats = []

for x in range(14):
    seat = cv2.selectROI('seat', img, False)
    cv2.destroyWindow('seat')
    seats.append(seat)

    for x, y, w, h in seats:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)

with open('seats.pkl','wb') as file:
    pickle.dump(seats, file)