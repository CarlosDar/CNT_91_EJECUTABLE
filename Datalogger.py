import CNT_9X_pendulum as CNT
import pyvisa
import numpy as np
import matplotlib.pyplot as plt


""" ****************************** DESCUBRIR RECURSOS DISPONIBLES AL USUARIO *************************** """


rm = pyvisa.ResourceManager()
resources = rm.list_resources()
print("Available VISA resources:", resources)

""" ****************************** EL USUARIO INTRODUCE EL ID DEL DISPOSITIVO *************************** """

Address_dispositivo = 'GPIB0::10::INSTR'
Num_dispositivo = 0

""" ****************************** CONEXIÓN CON EL DISPOSITIVO *************************** """

# 1. Descubrir recursos VISA disponibles

if not resources:
    raise RuntimeError("No se encontraron recursos VISA. Verifica la conexión GPIB/USB.")
# 2. Abrir el primer dispositivo de la lista
dev = rm.open_resource(resources[Num_dispositivo])
print(f"Conectado a: {resources[Num_dispositivo]}")
# 3. Instanciar tu frecuencímetro y asignar el device handle
objt_prueba = CNT.CNT_frequenciometro(Address_dispositivo)
objt_prueba.dev = dev





""" ****************************** SELECCION DE LA CONFIGURACIÓN POR EL USUARIO *************************** """

## Sugirimos los parametros por defecto y se puede desplegar para elegir el rango o boleano dependiendo
canal='1'
intervalo_s=1E-3
acoplamiento='DC'
impedancia='MIN'
atenuacion=1
trigger_level=None
trigger_slope='NEG'
filtro_Digital_PASSAbaja='200000'
filtro_Analog_PASSAbaja=True

canales = {'A': 'A', 'B': 'B', '1': 'A', '2': 'B'}
ch = str(canal).upper()
if ch not in canales:
    raise ValueError("El canal debe ser 'A', 'B', 1 o 2")
canal_cmd = canales[ch]

""" ****************************** CONFIGURACIÓN DEL DISPOSITIVO *************************** """

ruta = objt_prueba.configurar_dispositivo(
    canal=canal,
    intervalo_s=intervalo_s,
    acoplamiento=acoplamiento,
    impedancia=impedancia,
    atenuacion=atenuacion,
    trigger_level=trigger_level,
    trigger_slope=trigger_slope,
    filtro_Digital_PASSAbaja=filtro_Digital_PASSAbaja,
    filtro_Analog_PASSAbaja=filtro_Analog_PASSAbaja
)

""" ****************************** BOTÓN START/STOP MEDICIÓN CONTINUA *************************** """
# si el usuario le da a start comienza las medidas, sino esperamos
tiempo_espera = objt_prueba.start_continuous_measurement(intervalo_s=2E-4, canal='A')

""" ****************************** Realizamos extracciones Mediciónes de Frecuencias *************************** """
print("Iniciando medición continua (Ctrl+C para parar)...")
try:
    while True:
        frecs, ts = objt_prueba.fetch_continuous_samples(
            n_muestras=10,
            tiempo_espera=tiempo_espera
        )
        for f, t in zip(frecs, ts):
            objt_prueba.append_measurement(f, t)
            print(f"Muestra: {f:.9f} Hz  a t = {t:.9f} s")
except KeyboardInterrupt:
    """ ****************************** FINALIZACIÓN DE LA MEDICIÓN *************************** """ 
    print("\nMedición interrumpida por el usuario.")
    objt_prueba.abort_continuous_measurement()

    
  


