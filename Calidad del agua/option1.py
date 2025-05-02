import os
from pathlib import Path 
import pandas as pd
from datetime import datetime

def limpiar():
    os.system('cls')
def pausa():
    os.system("pause")

def menuOp1():
    print("Evaluación de calidad del agua.")
    print("1. Ingresar datos manualmente")
    print("2. importar archivos de datos")
    print("3. volver atras")

def getDataMenu():
    print("Ingresando datos")
    print("1. Crear un archivo nuevo.")
    print("2. Agregar a un archivo existente.")
    print("3. Atras.")
    op = int(input("Ingresa una opción: "))
    if(op == 1):
        newFile()
    if(op == 2):
        addDataToExistingFile()

def newFile():
    fileName = input("Ingrese el nombre del archivo: ")
    carpeta = Path("Datos")
    carpeta.mkdir(exist_ok=True)

    file = carpeta / f"{fileName}.xlsx"

    if file.exists():
        print("El archivo ya existe.")
        newFile()
    else:
        dates = []
        values = []
        while True:
            while True:
                date = input("Ingresa la fecha (formato dd/mm/aa): ")
                try:
                    datetime.strptime(date, "%d/%m/%y")
                    break
                except ValueError:
                    print("Formato inválido. Usa dd/mm/aa.")

            try:
                value = float(input("Ingresa el valor: "))
            except ValueError:
                print("Valor inválido. Intenta de nuevo.")
                continue
            dates.append(date)
            values.append(value)

            while True:
                try:
                    op = int(input("¿Deseas agregar otro dato? (1. Sí, 2. No): "))
                    if op in (1, 2):
                        break
                    else:
                        print("Opción inválida.")
                except ValueError:
                    print("Debes ingresar un número (1 o 2).")

            if op == 2:
                break

        data = {
            "Fecha": dates,
            "Valor": values
        }
        print("El archivo no existe. Será creado ahora.")
        df = pd.DataFrame(data)
        df.to_excel(file, index=False)
        print(f"Archivo '{file}' creado correctamente.")

def addDataToExistingFile():
    carpeta = Path("Datos")
    archivos = [archivo.name for archivo in carpeta.glob("*.xlsx")]

    if not archivos:
        print("No hay archivos disponibles para editar.")
        return

    print("Archivos existentes:")
    for i, archivo in enumerate(archivos, start=1):
        print(f"{i}. {archivo}")
    
    # Elegir el archivo
    while True:
        try:
            op = int(input("Selecciona el número del archivo para agregar datos (0 para salir): "))
            if op == 0:
                return  # Volver al menú anterior
            if 1 <= op <= len(archivos):
                file_name = archivos[op - 1]
                break
            else:
                print("Opción inválida. Elige un número válido.")
        except ValueError:
            print("Por favor ingresa un número válido.")

    # Cargar el archivo seleccionado
    file = carpeta / file_name
    df = pd.read_excel(file)

    # Mostrar datos actuales del archivo
    print(f"\nContenido actual de '{file_name}':")
    print(df)

    # Agregar nuevos datos
    dates = []
    values = []
    while True:
        # Validar formato de fecha
        while True:
            date = input("Ingresa la fecha (formato dd/mm/aa): ")
            try:
                # Intentamos convertir la cadena a una fecha real
                datetime.strptime(date, "%d/%m/%y")
                break
            except ValueError:
                print("Formato inválido. Usa dd/mm/aa.")

        # Ingreso de valor
        try:
            value = float(input("Ingresa el valor: "))
        except ValueError:
            print("Valor inválido. Intenta de nuevo.")
            continue

        dates.append(date)
        values.append(value)

        # Preguntar si desea continuar
        while True:
            try:
                op = int(input("¿Deseas agregar otro dato? (1. Sí, 2. No): "))
                if op in (1, 2):
                    break
                else:
                    print("Opción inválida.")
            except ValueError:
                print("Debes ingresar un número (1 o 2).")

        if op == 2:
            break

    # Agregar los nuevos datos al DataFrame
    new_data = {
        "Fecha": dates,
        "Valor": values
    }
    new_df = pd.DataFrame(new_data)

    # Concatenar los datos actuales con los nuevos
    df = pd.concat([df, new_df], ignore_index=True)

    # Guardar el archivo actualizado
    df.to_excel(file, index=False)
    print(f"Datos agregados correctamente al archivo '{file_name}'.")


def option1():
    while True:
        menuOp1()
        option = int(input("ingrese una opcion: "))
        if option == 1:
            print("Opcion 1")
            getDataMenu()
            pausa()
            limpiar()
        elif option == 2:
            print("option 2")
            limpiar()
        else:
            print("option 3")
            break
    