"""
Sistema de Evaluación de Calidad del Agua
Módulo: Gestión de Datos y Evaluación de Parámetros
"""
import os
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from config import config
import matplotlib.pyplot as plt

# ======================
# Constantes y Configuraciones
# ======================

#Lista de parametros de calidad, con su correspondiente unidad, rango, descripción y recomendación segun el ICA
PARAMETROS_CALIDAD = {
    "pH": {
        "unidades": "unidades",
        "rango_normal": (6.5, 8.5),
        "descripcion": "Medida de acidez o alcalinidad. Valores extremos afectan la vida acuática.",
        "recomendacion": "Ajustar el pH con agentes acidificantes o alcalinizantes según el desbalance detectado."
    },
    "Temperatura": {
        "unidades": "°C",
        "rango_normal": (10, 25),
        "descripcion": "Temperatura favorable para organismos acuáticos y oxígeno disuelto.",
        "recomendacion": "Controlar fuentes de calor o frío, evitar descargas térmicas industriales."
    },
    "Turbidez": {
        "unidades": "NTU",
        "rango_normal": (0, 5),
        "descripcion": "Medida de claridad del agua. Alta turbidez puede indicar contaminación por sedimentos o residuos.",
        "recomendacion": "Implementar filtración y control de escorrentías para reducir partículas suspendidas."
    },
    "Oxígeno Disuelto": {
        "unidades": "mg/L",
        "rango_normal": (5, 12),
        "descripcion": "Esencial para la vida acuática. Niveles bajos indican contaminación orgánica.",
        "recomendacion": "Mejorar la aireación del agua e identificar fuentes de materia orgánica para reducir su entrada."
    },
    "Conductividad": {
        "unidades": "µS/cm",
        "rango_normal": (100, 1000),
        "descripcion": "Mide la cantidad de sales y minerales disueltos en el agua.",
        "recomendacion": "Revisar descargas de aguas industriales y actividades agrícolas cercanas."
    },
    "Nitratos": {
        "unidades": "mg/L",
        "rango_normal": (0, 10),
        "descripcion": "Provienen de fertilizantes y aguas residuales. Contribuyen a la eutrofización.",
        "recomendacion": "Reducir el uso de fertilizantes y controlar fuentes de aguas residuales domésticas y agrícolas."
    },
    "Fosfatos": {
        "unidades": "mg/L",
        "rango_normal": (0, 0.1),
        "descripcion": "Nutriente que en exceso promueve el crecimiento de algas nocivas.",
        "recomendacion": "Limitar el uso de detergentes y fertilizantes con fósforo, y mejorar el tratamiento de aguas residuales."
    },
    "Coliformes Fecales": {
        "unidades": "UFC/100 mL",
        "rango_normal": (0, 200),
        "descripcion": "Indicador de contaminación biológica por desechos fecales.",
        "recomendacion": "Identificar y eliminar fuentes de contaminación fecal. Tratar el agua con desinfección (cloración o UV)."
    },
    "Demanda Bioquímica de Oxígeno DBO": {
        "unidades": "mg/L",
        "rango_normal": (0, 5),
        "descripcion": "Cantidad de oxígeno requerida para descomponer materia orgánica en el agua.",
        "recomendacion": "Reducir la descarga de materia orgánica y mejorar el tratamiento de aguas residuales."
    },
    "Sólidos Totales Disueltos TDS": {
        "unidades": "mg/L",
        "rango_normal": (200, 500),
        "descripcion": "Concentración total de sustancias disueltas. Valores altos afectan el sabor y uso del agua.",
        "recomendacion": "Filtrar el agua y controlar la fuente de contaminantes disueltos, como fertilizantes o aguas industriales."
    }
}


# ======================
# Funciones de Utilidad
# ======================

def limpiarConsola():
    #Limpia la pantalla de la consola
    os.system('cls')

def pausarConsola():
    #Pausa la ejecución hasta que el usuario presione una tecla
    os.system("pause")

def formatearNombreArchivo(parametro):
    #Convierte un nombre de parámetro a formato de nombre de archivo
    return f"DATOS_{parametro.replace(' ', '_').replace('(', '').replace(')', '')}.xlsx"

# ======================
# Funciones del Menú
# ======================

