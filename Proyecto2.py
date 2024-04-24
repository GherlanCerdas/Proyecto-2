import tkinter as tk
from tkinter import messagebox, PhotoImage
from PIL import Image, ImageTk

def guardar_jugador(nombre_entry, nickname_entry, ventana_registro):
    nombre = nombre_entry.get()
    nickname = nickname_entry.get()

    if nombre == "" or nickname == "":
        messagebox.showerror("Error", "Por favor, complete todos los campos.", parent=ventana_registro)
        return

    # Leer el archivo para asegurarse de que no se repitan nombres o nicknames
    try:
        with open("jugadores.txt", "r") as file:
            for line in file:
                stored_name, stored_nickname = line.strip().split(',')
                if stored_name == nombre or stored_nickname == nickname:
                    messagebox.showerror("Error", "El nombre o nickname ya está registrado.", parent=ventana_registro)
                    return
    except FileNotFoundError:
        pass  # Si el archivo no existe, simplemente lo crearemos

    # Guardar el nuevo jugador
    with open("jugadores.txt", "a") as file:
        file.write(f"{nombre},{nickname}\n")
        messagebox.showinfo("Éxito", "Jugador registrado con éxito.", parent=ventana_registro)
        nombre_entry.delete(0, tk.END)
        nickname_entry.delete(0, tk.END)

def abrir_ventana_registro():
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registro de Jugadores")
    ventana_registro.geometry("600x400")

    label_nombre = tk.Label(ventana_registro, text="Nombre:")
    label_nombre.pack(pady=(20, 5))

    entrada_nombre = tk.Entry(ventana_registro)
    entrada_nombre.pack()

    label_nickname = tk.Label(ventana_registro, text="Nickname:")
    label_nickname.pack(pady=(10, 5))

    entrada_nickname = tk.Entry(ventana_registro)
    entrada_nickname.pack()

    boton_guardar = tk.Button(ventana_registro, text="Guardar", command=lambda: guardar_jugador(entrada_nombre, entrada_nickname, ventana_registro))
    boton_guardar.pack(pady=20)

def abrir_ventana_juego():
    ventana_juego = tk.Toplevel()
    ventana_juego.title("Configuración del Juego")
    ventana_juego.geometry("600x400")

    # Leer jugadores de archivo
    try:
        with open("jugadores.txt", "r") as file:
            jugadores = [line.strip().split(',')[1] for line in file]  # Obtener solo los nicknames
    except FileNotFoundError:
        jugadores = []

    # Crear menú desplegable para seleccionar jugadores
    label_jugador1 = tk.Label(ventana_juego, text="Seleccionar Jugador 1:")
    label_jugador1.pack(pady=(20, 5))

    jugador1_var = tk.StringVar(ventana_juego)
    jugador1_var.set("Elegir jugador")
    jugador1_menu = tk.OptionMenu(ventana_juego, jugador1_var, *jugadores)
    jugador1_menu.pack()

    label_jugador2 = tk.Label(ventana_juego, text="Seleccionar Jugador 2:")
    label_jugador2.pack(pady=(20, 5))

    jugador2_var = tk.StringVar(ventana_juego)
    jugador2_var.set("Elegir jugador")
    jugador2_menu = tk.OptionMenu(ventana_juego, jugador2_var, *jugadores)
    jugador2_menu.pack()

    # Entrada para dimensiones del tablero
    label_filas = tk.Label(ventana_juego, text="Filas (mínimo 10):")
    label_filas.pack(pady=(20, 5))
    entrada_filas = tk.Entry(ventana_juego)
    entrada_filas.pack()

    label_columnas = tk.Label(ventana_juego, text="Columnas (mínimo 20):")
    label_columnas.pack(pady=(10, 5))
    entrada_columnas = tk.Entry(ventana_juego)
    entrada_columnas.pack()

    # Botón para continuar al juego
    boton_continuar = tk.Button(ventana_juego, text="Continuar", command=lambda: abrir_ventana_juego2(jugador1_var.get(), jugador2_var.get(), entrada_filas.get(), entrada_columnas.get()))
    boton_continuar.pack(pady=20)

