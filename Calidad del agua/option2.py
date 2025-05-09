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

#Funcion que nos imprime el menu de la opcion 2
def menuOp2():
    print("Generacion de Graficas.")
    print("1. Elegir tipo de Graficas")
    print("2. Mostrar Formato de Ejemplo")
    print("3. Atrás")

def lineGraph():
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
    ax.plot(dates, values)
    ax.set_title(fileName)
    ax.set_xlabel("Fecha")
    ax.set_ylabel(ylable)
    ax.grid(True)

    graphFolder = Path("Graficas") / "Lineas"
    graphFolder.mkdir(parents=True, exist_ok=True)

    date = datetime.now() 
    safe_date = date.strftime("%d-%m-%y_%H-%M-%S")
    figName = f"{ylable}-{safe_date}.png"
    figPath = graphFolder / figName
    plt.savefig(figPath)

    plt.show()
    pausa()

#Funcion para escoger opciones de generacion de Grafica
def option2():
    while True:
        limpiar()
        menuOp2()
        option = int(input("Ingrese una opcion: "))
        #Se llama la funcion limpiar para que limpie la pantalla cada vez que escoge
        limpiar()
        if option == 1:
            #methodData()
            #MenuTypeOfGrafic()
            testing()
        elif option == 2:
            print("Opcion 2")
        else:
            break

#Funcion para mostrar el menu con el tipo de Grafica y escoger
def MenuTypeOfGrafic():
    print("Tipo de Grafica.")
    print("1. Gráfico de Barras")
    print("2. Histograma")
    print("3. Gráfico de dispersión")
    print("4. Grafico lineal")
    print("5. Gráfico Circular")
    print("6. Atrás")
    option = int(input("Ingresa una Opción: "))
     #Se llama la funcion limpiar para que limpie la pantalla cada vez que escoge
    limpiar()
    while True:
        if option >= 1 and option <= 6:
            if option == 1:
                #methodData()
                #chartbar(df["Fecha"], df["Valor"])
                print("")
            elif option == 2:
                print("Opcion 2")
            elif option == 3:
                print("Opcion 3")
            elif option == 4:
                print("Opcion 4")
            elif option == 5:
                print("Opcion 5")
            else:
                print("Opcion 6")
                main.mainMenu()
        limpiar()

#Funcion para obtener datos del menu de tipos de Graficos
def methodData():
    print("Metodo para ingresar Datos.")
    print("1. Ingresar Datos Manualmente")
    print("2. Importar Archivo de Excel")
    print("3. Atrás")
    while True:
        option = int(input("Ingresa una Opción: "))
        limpiar()
        if option >= 1 and option <= 3:
            if option == 1:
                print("NEWFILE")
                #MenuTypeOfGrafic()
                pausa()
            elif option == 2:
                print("Opcion 2")
            else:
                menuOp2()
                break


#Funcion para Generar la Grafica de Barras
def chartbar(fechas, valores):
    plt.bar(fechas, valores)
    plt.title("Gráfico de Barras")
    plt.xlabel("Fecha")
    plt.ylabel("Valor")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()