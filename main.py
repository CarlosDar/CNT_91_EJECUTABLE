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

# Variable global para el canal seleccionado ('A' o 'B')
canal_seleccionado = 'A'

# Variable global para el intervalo de captura (en segundos)
intervalo_s = 0.2

# Variable global para el acoplamiento ('AC' o 'DC')
acoplamiento = 'AC'

# Variable global para la impedancia ('Max' o 'Min')
impedancia = 'Max'  # Nuevo parámetro: 'Max' para 1MΩ, 'Min' para 50Ω

# Función para mostrar el menú de selección de canal
def mostrar_menu_canal(widgets):
    global canal_seleccionado, intervalo_s, acoplamiento, impedancia
    frame_contenido = widgets['frame_contenido']
    
    # Limpiar el frame de contenido
    for widget in frame_contenido.winfo_children():
        widget.destroy()
    
    # Frame principal con padding
    main_frame = tk.Frame(frame_contenido, bg='#f6f7fa')
    main_frame.pack(fill='both', expand=True, padx=10, pady=5)
    
    # Título principal - Frequency Datalogger
    titulo_frame = tk.Frame(main_frame, bg='#f6f7fa')
    titulo_frame.pack(fill='x', pady=(0, 10))
    
    titulo = tk.Label(titulo_frame, text='Frequency Datalogger', 
                     font=('Segoe UI', 14, 'bold'), 
                     fg='#25364a', bg='#f6f7fa')
    titulo.pack(anchor='w')
    
    # Línea separadora
    separador = tk.Frame(titulo_frame, height=1, bg='#2980f2')
    separador.pack(fill='x', pady=(3, 0))
    
    # Frame de configuración
    config_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
    config_frame.pack(fill='x', pady=(0, 5))
    
    # Título de configuración
    config_titulo = tk.Label(config_frame, text='Configuración:', 
                            font=('Segoe UI', 10, 'bold'), 
                            fg='#25364a', bg='white')
    config_titulo.pack(anchor='w', padx=10, pady=(8, 5))
    
    # Variable interna para el selector de canal
    canal_var = tk.StringVar(value='A')
    
    # Variable interna para el intervalo
    intervalo_var = tk.StringVar(value=str(intervalo_s))
    
    # Variable interna para el acoplamiento
    acoplamiento_var = tk.StringVar(value=acoplamiento)
    
    # Variable interna para la impedancia
    impedancia_var = tk.StringVar(value=impedancia)
    
    # Frame para el selector de canal
    selector_frame = tk.Frame(config_frame, bg='white')
    selector_frame.pack(fill='x', padx=10, pady=(0, 8))
    
    # Etiqueta del selector de canal
    label_canal = tk.Label(selector_frame, text='Canal de medición:', 
                          font=('Segoe UI', 8, 'bold'), 
                          fg='#6c757d', bg='white')
    label_canal.pack(anchor='w', pady=(0, 3))
    
    # Frame para los radio buttons de canal
    radio_frame = tk.Frame(selector_frame, bg='white')
    radio_frame.pack(anchor='w')
    
    # Radio buttons con mejor estilo
    radio_a = tk.Radiobutton(radio_frame, text='Canal A', 
                            variable=canal_var, value='A', 
                            font=('Segoe UI', 8), 
                            fg='#25364a', bg='white',
                            selectcolor='white',
                            activebackground='white',
                            activeforeground='#2980f2')
    radio_a.pack(side='left', padx=(0, 15))
    
    radio_b = tk.Radiobutton(radio_frame, text='Canal B', 
                            variable=canal_var, value='B', 
                            font=('Segoe UI', 8), 
                            fg='#25364a', bg='white',
                            selectcolor='white',
                            activebackground='white',
                            activeforeground='#2980f2')
    radio_b.pack(side='left')
    
    # Separador entre configuraciones
    separador_config = tk.Frame(config_frame, height=1, bg='#e0e0e0')
    separador_config.pack(fill='x', padx=10, pady=5)
    
    # Frame para el selector de intervalo
    intervalo_frame = tk.Frame(config_frame, bg='white')
    intervalo_frame.pack(fill='x', padx=10, pady=(0, 8))
    
    # Etiqueta del selector de intervalo
    label_intervalo = tk.Label(intervalo_frame, text='Intervalo de captura (segundos):', 
                              font=('Segoe UI', 8, 'bold'), 
                              fg='#6c757d', bg='white')
    label_intervalo.pack(anchor='w', pady=(0, 3))
    
    # Frame para el control de intervalo
    control_intervalo_frame = tk.Frame(intervalo_frame, bg='white')
    control_intervalo_frame.pack(anchor='w')
    
    # Función para validar entrada manual
    def validar_entrada_intervalo(*args):
        try:
            texto_actual = intervalo_var.get()
            if texto_actual == "" or texto_actual == "0":
                return  # Permitir campo vacío o solo "0"
            
            valor = float(texto_actual)
            
            # Solo validar si el valor está completo y es menor que el mínimo
            if valor < 2e-8 and valor != 0:
                intervalo_var.set("2.00e-08")
            elif valor > 1000:
                intervalo_var.set("1000.000")
        except ValueError:
            # Si no es un número válido, no hacer nada (permitir que el usuario siga escribiendo)
            pass
    
    # Vincular validación a cambios en la variable
    intervalo_var.trace('w', validar_entrada_intervalo)
    
    # Entry para el valor del intervalo
    entry_intervalo = tk.Entry(control_intervalo_frame, 
                              textvariable=intervalo_var,
                              font=('Segoe UI', 8),
                              width=12,
                              justify='left')
    entry_intervalo.pack(side='left')
    
    # Separador entre configuraciones
    separador_config2 = tk.Frame(config_frame, height=1, bg='#e0e0e0')
    separador_config2.pack(fill='x', padx=10, pady=5)
    
    # Frame para el selector de acoplamiento
    acoplamiento_frame = tk.Frame(config_frame, bg='white')
    acoplamiento_frame.pack(fill='x', padx=10, pady=(0, 8))
    
    # Etiqueta del selector de acoplamiento
    label_acoplamiento = tk.Label(acoplamiento_frame, text='Acoplamiento:', 
                                 font=('Segoe UI', 8, 'bold'), 
                                 fg='#6c757d', bg='white')
    label_acoplamiento.pack(anchor='w', pady=(0, 3))
    
    # Frame para los radio buttons de acoplamiento
    radio_acoplamiento_frame = tk.Frame(acoplamiento_frame, bg='white')
    radio_acoplamiento_frame.pack(anchor='w')
    
    # Radio buttons para acoplamiento
    radio_ac = tk.Radiobutton(radio_acoplamiento_frame, text='AC', 
                             variable=acoplamiento_var, value='AC', 
                             font=('Segoe UI', 8), 
                             fg='#25364a', bg='white',
                             selectcolor='white',
                             activebackground='white',
                             activeforeground='#2980f2')
    radio_ac.pack(side='left', padx=(0, 15))
    
    radio_dc = tk.Radiobutton(radio_acoplamiento_frame, text='DC', 
                             variable=acoplamiento_var, value='DC', 
                             font=('Segoe UI', 8), 
                             fg='#25364a', bg='white',
                             selectcolor='white',
                             activebackground='white',
                             activeforeground='#2980f2')
    radio_dc.pack(side='left')
    
    # Separador entre configuraciones
    separador_config3 = tk.Frame(config_frame, height=1, bg='#e0e0e0')
    separador_config3.pack(fill='x', padx=10, pady=5)
    
    # Frame para el selector de impedancia
    impedancia_frame = tk.Frame(config_frame, bg='white')
    impedancia_frame.pack(fill='x', padx=10, pady=(0, 8))
    
    # Etiqueta del selector de impedancia
    label_impedancia = tk.Label(impedancia_frame, text='Impedancia:', 
                                 font=('Segoe UI', 8, 'bold'), 
                                 fg='#6c757d', bg='white')
    label_impedancia.pack(anchor='w', pady=(0, 3))
    
    # Frame para los radio buttons de impedancia
    radio_impedancia_frame = tk.Frame(impedancia_frame, bg='white')
    radio_impedancia_frame.pack(anchor='w')
    
    # Radio buttons para impedancia
    radio_max = tk.Radiobutton(radio_impedancia_frame, text='1MΩ (Max)', 
                             variable=impedancia_var, value='Max', 
                             font=('Segoe UI', 8), 
                             fg='#25364a', bg='white',
                             selectcolor='white',
                             activebackground='white',
                             activeforeground='#2980f2')
    radio_max.pack(side='left', padx=(0, 15))
    
    radio_min = tk.Radiobutton(radio_impedancia_frame, text='50Ω (Min)', 
                             variable=impedancia_var, value='Min', 
                             font=('Segoe UI', 8), 
                             fg='#25364a', bg='white',
                             selectcolor='white',
                             activebackground='white',
                             activeforeground='#2980f2')
    radio_min.pack(side='left')
    
    # Función para guardar selección
    def guardar_seleccion():
        global canal_seleccionado, intervalo_s, acoplamiento, impedancia
        canal_seleccionado = canal_var.get()
        acoplamiento = acoplamiento_var.get()
        impedancia = impedancia_var.get()
        
        try:
            intervalo_s = float(intervalo_var.get())
            # Validar límites finales
            if intervalo_s < 2e-8:
                intervalo_s = 2e-8
            elif intervalo_s > 1000:
                intervalo_s = 1000
        except ValueError:
            intervalo_s = 0.2  # Valor por defecto si hay error
        
        # Formatear el intervalo para mostrar
        if intervalo_s < 0.001:
            intervalo_formato = f"{intervalo_s:.2e}"
        elif intervalo_s < 1:
            intervalo_formato = f"{intervalo_s:.6f}"
        else:
            intervalo_formato = f"{intervalo_s:.3f}"
        
        resultado_label.config(text=f"✓ Configuración guardada: Canal {canal_seleccionado}, Intervalo {intervalo_formato} s, Acoplamiento {acoplamiento}, Impedancia {impedancia}", fg='#27ae60')
    
    # Frame para botón y resultado
    accion_frame = tk.Frame(config_frame, bg='white')
    accion_frame.pack(fill='x', padx=10, pady=(0, 8))
    
    # Botón para guardar selección con estilo profesional
    btn_guardar = tk.Button(accion_frame, text='Guardar Configuración', 
                           command=guardar_seleccion, 
                           font=('Segoe UI', 8, 'bold'),
                           bg='#2980f2', fg='white',
                           relief='flat', padx=10, pady=3,
                           cursor='hand2')
    btn_guardar.pack(side='left', pady=(3, 0))
    
    # Label para mostrar resultado
    resultado_label = tk.Label(accion_frame, text='', 
                              font=('Segoe UI', 8), 
                              fg='#27ae60', bg='white')
    resultado_label.pack(side='left', padx=(8, 0), pady=(3, 0))

