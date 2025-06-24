import tkinter as tk
from tkinter import ttk


def crear_layout_principal(root):
    """
    Crea la estructura principal de la interfaz gráfica, imitando el diseño de la imagen proporcionada, pero con calidad visual mejorada:
    - Panel lateral azul oscuro con botones y secciones
    - Barra superior blanca con estado de conexión
    - Área principal de contenido en gris claro
    - Botones con efecto hover y esquinas redondeadas (simuladas)
    - Entrada de texto para el identificador del dispositivo
    """
    # Colores
    azul_lateral = '#25364a'
    azul_boton = '#2980f2'
    azul_hover = '#3a8bfd'
    gris_fondo = '#f6f7fa'
    blanco = '#ffffff'
    gris_texto = '#6c757d'
    rojo_estado = '#e74c3c'
    azul_activo = '#1c2a3a'

    # Configuración de la ventana principal
    root.configure(bg=gris_fondo)
    root.geometry('1600x800')
    root.title('CNT-91')

    style = ttk.Style()
    style.theme_use('clam')
    # Estilo para los botones laterales
    style.configure('Sidebar.TButton',
                    font=('Segoe UI', 12),
                    foreground='white',
                    background=azul_lateral,
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor=azul_boton,
                    padding=10)
    style.map('Sidebar.TButton',
              background=[('active', azul_hover), ('!active', azul_lateral)],
              relief=[('pressed', 'sunken'), ('!pressed', 'flat')])
    # Estilo para el botón principal (Conectar)
    style.configure('PrimarySidebar.TButton',
                    font=('Segoe UI', 12, 'bold'),
                    foreground='white',
                    background=azul_boton,
                    borderwidth=0,
                    focusthickness=3,
                    focuscolor=azul_boton,
                    padding=10)
    style.map('PrimarySidebar.TButton',
              background=[('active', azul_hover), ('!active', azul_boton)],
              relief=[('pressed', 'sunken'), ('!pressed', 'flat')])

    # Panel lateral
    frame_lateral = tk.Frame(root, bg=azul_lateral, width=220)
    frame_lateral.pack(side='left', fill='y')

    # Logo y título
    logo = tk.Label(frame_lateral, text='⚙️', bg=azul_lateral, fg='white', font=('Segoe UI', 22, 'bold'))
    logo.pack(pady=(24, 0))
    titulo = tk.Label(frame_lateral, text='CNT-91', bg=azul_lateral, fg='white', font=('Segoe UI', 18, 'bold'))
    titulo.pack(pady=(0, 10))

    # Entrada de texto para el identificador del dispositivo
    label_id = tk.Label(frame_lateral, text='Identificador GPIB:', bg=azul_lateral, fg='#b0b8c1', font=('Segoe UI', 10, 'bold'))
    label_id.pack(padx=20, anchor='w')
    entry_id = ttk.Entry(frame_lateral, font=('Segoe UI', 11))
    entry_id.insert(0, 'GPIB0::10::INSTR')
    entry_id.pack(fill='x', padx=20, pady=(0, 18))

    # Botón Conectar
    btn_conectar = ttk.Button(frame_lateral, text='🔌  Conectar', style='PrimarySidebar.TButton')
    btn_conectar.pack(fill='x', padx=20, pady=(0, 10))

    # Separador sutil
    sep1 = tk.Frame(frame_lateral, bg='#34495e', height=2)
    sep1.pack(fill='x', padx=20, pady=(0, 10))

    # Botón Configuración
    btn_config = ttk.Button(frame_lateral, text='⚙️  Configuración', style='Sidebar.TButton')
    btn_config.pack(fill='x', padx=20, pady=(0, 10))

    # Botón Mediciones
    btn_mediciones = ttk.Button(frame_lateral, text='📈  Mediciones', style='Sidebar.TButton')
    btn_mediciones.pack(fill='x', padx=20, pady=(0, 10))

    # Botón Información
    btn_info = ttk.Button(frame_lateral, text='ℹ️  Información CNT-91', style='Sidebar.TButton')
    btn_info.pack(fill='x', padx=20, pady=(0, 10))

    # Simular esquinas redondeadas y efecto hover
    def on_enter(e):
        e.widget.configure(style='PrimarySidebar.TButton' if e.widget == btn_conectar else 'Sidebar.TButton')
        e.widget['cursor'] = 'hand2'
    def on_leave(e):
        e.widget.configure(style='PrimarySidebar.TButton' if e.widget == btn_conectar else 'Sidebar.TButton')
        e.widget['cursor'] = ''
    for btn in [btn_conectar, btn_config, btn_mediciones, btn_info]:
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)

    # Barra superior
    frame_superior = tk.Frame(root, bg=blanco, height=50, highlightbackground='#e0e0e0', highlightthickness=1)
    frame_superior.pack(side='top', fill='x')
    frame_superior.pack_propagate(False)

    # Estado de conexión
    estado = tk.Label(frame_superior, text='Estado:  Desconectado', bg=blanco, fg=rojo_estado, font=('Segoe UI', 12, 'bold'))
    estado.pack(side='left', padx=30, pady=10)

    # Área principal de contenido
    frame_contenido = tk.Frame(root, bg=gris_fondo)
    frame_contenido.pack(expand=True, fill='both')

    # Retornar referencias útiles para enlazar lógica después
    return {
        'frame_lateral': frame_lateral,
        'entry_id': entry_id,
        'btn_conectar': btn_conectar,
        'btn_config': btn_config,
        'btn_mediciones': btn_mediciones,
        'btn_info': btn_info,
        'frame_superior': frame_superior,
        'estado': estado,
        'frame_contenido': frame_contenido
    } 