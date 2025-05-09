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

# Función que se ejecuta si el usuario desea crear un archivo nuevo de datos.
def newFile():
    # ========= INGRESO DEL NOMBRE Y VERIFICACIÓN DE ARCHIVO =========

    fileName = input("Ingrese el nombre del archivo: ")  # Solicita el nombre para el nuevo archivo
    print("")  # jump de línea para mejorar la presentación

    # Se define la carpeta "Datos" usando Path para manejo seguro de rutas
    folder = Path("Datos")
    folder.mkdir(exist_ok=True)  # Crea la carpeta si no existe

    # Construye la ruta completa al archivo a crear
    file = folder / f"{fileName}.xlsx"

    # Verifica si el archivo ya existe. Si existe, reinicia la función (llamada recursiva)
    if file.exists():
        print("El archivo ya existe.")
        newFile()  # Vuelve a pedir un nuevo nombre
    else:
        # ========= INGRESO DE DATOS =========

        # Inicializa listas vacías para fechas y valores
        dates = []
        values = []

        # Ciclo principal para recolección de datos
        while True:
            # Solicita y valida la fecha en formato dd/mm/aa
            while True:
                date = input("Ingresa la fecha (formato dd/mm/aa): ")
                try:
                    datetime.strptime(date, "%d/%m/%y")  # Valida el formato
                    break
                except ValueError:
                    print("Formato inválido. Usa dd/mm/aa.")

            # Solicita y valida que el valor ingresado sea un número flotante
            try:
                value = float(input("Ingresa el valor: "))
            except ValueError:
                print("Valor inválido. Intenta de nuevo.")
                continue  # Vuelve a pedir la fecha y el valor

            # Almacena los datos válidos
            dates.append(date)
            values.append(value)

            # Pregunta al usuario si desea ingresar más datos
            while True:
                try:
                    op = int(input("¿Deseas agregar otro dato? (1. Sí, 2. No): "))
                    if op in (1, 2):
                        print("")
                        break  # Sal del ciclo si la opción es válida
                    else:
                        print("Opción inválida.")
                except ValueError:
                    print("Debes ingresar un número (1 o 2).")

            if op == 2:  # Si el usuario elige no agregar más datos
                break

        # ========= CREACIÓN DEL ARCHIVO EXCEL =========

        # Crea un diccionario con los datos recolectados
        data = {
            "Fecha": dates,
            "Valor": values
        }

        print("El archivo no existe. Será creado ahora.")

        # Convierte el diccionario a DataFrame y guarda el archivo en formato Excel
        df = pd.DataFrame(data)
        df.to_excel(file, index=False)

        print(f"Archivo '{file}' creado correctamente.")


