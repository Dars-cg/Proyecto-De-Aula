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
    """Limpia la pantalla de la consola"""
    os.system('cls')

def pausarConsola():
    """Pausa la ejecución hasta que el usuario presione una tecla"""
    os.system("pause")

# ======================
# Funciones del Menú
# ======================

def mostrarMenuPrincipalGraficas():
    """Muestra el menú principal de generación de gráficas"""
    print("=================================")
    print("     GENERACIÓN DE GRÁFICAS")
    print("=================================")
    print("\n1. Crear nueva gráfica")
    print("2. Visualizar gráficas guardadas")
    print("3. Volver al menú anterior")

def mostrarMenuTipoGrafica():
    """Muestra los tipos de gráficas disponibles"""
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
    """Retorna la ruta a la carpeta de datos del cuerpo de agua activo"""
    return Path(f"CuerposDeAgua/{config.activeWaterBody}/Datos")

def obtenerRutaGraficas(tipo=None):
    """Retorna la ruta a la carpeta de gráficas"""
    base = Path(f"CuerposDeAgua/{config.activeWaterBody}/Graficas")
    if tipo:
        return base / tipo
    return base

def seleccionarArchivo(files, mensaje):
    """Permite al usuario seleccionar un archivo de la lista"""
    print("\nArchivos disponibles:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")

    while True:
        try:
            opcion = int(input(f"\n{mensaje} (0 para cancelar): "))
            if opcion == 0:
                return None
            if 1 <= opcion <= len(files):
                return files[opcion-1]
            print("Error: Número fuera de rango")
        except ValueError:
            print("Error: Ingrese un número válido")

def crearGrafica(tipo_grafica):
    """Crea y guarda una gráfica según el tipo seleccionado"""
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    # Obtener lista de archivos disponibles
    ruta_datos = obtenerRutaDatos()
    if not ruta_datos.exists():
        print("Error: No hay datos disponibles.")
        pausarConsola()
        return

    archivos = [archivo.name for archivo in ruta_datos.glob("*.xlsx")]
    if not archivos:
        print("No hay archivos disponibles")
        pausarConsola()
        return

    # Seleccionar archivo
    archivo_seleccionado = seleccionarArchivo(archivos, "Seleccione archivo a graficar")
    if not archivo_seleccionado:
        return

    # Leer datos
    ruta_archivo = ruta_datos / archivo_seleccionado
    try:
        df = pd.read_excel(ruta_archivo)
        fechas = df['Fecha'].to_numpy()
        valores = df['Valor'].to_numpy()
    except Exception as e:
        print(f"Error al leer archivo: {e}")
        pausarConsola()
        return

    # Configurar gráfico
    fig, ax = plt.subplots()
    nombre_archivo = archivo_seleccionado.replace(".xlsx", "")

    # Crear gráfico según tipo seleccionado
    tipos = {
        1: ("Barras", lambda: ax.bar(fechas, valores)),
        2: ("Dispersion", lambda: ax.scatter(fechas, valores)),
        3: ("Lineal", lambda: ax.plot(fechas, valores, marker='o'))
    }

    if tipo_grafica not in tipos:
        print("Error: Tipo de gráfica inválido")
        pausarConsola()
        return

    nombre_tipo, funcion_grafica = tipos[tipo_grafica]
    funcion_grafica()

    # Configuración del gráfico
    ax.set_title(nombre_archivo)
    ax.set_xlabel("Fecha")
    ax.set_ylabel(nombre_archivo)
    ax.grid(True)

    # Guardar gráfico
    ruta_graficas = obtenerRutaGraficas(nombre_tipo)
    ruta_graficas.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    nombre_grafica = f"{nombre_archivo}-{timestamp}.png"
    ruta_completa = ruta_graficas / nombre_grafica

    plt.savefig(ruta_completa)
    plt.show()
    print(f"\nGràfica guardada en: {ruta_completa}")
    pausarConsola()

def visualizarGraficas():
    """Muestra las gráficas guardadas y permite visualizarlas"""
    if not config.activeWaterBody:
        print("Error: No hay cuerpo de agua seleccionado")
        pausarConsola()
        return

    ruta_base = obtenerRutaGraficas()
    if not ruta_base.exists():
        print("No hay gráficas guardadas")
        pausarConsola()
        return

    # Listar tipos de gráficas disponibles
    carpetas = [carpeta for carpeta in ruta_base.iterdir() if carpeta.is_dir()]
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

    carpeta_seleccionada = carpetas[opcion - 1]
    graficas = list(carpeta_seleccionada.glob("*.png"))

    # Ordenar por fecha de modificación (más reciente primero)
    graficas.sort(key=lambda x: x.stat().st_mtime, reverse=True)

    if not graficas:
        print(f"No hay gráficas en {carpeta_seleccionada.name}")
        pausarConsola()
        return

    # Mostrar gráficas disponibles
    print(f"\nGráficas disponibles en {carpeta_seleccionada.name}:")
    for i, grafica in enumerate(graficas, 1):
        print(f"{i}. {grafica.name}")
    # Seleccionar gráfica para visualizar
    try:
        opcion = int(input("\nSeleccione gráfica (0 para cancelar): "))
        if opcion == 0:
            return
        if 1 <= opcion <= len(graficas):
            grafica_seleccionada = graficas[opcion-1]
            os.startfile(grafica_seleccionada)  # Abre con visor predeterminado
        else:
            print("Error: Opción inválida")
    except ValueError:
        print("Error: Ingrese un número válido")
    
    pausarConsola()

# ======================
# Flujo Principal
# ======================

def menuTipoGrafica():
    """Maneja la selección del tipo de gráfica"""
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
    """Controla el flujo principal de la opción 2"""
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