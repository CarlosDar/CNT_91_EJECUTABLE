import tkinter as tk
from frontend_widgets import crear_layout_principal

if __name__ == '__main__':
    root = tk.Tk()
    widgets = crear_layout_principal(root)
    root.mainloop()
