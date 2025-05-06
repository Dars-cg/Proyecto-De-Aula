#En este archivo estamos haciendo las funciones de la opción 1, en la que tenemos la funcionalidad
#de evaluación de calidad del agua. 

import os
from pathlib import Path 
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
#Fin de las importaciones. (pathlib, pandas, datetime, os, numpy, openpyxl)

#Definimos las funciones para limpiar y hacer una pausa en la consola, usando la libreria os(Operative System).
def clean():
    os.system('cls')
def pause():
    os.system("pause")

#En esta función lo que hacemos es imprimir las sub-opciones de la opción 1.
def menuOp1():
    print("Evaluación de calidad del agua.")
    print("1. Ingresar datos manualmente")
    print("2. importar archivos de datos")
    print("3. Imprimir un archivo existente")
    print("4. Hacer predicciones")
    print("5. volver atras")

#Aqui imprimimos algunas opciones en las que el usuario puede decidir la manera en la que ingresa sus datos.
def getDataMenu():
    clean() #Limpiar consola
    print("Ingresando datos")
    print("1. Crear un archivo nuevo.")
    print("2. Agregar a un archivo existente.")
    print("3. Atras.")
    op = int(input("Ingresa una opción: "))
    if(op == 1):
        newFile()
    elif(op == 2):
        addDataToExistingFile()
    elif(op == 3):
        return
    else:
        print("Opción invalida.")
        pause()
        getDataMenu()

def newFile():
    fileName = input("Ingrese el nombre del archivo: ")
    print("")
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
                        print("")
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

def printExistingFile():
    carpeta = Path("Datos")
    archivos = [archivo.name for archivo in carpeta.glob("*.xlsx")]

    if not archivos:
        print("No hay archivos disponibles para mostrar.")
        pause()
        return

    print("Archivos disponibles:")
    for i, archivo in enumerate(archivos, start=1):
        print(f"{i}. {archivo}")

    while True:
        try:
            op = int(input("Selecciona el número del archivo a imprimir (0 para salir): "))
            if op == 0:
                return
            if 1 <= op <= len(archivos):
                file_name = archivos[op - 1]
                break
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor ingresa un número válido.")

    file_path = carpeta / file_name
    df = pd.read_excel(file_path)
    print(f"\nContenido del archivo '{file_name}':\n")
    print(df)
    print("")  # Línea extra para estética
    pause()
    


def predictions():
    carpeta = "Datos"  # Asegúrate de que el nombre coincide con el resto del código
    archivos = os.listdir(carpeta)
    archivos_excel = [f for f in archivos if f.endswith(".xlsx")]

    if not archivos_excel:
        print("No se encontraron archivos Excel en la carpeta 'Datos'.")
        pause()
        return

    print("Archivos disponibles:")
    for i, archivo in enumerate(archivos_excel, 1):
        print(f"{i}. {archivo}")

    try:
        eleccion = int(input("Seleccione un archivo por número: "))
        archivo_seleccionado = archivos_excel[eleccion - 1]
    except (IndexError, ValueError):
        print("Selección inválida.")
        pause()
        return

    ruta = os.path.join(carpeta, archivo_seleccionado)
    try:
        df = pd.read_excel(ruta)
        df.columns = df.columns.str.lower()  # Normaliza nombres de columna
        df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%y", errors="coerce")
        if df["fecha"].isnull().any():
            print("Algunas fechas no se pudieron convertir. Revisa el archivo.")
            pause()
            return
        df["dias"] = (df["fecha"] - df["fecha"].min()).dt.days
    except Exception as e:
        print("Error al procesar el archivo:", e)
        pause()
        return

    # Regresión lineal simple
    X = df["dias"].values
    y = df["valor"].values
    coef = np.polyfit(X, y, 1)
    modelo = np.poly1d(coef)

    # Selección de predicción
    print("\n¿En qué unidad quieres hacer predicciones?")
    print("1. Días")
    print("2. Meses")
    print("3. Años")
    try:
        unidad = int(input("Seleccione una opción (1-3): "))
        cantidad = int(input("¿Cuántos pasos a futuro quieres predecir?: "))
    except ValueError:
        print("Entrada inválida.")
        pause()
        return

    if unidad == 1:
        salto = timedelta(days=1)
    elif unidad == 2:
        salto = timedelta(days=30)
    elif unidad == 3:
        salto = timedelta(days=365)
    else:
        print("Unidad inválida.")
        pause()
        return

    fecha_base = df["fecha"].max()
    dias_base = df["dias"].max()

    print("\nPredicciones:")
    for i in range(1, cantidad + 1):
        fecha_pred = fecha_base + salto * i
        dias_pred = dias_base + (salto * i).days
        valor_pred = modelo(dias_pred)
        print(f"{fecha_pred.strftime('%d/%m/%y')}: {valor_pred:.2f}")
   

def option1():
    while True:
        menuOp1()
        option = int(input("ingrese una opcion: "))
        if option == 1:
            getDataMenu()
            pause()
            clean()
        elif option == 2:
            
            clean()
        elif option == 3:
            clean()
            printExistingFile()
            clean()
        elif option == 4:
            clean()
            print("Realizar predicciones")
            predictions()
            pause()
            clean()
        elif option == 5:
            clean()
            break
        else:
            print("Opción invalida.")
            pause()
            clean()
    