def mostrarMenuPrincipal():
    #Muestra el menú principal de evaluación de calidad
    print("\n" + "="*40)
    print("    EVALUACIÓN DE CALIDAD DEL AGUA")
    print("="*40)
    print(f"\nCuerpo de agua activo: {config.activeWaterBody or 'Ninguno'}")
    print("\n1. Ingresar datos de parámetros")
    print("2. Evaluar parámetros actuales")
    print("3. Visualizar datos")
    print("4. Realizar predicciones")
    print("5. Evaluación de la calidad segun el ICA")
    print("6. Volver al menú anterior")

def mostrarMenuIngresoDatos():
    #Muestra el submenú para ingreso de datos
    print("\n" + "="*40)
    print("     INGRESO DE DATOS")
    print("="*40)
    print("\n1. Crear nuevo registro de parámetro")
    print("2. Agregar datos a parámetro existente")
    print("3. Volver")

# =================================
# Funciones de Gestión de Archivos
# =================================

def obtenerRutaDatos():
    #Retorna la ruta a la carpeta de datos del cuerpo de agua activo
    return Path("CuerposDeAgua") / config.activeWaterBody / config.data_folder #CuerposDeAgua/Lago de bonanza/Datos

def listarArchivosDisponibles():
    #Lista los archivos Excel disponibles en la carpeta de datos
    rutaDatos = obtenerRutaDatos()
    #Si la carpeta no existe, retorna none
    if not rutaDatos.exists():
        return None
    #============================================================
    #Si si existe, retorna una lista con los nombres de los archivos terminados en .xlsx en la carpeta Datos
    return [archivo.name for archivo in rutaDatos.glob("*.xlsx")]

def seleccionarOpcion(mensaje, maxOpcion):
    #Maneja la selección de opciones del usuario
    while True:
        try:
            opcion = int(input(f"\n{mensaje} (0 para cancelar): "))
            if 0 <= opcion <= maxOpcion:
                return opcion
            print("Error: Número fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")

def seleccionarArchivo(archivos, mensaje):
    #Permite al usuario seleccionar un archivo de la lista
    print("\nArchivos disponibles:")
    #Ciclo que enumera los archivos disponibles
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")
    
    #Se le pide al usuario la opción
    opcion = seleccionarOpcion(mensaje, len(archivos))
    if opcion == 0:
        return None
    return archivos[opcion-1]

# ======================
# Funciones de Datos
# ======================

def seleccionarParametro():
    #Muestra lista de parámetros y permite seleccionar uno
    print("\nParámetros de calidad disponibles:")
    for i, parametro in enumerate(PARAMETROS_CALIDAD.keys(), 1):
        print(f"{i}. {parametro}")
    
    opcion = seleccionarOpcion("Seleccione el parámetro", len(PARAMETROS_CALIDAD))
    if opcion == 0:
        return None
    return list(PARAMETROS_CALIDAD.keys())[opcion-1]

def crearNuevoArchivo():
    #Crea un nuevo archivo de datos para un parámetro específico
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    #Se almacena en una variable el parametro seleccionado
    parametro = seleccionarParametro()
    #Si no existe, corta la ejecución de la función
    if not parametro:
        return

    #Se llama a la función para formatear el nombre del archivo
    nombreArchivo = formatearNombreArchivo(parametro)
    #Obtenemos la ruta Datos
    rutaDatos = obtenerRutaDatos()
    #Si no existe, creala
    rutaDatos.mkdir(parents=True, exist_ok=True)
    #La ruta del archivo es Datos nombreArchivo.xlsx
    rutaArchivo = rutaDatos / nombreArchivo

    #Si el archivo ya existe, imprimir en pantalla
    if rutaArchivo.exists():
        print(f"\nEl archivo para {parametro} ya existe. Use la opción 'Agregar datos'")
        pausarConsola()
        return

    #Se definen dos listas, que corresponden a las columnas de nuestro data frame
    fechas = []
    valores = []

    #Mensajes para el usuario
    print(f"\nIngrese datos para {parametro} (deje la fecha vacía para terminar):")
    print(f"Unidades: {PARAMETROS_CALIDAD[parametro]['unidades']}")
    print(f"Rango ideal: {PARAMETROS_CALIDAD[parametro]['rango_normal']}")
    print(f"Unidades: {PARAMETROS_CALIDAD[parametro]['descripcion']}")
    
    #Ciclo que pide fechas y valores y valida el formato de cada uno de estos hastas que se deja la fecha vacia
    while True:
        fecha = input("\nFecha (dd/mm/aa): ").strip()
        if not fecha:
            break
            
        try:
            datetime.strptime(fecha, "%d/%m/%y")
        except ValueError:
            print("Error: Formato inválido. Use dd/mm/aa")
            continue
            
        try:
            valor = float(input(f"Valor de {parametro}: "))
            fechas.append(fecha)
            valores.append(valor)
        except ValueError:
            print("Error: Ingrese un valor numérico válido")

    #Si no hay fechas, quiere decir que no se ingreso ningun dato
    if not fechas:
        print("No se ingresaron datos. Archivo no creado.")
        pausarConsola()
        #Se corta la ejecución de la función
        return

    #Definimos el data frame que es igual lo que retorna la función DataFrame de la libreria pandas
    #Que tiene como parametro un objeto con las fechas y los valores dados por el usuario
    df = pd.DataFrame({
        "Fecha": fechas,
        "Valor": valores,
    })
    
    #Se crea el archivo de excel en la ruta definida anteriormente
    df.to_excel(rutaArchivo, index=False)
    print(f"\nArchivo '{nombreArchivo}' creado con {len(df)} registros.")
    pausarConsola()

