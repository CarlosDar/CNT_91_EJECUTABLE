# -*- coding: utf-8 -*-
"""
Barrido logarítmico de intervalo_s y gráfica log-log de Estabilidad_Adev vs τ
"""

import CNT_9X_pendulum as CNT
import pyvisa
import numpy as np
import matplotlib.pyplot as plt

# === Inicialización del instrumento ===
rm = pyvisa.ResourceManager()
print("Available VISA resources:", rm.list_resources())
objt_prueba = CNT.CNT_frequenciometro()

# === Llamada a la función y captura de resultados ===
resultados = objt_prueba.calc_Adev_Estadistics1(
    BTB = True,
    canal='A',
    N_muestras=40,
    intervalo_captura_min=1e-4,
    intervalo_captura_max=10
    ,
    pasos=6,
    pacing_time=None,
    acoplamiento='AC',
    impedancia='Min',
    atenuacion=None,
    trigger_level=None,
    trigger_slope=None,
    filtro_Digital_PASSAbaja=None,
    filtro_Analog_PASSAbaja=None,
    guardar=False
)

# === Extracción de X (τ) e Y (Estabilidad_Adev) ===
xs = [d['intervalo_captura'] for d in resultados]
ys = [d['Estabilidad_Adev'] for d in resultados]

# (Opcional) filtrar valores None
xs_f, ys_f = [], []
for x, y in zip(xs, ys):
    if y is not None:
        xs_f.append(x)
        ys_f.append(y)

# === Gráfica log-log ===
plt.figure(figsize=(6,4))
plt.loglog(xs_f, ys_f, 'o-')
plt.xlabel('τ [s]')
plt.ylabel('Estabilidad Adev [-] ')
plt.title('Estabilidad de Allan vs τ ESTADISTICAS INTERNAS DEL CNT')
plt.grid(True, which='both', ls='--', alpha=0.5)
plt.tight_layout()
plt.show()