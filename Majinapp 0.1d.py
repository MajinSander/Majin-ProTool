import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import ctypes
import sys

# Función para ejecutar el programa con permisos de administrador
def solicitar_permisos_administrador():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        # Si no tiene permisos de administrador, se reinicia con elevación de privilegios
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

# Verificamos si tenemos permisos de administrador al iniciar
solicitar_permisos_administrador()

def obtener_perfil_red():
    try:
        comando = 'powershell -Command "Get-NetConnectionProfile | Select-Object -ExpandProperty NetworkCategory"'
        resultado = subprocess.check_output(comando, shell=True, text=True).strip()
        return resultado
    except Exception as e:
        print(f"Error al obtener el perfil de red: {e}")
        return None

def cambiar_perfil_red():
    estado_actual = obtener_perfil_red()
    if estado_actual == 'Private':
        nuevo_estado = 'Public'
    else:
        nuevo_estado = 'Private'
    try:
        comando = f'powershell -Command "Get-NetConnectionProfile | Set-NetConnectionProfile -NetworkCategory {nuevo_estado}"'
        subprocess.run(comando, shell=True)
        actualizar_estado_red()
    except Exception as e:
        print(f"Error al cambiar el perfil de red: {e}")

def es_conexion_cableada():
    try:
        comando = 'powershell -Command "Get-NetAdapter | Where-Object { $_.Status -eq \'Up\' -and $_.MediaType -eq \'802.3\' }"'
        resultado = subprocess.check_output(comando, shell=True, text=True).strip()
        return bool(resultado)  # Retorna True si hay una conexión cableada
    except Exception as e:
        print(f"Error al obtener el tipo de conexión: {e}")
        return False

def mostrar_ayuda():
    messagebox.showinfo("Información", "Puedes cambiar entre red pública y privada aquí si la conexión no es cableada.")

def actualizar_estado_red():
    estado_actual = obtener_perfil_red()
    if es_conexion_cableada():
        chk_red.config(state='disabled')  # Deshabilita el botón si la conexión es cableada
        chk_red.config(text='Red cableada o desconectada')
    else:
        chk_red.config(state='normal')  # Habilita el botón si no es una conexión cableada
        if estado_actual == 'Private':
            var_red.set(1)
            chk_red.config(text='Red Privada')
        elif estado_actual == 'Public':
            var_red.set(0)
            chk_red.config(text='Red Pública')
        else:
            var_red.set(0)
            chk_red.config(text='Red cableada o desconectada')

# Crear la ventana principal
root = tk.Tk()
root.title("Herramientas de Técnico IT")
root.geometry("400x300")

# Crear el notebook (pestañas)
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Crear las pestañas para cada categoría
config_frame = ttk.Frame(notebook)
instalacion_frame = ttk.Frame(notebook)
datos_frame = ttk.Frame(notebook)
mantenimiento_frame = ttk.Frame(notebook)

notebook.add(config_frame, text='Configuración')
notebook.add(instalacion_frame, text='Instalación')
notebook.add(datos_frame, text='Datos')
notebook.add(mantenimiento_frame, text='Mantenimiento')

# Variable para el estado del interruptor
var_red = tk.IntVar()

# Crear el marco para el texto y el Checkbutton
frame_red = ttk.Frame(config_frame)
frame_red.pack(pady=20)

# Etiqueta de texto a la izquierda del botón
label_estado_red = ttk.Label(frame_red, text="Estado de la red")
label_estado_red.pack(side='left', padx=(0, 20))  # Alinear el texto más a la derecha

# Agregar el ícono de ayuda con tamaño reducido
help_button = ttk.Button(frame_red, text="?", width=2, command=mostrar_ayuda)
help_button.pack(side='left')

# Crear el interruptor (Checkbutton) al lado del texto
chk_red = ttk.Checkbutton(frame_red, text='Red', variable=var_red, command=cambiar_perfil_red)
chk_red.pack(side='left')

# Inicializar el estado del interruptor
actualizar_estado_red()

# Ejecutar la aplicación
root.mainloop()