def agregarDatosExistente():
    #Agrega datos a un archivo de parámetro existente
    
    #Si no hay un cuerpo de agua activo en las configuraciones, corta la ejeciución
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    #Obten la lista de archivos disponibles
    archivos = listarArchivosDisponibles()
    #Si no hay, corta la ejecución y muestra un mensaje en pantalla
    if not archivos:
        print("No hay archivos de parámetros disponibles")
        pausarConsola()
        #Corta la ejecución de la función
        return

    #Almacena el archivo seleccionado
    archivoSeleccionado = seleccionarArchivo(archivos, "Seleccione parámetro para editar")
    #Si no se eligio ninguno, corta la ejecución
    if not archivoSeleccionado:
        return

    #Define la ruta del archivo en el que almacenar los nuevos datos
    rutaArchivo = obtenerRutaDatos() / archivoSeleccionado
    try:
        #Define el data frame que es igual a los datos del excel
        df = pd.read_excel(rutaArchivo)

        #Parametro es igual a el parametro formateado
        parametro = str(archivoSeleccionado).replace("DATOS_", "").replace("_", " ").replace(".xlsx", "")
    except Exception as e: #Manejo de errores
        print(f"Error al leer archivo: {e}")
        pausarConsola()
        return
    
    #Se obtiene el rango ideal del parametro actual, en el diccionario de parametros
    rangoideal = PARAMETROS_CALIDAD.get(parametro, {}).get('rango_normal', 'No disponible')
    
    #Mensajes para el usuario
    print(f"\nDatos actuales de {parametro} ({len(df)} registros):")
    print(df.to_string(index=False))
    print(f"\nRango ideal: {rangoideal}")

    #Se define una función con los nuevos datos ingresados
    nuevosDatos = []
    #Mensajes para el usuario
    print(f"\nIngrese nuevos datos para {parametro} (deje fecha vacía para terminar):")
    print(f"Unidades: {PARAMETROS_CALIDAD.get(parametro, {}).get('unidades', 'Desconocidas')}")
    
    #Se piden los nuevos datos, en el ciclo se valida que se tenga el formato correcto tanto para fecha como para los valores
    while True:
        fecha = input("\nFecha (dd/mm/aa): ").strip()
        if not fecha:
            break
        try:
            datetime.strptime(fecha, "%d/%m/%y")
        except ValueError:
            print("Error: Formato inválido. Use dd/mm/aa")
            continue
            
        try:
            valor = float(input(f"Valor de {parametro}: "))
            nuevosDatos.append({
                "Fecha": fecha,
                "Parámetro": parametro,
                "Valor": valor,
                "Unidades": PARAMETROS_CALIDAD[parametro]["unidades"]
            })
        except ValueError:
            print("Error: Ingrese un valor numérico válido")

    #Si no se ingresaron nuevos datos, muestralo en pantalla
    if not nuevosDatos:
        print("No se agregaron datos nuevos")
        pausarConsola()
        return

    # Combinar y guardar
    dfNuevos = pd.DataFrame(nuevosDatos)
    df = pd.concat([df, dfNuevos], ignore_index=True)
    df.to_excel(rutaArchivo, index=False)
    
    print(f"\nSe agregaron {len(dfNuevos)} registros. Total: {len(df)}")
    pausarConsola()

