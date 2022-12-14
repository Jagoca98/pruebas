from calendar import EPOCH
from tabnanny import verbose
import tensorflow as tf
import numpy as np

celsius = np.array([-40, -10, 0, 8, 15, 22, 38], dtype=float)
fahrenheit = np.array([-40, 14, 32, 46, 59, 72, 100], dtype=float)


oculta1 = tf.keras.layers.Dense(units=3, input_shape=[1])
oculta2 = tf.keras.layers.Dense(units=3)
salida = tf.keras.layers.Dense(units=1)
modelo = tf.keras.Sequential([oculta1, oculta2, salida])

modelo.compile(
    optimizer = tf.keras.optimizers.Adam(0.1), 
    loss = 'mean_squared_error'
)

print("Comenzando a entrenar...")
historial = modelo.fit(celsius, fahrenheit, epochs=60, verbose=False)

import matplotlib.pyplot as plt
plt.xlabel("# Epoca")
plt.ylabel("Magnitud de perdida")
plt.plot(historial.history["loss"])
plt.show()

print("Hagamos una prediccion")
resultado = modelo.predict([100.0])
print("El resultado es " + str(resultado) + "farhrenheit")


print("Variables internas del modelo")
print(oculta1.get_weights())
print(oculta2.get_weights())
print(salida.get_weights())
