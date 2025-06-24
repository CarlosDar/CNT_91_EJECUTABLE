# ===============================
# INICIO DEL PROGRAMA PRINCIPAL
# ===============================
# Este archivo es el punto de entrada de la aplicación de escritorio CNT-91.
# Al ejecutarlo, se carga la ventana principal con el diseño profesional definido en frontend_widgets.py

import tkinter as tk
from frontend_widgets import crear_layout_principal
import CNT_9X_pendulum as CNT

# Variable global para el objeto del frecuencímetro
cnt_device = None

# Valor por defecto del identificador GPIB
DEFAULT_GPIB = 'GPIB0::10::INSTR'

# Función para manejar la conexión al dispositivo
def conectar_dispositivo(widgets):
    global cnt_device
    entry_id = widgets['entry_id']
    estado_label = widgets['estado']
    btn_conectar = widgets['btn_conectar']
    address = entry_id.get().strip()
    # Si el campo está vacío, usar el valor por defecto
    if not address:
        address = DEFAULT_GPIB
        entry_id.delete(0, tk.END)
        entry_id.insert(0, DEFAULT_GPIB)
    # Cambiar estado a "Trying to connect" en naranja
    estado_label.config(text='Estado:  Trying to connect', fg='#e67e22')
    widgets['frame_superior'].update_idletasks()
    try:
        cnt_device = CNT.CNT_frequenciometro(address)
        # Si no hay excepción, conexión exitosa
        estado_label.config(text='Estado:  Conectado', fg='#27ae60')
        # Cambiar el botón a rojo con texto "Desconectar"
        btn_conectar.config(text='🔌  Desconectar', style='DangerSidebar.TButton')
        # Cambiar la función del botón para desconectar
        btn_conectar.config(command=lambda: desconectar_dispositivo(widgets))
        # Actualizar el estado del botón
        btn_conectar.estado_conectado = True
    except Exception as e:
        estado_label.config(text='Estado:  Desconectado', fg='#e74c3c')
        tk.messagebox.showerror('Error de conexión', 'No se logró conexión con el Dispositivo.\nRevise alimentación o instalación de drivers de comunicación.')

# Función para manejar la desconexión del dispositivo
def desconectar_dispositivo(widgets):
    global cnt_device
    estado_label = widgets['estado']
    btn_conectar = widgets['btn_conectar']
    
    try:
        if cnt_device is not None:
            # Cerrar la conexión usando la función que creamos
            cnt_device.cerrar_conexion()
            cnt_device = None
            # Cambiar estado a desconectado
            estado_label.config(text='Estado:  Desconectado', fg='#e74c3c')
            # Cambiar el botón de vuelta a azul con texto "Conectar"
            btn_conectar.config(text='🔌  Conectar', style='PrimarySidebar.TButton')
            # Cambiar la función del botón para conectar
            btn_conectar.config(command=lambda: conectar_dispositivo(widgets))
            # Actualizar el estado del botón
            btn_conectar.estado_conectado = False
            print("Dispositivo desconectado correctamente.")
    except Exception as e:
        print(f"Error al desconectar: {e}")
        # Aún así, resetear el estado de la interfaz
        estado_label.config(text='Estado:  Desconectado', fg='#e74c3c')
        btn_conectar.config(text='🔌  Conectar', style='PrimarySidebar.TButton')
        btn_conectar.config(command=lambda: conectar_dispositivo(widgets))
        btn_conectar.estado_conectado = False

if __name__ == '__main__':
    # Crear la ventana principal de la aplicación
    root = tk.Tk()
    widgets = crear_layout_principal(root)

    # Importar messagebox aquí para evitar problemas de importación circular
    import tkinter.messagebox
    tk.messagebox = tkinter.messagebox

    # Asignar la función al botón de conectar
    widgets['btn_conectar'].config(command=lambda: conectar_dispositivo(widgets))

    # Iniciar el bucle principal de la interfaz gráfica (espera eventos del usuario)
    root.mainloop() 