def evaluarParametros():
    #Evalúa los parámetros actuales contra sus rangos normales 
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    #Se listan archivos
    archivos = listarArchivosDisponibles()
    #SI no hay, corta la ejecución
    if not archivos:
        print("No hay parámetros registrados para evaluar")
        pausarConsola()
        return

    #Selecciona el archivo
    archivoSeleccionado = seleccionarArchivo(archivos, "Seleccione parámetro a evaluar")
    if not archivoSeleccionado:
        return

    # Cargar datos
    rutaArchivo = obtenerRutaDatos() / archivoSeleccionado
    try:
        df = pd.read_excel(rutaArchivo)
        
        # Verificar que el archivo tenga las columnas correctas
        if 'Fecha' not in df.columns or 'Valor' not in df.columns:
            print("Error: El archivo no tiene el formato correcto (debe contener 'Fecha' y 'Valor')")
            pausarConsola()
            return
            
        # Obtener el nombre del parámetro del nombre del archivo
        parametro = archivoSeleccionado.replace('DATOS_', '').replace('.xlsx', '').replace('_', ' ')
        ultimoValor = df['Valor'].iloc[-1]
        fechaUltimo = df['Fecha'].iloc[-1]
        
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        pausarConsola()
        return

    # Obtener Rango ideal
    rango = PARAMETROS_CALIDAD.get(parametro, {}).get("rango_normal")
    recomendacion = PARAMETROS_CALIDAD.get(parametro, {}).get("recomendacion")
    unidades = PARAMETROS_CALIDAD.get(parametro, {}).get("unidades", "Desconocidas")
    
    # Evaluar
    limpiarConsola()
    print("\n" + "="*40)
    print(f"   EVALUACIÓN DE {parametro.upper()}")
    print("="*40)
    print(f"\nÚltima medición: {fechaUltimo}")
    print(f"Valor actual: {ultimoValor} {unidades}")
    
    if rango:
        print(f"Rango ideal: {rango[0]} - {rango[1]} {unidades}")
        
        if ultimoValor < rango[0]:
            print("\nRESULTADO: VALOR POR DEBAJO DEL Rango ideal ⚠️")
            print(f"Recomendacion: {recomendacion}")
        elif ultimoValor > rango[1]:
            print("\nRESULTADO: VALOR POR ENCIMA DEL Rango ideal ⚠️")
            print(f"Recomendacion: {recomendacion}")
        else:
            print("\nRESULTADO: VALOR DENTRO DEL Rango ideal ✅")
    else:
        print("\nNo se encontró información de Rango ideal para este parámetro")
    
    # Mostrar tendencia si hay suficientes datos
    if len(df) > 1:
        tendencia = "↑ Aumentando" if df['Valor'].iloc[-1] > df['Valor'].iloc[-2] else "↓ Disminuyendo"
        print(f"\nTendencia: {tendencia} (vs medición anterior)")
    
    pausarConsola()

