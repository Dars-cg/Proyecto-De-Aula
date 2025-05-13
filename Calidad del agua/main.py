"""
Sistema de Gestión de Cuerpos de Agua
Módulo: Menú Principal
"""
import os
from pathlib import Path
import menu
import config
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

def mostrarMenuPrincipal():
    """Muestra el menú principal del sistema"""
    print("======================================")
    print("SISTEMA DE ANÁLISIS DE CALIDAD DE AGUA ")
    print("======================================")
    print("\n1. Agregar cuerpo de agua")
    print("2. Acceder a cuerpo de agua existente")
    print("3. Salir")

def crearCuerpoAgua():
    """
    Crea un nuevo directorio para un cuerpo de agua
    y lo establece como activo en la configuración
    """
    nombre = input("Ingrese el nombre del cuerpo de agua: ")
    ruta = Path("CuerposDeAgua") / nombre

    if ruta.exists():
        print(f"\nEl cuerpo de agua '{nombre}' ya existe.")
        pausarConsola()
        return

    ruta.mkdir(parents=True, exist_ok=True)
    config.activeWaterBody = nombre
    print(f"\nCuerpo de agua '{nombre}' creado exitosamente!")
    pausarConsola()
    menu.ejecutarAplicacion()

def accederCuerpoAgua():
    """
    Muestra lista de cuerpos de agua existentes
    y permite seleccionar uno para trabajar
    """
    rutaBase = Path("CuerposDeAgua")
    rutaBase.mkdir(exist_ok=True)  # Asegura que la carpeta exista

    cuerposAgua = [carpeta.name for carpeta in rutaBase.iterdir() if carpeta.is_dir()]

    if not cuerposAgua:
        print("\nNo hay cuerpos de agua registrados.")
        pausarConsola()
        return

    print("\nCuerpos de agua disponibles:")
    for i, cuerpo in enumerate(cuerposAgua, 1):
        print(f"{i}. {cuerpo}")

    while True:
        try:
            seleccion = int(input("\nSeleccione un número (0 para cancelar): "))
            if seleccion == 0:
                return
            if 1 <= seleccion <= len(cuerposAgua):
                cuerpoSeleccionado = cuerposAgua[seleccion - 1]
                config.activeWaterBody = cuerpoSeleccionado
                menu.ejecutarAplicacion()
                break
            print("Error: Número fuera de rango")
        except ValueError:
            print("Error: Debe ingresar un número válido")
        pausarConsola()

# ======================
# Bucle Principal
# ======================

def ejecutarSistema():
    """Controla el flujo principal de la aplicación"""
    limpiarConsola()
    while True:
        mostrarMenuPrincipal()
        try:
            opcion = int(input("\nSeleccione una opción: "))
            if opcion == 1:
                crearCuerpoAgua()
            elif opcion == 2:
                accederCuerpoAgua()
            elif opcion == 3:
                print("Saliendo del sistema...")
                break
            else:
                print("Error: Opción debe ser entre 1 y 3")
                pausarConsola()
        except ValueError:
            print("Error: Debe ingresar un número válido")
            pausarConsola()
        limpiarConsola()

if __name__ == "__main__":
    ejecutarSistema()