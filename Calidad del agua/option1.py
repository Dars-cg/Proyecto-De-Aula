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
    """Limpia la pantalla de la consola"""
    os.system('cls')

def pausarConsola():
    """Pausa la ejecución hasta que el usuario presione una tecla"""
    os.system("pause")

def formatearNombreArchivo(parametro):
    """Convierte un nombre de parámetro a formato de nombre de archivo"""
    return f"DATOS_{parametro.replace(' ', '_').replace('(', '').replace(')', '')}.xlsx"

# ======================
# Funciones del Menú
# ======================

def mostrarMenuPrincipal():
    """Muestra el menú principal de evaluación de calidad"""
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
    """Muestra el submenú para ingreso de datos"""
    print("\n" + "="*40)
    print("     INGRESO DE DATOS")
    print("="*40)
    print("\n1. Crear nuevo registro de parámetro")
    print("2. Agregar datos a parámetro existente")
    print("3. Volver")

# ======================
# Funciones de Gestión de Archivos
# ======================

def normalizar_parametro(nombre):
    import re
    nombre = re.sub(r"[()]", "", nombre)
    nombre = " ".join(nombre.split())
    return nombre

def obtenerRutaDatos():
    """Retorna la ruta a la carpeta de datos del cuerpo de agua activo"""
    return Path("CuerposDeAgua") / config.activeWaterBody / config.data_folder #CuerposDeAgua/Lago de bonanza/Datos

def listarArchivosDisponibles():
    """Lista los archivos Excel disponibles en la carpeta de datos"""
    ruta_datos = obtenerRutaDatos()
    if not ruta_datos.exists():
        return None
    return [archivo.name for archivo in ruta_datos.glob("*.xlsx")]

def seleccionarOpcion(mensaje, max_opcion):
    """Maneja la selección de opciones del usuario"""
    while True:
        try:
            opcion = int(input(f"\n{mensaje} (0 para cancelar): "))
            if 0 <= opcion <= max_opcion:
                return opcion
            print("Error: Número fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")

def seleccionarArchivo(archivos, mensaje):
    """Permite al usuario seleccionar un archivo de la lista"""
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(archivos, 1):
        print(f"{i}. {archivo}")
    
    opcion = seleccionarOpcion(mensaje, len(archivos))
    if opcion == 0:
        return None
    return archivos[opcion-1]

# ======================
# Funciones de Datos
# ======================

def seleccionarParametro():
    """Muestra lista de parámetros y permite seleccionar uno"""
    print("\nParámetros de calidad disponibles:")
    for i, parametro in enumerate(PARAMETROS_CALIDAD.keys(), 1):
        print(f"{i}. {parametro}")
    
    opcion = seleccionarOpcion("Seleccione el parámetro", len(PARAMETROS_CALIDAD))
    if opcion == 0:
        return None
    return list(PARAMETROS_CALIDAD.keys())[opcion-1]

def crearNuevoArchivo():
    """Crea un nuevo archivo de datos para un parámetro específico"""
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    parametro = seleccionarParametro()
    if not parametro:
        return

    nombre_archivo = formatearNombreArchivo(parametro)
    ruta_datos = obtenerRutaDatos()
    ruta_datos.mkdir(parents=True, exist_ok=True)
    ruta_archivo = ruta_datos / nombre_archivo

    if ruta_archivo.exists():
        print(f"\nEl archivo para {parametro} ya existe. Use la opción 'Agregar datos'")
        pausarConsola()
        return

    fechas = []
    valores = []

    print(f"\nIngrese datos para {parametro} (deje la fecha vacía para terminar):")
    print(f"Unidades: {PARAMETROS_CALIDAD[parametro]['unidades']}")
    print(f"Rango ideal: {PARAMETROS_CALIDAD[parametro]['rango_normal']}")
    print(f"Unidades: {PARAMETROS_CALIDAD[parametro]['descripcion']}")
    
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

    if not fechas:
        print("No se ingresaron datos. Archivo no creado.")
        pausarConsola()
        return

    df = pd.DataFrame({
        "Fecha": fechas,
        "Valor": valores,
    })
    
    df.to_excel(ruta_archivo, index=False)
    print(f"\nArchivo '{nombre_archivo}' creado con {len(df)} registros.")
    pausarConsola()