def realizarPredicciones():
    #Realiza predicciones basadas en datos históricos
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    #Se listan los archivos
    archivos = listarArchivosDisponibles()
    if not archivos:
        print("No hay archivos disponibles para predicción")
        pausarConsola()
        return

    #Se seleccionan los archivos
    archivoSeleccionado = seleccionarArchivo(archivos, "Seleccione archivo para predicción")
    if not archivoSeleccionado:
        return

    # Cargar datos
    rutaArchivo = obtenerRutaDatos() / archivoSeleccionado
    try:
        df = pd.read_excel(rutaArchivo)
        
        # Verificar columnas necesarias
        if 'Fecha' not in df.columns or 'Valor' not in df.columns:
            print("Error: El archivo debe contener columnas 'Fecha' y 'Valor'")
            pausarConsola()
            return
            
        # Convertir fechas
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%y', errors='coerce')
        if df['Fecha'].isnull().any():
            print("Error: Algunas fechas no pudieron ser interpretadas (formato dd/mm/aa)")
            pausarConsola()
            return
            
        # Calcular días desde primera fecha
        df['Dias'] = (df['Fecha'] - df['Fecha'].min()).dt.days
        
    except Exception as e:
        print(f"Error al procesar archivo: {e}")
        pausarConsola()
        return

    # Configurar predicción
    print("\nOpciones de predicción:")
    print("1. Días futuros")
    print("2. Semanas futuras")
    print("3. Meses futuros")
    print("4. Años futuros")
    
    try:
        #Selecciona como se quieren ver las predicciones
        unidadTiempo = int(input("Seleccione unidad de tiempo (1-4): "))
        if unidadTiempo not in [1, 2, 3, 4]:
            print("Error: Seleccione 1-4")
            pausarConsola()
            return
            
        periodos = int(input("Cantidad de períodos a predecir: "))
        if periodos <= 0:
            print("Error: Debe ser un número positivo")
            pausarConsola()
            return
    except ValueError:
        print("Error: Ingrese un número válido")
        pausarConsola()
        return

    # Calcular regresión lineal
    X = df['Dias'].values
    y = df['Valor'].values
    
    try:
        coeficientes = np.polyfit(X, y, 1)
        predictor = np.poly1d(coeficientes)
    except Exception as e:
        print(f"Error al calcular predicción: {e}")
        pausarConsola()
        return

    # Generar predicciones
    ultimaFecha = df['Fecha'].max()
    ultimoDia = df['Dias'].max()
    
    print("\nPredicciones:")
    print("-------------")
    print(f"Última fecha registrada: {ultimaFecha.strftime('%d/%m/%Y')}")
    print(f"Último valor registrado: {y[-1]:.2f}")
    print("-------------")
    
    timeDeltas = {
        1: timedelta(days=1),
        2: timedelta(weeks=1),
        3: timedelta(days=30),
        4: timedelta(days=365)
    }
    
    #Se listan los nombres de las unidades
    nombresUnidades = {1: "días", 2: "semanas", 3: "meses", 4: "años"}
    delta = timeDeltas[unidadTiempo]
    
    for i in range(1, periodos+1):
        fechaFutura = ultimaFecha + i * delta
        diasFuturos = ultimoDia + (fechaFutura - ultimaFecha).days
        valoresPrediccion = predictor(diasFuturos)
        
        print(f"{i} {nombresUnidades[unidadTiempo]}: {fechaFutura.strftime('%d/%m/%Y')} -> {valoresPrediccion:.2f}")
    
    pausarConsola()

def visualizarArchivo():
    #Muestra el contenido de un archivo seleccionado
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    #Se listan los archivos
    archivos = listarArchivosDisponibles()
    if not archivos:
        print("No hay archivos disponibles")
        pausarConsola()
        return

    #Se selecciona el archivo
    archivoSeleccionado = seleccionarArchivo(archivos, "Seleccione archivo a visualizar")
    #Si no se selecciono corta el flujo
    if not archivoSeleccionado:
        return

    # Mostrar datos
    rutaArchivo = obtenerRutaDatos() / archivoSeleccionado
    try:
        df = pd.read_excel(rutaArchivo, usecols=["Fecha", "Valor"])
        parametro = archivoSeleccionado.replace('DATOS_', '').replace('.xlsx', '').replace('_', ' ')
        
        limpiarConsola()
        print("\n" + "="*40)
        print(f"        DATOS DE {parametro.upper()}")
        print("="*40)
        print(f"\n{df.to_string(index=False)}")
        print(f"\nTotal registros: {len(df)}")
        
        if parametro in PARAMETROS_CALIDAD:
            print(f"Unidades: {PARAMETROS_CALIDAD[parametro]['unidades']}")
            print(f"Rango ideal: {PARAMETROS_CALIDAD[parametro]['rango_normal']}")
    except Exception as e:
        print(f"Error al leer archivo: {e}")
    
    pausarConsola()


def obtenerValores(rutaDatos, archivos):
    #Se define el diccionario de valores
    valores = {}

    #Extraemos el ultimo valor de cada archivo disponible
    for archivo in archivos:
        ruta = rutaDatos / archivo
        df   = pd.read_excel(ruta)

        if df.empty:
            continue

        ultimoValor = df["Valor"].iloc[-1]
        if isinstance(ultimoValor, np.generic):
            ultimoValor = ultimoValor.item()

        nombreParam = archivo.replace("DATOS_", "").replace(".xlsx", "").replace("_", " ")
        valores[nombreParam] = ultimoValor
    
    return valores
        

