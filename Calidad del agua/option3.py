"Generación de reportes"""
from config import config
import os
from pathlib import Path
from datetime import datetime, timedelta

def limpiarConsola():
    """Limpia la pantalla de la consola"""
    os.system('cls')

def pausarConsola():
    """Pausa la ejecución hasta que el usuario presione una tecla"""
    os.system("pause")

def menuReportes():
    """Muestra el menú principal de evaluación de calidad"""
    print("\n" + "="*40)
    print("               REPORTES")
    print("="*40)
    print(f"\nCuerpo de agua activo: {config.activeWaterBody or 'Ninguno'}")
    print('\n1. Crear un nuevo reporte.')
    print('2. Mostrar reportes existentes.')
    print('3. Editar un reporte.')
    print("4. Eliminar un reporte.")
    print('5. Volver al menu anterior.')


def obtenerRuta(nombreArchivo):
    if(nombreArchivo):
        return Path("CuerposDeAgua") / config.activeWaterBody / config.report_folder / nombreArchivo
    else:
        return Path("CuerposDeAgua") / config.activeWaterBody / config.report_folder


def crearReportes():
    titulo = input("Ingresa titulo del reporte: ")
    fechaActual = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    nombreArchivo = "Reporte_" + titulo + "_" + fechaActual + ".txt"
    ruta = obtenerRuta(nombreArchivo)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    texto = input("Ingresa el contenido del reporte: ")
    contenido = titulo + "\n" + texto
    with open(ruta, "w") as archivo:
        archivo.write(contenido)
    print(f"\nReporte guardado.")

def listarArchivosDisponibles():
    """Lista los archivos Excel disponibles en la carpeta de datos"""
    ruta_datos = obtenerRuta("")
    if not ruta_datos.exists():
        return None
    return [archivo.name for archivo in ruta_datos.glob("*.txt")]


def mostrarReportes():
    limpiarConsola()
    print("\nReportes disponibles: ")
    listaReportes = listarArchivosDisponibles()
    for i, archivo in enumerate(listaReportes, start=1):
        print(f"{i}. {archivo}.")

    while True:
        op = int(input("\nIngresa el numero del archivo (0 para cancelar): "))
        if(op == 0):
            break
        elif(op <= len(listaReportes)):
            ruta = obtenerRuta(listaReportes[op-1])
            with open(ruta, "r") as archivo:
                contenido = archivo.read()
                print(contenido)
            break
        else:
            print("Error: Opción invalida.")


def editarReportes():
    limpiarConsola()
    print("\nReportes disponibles: ")
    listaReportes = listarArchivosDisponibles()
    for i, archivo in enumerate(listaReportes, start=1):
        print(f"{i}. {archivo}.")
    
    while True:
        op = int(input("\nIngresa el numero del archivo (0 para cancelar): "))
        if(op == 0):
            break
        elif(op <= len(listaReportes)):
            ruta = obtenerRuta(listaReportes[op-1])
            os.startfile(ruta)
            break
        else:
            print("Error: Opción invalida.")


def eliminarReportes():
    limpiarConsola()
    print("\nReportes disponibles: ")
    listaReportes = listarArchivosDisponibles()
    for i, archivo in enumerate(listaReportes, start=1):
        print(f"{i}. {archivo}.")
    
    while True:
        op = int(input("\nIngresa el numero del archivo (0 para cancelar): "))
        if(op == 0):
            break
        elif(op <= len(listaReportes)):
            ruta = obtenerRuta(listaReportes[op-1])
            while True:
                op = input("¿Seguro que deseas eliminarlo? (SI/NO): ")

                if(op == "SI"):
                    os.remove(ruta)
                    print("Archivo eliminado correctamente.")
                    return
                elif(op == "NO"):
                    print("No se elimino el archivo.")
                    return
                else:
                    print("Error: Opción invalida.")
            break
        else:
            print("Error: Opción invalida.")



def ejecutarOpcion3():
    while True:
        menuReportes()
        op = int(input("Ingresa una opción: "))
        if op == 1:
            crearReportes()
        elif op == 2:
            mostrarReportes()
        elif op == 3:
            editarReportes()
        elif op == 4:
            eliminarReportes()
        elif op == 5:
            break
        else:
            print("Error: Opción invalida.")
        pausarConsola()
        limpiarConsola()