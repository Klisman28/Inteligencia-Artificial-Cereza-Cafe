                                                                                                                            from PIL import Image
from os import listdir


def sacar_pixels(direccion, archivo):
    #se abre la imagen
    im = Image.open(direccion)
    im = im.resize((50, 10), Image.ANTIALIAS)
    #im.save("hola.jpg")
    #lectura de pixels
    pixels = im.load()
    #se abre el archivo para lectura escritura
    archivo_entrenamiento = open(archivo, "a")
    filas, columnas = im.size
    for columna in range (columnas):
        for fila in range(filas):
            #se separan los valores RGB y se escriben en el archivo
            cadena = str(pixels[fila,columna][0]) + " " + str(pixels[fila,columna][1]) + " " + str(pixels[fila,columna][2]) + " "
            archivo_entrenamiento.write(cadena)

    #pix[x,y] = value # Set the RGBA Value of the image (tuple)
    archivo_entrenamiento.write("\n")
    archivo_entrenamiento.close()

def recorrer_directorio(carpeta_entrada, lista_imagenes, archivo):
    for nombre_imagen in lista_imagenes:
        sacar_pixels(carpeta_entrada + "/" +nombre_imagen, archivo)

recorrer_directorio("madurorecorte", listdir("./madurorecorte"), "maduro.ccv")
recorrer_directorio("verderecorte",  listdir("./verderecorte"),  "maduro.ccv")