def evaluarCalidadICA():

    #Se obtiene la ruta base
    rutaDatos = obtenerRutaDatos()
    #Se crea una lista con los nombres de los archivos que terminan en xlsx en la carpeta Datos
    archivos   = [f.name for f in rutaDatos.glob("*.xlsx")]
    #Se obtienen los valores
    valores = obtenerValores(rutaDatos, archivos)
    
    #Definimos el diccionario de ponderaciones
    ponderaciones = {
        "pH": 0.11,
        "Temperatura": 0.10,
        "Turbidez": 0.08,
        "Oxígeno Disuelto": 0.17,
        "Conductividad": 0.07,
        "Nitratos": 0.10,
        "Fosfatos": 0.10,
        "Coliformes Fecales": 0.12,
        "Demanda Bioquímica de Oxígeno (DBO)": 0.10,
        "Sólidos Totales Disueltos (TDS)": 0.05
    }

    #Definimos el diccionario de rangos ideales segun ica
    rangosIdeales = {
        "pH": (6.5, 8.5),
        "Temperatura": (10, 25),
        "Turbidez": (0, 5),
        "Oxígeno Disuelto": (5, 12),
        "Conductividad": (100, 1000),
        "Nitratos": (0, 10),
        "Fosfatos": (0, 0.1),
        "Coliformes Fecales": (0, 200),
        "Demanda Bioquímica de Oxígeno DBO": (0, 5),
        "Sólidos Totales Disueltos TDS": (200, 500)
    }

    #Se definen la variables
    icaTotal = 0
    observaciones = []

    #Ciclo que recorre los valores de los parametros, evaluando la calidad de cada uno de ellos
    for parametro, valor in valores.items():
        #Si no existen parametros ideales registrados, pasa al siguiente item
        if parametro not in rangosIdeales:
            observaciones.append(f"{parametro} no se reconoce para ICA.")
            continue

        #Se desestructuran esos rangos ideales y se define el peso usando las ponderaciones
        minVal, maxVal = rangosIdeales[parametro]
        peso = ponderaciones.get(parametro, 0)

        #Si el valor esta dentro del rango ideal, su puntaje es 100
        if minVal <= valor <= maxVal:
            indice = 100
            observaciones.append(f"{parametro}\n   Rango ideal: {rangosIdeales[parametro]}\n   Valor actual: {valor}\n   Dentro del rango ✅\n")
        else:
            #Sino calcula su exeso
            exceso = max(abs(valor - minVal), abs(valor - maxVal))
            indice = max(0, 100 - exceso * 10)
        
        #Calcula el ica total
        icaTotal += indice * peso

        if not (minVal <= valor <= maxVal):
            observaciones.append(f"{parametro}\n   Rango ideal: {rangosIdeales[parametro]}\n   Valor actual: {valor}\n   Fuera del rango ⚠️\n")
        
    if icaTotal >= 91:
        nivel = "Excelente"
    elif icaTotal >= 71:
        nivel = "Buena"
    elif icaTotal >= 51:
        nivel = "Aceptable"
    elif icaTotal >= 26:
        nivel = "Mala"
    else:
        nivel = "Muy mala"

    #Se le muestra al usuario los resultados de la evaluación
    print("==============================================")
    print("Evaluación de la calidad del agua segun el ICA")
    print("==============================================\n")
    print(f"ICA: {round(icaTotal, 2)}%")
    print(f"Nivel de calidad: {nivel}")
    if len(archivos) < 10:
        print(f"Nota: No se tienen todos los parametros necesarios para la evaluación")
    print(f"\nObservaciones:")
    for observacion in observaciones:
        print(f"- {observacion}")

    pausarConsola()


