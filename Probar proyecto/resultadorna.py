from __future__ import division
import cv2
import numpy as np
from PIL import Image
from os import listdir
import os
import neurolab as nl
import scipy as sp

def mostar(imagen):
    imagen = cv2.resize(imagen, (100, 50))
    cv2.imshow('tomate', imagen)
    cv2.waitKey(0)
#Encuentra el contorno de una imagen
def encontar_contorno(imagen):
    imagen = imagen.copy()
    img, contornos, jerarquia =\
        cv2.findContours(imagen, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contour_sizes = \
        [(cv2.contourArea(contorno), contorno) for contorno in contornos]
    mayor_contorno = max(contour_sizes, key=lambda x: x[0])[1]

    mascara = np.zeros(imagen.shape, np.uint8)
    cv2.drawContours(mascara, [mayor_contorno], -1, 255, -1)
    return mayor_contorno, mascara



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

# encontramos el cafe de la imagen y generamos mascaras de colores
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


#diferente funcion para imagen

def sacar_pixels(imagen):
    #sCrea los pixeles a datos matriaz
    im = Image.open(imagen)
    im = im.resize((40, 10), Image.ANTIALIAS)
    pixels = im.load
    ()

    filas, columnas = im.size
    decimales = 4
    cadena = ""
    for columna in range (columnas):
        for fila in range(filas):
            #se separan los valores RGB y se escriben en el archivo
            rojo = str(normalizar(pixels[fila,columna][0]))
            verde = str(normalizar(pixels[fila,columna][1]))
            azul = str(normalizar(pixels[fila,columna][2]))
            cadena = cadena + rojo[:rojo.find(".")+decimales] + " " + verde[:verde.find(".")+decimales] + " " + azul[:azul.find(".")+decimales] + " "

    return cadena
#normaliza datos de la matriz de una columna de imagen
def normalizar(valor):
    salida = (valor*1.)/255.
    return salida

imagen = cv2.imread("prueba2.jpg")
imagen = encontrar_cafe(imagen)
cv2.imwrite("imagenprueba.jpg",imagen)

cadena =  sacar_pixels("imagenprueba.jpg")

if(os.path.exists("datoscafe.csv")== True):
    os.remove("datoscafe.csv")

archivo_entrenamiento = open("datoscafe.csv", "a")

archivo_entrenamiento.write(cadena)
archivo_entrenamiento.close()

datos = np.matrix(sp.genfromtxt("datoscafe.csv", delimiter=" "))

print datos.shape

rna = nl.load("red-neuronal-artificial.tmt")

salida = rna.sim(datos)

maduro = salida[0][1] * 100
verde = salida[0][2] * 100

print "maduro",maduro
print "verde",verde