# Función para manejar la conexión al dispositivo
def conectar_dispositivo(widgets):
    global cnt_device
    entry_id = widgets['entry_id']
    estado_label = widgets['estado']
    btn_conectar = widgets['btn_conectar']
    btn_mediciones = widgets['btn_mediciones']
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
        # Habilitar botón Mediciones
        btn_mediciones.config(state='normal')
    except Exception as e:
        estado_label.config(text='Estado:  Desconectado', fg='#e74c3c')
        tk.messagebox.showerror('Error de conexión', 'No se logró conexión con el Dispositivo.\nRevise alimentación o instalación de drivers de comunicación.')
        btn_mediciones.config(state='disabled')

# Función para manejar la desconexión del dispositivo
def desconectar_dispositivo(widgets):
    global cnt_device
    estado_label = widgets['estado']
    btn_conectar = widgets['btn_conectar']
    btn_mediciones = widgets['btn_mediciones']
    
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
            btn_mediciones.config(state='disabled')
            print("Dispositivo desconectado correctamente.")
    except Exception as e:
        print(f"Error al desconectar: {e}")
        # Aún así, resetear el estado de la interfaz
        estado_label.config(text='Estado:  Desconectado', fg='#e74c3c')
        btn_conectar.config(text='🔌  Conectar', style='PrimarySidebar.TButton')
        btn_conectar.config(command=lambda: conectar_dispositivo(widgets))
        btn_conectar.estado_conectado = False
        btn_mediciones.config(state='disabled')

if __name__ == '__main__':
    # Crear la ventana principal de la aplicación
    root = tk.Tk()
    widgets = crear_layout_principal(root)

    # Importar messagebox aquí para evitar problemas de importación circular
    import tkinter.messagebox
    tk.messagebox = tkinter.messagebox

    # Deshabilitar botón Mediciones por defecto
    widgets['btn_mediciones'].config(state='disabled')

    # Asignar la función al botón de conectar
    widgets['btn_conectar'].config(command=lambda: conectar_dispositivo(widgets))

    # Asignar función al botón Mediciones
    widgets['btn_mediciones'].config(command=lambda: mostrar_menu_canal(widgets))

    # Iniciar el bucle principal de la interfaz gráfica (espera eventos del usuario)
    root.mainloop() 