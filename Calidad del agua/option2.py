"""
Sistema de Gestión de Calidad del Agua
Módulo: Generación y Visualización de Gráficas
"""
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from config import config

# ======================
# Funciones de Utilidad
# ======================

def limpiarConsola():
    #Limpia la pantalla de la consola 
    os.system('cls')

def pausarConsola():
    #Pausa la ejecución hasta que el usuario presione una tecla 
    os.system("pause")

# ======================
# Funciones del Menú
# ======================

def mostrarMenuPrincipalGraficas():
    #Muestra el menú principal de generación de gráficas 
    print("=================================")
    print("     GENERACIÓN DE GRÁFICAS")
    print("=================================")
    print("\n1. Crear nueva gráfica")
    print("2. Visualizar gráficas guardadas")
    print("3. Volver al menú anterior")

def mostrarMenuTipoGrafica():
    #Muestra los tipos de gráficas disponibles 
    print("=========================")
    print("    TIPO DE GRÁFICA")
    print("=========================")
    print("\n1. Gráfico de Barras")
    print("2. Gráfico de Dispersión")
    print("3. Gráfico Lineal")
    print("4. Volver")

# ======================
# Funciones de Gráficas
# ======================

def obtenerRutaDatos():
    #Retorna la ruta a la carpeta de datos del cuerpo de agua activo 
    return Path(f"CuerposDeAgua/{config.activeWaterBody}/Datos")

def obtenerRutaGraficas(tipo=None):
    #Retorna la ruta a la carpeta de gráficas 
    base = Path(f"CuerposDeAgua/{config.activeWaterBody}/Graficas")
    if tipo:
        return base / tipo
    return base

def seleccionarArchivo(arvhivos, mensaje):
    #Permite al usuario seleccionar un archivo de la lista 
    print("\nArchivos disponibles:")
    for i, archivo in enumerate(arvhivos, 1):
        print(f"{i}. {archivo}")

    while True:
        try:
            opcion = int(input(f"\n{mensaje} (0 para cancelar): "))
            if opcion == 0:
                return None
            if 1 <= opcion <= len(arvhivos):
                return arvhivos[opcion-1]
            print("Error: Número fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")

def crearGrafica(tipoGrafica):
    """Crea y guarda una gráfica según el tipo seleccionado con opción de invertir eje X (fechas)"""
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    # Obtener lista de archivos disponibles
    rutaDatos = obtenerRutaDatos()
    if not rutaDatos.exists():
        print("Error: No hay datos disponibles.")
        pausarConsola()
        return

    archivos = [archivo.name for archivo in rutaDatos.glob("*.xlsx")]
    if not archivos:
        print("No hay archivos disponibles")
        pausarConsola()
        return

    # Seleccionar archivo
    archivoSeleccionado = seleccionarArchivo(archivos, "Seleccione archivo a graficar")
    if not archivoSeleccionado:
        return

    # Leer datos
    rutaArchivo = rutaDatos / archivoSeleccionado
    try:
        df = pd.read_excel(rutaArchivo)
        # Convertir fechas a datetime para ordenamiento correcto
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d/%m/%y')
        df = df.sort_values('Fecha')  # Ordenar por fecha
        fechas = df['Fecha']
        valores = df['Valor'].to_numpy()
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        pausarConsola()
        return

    # Configurar gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    nombreArchivo = archivoSeleccionado.replace(".xlsx", "")

    # Crear gráfico según tipo seleccionado
    tipos = {
        1: ("Barras", lambda: ax.bar(fechas, valores)),
        2: ("Dispersion", lambda: ax.scatter(fechas, valores)),
        3: ("Lineal", lambda: ax.plot(fechas, valores, marker='o'))
    }

    if tipoGrafica not in tipos:
        print("Error: Tipo de gráfica inválido")
        pausarConsola()
        return

    nombreTipo, funcionGrafica = tipos[tipoGrafica]
    funcionGrafica()

    # Configuración del gráfico
    ax.set_title(nombreArchivo)
    ax.set_xlabel("Fecha")
    ax.set_ylabel(nombreArchivo)
    ax.grid(True)
    
    # Formatear fechas para mejor visualización
    plt.xticks(rotation=45)
    fig.autofmt_xdate()
    
    # Preguntar si desea invertir el eje X (fechas)
    invertir = input("\n¿Desea invertir el eje de fechas (mostrar más recientes primero)? (s/n): ").lower()
    if invertir == 's':
        ax.invert_xaxis()

    # Guardar gráfico
    rutaGraficas = obtenerRutaGraficas(nombreTipo)
    rutaGraficas.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    nombreGrafica = f"{nombreArchivo}-{timestamp}.png"
    rutaCompleta = rutaGraficas / nombreGrafica

    plt.tight_layout()  # Ajustar layout para que no se corten las etiquetas
    plt.savefig(rutaCompleta)
    plt.show()
    print(f"\nGráfica guardada en: {rutaCompleta}")
    pausarConsola()
    
    
