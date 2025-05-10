import os
from pathlib import Path 
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from config import config

# Funciones auxiliares
def clean():
    os.system('cls')
def pause():
    os.system("pause")

# Menú de la opción 1
def menuOp1():
    print("Evaluación de calidad del agua.")
    print(f"Cuerpo de agua activo: {config.activeWaterBody}")
    print("\n1. Ingresar datos manualmente")
    print("2. Importar archivos de datos")
    print("3. Imprimir un archivo existente")
    print("4. Hacer predicciones")
    print("5. Volver atrás")

# Función para crear nuevo archivo
def newFile():
    if not config.activeWaterBody:
        print("Error: No hay ningún cuerpo de agua seleccionado.")
        pause()
        return

    fileName = input("Ingrese el nombre del archivo (sin extensión): ").strip()
    if not fileName:
        print("Error: El nombre no puede estar vacío.")
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
        return

    # Estructura de carpetas
    base_folder = Path("CuerposDeAgua") / config.activeWaterBody
    data_folder = base_folder / config.data_folder
    data_folder.mkdir(parents=True, exist_ok=True)

    file_path = data_folder / f"{fileName}.xlsx"

    if file_path.exists():
        print(f"Error: El archivo '{fileName}.xlsx' ya existe.")
        pause()
        return

    # Recolección de datos
    dates = []
    values = []
    
    print("\nIngrese los datos (deje la fecha vacía para terminar):")
    while True:
        date = input("\nFecha (dd/mm/aa): ").strip()
        if not date:
            break
            
        try:
            datetime.strptime(date, "%d/%m/%y")
        except ValueError:
            print("Error: Formato de fecha inválido. Use dd/mm/aa")
            continue
            
        try:
            value = float(input("Valor numérico: "))
            dates.append(date)
            values.append(value)
        except ValueError:
            print("Error: Ingrese un valor numérico válido")

    if not dates:
        print("No se ingresaron datos. Archivo no creado.")
        pause()
        return

    # Crear DataFrame y guardar
    df = pd.DataFrame({"Fecha": dates, "Valor": values})
    df.to_excel(file_path, index=False)
    print(f"\nArchivo '{fileName}.xlsx' creado exitosamente con {len(df)} registros.")
    pause()

# Función para agregar datos a archivo existente
def addDataToExistingFile():
    #Damos formato usando la libreria path
    folder = Path("Datos")
    #En este array se almacenan los nombres de todos los archivos en la carpeta "Datos" que tengan la extensión ".xlsx".
    files = [archivo.name for archivo in folder.glob("*.xlsx")]
    
    #Si la carpeta está vacia, muestra un mensaje.
    if not files:
        if not config.activeWaterBody:
            print("Error: No hay ningún cuerpo de agua seleccionado.")
            pause()
            return

    # Obtener lista de archivos
    data_folder = Path("CuerposDeAgua") / config.activeWaterBody / config.data_folder
    if not data_folder.exists():
        print("Error: No existe la carpeta de datos para este cuerpo de agua.")
        pause()
        return

    archivos = [archivo.name for archivo in data_folder.glob("*.xlsx")]
    if not archivos:
        print("No hay archivos disponibles para editar.")
        pause()
        return

    #Si hay archivos dentro de la carpeta, imprime la lista en pantalla.
    print("files existentes:")
    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")
    
    # Elegir el archivo.
    # Mostrar archivos disponibles
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")

    # Selección de archivo
    while True:
        try:
            op = int(input("Sselectiona el número del archivo para agregar datos (0 para salir): "))
            op = input("\nSeleccione el archivo (0 para cancelar): ")
            op = int(op)
            if op == 0:
                return  # Volver al menú anterior.
            if 1 <= op <= len(files):
                fileName = files[op - 1]
                return
            if 1 <= op <= len(archivos):
                selected_file = archivos[op-1]
                break
            print("Error: Número fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")

    # Cargar el archivo sselectionado.
    file = folder / fileName
    df = pd.read_excel(file)

    # Mostrar datos actuales del archivo.
    print(f"\nContenido actual de '{fileName}':")
    print(df)
    # Cargar archivo existente
    file_path = data_folder / selected_file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        pause()
        return

    print(f"\nDatos actuales en '{selected_file}':")
    print(df.to_string(index=False))

    # Ingresar nuevos datos
    new_dates = []
    new_values = []
    
    print("\nIngrese los nuevos datos (deje la fecha vacía para terminar):")
    while True:
        date = input("\nFecha (dd/mm/aa): ").strip()
        if not date:
            break
            
        try:
            datetime.strptime(date, "%d/%m/%y")
        except ValueError:
            print("Error: Formato de fecha inválido. Use dd/mm/aa")
            continue
            
        try:
            value = float(input("Valor numérico: "))
            new_dates.append(date)
            new_values.append(value)
        except ValueError:
            print("Error: Ingrese un valor numérico válido")

    if not new_dates:
        print("No se ingresaron nuevos datos.")
        pause()
        return

    # Combinar datos y guardar
    new_df = pd.DataFrame({"Fecha": new_dates, "Valor": new_values})
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_excel(file_path, index=False)
    
    print(f"\nSe agregaron {len(new_df)} registros al archivo '{selected_file}'")
    print("Datos actualizados:")
    print(df.to_string(index=False))
    pause()

