from PIL import Image
from os import listdir

def sacar_pixels(direccion, entrada):
    #se abre la imagen
    im = Image.open(direccion)
    im = im.resize((100, 50), Image.ANTIALIAS)
    #im.save("hola.jpg")
    #lectura de pixels
    pixels = im.load()
    #se abre el archivo para lectura escritura
    archivo_entrenamiento = open("datos-entrenamiento.csv", "a")
    filas, columnas = im.size
    for columna in range (columnas):
        for fila in range(filas):
            #se separan los valores RGB y se escriben en el archivo
            rojo = str(normalizar(pixels[fila,columna][0]))
            verde = str(normalizar(pixels[fila,columna][1]))
            azul = str(normalizar(pixels[fila,columna][2]))
            cadena = rojo[:rojo.find(".")+3] + " " + verde[:verde.find(".")+3] + " " + azul[:azul.find(".")+3] + " "
            archivo_entrenamiento.write(cadena)

    #pix[x,y] = value # Set the RGBA Value of the image (tuple) 
    archivo_entrenamiento.write(entrada)
    archivo_entrenamiento.write("\n")
    archivo_entrenamiento.close()

def recorrer_directorio(carpeta_entrada, lista_imagenes, salida):
    for nombre_imagen in lista_imagenes:
        sacar_pixels(carpeta_entrada + "/" +nombre_imagen, salida)

def normalizar(valor):
    salida = (valor*1.)/255.
    return salida
    


recorrer_directorio("madurorecorte", listdir("./madurorecorte"), "1 0 0 ")
recorrer_directorio("verderecorte",  listdir("./verderecorte"), "0 1 0 ")