def visualizarGraficas():
    #Muestra las gráficas guardadas y permite visualizarlas 
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    rutaBase = obtenerRutaGraficas()
    if not rutaBase.exists():
        print("No hay gráficas guardadas")
        pausarConsola()
        return

    # Listar tipos de gráficas disponibles
    carpetas = [carpeta for carpeta in rutaBase.iterdir() if carpeta.is_dir()]
    if not carpetas:
        print("No hay gráficas guardadas")
        pausarConsola()
        return

    print("\nTipos de gráficas disponibles:")
    for i, carpeta in enumerate(carpetas, 1):
        print(f"{i}. {carpeta.name}")

    # Seleccionar tipo de gráfica
    try:
        opcion = int(input("\nSeleccione tipo (0 para cancelar): "))
        if opcion == 0:
            return
        if not 1 <= opcion <= len(carpetas):
            print("Error: Opción inválida")
            pausarConsola()
            return
    except ValueError:
        print("Error: Ingrese un número válido")
        pausarConsola()
        return

    carpetaSeleccionada = carpetas[opcion - 1]
    graficas = list(carpetaSeleccionada.glob("*.png"))

    # Ordenar por fecha de modificación (más reciente primero)
    graficas.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    if not graficas:
        print(f"No hay gráficas en {carpetaSeleccionada.name}")
        pausarConsola()
        return

    # Mostrar gráficas disponibles
    print(f"\nGráficas disponibles en {carpetaSeleccionada.name}:")
    for i, grafica in enumerate(graficas, 1):
        print(f"{i}. {grafica.name}")
    # Seleccionar gráfica para visualizar
    try:
        opcion = int(input("\nSeleccione gráfica (0 para cancelar): "))
        if opcion == 0:
            return
        if 1 <= opcion <= len(graficas):
            graficaSeleccionada = graficas[opcion-1]
            os.startfile(graficaSeleccionada)  # Abre con visor predeterminado
        else:
            print("Error: Opción inválida")
    except ValueError:
        print("Error: Ingrese un número válido")
    
    pausarConsola()

# ======================
# Flujo Principal
# ======================

def menuTipoGrafica():
    #Maneja la selección del tipo de gráfica 
    while True:
        limpiarConsola()
        mostrarMenuTipoGrafica()
        
        try:
            opcion = int(input("\nSeleccione opción: "))
            limpiarConsola()
            
            if 1 <= opcion <= 3:
                crearGrafica(opcion)
            elif opcion == 4:
                break
            else:
                print("Error: Opción inválida")
                pausarConsola()
        except ValueError:
            print("Error: Ingrese un número válido")
            pausarConsola()

def ejecutarOpcion2():
    #Controla el flujo principal de la opción 2 
    while True:
        limpiarConsola()
        mostrarMenuPrincipalGraficas()
        
        try:
            opcion = int(input("\nSeleccione opción: "))
            limpiarConsola()
            
            if opcion == 1:
                menuTipoGrafica()
            elif opcion == 2:
                visualizarGraficas()
            elif opcion == 3:
                break
            else:
                print("Error: Opción inválida")
                pausarConsola()
        except ValueError:
            print("Error: Ingrese un número válido")
            pausarConsola()

if __name__ == "__main__":
    ejecutarOpcion2()