import cv2

def get_first_frame(video_path):
    # Abre el video
    cap = cv2.VideoCapture(video_path)
    # Obtiene el primer frame
    ret, frame = cap.read()
    # Cierra el video
    cap.release()
    # Devuelve el frame
    return frame


# Ejemplo de uso
video_path = "prueba.mp4"

# Obtiene el primer frame
frame = get_first_frame(video_path)

# Muestra el frame
cv2.imshow("table.jpg", frame)
cv2.waitKey(0)

# Guarda el frame
cv2.imwrite("table.jpg", frame)