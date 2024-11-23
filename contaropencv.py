import cv2
import numpy as np

# Cargar la imagen
imagen = cv2.imread('pollos.jpg')

# Redimensionar la imagen para que la ventana sea más pequeña
scale_percent = 50  # Porcentaje del tamaño original
width = int(imagen.shape[1] * scale_percent / 100)
height = int(imagen.shape[0] * scale_percent / 100)
dim = (width, height)
imagen = cv2.resize(imagen, dim, interpolation=cv2.INTER_AREA)

# Convertir la imagen a espacio de color HSV
hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)

# Definir el rango de colores amarillos en HSV
lower_yellow = np.array([15, 100, 100])
upper_yellow = np.array([35, 255, 255])

# Crear una máscara para los colores amarillos
mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

# Aplicar operaciones morfológicas para limpiar la máscara
kernel = np.ones((1, 1), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Aplicar la máscara a la imagen original
res = cv2.bitwise_and(imagen, imagen, mask=mask)

# Convertir la imagen resultante a escala de grises
gris = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

# Aplicar umbralización
_, binaria = cv2.threshold(gris, 1, 255, cv2.THRESH_BINARY)

# Aplicar operaciones morfológicas adicionales para mejorar la detección de contornos
kernel = np.ones((3, 3), np.uint8)
binaria = cv2.dilate(binaria, kernel, iterations=2)
binaria = cv2.erode(binaria, kernel, iterations=2)

# Encontrar contornos
contornos, _ = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar contornos y numerar pollos
for i, contorno in enumerate(contornos):
    cv2.drawContours(imagen, [contorno], -1, (0, 255, 0), 2)
    # Obtener el centro del contorno
    M = cv2.moments(contorno)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0
    # Dibujar el número en el centro del contorno
    cv2.putText(imagen, str(i + 1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# Mostrar el número de pollos detectados
print(f"Number of chickens: {len(contornos)}")

# Mostrar la imagen con los contornos y números
cv2.imshow("Detected Chickens", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()