# Función para imprimir archivo existente
def printExistingFile():
    if not config.activeWaterBody:
        print("Error: No hay ningún cuerpo de agua seleccionado.")
        pause()
        return

    # Obtener lista de archivos
    data_folder = Path("CuerposDeAgua") / config.activeWaterBody / config.data_folder
    if not data_folder.exists():
        print("Error: No existe la carpeta de datos para este cuerpo de agua.")
        pause()
        return

    archivos = [archivo.name for archivo in data_folder.glob("*.xlsx")]
    if not archivos:
        print("No hay archivos disponibles para mostrar.")
        pause()
        return

    # Mostrar archivos disponibles
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")

    # Selección de archivo
    while True:
        try:
            op = input("\nSeleccione el archivo a imprimir (0 para cancelar): ")
            op = int(op)
            if op == 0:
                return
            if 1 <= op <= len(archivos):
                selected_file = archivos[op-1]
                break
            print("Error: Número fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")

    # Leer y mostrar archivo
    file_path = data_folder / selected_file
    try:
        df = pd.read_excel(file_path)
        print(f"\nContenido de '{selected_file}':")
        print(df.to_string(index=False))
        print(f"\nTotal de registros: {len(df)}")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
    
    pause()

# Función para hacer predicciones
def predictions():
    if not config.activeWaterBody:
        print("Error: No hay ningún cuerpo de agua seleccionado.")
        pause()
        return

    # Obtener lista de archivos
    data_folder = Path("CuerposDeAgua") / config.activeWaterBody / config.data_folder
    if not data_folder.exists():
        print("Error: No existe la carpeta de datos para este cuerpo de agua.")
        pause()
        return

    archivos = [archivo.name for archivo in data_folder.glob("*.xlsx")]
    if not archivos:
        print("No hay archivos disponibles para análisis.")
        pause()
        return

    # Mostrar archivos disponibles
    print("\nArchivos disponibles para predicción:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")

    # Selección de archivo
    while True:
        try:
            op = input("\nSeleccione el archivo (0 para cancelar): ")
            op = int(op)
            if op == 0:
                return
            if 1 <= op <= len(archivos):
                selected_file = archivos[op-1]
                break
            print("Error: Número fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")

    # Procesar archivo
    file_path = data_folder / selected_file
    try:
        df = pd.read_excel(file_path)
        
        # Verificar columnas necesarias
        if 'Fecha' not in df.columns or 'Valor' not in df.columns:
            print("Error: El archivo debe contener columnas 'Fecha' y 'Valor'")
            pause()
            return
            
        # Convertir fechas
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%y', errors='coerce')
        if df['Fecha'].isnull().any():
            print("Error: Algunas fechas no pudieron ser interpretadas (formato dd/mm/aa)")
            pause()
            return
            
        # Calcular días desde primera fecha
        df['Dias'] = (df['Fecha'] - df['Fecha'].min()).dt.days
        
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        pause()
        return

    # Configurar predicción
    print("\nOpciones de predicción:")
    print("1. Días futuros")
    print("2. Semanas futuras")
    print("3. Meses futuros")
    print("4. Años futuros")
    
    while True:
        try:
            time_unit = int(input("Seleccione unidad de tiempo: "))
            if time_unit not in [1, 2, 3, 4]:
                print("Error: Seleccione 1-4")
                continue
                
            steps = int(input("Cantidad de períodos a predecir: "))
            if steps <= 0:
                print("Error: Debe ser un número positivo")
                continue
                
            break
        except ValueError:
            print("Error: Ingrese un número válido")

    # Calcular regresión lineal
    X = df['Dias'].values
    y = df['Valor'].values
    
    try:
        coefficients = np.polyfit(X, y, 1)
        predictor = np.poly1d(coefficients)
    except Exception as e:
        print(f"Error al calcular predicción: {e}")
        pause()
        return

    # Generar predicciones
    last_date = df['Fecha'].max()
    last_days = df['Dias'].max()
    
    print("\nPredicciones:")
    print("-------------")
    print(f"Fecha actual: {last_date.strftime('%d/%m/%Y')}")
    print(f"Valor actual: {y[-1]:.2f}")
    print("-------------")
    
    time_deltas = {
        1: timedelta(days=1),
        2: timedelta(weeks=1),
        3: timedelta(days=30),
        4: timedelta(days=365)
    }
    
    delta = time_deltas[time_unit]
    unit_names = {1: "días", 2: "semanas", 3: "meses", 4: "años"}
    
    for i in range(1, steps+1):
        future_date = last_date + i * delta
        future_days = last_days + (future_date - last_date).days
        predicted_value = predictor(future_days)
        
        print(f"{i} {unit_names[time_unit]}: {future_date.strftime('%d/%m/%Y')} -> {predicted_value:.2f}")
    
    pause()

# Función principal de la opción 1
def option1():
    while True:
        menuOp1()
        try:
            option = int(input("\nIngrese una opción: "))
            clean()
            
            if option == 1:
                getDataMenu()
            elif option == 2:
                clean()
                # Implementación de importar archivos
                print("Función de importar archivos no implementada aún")
                pause()
            elif option == 3:
                printExistingFile()
            elif option == 4:
                predictions()
            elif option == 5:
                break
            else:
                print("Opción inválida.")
                pause()
        except ValueError:
            print("Error: Ingrese un número válido")
            pause()
        clean()

# Menú para ingreso de datos
def getDataMenu():
    while True:
        clean()
        print("Ingreso de datos")
        print("1. Crear nuevo archivo")
        print("2. Agregar a archivo existente")
        print("3. Volver")
        
        try:
            op = int(input("Seleccione: "))
            if op == 1:
                newFile()
            elif op == 2:
                addDataToExistingFile()
            elif op == 3:
                break
            else:
                print("Opción inválida")
                pause()
        except ValueError:
            print("Error: Ingrese un número válido")
            pause()