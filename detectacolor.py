import cv2
import numpy as np

def nothing(x):
    pass

# Cargar la imagen
imagen = cv2.imread('pollos.jpg')
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Crear una ventana
cv2.namedWindow('Trackbars')

# Crear trackbars para ajustar los valores de HSV
cv2.createTrackbar('Lower Hue', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('Upper Hue', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('Lower Saturation', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Upper Saturation', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Lower Value', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Upper Value', 'Trackbars', 255, 255, nothing)

while True:
    # Obtener los valores actuales de las trackbars
    lower_hue = cv2.getTrackbarPos('Lower Hue', 'Trackbars')
    upper_hue = cv2.getTrackbarPos('Upper Hue', 'Trackbars')
    lower_saturation = cv2.getTrackbarPos('Lower Saturation', 'Trackbars')
    upper_saturation = cv2.getTrackbarPos('Upper Saturation', 'Trackbars')
    lower_value = cv2.getTrackbarPos('Lower Value', 'Trackbars')
    upper_value = cv2.getTrackbarPos('Upper Value', 'Trackbars')

    # Definir el rango de colores amarillos en HSV
    lower_yellow = np.array([lower_hue, lower_saturation, lower_value])
    upper_yellow = np.array([upper_hue, upper_saturation, upper_value])

    # Crear una máscara para los colores amarillos
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Aplicar la máscara a la imagen original
    res = cv2.bitwise_and(imagen, imagen, mask=mask)

    # Mostrar la imagen resultante
    cv2.imshow('Original', imagen)
    cv2.imshow('Mask', mask)
    cv2.imshow('Result', res)

    # Salir del bucle con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()