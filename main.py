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
    except Exception as e:
        estado_label.config(text='Estado:  Desconectado', fg='#e74c3c')
        tk.messagebox.showerror('Error de conexión', 'No se logró conexión con el Dispositivo.\nRevise alimentación o instalación de drivers de comunicación.')

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