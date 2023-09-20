import cv2

def get_frame(video_path, frame_number):
    # Abre el video
    cap = cv2.VideoCapture(video_path)
    # Avanza hasta el frame especificado
    for i in range(frame_number):
        ret, frame = cap.read()
        if not ret:
            raise ValueError(f"El vídeo no tiene {frame_number} frames.")
    # Cierra el video
    cap.release()
    # Devuelve el frame
    return frame


# Ejemplo de uso
video_path = "prueba.mp4"

# Obtiene el frame 1500
frame = get_frame(video_path, 1500)

# Muestra el frame
cv2.imshow("table.jpg", frame)
cv2.waitKey(0)

# Guarda el frame
cv2.imwrite("table.jpg", frame)