def definirDiagramaPareto():
    #Se hace el analisis de pareto para los parametros
    
    #Se obtiene la ruta de los datos
    rutaDatos = obtenerRutaDatos()
    #Se extrae en una lista los archivos que terminan en xlsx dentro de la carpeta Datos
    archivos = [f.name for f in rutaDatos.glob("*.xlsx")]
    valores = obtenerValores(rutaDatos, archivos)

    #Se definen los rangos ideales
    rangosIdeales = {
        "pH": (6.5, 8.5),
        "Temperatura": (10, 25),
        "Turbidez": (0, 5),
        "Oxígeno Disuelto": (5, 12),
        "Conductividad": (100, 1000),
        "Nitratos": (0, 10),
        "Fosfatos": (0, 0.1),
        "Coliformes Fecales": (0, 200),
        "Demanda Bioquímica de Oxígeno (DBO)": (0, 5),
        "Sólidos Totales Disueltos (TDS)": (200, 500)
    }

    #Se define un diccionario
    impactosNegativos = {}

    #Ciclo en el que se calucla el ICA por parametro y luego se calcula el impacto negativo
    for parametro, valor in valores.items():
        if parametro not in rangosIdeales:
            continue
        
        minVal, maxVal = rangosIdeales[parametro]
        
        # Calcular puntaje ICA del parámetro
        if minVal <= valor <= maxVal:
            puntaje = 100
        else:
            if valor < minVal:
                exceso = minVal - valor
            else:  # valor > maxVal
                exceso = valor - maxVal

            puntaje = max(0, 100 - exceso * 10)

        # A menor puntaje, mayor impacto negativo (100 - puntaje)
        impacto = 100 - puntaje
        impactosNegativos[parametro] = impacto

    # Ordenar de mayor a menor impacto
    impactosOrdenados = dict(sorted(impactosNegativos.items(), key=lambda x: x[1], reverse=True))

    #Damos formato a la grafica
    etiquetas = list(impactosOrdenados.keys())
    valoresGrafica = list(impactosOrdenados.values())

    #Calculamos el total
    total = sum(valoresGrafica)
    #Definimos el diccionario de porcentajes acumulados
    porcentajesAcumulados = []
    acumulado = 0
    
    #Se recorren los valore y se calcula el acumulado
    for v in valoresGrafica:
        acumulado += v
        porcentaje = (acumulado / total) * 100 if total != 0 else 0
        porcentajesAcumulados.append(porcentaje)

    print(f"{parametro}: valor={valor:.2f}, puntaje ICA={puntaje:.2f}, impacto={impacto:.2f}")
    # === Gráfico ===
    fig, ax1 = plt.subplots()

    ax1.bar(etiquetas, valoresGrafica, color='skyblue')
    ax1.set_ylabel("Impacto negativo (100 - puntaje ICA)")
    ax1.set_title("Diagrama de Pareto - Impacto negativo por parámetro")
    ax1.tick_params(axis='x', rotation=45)

    ax2 = ax1.twinx()
    ax2.plot(etiquetas, porcentajesAcumulados, color="orange", marker="o", linestyle="-")
    ax2.set_ylabel("% acumulado")
    ax2.axhline(80, color='red', linestyle='--', linewidth=1)

    plt.tight_layout()
    plt.show()

    # === Conclusiones ===
    conclusiones = []
    for i, porcentaje in enumerate(porcentajesAcumulados):
        if porcentaje >= 80:
            conclusiones = etiquetas[:i+1]
            break

    print("\nConclusiones 80/20:")
    print("Los siguientes parámetros representan aproximadamente el 80% del impacto negativo en la calidad del agua:")
    for p in conclusiones:
        print(f"- {p}: Valor medido = {valores[p]}")

    pausarConsola()

            

# ======================
# Flujo Principal
# ======================

def menuIngresoDatos():
    """Maneja el submenú de ingreso de datos"""
    while True:
        limpiarConsola()
        mostrarMenuIngresoDatos()
        
        opcion = seleccionarOpcion("Seleccione opción", 3)
        limpiarConsola()
        
        if opcion == 1:
            crearNuevoArchivo()
        elif opcion == 2:
            agregarDatosExistente()
        elif opcion == 3:
            break

def ejecutarOpcion1():
    """Controla el flujo principal de la opción 1"""
    while True:
        limpiarConsola()
        mostrarMenuPrincipal()
        
        opcion = seleccionarOpcion("Seleccione opción", 6)
        limpiarConsola()
        
        if opcion == 1:
            menuIngresoDatos()
        elif opcion == 2:
            evaluarParametros()
        elif opcion == 3:
            visualizarArchivo()
        elif opcion == 4:
            realizarPredicciones()
        elif opcion == 5:
            evaluarCalidadICA()
        elif opcion == 6:
            break

if __name__ == "__main__":
    ejecutarOpcion1()