#Función en la que podemos agregar datos a un registros a un archivo existente.
def addDataToExistingFile():
    #Damos formato usando la libreria path
    folder = Path("Datos")
    #En este array se almacenan los nombres de todos los archivos en la carpeta "Datos" que tengan la extensión ".xlsx".
    files = [archivo.name for archivo in folder.glob("*.xlsx")]
    
    #Si la carpeta está vacia, muestra un mensaje.
    if not files:
        print("No hay archivos disponibles para editar.")
        return

    #Si hay archivos dentro de la carpeta, imprime la lista en pantalla.
    print("files existentes:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    
    # Elegir el archivo.
    while True:
        try:
            op = int(input("Sselectiona el número del archivo para agregar datos (0 para salir): "))
            if op == 0:
                return  # Volver al menú anterior.
            if 1 <= op <= len(files):
                fileName = files[op - 1]
                break
            else:
                print("Opción inválida. Elige un número válido.")
        except ValueError:
            print("Por favor ingresa un número válido.")

    # Cargar el archivo sselectionado.
    file = folder / fileName
    df = pd.read_excel(file)

    # Mostrar datos actuales del archivo.
    print(f"\nContenido actual de '{fileName}':")
    print(df)

    # Agregar nuevos datos.
    #Creamos los arrays que representan a las fechas y los valores.
    dates = []
    values = []
    while True:
        # Validar formato de fecha.
        while True:
            date = input("Ingresa la fecha (formato dd/mm/aa): ")
            try:
                # Intentamos convertir la cadena a una fecha real.
                datetime.strptime(date, "%d/%m/%y")
                break
            except ValueError:
                print("Formato inválido. Usa dd/mm/aa.")

        # Ingreso de valor.
        try:
            value = float(input("Ingresa el valor: "))
        except ValueError:
            print("Valor inválido. Intenta de nuevo.")
            continue

        #Agrega los nuevos datos a los arrays.
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
    newData = {
        "Fecha": dates,
        "Valor": values
    }
    newDf = pd.DataFrame(newData)

    # Concatenar los datos actuales con los nuevos
    df = pd.concat([df, newDf], ignore_index=True)

    # Guardar el archivo actualizado
    df.to_excel(file, index=False)
    print(f"Datos agregados correctamente al archivo '{fileName}'.")


def printExistingFile():
    # ========= SELECCIÓN DE ARCHIVOS =========
    
    # Usa la clase Path para trabajar con rutas de archivos de forma más segura y clara
    folder = Path("Datos")

    # Obtiene una lista con los nombres de todos los archivos con extensión .xlsx en la carpeta
    files = [file.name for file in folder.glob("*.xlsx")]

    # Si no hay archivos disponibles, muestra un mensaje y finaliza la función
    if not files:
        print("No hay archivos disponibles para mostrar.")
        pause()
        return

    # Muestra la lista numerada de archivos disponibles
    print("Archivos disponibles:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    # ========= SELECCIÓN DEL ARCHIVO POR PARTE DEL USUARIO =========

    while True:
        try:
            # Solicita al usuario que elija un archivo por su número
            op = int(input("Sselectiona el número del archivo a imprimir (0 para salir): "))
            if op == 0:
                return  # Sale si elige 0
            if 1 <= op <= len(files):
                fileName = files[op - 1]  # Guarda el nombre del archivo sselectionado
                break
            else:
                print("Opción inválida.")  # Si el número está fuera de rango
        except ValueError:
            print("Por favor ingresa un número válido.")  # Si se ingresa un valor no numérico

    # ========= LECTURA Y MOSTRADO DEL ARCHIVO =========
    
    filePath = folder / fileName  # Construye la ruta completa al archivo
    df = pd.read_excel(filePath)    # Lee el archivo Excel como DataFrame de pandas

    print(f"\nContenido del archivo '{fileName}':\n")
    print(df)  # Muestra el contenido del DataFrame en consola
    print("")  # Línea vacía para mejor presentación
    pause()    # Pausa para que el usuario pueda ver el resultado antes de continuar



def predictions():
    # Define la carpeta donde se encuentran los archivos de datos
    folder = Path("Datos")
    # Filtra solo los archivos Excel (.xlsx)
    excelFiles = [file.name for file in folder.glob("*.xlsx")]

    # Verifica si hay archivos disponibles
    if not excelFiles:
        print("No se encontraron archivos Excel en la carpeta 'Datos'.")
        pause()
        return

    # Muestra la lista de archivos al usuario
    print("Archivos disponibles:")
    for i, file in enumerate(excelFiles, 1):
        print(f"{i}. {file}")

    # Solicita al usuario que elija uno de los archivos por número
    try:
        selection = int(input("Sselectione un archivo por número: "))
        selectedFile = excelFiles[selection - 1]
    except (IndexError, ValueError):
        print("Selección inválida.")
        pause()
        return

    # Construye la ruta completa del archivo sselectionado
    ruta = folder / selectedFile
    try:
        # Lee el archivo Excel
        df = pd.read_excel(ruta)

        # Convierte los nombres de columna a minúsculas por seguridad (e.g. 'Fecha' → 'fecha')
        df.columns = df.columns.str.lower()

        # Intenta convertir la columna 'fecha' al formato correcto dd/mm/aa
        df["fecha"] = pd.to_datetime(df["fecha"], format="%d/%m/%y", errors="coerce")

        # Si alguna fecha no se puede convertir, lanza una advertencia
        if df["fecha"].isnull().any():
            print("Algunas fechas no se pudieron convertir. Revisa el archivo.")
            pause()
            return

        # Calcula la cantidad de días desde la primera fecha registrada
        df["dias"] = (df["fecha"] - df["fecha"].min()).dt.days

    except Exception as e:
        print("Error al procesar el archivo:", e)
        pause()
        return

    # ========= REGRESIÓN LINEAL =========

    # Extrae los valores numéricos para regresión
    X = df["dias"].values  # Eje X: días desde la fecha inicial
    y = df["valor"].values  # Eje Y: valores de medición

    # Ajusta un modelo de regresión lineal simple: y = m*x + b
    coef = np.polyfit(X, y, 1)
    model = np.poly1d(coef)

    # ========= CONFIGURACIÓN DE PREDICCIÓN =========

    # Pregunta al usuario en qué unidad de tiempo quiere predecir
    print("\n¿En qué unidad quieres hacer predicciones?")
    print("1. Días")
    print("2. Meses")
    print("3. Años")
    try:
        unit = int(input("Sselectione una opción (1-3): "))
        quantity = int(input("¿Cuántos pasos a futuro quieres predecir?: "))
    except ValueError:
        print("Entrada inválida.")
        pause()
        return

    # Define el jump temporal según la unidad sselectionada
    if unit == 1:
        jump = timedelta(days=1)
    elif unit == 2:
        jump = timedelta(days=30)
    elif unit == 3:
        jump = timedelta(days=365)
    else:
        print("Unidad inválida.")
        pause()
        return

    # ========= GENERACIÓN DE PREDICCIONES =========

    baseDate = df["fecha"].max()   # Última fecha registrada en el archivo
    baseDays = df["dias"].max()     # Última cantidad de días desde el inicio

    print("\nPredicciones:")
    for i in range(1, quantity + 1):
        # Calcula la nueva fecha de predicción
        predDate = baseDate + jump * i

        # Calcula los días correspondientes a esa fecha predicha
        predDays = baseDays + (jump * i).days

        # Aplica el modelo de regresión para estimar el valor
        predValue = model(predDays)

        # Imprime el resultado en formato dd/mm/aa
        print(f"{predDate.strftime('%d/%m/%y')}: {predValue:.2f}")
  

# Función que gestiona el menú principal de la opción 1
def option1():
    # Ciclo principal que mantiene el menú activo hasta que el usuario elija salir
    while True:
        menuOp1()  # Muestra el submenú de opciones
        option = int(input("Ingrese una opción: "))  # Solicita al usuario que sselectione una opción

        if option == 1:
            # Opción 1: Obtener y guardar nuevos datos en un archivo Excel
            getDataMenu()
            pause()   # Espera que el usuario presione una tecla
            clean()   # Limpia la pantalla

        elif option == 2:
            # Opción 2: Reservada o sin implementar aún (por ahora solo limpia la pantalla)
            clean()

        elif option == 3:
            # Opción 3: Muestra el contenido de un archivo Excel existente
            clean()
            printExistingFile()
            clean()

        elif option == 4:
            # Opción 4: Realiza predicciones a partir de un archivo existente
            clean()
            print("Realizar predicciones")
            predictions()
            pause()
            clean()

        elif option == 5:
            # Opción 5: Salir del menú
            clean()
            break

        else:
            # Si la opción ingresada no es válida, se informa al usuario
            print("Opción inválida.")
            pause()
            clean()

    