def agregarDatosExistente():
    """Agrega datos a un archivo de parámetro existente"""
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    archivos = listarArchivosDisponibles()
    if not archivos:
        print("No hay archivos de parámetros disponibles")
        pausarConsola()
        return

    archivo_seleccionado = seleccionarArchivo(archivos, "Seleccione parámetro para editar")
    if not archivo_seleccionado:
        return

    ruta_archivo = obtenerRutaDatos() / archivo_seleccionado
    try:
        df = pd.read_excel(ruta_archivo)

        parametro = str(archivo_seleccionado).replace("DATOS_", "").replace("_", " ").replace(".xlsx", "")

    except Exception as e:
        print(f"Error al leer archivo: {e}")
        pausarConsola()
        return
    rangoideal = PARAMETROS_CALIDAD.get(parametro, {}).get('rango_normal', 'No disponible')
    print(f"\nDatos actuales de {parametro} ({len(df)} registros):")
    print(df.to_string(index=False))
    print(f"\nRango ideal: {rangoideal}")

    nuevos_datos = []
    print(f"\nIngrese nuevos datos para {parametro} (deje fecha vacía para terminar):")
    print(f"Unidades: {PARAMETROS_CALIDAD.get(parametro, {}).get('unidades', 'Desconocidas')}")
    
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
            nuevos_datos.append({
                "Fecha": fecha,
                "Parámetro": parametro,
                "Valor": valor,
                "Unidades": PARAMETROS_CALIDAD[parametro]["unidades"]
            })
        except ValueError:
            print("Error: Ingrese un valor numérico válido")

    if not nuevos_datos:
        print("No se agregaron datos nuevos")
        pausarConsola()
        return

    # Combinar y guardar
    df_nuevos = pd.DataFrame(nuevos_datos)
    df = pd.concat([df, df_nuevos], ignore_index=True)
    df.to_excel(ruta_archivo, index=False)
    
    print(f"\nSe agregaron {len(df_nuevos)} registros. Total: {len(df)}")
    pausarConsola()

def evaluarParametros():
    """Evalúa los parámetros actuales contra sus rangos normales"""
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    archivos = listarArchivosDisponibles()
    if not archivos:
        print("No hay parámetros registrados para evaluar")
        pausarConsola()
        return

    archivo_seleccionado = seleccionarArchivo(archivos, "Seleccione parámetro a evaluar")
    if not archivo_seleccionado:
        return

    # Cargar datos
    ruta_archivo = obtenerRutaDatos() / archivo_seleccionado
    try:
        df = pd.read_excel(ruta_archivo)
        
        # Verificar que el archivo tenga las columnas correctas
        if 'Fecha' not in df.columns or 'Valor' not in df.columns:
            print("Error: El archivo no tiene el formato correcto (debe contener 'Fecha' y 'Valor')")
            pausarConsola()
            return
            
        # Obtener el nombre del parámetro del nombre del archivo
        parametro = archivo_seleccionado.replace('DATOS_', '').replace('.xlsx', '').replace('_', ' ')
        ultimo_valor = df['Valor'].iloc[-1]
        fecha_ultimo = df['Fecha'].iloc[-1]
        
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
    print(f"\nÚltima medición: {fecha_ultimo}")
    print(f"Valor actual: {ultimo_valor} {unidades}")
    
    if rango:
        print(f"Rango ideal: {rango[0]} - {rango[1]} {unidades}")
        
        if ultimo_valor < rango[0]:
            print("\nRESULTADO: VALOR POR DEBAJO DEL Rango ideal ⚠️")
            print(f"Recomendacion: {recomendacion}")
        elif ultimo_valor > rango[1]:
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
    """Realiza predicciones basadas en datos históricos"""
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    archivos = listarArchivosDisponibles()
    if not archivos:
        print("No hay archivos disponibles para predicción")
        pausarConsola()
        return

    archivo_seleccionado = seleccionarArchivo(archivos, "Seleccione archivo para predicción")
    if not archivo_seleccionado:
        return

    # Cargar datos
    ruta_archivo = obtenerRutaDatos() / archivo_seleccionado
    try:
        df = pd.read_excel(ruta_archivo)
        
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
        unidad_tiempo = int(input("Seleccione unidad de tiempo (1-4): "))
        if unidad_tiempo not in [1, 2, 3, 4]:
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
        coefficients = np.polyfit(X, y, 1)
        predictor = np.poly1d(coefficients)
    except Exception as e:
        print(f"Error al calcular predicción: {e}")
        pausarConsola()
        return

    # Generar predicciones
    last_date = df['Fecha'].max()
    last_days = df['Dias'].max()
    
    print("\nPredicciones:")
    print("-------------")
    print(f"Última fecha registrada: {last_date.strftime('%d/%m/%Y')}")
    print(f"Último valor registrado: {y[-1]:.2f}")
    print("-------------")
    
    time_deltas = {
        1: timedelta(days=1),
        2: timedelta(weeks=1),
        3: timedelta(days=30),
        4: timedelta(days=365)
    }
    
    unit_names = {1: "días", 2: "semanas", 3: "meses", 4: "años"}
    delta = time_deltas[unidad_tiempo]
    
    for i in range(1, periodos+1):
        future_date = last_date + i * delta
        future_days = last_days + (future_date - last_date).days
        predicted_value = predictor(future_days)
        
        print(f"{i} {unit_names[unidad_tiempo]}: {future_date.strftime('%d/%m/%Y')} -> {predicted_value:.2f}")
    
    pausarConsola()

