from __future__ import division
import cv2
import numpy as np
from math import cos, sin
from os import listdir


green = (0, 255)
def show(image):
    imagen = cv2.resize(image, (50, 20))
    cv2.imshow('cereza', imagen)
    cv2.waitKey(0)

def recorrer_directorio(carpeta_entrada, lista_imagenes, carpeta_salida):
    for nombre_imagen in lista_imagenes:
        imagen = cv2.imread(carpeta_entrada + "/" +nombre_imagen)
        encontrar = encontrar_cafe(imagen)
        cv2.imwrite(carpeta_salida + "/" + nombre_imagen, encontrar)

def encontar_contorno(image):
    image = image.copy()
    img, contours, hierarchy =\
        cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = \
        [(cv2.contourArea(contour), contour) for contour in contours]
    biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

    mask = np.zeros(image.shape, np.uint8)
    cv2.drawContours(mask, [biggest_contour], -1, 255, -1)
    #devuelve el mayo contorno y la mascara
    return biggest_contour, mask


#def recortar(imagen, x1, x2, y1, y2):
    #max_dimension = max(imagen.shape)
    #scale = 700/max_dimension
    #cv2.resize(imagen, None, fx=scale, fy=scale)
    #cropped = image[x1:x2, y1:y2]
    #cv2.imwrite("recorte.jpg",cropped)
    #cv2.imshow("Recorte", cropped)
    #cv2.waitKey(0)


def circle_contour(image, contour):
    imagenConElipse = image.copy()
    ellipse = cv2.fitEllipse(contour)
    print ellipse
    factor_red = 0.7
    sx = int((ellipse[1][0]*factor_red)/2)
    sy = int((ellipse[1][1]*factor_red)/2)
    x = int(ellipse[0][0]) - sy
    y = int(ellipse[0][1]) - sx
    imagenConElipse = imagenConElipse[y:(y + sx*2), x:(x + sy*2)]
    return imagenConElipse

def encontrar_cafe(imagen):
    im2 = imagen.copy()
    im3 = imagen.copy()
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2HSV)
    max_dimension = max(im2.shape)
    scale = 700/max_dimension
    im2 = cv2.resize(im2, None, fx=scale, fy=scale)
    im3 = cv2.resize(im3, None, fx=scale, fy=scale)
    image_blur = cv2.GaussianBlur(im2, (7, 7), 0)

    #asignar mascaras verdes
    verde_bajos = np.array([49,50,50])
    verde_altos = np.array([80, 255, 255])
    mask3 = cv2.inRange(image_blur, verde_bajos, verde_altos)

    #asignar mascaras rojo
    min_red = np.array([0, 100, 80])
    max_red = np.array([10, 256, 256])
    mask1 = cv2.inRange(image_blur, min_red, max_red)
    min_red2 = np.array([170, 100, 80])
    max_red2 = np.array([180, 256, 256])
    mask2 = cv2.inRange(image_blur, min_red2, max_red2)
    mask = mask1 + mask2 + mask3

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
    mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)

    big_strawberry_contour, mask_strawberries = encontar_contorno(mask_clean)

    circled = circle_contour(im3, big_strawberry_contour)
    circled= cv2.resize(circled,(100,50))
    return circled


recorrer_directorio("maduro", listdir("maduro"), "madurorecorte")
recorrer_directorio("verde",  listdir("verde"),  "verderecorte")
