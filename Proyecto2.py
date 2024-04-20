import tkinter as tk

def create_game_board(rows, cols):
    # Destruye la ventana inicial y crea una nueva para el tablero de juego
    root.destroy()
    game_root = tk.Tk()
    game_root.title("Batalla Naval")

    buttons = []
    for row in range(rows):
        row_of_buttons = []
        for col in range(cols):
            button = tk.Button(game_root, text=" ", width=4, height=2,
                               command=lambda r=row, c=col: button_click(r, c, buttons))
            button.grid(row=row, column=col)
            row_of_buttons.append(button)
        buttons.append(row_of_buttons)

    game_root.mainloop()

def button_click(row, col, buttons):
    print(f"Button at row {row}, column {col} clicked")
    buttons[row][col].config(text="X", state="disabled")

def submit_dimensions():
    rows = int(row_entry.get())
    cols = int(col_entry.get())
    create_game_board(rows, cols)

# Ventana inicial para ingresar las dimensiones del tablero
root = tk.Tk()
root.title("Configuración del Juego")

tk.Label(root, text="Número de filas:").grid(row=0, column=0)
row_entry = tk.Entry(root)
row_entry.grid(row=0, column=1)

tk.Label(root, text="Número de columnas:").grid(row=1, column=0)
col_entry = tk.Entry(root)
col_entry.grid(row=1, column=1)

submit_button = tk.Button(root, text="Crear Tablero", command=submit_dimensions)
submit_button.grid(row=2, column=0, columnspan=2)

root.mainloop()