def abrir_ventana_juego2(jugador1, jugador2, filas, columnas):
    ventana_juego2 = tk.Toplevel()
    ventana_juego2.title(f"Juego Batalla Naval - {jugador1} vs {jugador2}")

    try:
        filas = int(filas)
        columnas = int(columnas)
        assert filas >= 10 and columnas >= 20
    except (ValueError, AssertionError):
        messagebox.showerror("Error", "Asegúrese de que las filas sean al menos 10 y las columnas al menos 20")
        return

    ventana_juego2.geometry("800x600")

    # Ruta de las imágenes
    ruta = "C:/Users/Xtremetech/Desktop/Python/Proyecto2/"

    # Carga las imágenes de los barcos con las extensiones de archivo correctas
    imagenes_barcos = {
        "Destructor": ImageTk.PhotoImage(Image.open(ruta + "Destructor.png").resize((40, 40))),
        "CruceroPopa": ImageTk.PhotoImage(Image.open(ruta + "CruceroPopa.png").resize((40, 40))),
        "CruceroProa": ImageTk.PhotoImage(Image.open(ruta + "CruceroProa.png").resize((40, 40))),
        "AcorazadoPopa": ImageTk.PhotoImage(Image.open(ruta + "AcorazadoPopa.png").resize((40, 40))),
        "AcorazadoMedio": ImageTk.PhotoImage(Image.open(ruta + "AcorazadoMedio.png").resize((40, 40))),
        "AcorazadoProa": ImageTk.PhotoImage(Image.open(ruta + "AcorazadoProa.png").resize((40, 40)))
    }

    estado_juego = {
        "turno_jugador": jugador1,
        "barcos": {
            jugador1: {"Destructor": 6, "Crucero": 4, "Acorazado": 2},
            jugador2: {"Destructor": 6, "Crucero": 4, "Acorazado": 2}
        },
        "barcos_colocados": {
            jugador1: [],
            jugador2: []
        }
    }

    def obtener_barco_actual(jugador):
        for tipo_barco, cantidad in estado_juego["barcos"][jugador].items():
            if cantidad > 0:
                return tipo_barco
        return None

    def colocar_barco(fila, columna):
        
        jugador_actual = estado_juego["turno_jugador"]
        barco_actual = obtener_barco_actual(jugador_actual)
        if barco_actual is None:
            return

        # Verificar si el jugador actual tiene permiso para colocar un barco en esta posición
        if jugador_actual == jugador1 and columna >= columnas_jugador1:
            messagebox.showerror("Error", "No puedes colocar barcos en el área del Jugador 2.")
            return
        elif jugador_actual == jugador2 and columna < columnas_jugador1:
            messagebox.showerror("Error", "No puedes colocar barcos en el área del Jugador 1.")
            return

        if barco_actual == "Destructor":
            botones_tablero[fila][columna].config(image=imagenes_barcos["Destructor"])
            botones_tablero[fila][columna].image = imagenes_barcos["Destructor"]
        elif barco_actual == "Crucero":
            if columna + 1 < columnas:
                botones_tablero[fila][columna].config(image=imagenes_barcos["CruceroProa"])
                botones_tablero[fila][columna + 1].config(image=imagenes_barcos["CruceroPopa"])
                botones_tablero[fila][columna].image = imagenes_barcos["CruceroProa"]
                botones_tablero[fila][columna + 1].image = imagenes_barcos["CruceroPopa"]
        elif barco_actual == "Acorazado":
            if columna + 2 < columnas:
                botones_tablero[fila][columna].config(image=imagenes_barcos["AcorazadoProa"])
                botones_tablero[fila][columna + 1].config(image=imagenes_barcos["AcorazadoMedio"])
                botones_tablero[fila][columna + 2].config(image=imagenes_barcos["AcorazadoPopa"])
                botones_tablero[fila][columna].image = imagenes_barcos["AcorazadoProa"]
                botones_tablero[fila][columna + 1].image = imagenes_barcos["AcorazadoMedio"]
                botones_tablero[fila][columna + 2].image = imagenes_barcos["AcorazadoPopa"]

        # Actualizar el estado del juego
        estado_juego["barcos"][jugador_actual][barco_actual] -= 1
        estado_juego["barcos_colocados"][jugador_actual].append((fila, columna, barco_actual))

        # Comprobar si el jugador actual ha terminado
        if obtener_barco_actual(jugador_actual) is None:
            if jugador_actual == jugador1:
                estado_juego["turno_jugador"] = jugador2
                messagebox.showinfo("Turno", f"Todos los barcos de {jugador1} han sido colocados. Turno de {jugador2}.")
            else:
                messagebox.showinfo("Juego listo", "Todos los barcos han sido colocados. El juego está listo para comenzar.")

    # Crear el tablero
    frame_tablero = tk.Frame(ventana_juego2)
    frame_tablero.pack(expand=True, fill="both")
    botones_tablero = []

    # Calcular el número de columnas para cada jugador
    columnas_jugador1 = columnas // 2
    columnas_jugador2 = columnas - columnas_jugador1

    for fila in range(filas):
        fila_botones = []
        for columna in range(columnas):
            boton = tk.Button(frame_tablero, width=5, height=2)
            boton.grid(row=fila, column=columna, sticky="nsew")
            boton.config(command=lambda f=fila, c=columna: colocar_barco(f, c))
            fila_botones.append(boton)
        botones_tablero.append(fila_botones)

    # Configurar la expansión proporcional de las celdas del grid
    for i in range(filas):
        frame_tablero.rowconfigure(i, weight=1)
    for j in range(columnas):
        frame_tablero.columnconfigure(j, weight=1)

def abrir_ventana_reporte():
    ventana_reporte = tk.Toplevel()
    ventana_reporte.title("Reporte de Partida")
    ventana_reporte.geometry("600x400")

# Crea la ventana principal
ventana_principal = tk.Tk()
ventana_principal.title("Menú Principal del Juego Batalla Naval")
ventana_principal.geometry("600x400")

# Botones del menú principal
boton_registro = tk.Button(ventana_principal, text="Registro de Jugadores", command=abrir_ventana_registro)
boton_registro.pack(pady=10)

boton_juego = tk.Button(ventana_principal, text="Juego", command=abrir_ventana_juego)
boton_juego.pack(pady=10)

boton_reporte = tk.Button(ventana_principal, text="Reporte de Partida", command=abrir_ventana_reporte)
boton_reporte.pack(pady=10)

# Inicia el bucle principal de la GUI
ventana_principal.mainloop()
