import neurolab as nl
import numpy as np
import scipy as sp


datos = np.matrix(sp.genfromtxt("datos-entrenamiento.csv", delimiter=" "))


entrada = datos[:,:-3]
objetivo = datos[:,-3:]


maxmin = np.matrix([[ -5, 5] for i in range(len(entrada[1,:].T))])

capa_entrada = entrada.shape[0]
capa_oculta1 = int(capa_entrada*0.6)
capa_oculta2 = int(capa_entrada*0.33)
capa_salida = 3


# Crear red neuronal con 2 capas
rna = nl.net.newff(maxmin, [ capa_entrada, capa_oculta1, capa_oculta2, capa_salida])

#Cambio de algoritmo a back progation simple
rna.trainf = nl.train.train_gd

#Datos para la RNAd
error = rna.train(entrada, objetivo, epochs=75000, show=10, goal=0.02)


#rna.save("neurona.tmt")
# Simulacion RNA
rna.save("red-neuronal-artificial.tmt")
salida = rna.sim(entrada)


#print rna.layers[0].np['w']
#print rna.layers[1].np['w']

print salida