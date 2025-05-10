import os
from pathlib import Path 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

#Funciones para limpiar y hacer pausas en la consola
def limpiar():
    os.system('cls')
def pausa():
    os.system("pause")

def createGraph(graphType):
    if(graphType == 4):
        return
    
    folder = Path("Datos")
    files = [file.name for file in folder.glob("*.xlsx")]

    if not files:
        print("No hay arhcivos disponibles.")
        return

    print("Archivos disponibles:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    while True:
        try:
            # Solicita al usuario que elija un archivo por su número
            op = int(input("Sselectiona el número del archivo a graficar (0 para salir): "))
            if op == 0:
                return  # Sale si elige 0
            if 1 <= op <= len(files):
                fileName = files[op - 1]  # Guarda el nombre del archivo sselectionado
                break
            else:
                print("Opción inválida.")  # Si el número está fuera de rango
        except ValueError:
            print("Por favor ingresa un número válido.")  # Si se ingresa un valor no numérico

    filePath = folder / fileName 
    df = pd.read_excel(filePath)

    column1 = df['Fecha']
    #Parseado de columna de dataframe a numpy
    dates = column1.to_numpy()
    column2 = df['Valor']
    #Parseado de columna de dataframe a numpy
    values = column2.to_numpy()
    print(dates)
    print(values)

    extension = ".xlsx"

    ylable = fileName.replace(extension, "")

    fig, ax = plt.subplots()
    if(graphType == 1):
        ax.bar(dates, values)
        subfolder = "Barra"
    elif(graphType == 2):
        ax.scatter(dates, values)
        subfolder = "Dispersion"
    elif(graphType == 3):
        ax.plot(dates, values)
        subfolder = "Lineal"
    else:
        print("Opción invalida")
        return

    ax.set_title(fileName)
    ax.set_xlabel("Fecha")
    ax.set_ylabel(ylable)
    ax.grid(True)

    graphFolder = Path("Graficas") / subfolder
    graphFolder.mkdir(parents=True, exist_ok=True)

    date = datetime.now() 
    safe_date = date.strftime("%d-%m-%y_%H-%M-%S")
    figName = f"{ylable}-{safe_date}.png"
    figPath = graphFolder / figName
    plt.savefig(figPath)

    plt.show()
    pausa()

def showGraphs():
    graph_base = Path("Graficas")

    if not graph_base.exists():
        print("No hay carpeta de gráficas.")
        pausa()
        return

    subfolders = [f for f in graph_base.iterdir() if f.is_dir()]
    if not subfolders:
        print("No hay subcarpetas de gráficas disponibles.")
        pausa()
        return

    print("Tipos de gráficas guardadas:")
    for i, folder in enumerate(subfolders, start=1):
        print(f"{i}. {folder.name}")
    
    try:
        folder_choice = int(input("Selecciona una carpeta (0 para salir): "))
        if folder_choice == 0:
            return
        if 1 <= folder_choice <= len(subfolders):
            selected_folder = subfolders[folder_choice - 1]
        else:
            print("Opción inválida.")
            pausa()
            return
    except ValueError:
        print("Entrada inválida.")
        pausa()
        return

    images = list(selected_folder.glob("*.png"))
    if not images:
        print("No hay imágenes en esta carpeta.")
        pausa()
        return

    print(f"Imágenes en {selected_folder.name}:")
    for i, img in enumerate(images, start=1):
        print(f"{i}. {img.name}")

    try:
        img_choice = int(input("Selecciona una imagen para abrir (0 para salir): "))
        if img_choice == 0:
            return
        if 1 <= img_choice <= len(images):
            img_path = images[img_choice - 1]
            os.startfile(img_path)  # Abre la imagen con el visor predeterminado de Windows
        else:
            print("Opción inválida.")
    except ValueError:
        print("Entrada inválida.")
    
    pausa()


def menuOp2():
    print("Generacion de Graficas.")
    print("1. Elegir tipo de Graficas")
    print("2. Mostrar graficas guardadas")
    print("3. Atrás")

#Funcion para escoger opciones de generacion de Grafica
def option2():
    while True:
        limpiar()
        menuOp2()
        option = int(input("Ingrese una opcion: "))
        #Se llama la funcion limpiar para que limpie la pantalla cada vez que escoge
        limpiar()
        if option == 1:
            MenuTypeOfGrafic()
        elif option == 2:
            showGraphs()
        else:
            break

#Funcion para mostrar el menu con el tipo de Grafica y escoger
def MenuTypeOfGrafic():
    print("============================")
    print("      Generar Graficos")
    print("============================")
    print("Tipo de Grafica: ")
    print("1. Gráfico de Barras")
    print("2. Gráfico de dispersión")
    print("3. Grafico lineal")
    print("4. Atrás")
    op = int(input("Ingresa una Opción: "))
    limpiar()
    if(op >= 1 or op <= 4):
        createGraph(op)
    else:
        print("Opción invalida.")
        pausa()
        limpiar()
        MenuTypeOfGrafic()