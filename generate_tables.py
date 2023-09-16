import cv2
import pickle

img = cv2.imread('table.png')

tables = []

for x in range(4):
    table = cv2.selectROI('table', img, False)
    cv2.destroyWindow('table')
    tables.append(table)

    for x, y, w, h in tables:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255,0,0), 2)

with open('tables.pkl','wb') as file:
    pickle.dump(tables, file)