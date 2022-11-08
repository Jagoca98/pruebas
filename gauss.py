import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  
from scipy.stats import multivariate_normal

def Gaussian_Distribution(N=2, M=1000, m=0, sigma=1):
    '''
    Parameters
    ----------
         Dimensión N
         M número de muestras
         m media muestral
         sigma: varianza de la muestra
    
    Returns
    -------
         forma de datos (M, N), M muestras de distribución gaussiana N-dimensional
         Función de densidad de probabilidad de distribución gaussiana gaussiana
    '''
    mean = np.zeros(N) + m  # Matriz media, la media de cada dimensión es m
    cov = np.eye(N) * sigma  # Matriz de covarianza, la varianza de cada dimensión es sigma

    # Genere datos de distribución gaussiana N-dimensional
    data = np.random.multivariate_normal(mean, cov, M)
    # Función de densidad de probabilidad de distribución gaussiana de datos N-dimensionales
    Gaussian = multivariate_normal(mean=mean, cov=cov)
    
    return data, Gaussian

M = 1000
data, Gaussian = Gaussian_Distribution(N=2, M=M, sigma=0.1)
# Generar un plano de cuadrícula bidimensional
X, Y = np.meshgrid(np.linspace(-1,1,M), np.linspace(-1,1,M))
# Datos de coordenadas bidimensionales
d = np.dstack([X,Y])
# Calcule la probabilidad gaussiana conjunta bidimensional
Z = Gaussian.pdf(d).reshape(M,M)


'' 'Mapa de distribución de probabilidad binaria gaussiana' ''
fig = plt.figure(figsize=(6,4))
ax = Axes3D(fig)
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='seismic', alpha=0.8)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()