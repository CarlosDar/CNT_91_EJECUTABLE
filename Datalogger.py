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

canal = '1'
intervalo_s = 2e-1
acoplamiento = 'DC'
impedancia = 'MIN'
atenuacion = 1
trigger_level = None
trigger_slope = 'POS'
filtro_Digital_PASSAbaja = None
filtro_Analog_PASSAbaja = True


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
    filtro_Analog_PASSAbaja=filtro_Analog_PASSAbaja,
    
)

""" ****************************** BOTÓN START/STOP MEDICIÓN CONTINUA *************************** """
n_muestras = 1

tiempo_espera = objt_prueba.start_continuous_measurement(intervalo_s=intervalo_s, canal=canal_cmd)

""" ****************************** Realizamos extracciones Mediciónes de Frecuencias *************************** """
print("Iniciando medición continua (Ctrl+C para parar)...")
if intervalo_s < 2:
    tiempo_espera = 0
    lenght = 10
elif intervalo_s < 5:
    lenght = 1
    tiempo_espera = 2.5 * (intervalo_s - 2) ** 2 + 0.09
elif intervalo_s < 10:
    lenght = 2
    tiempo_espera = 1.2 * (intervalo_s )  + 0.09
else:
    lenght = 1
    tiempo_espera =  (intervalo_s ) + 5
try:
    buffer_frecs = []
    buffer_ts = []
    t0 = None  # Primer timestamp para calcular tiempos relativos
    while True:
        frecs, ts = objt_prueba.fetch_continuous_samples(
            n_muestras=n_muestras,
            tiempo_espera=tiempo_espera
        )
        for f, t in zip(frecs, ts):
            if t0 is None:
                t0 = t
            t_rel = t - t0
            buffer_frecs.append((f, t, t_rel))
            print(f"Muestra: {f:.9f} Hz  a t = {t:.9f} s  (T. Relativo = {t_rel:.9f} s)")
        
        if len(buffer_frecs) >= lenght:
            for f, t, t_rel in buffer_frecs:
                objt_prueba.append_measurement(f, t, t_rel)
            buffer_frecs.clear()
            buffer_ts.clear()

except KeyboardInterrupt:
    """ ****************************** FINALIZACIÓN DE LA MEDICIÓN *************************** """ 
    print("\nMedición interrumpida por el usuario.")
    
    # Cerrar el archivo Excel de manera segura antes de abortar
    try:
        objt_prueba.cerrar_archivo_excel()
    except Exception as e:
        print(f"Advertencia al cerrar archivo Excel: {e}")
    
    # Abortar la medición continua
    try:
        objt_prueba.abort_continuous_measurement()
    except Exception as e:
        print(f"Advertencia al abortar medición: {e}")
    
    # Cerrar la conexión de manera completa
    try:
        objt_prueba.cerrar_conexion()
    except Exception as e:
        print(f"Advertencia al cerrar conexión: {e}")
    
    print("Medición finalizada correctamente.")