def visualizarArchivo():
    """Muestra el contenido de un archivo seleccionado"""
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    archivos = listarArchivosDisponibles()
    if not archivos:
        print("No hay archivos disponibles")
        pausarConsola()
        return

    archivo_seleccionado = seleccionarArchivo(archivos, "Seleccione archivo a visualizar")
    if not archivo_seleccionado:
        return

    # Mostrar datos
    ruta_archivo = obtenerRutaDatos() / archivo_seleccionado
    try:
        df = pd.read_excel(ruta_archivo, usecols=["Fecha", "Valor"])
        parametro = archivo_seleccionado.replace('DATOS_', '').replace('.xlsx', '').replace('_', ' ')
        
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
    valores = {}

    for archivo in archivos:
        ruta = rutaDatos / archivo
        df   = pd.read_excel(ruta)

        if df.empty:
            continue

        ultimo_valor = df["Valor"].iloc[-1]
        if isinstance(ultimo_valor, np.generic):
            ultimo_valor = ultimo_valor.item()

        nombre_param = archivo.replace("DATOS_", "").replace(".xlsx", "").replace("_", " ")
        valores[nombre_param] = ultimo_valor
    
    return valores
        

def evaluarCalidadICA():

    rutaDatos = obtenerRutaDatos()
    archivos   = [f.name for f in rutaDatos.glob("*.xlsx")]
    valores = obtenerValores(rutaDatos, archivos)
    
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

    icaTotal = 0
    observaciones = []

    for parametro, valor in valores.items():
        if parametro not in rangosIdeales:
            observaciones.append(f"{parametro} no se reconoce para ICA.")
            continue

        minVal, maxVal = rangosIdeales[parametro]
        peso = ponderaciones.get(parametro, 0)

        if minVal <= valor <= maxVal:
            indice = 100
            observaciones.append(f"{parametro}\n   Rango ideal: {rangosIdeales[parametro]}\n   Valor actual: {valor}\n   Dentro del rango ✅\n")
        else:
            exceso = max(abs(valor - minVal), abs(valor - maxVal))
            indice = max(0, 100 - exceso * 10)
        
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

    print("==============================================")
    print("Evaluación de la calidad del agua segun el ICA")
    print("==============================================\n")
    print(f"ICA: {round(icaTotal, 2)}")
    print(f"Nivel de calidad: {nivel}")
    if len(archivos) < 10:
        print(f"Nota: No se tienen todos los parametros necesarios para la evaluación")
    print(f"\nObservaciones:")
    for observacion in observaciones:
        print(f"- {observacion}")

    pausarConsola()


def definirDiagramaPareto():
    rutaDatos = obtenerRutaDatos()
    archivos = [f.name for f in rutaDatos.glob("*.xlsx")]
    valores = obtenerValores(rutaDatos, archivos)

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

    impactosNegativos = {}

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

    etiquetas = list(impactosOrdenados.keys())
    valoresGrafica = list(impactosOrdenados.values())

    total = sum(valoresGrafica)
    porcentajesAcumulados = []
    acumulado = 0
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