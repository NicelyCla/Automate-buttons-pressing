import tkinter as tk
from tkinter import ttk
from subprocess import run

nome_bottoni = []

def capture_rect(file_output):
    try:
        # Esegui il comando per catturare uno screenshot della regione e salvarlo come file_output
        run(['xfce4-screenshooter', '--region', '--save', file_output])
        print(f'Screenshot catturato e salvato come {file_output}')
    except Exception as e:
        print(f'Errore durante la cattura dello screenshot: {e}')

def stampa_testo():
    name_button_text = entry.get()
    nome_bottoni.append(name_button_text)
    
    # Aggiorna la Listbox con l'elenco aggiornato
    update_listbox()

    # Chiamata alla funzione per catturare lo screenshot
    capture_rect(f"{name_button_text}.png")

def remove_element():
    selected_index = listbox.curselection()
    if selected_index:
        # Rimuovi l'elemento dalla lista e aggiorna la Listbox
        nome_bottoni.pop(selected_index[0])
        update_listbox()

def update_listbox():
    # Cancella tutti gli elementi nella Listbox
    listbox.delete(0, tk.END)
    
    # Aggiungi gli elementi dell'array alla Listbox
    for nome in nome_bottoni:
        listbox.insert(tk.END, f"{nome}.png")

def gen_code():
    file_name = 'generated.py'

    code = '''import pyautogui
import time
import numpy as np
from pynput.mouse import Button, Controller

mouse = Controller()
n = 5
confidence = 0.90  # Livello di confidenza per il riconoscimento dell'immagine

pyautogui.FAILSAFE = False
pyautogui.useImageNotFoundException(False)
while True:

'''

    for i in range(len(nome_bottoni)):
        code += f"    location_{i} = pyautogui.locateOnScreen('{nome_bottoni[i]}.png', confidence = confidence)\n"
        code += f'''    if location_{i}:
        print(location_{i})
        center_x = location_{i}.left + location_{i}.width // 2
        center_y = location_{i}.top + location_{i}.height // 2
        pyautogui.moveTo(center_x, center_y)
        time.sleep(0.2)
        mouse.click(Button.left, 1)
        pyautogui.moveTo(location_{i}.left+80, location_{i}.top+50)
        time.sleep(0.5)

'''


    script_content = code
    
    # Write the content to the file
    with open(file_name, 'w') as file:
        file.write(script_content)

    print(f'The file "{file_name}" has been generated.')


# Creazione della finestra principale
finestra = tk.Tk()
finestra.title("Automater")

# Centra la finestra nella schermata
larghezza_finestra = 300
altezza_finestra = 350
larghezza_schermo = finestra.winfo_screenwidth()
altezza_schermo = finestra.winfo_screenheight()
posizione_x = (larghezza_schermo - larghezza_finestra) // 2
posizione_y = (altezza_schermo - altezza_finestra) // 2
finestra.geometry(f"{larghezza_finestra}x{altezza_finestra}+{posizione_x}+{posizione_y}")

# Creazione del Label
label = ttk.Label(finestra, text="Name element: (no space)")
label.pack()

# Creazione del TextBox
entry = ttk.Entry(finestra, width=30)
entry.pack()

# Creazione del Bottone "Add"
bottone_add = ttk.Button(finestra, text="Add", command=stampa_testo)
bottone_add.pack(pady=5)

# Creazione della Listbox
listbox = tk.Listbox(finestra, selectmode=tk.SINGLE)
listbox.pack()

# Creazione del Bottone "Remove"
bottone_remove = ttk.Button(finestra, text="Remove", command=remove_element)
bottone_remove.pack(pady=10)  # Posiziona il bottone in basso

# Creazione del Bottone "Remove"
bottone_generate = ttk.Button(finestra, text="Generate", command=gen_code)
bottone_generate.pack()  # Posiziona il bottone in basso

# Esecuzione del loop principale
finestra.mainloop()
