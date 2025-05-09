import os
import menu
from pathlib import Path
import config
from config import config
#========================
#Fin de las importaciones (os)

#Funciones para limpiar y hacer pausas en la consola usando la libreria os(Operative System).
def clean():
    os.system('cls')#Clear console
def pause():
    os.system("pause")


#Función que nos imprime las opciones del menu 1
def menu1():
    print("=======================================")
    print("          Cuidado del agua.")
    print("=======================================")
    print("")
    print("1. Agregar un cuerpo de agua.")
    print("2. Acceder a un cuerpo de agua.")
    print("3. Salir.")
    
    

def createFolder():
    # Solicita el nombre del cuerpo de agua
    waterBodyName = input("Ingrese el nombre del cuerpo de agua: ")
    folder = Path("CuerposDeAgua") / waterBodyName

    # Verifica si la carpeta ya existe
    if folder.exists():
        print(f"El cuerpo de agua '{waterBodyName}' ya existe.")
        return  # Sale de la función sin hacer nada más

    # Si no existe, crea la carpeta
    folder.mkdir(parents=True, exist_ok=True)
    config.activeWaterBody = waterBodyName
    print(f"Se ha agregado '{waterBodyName}' exitosamente!")
    pause()
    menu.application()
    
    
def accesFolder():
    folder = Path("CuerposDeAgua")
    folders = [fold.name for fold in folder.iterdir() if fold.is_dir()]
    
    if not folders:
        print("No hay archivos disponibles para editar.")
        pause()
        return
    
    print("Archivos existentes:")
    for i, archivo in enumerate(folders, start=1):
        print(f"{i}. {archivo}")
    
    while True:
        try:
            op = int(input("Selecciona el número del cuerpo de agua (0 para salir): "))
            if op == 0:
                return  # Volver al menú anterior.
            if 1 <= op <= len(folders):
                waterBodyName = folders[op - 1]
                config.activeWaterBody = waterBodyName
                break
            else:
                print("Opción inválida. Elige un número válido.")
                pause()
        except ValueError:
            print("Por favor ingresa un número válido.")
            pause()
            
    menu.application()

    
#Ciclo principal en el que estamos corriendo constantemente el menu
#con la condición de que si la opción no está en el rango permitido
#no nos permite avanzar.
clean()
while True:
    menu1()
    opcion = int(input("Ingrese una opcion: "))
    clean()
    if opcion >= 1 and opcion <= 5:
        if opcion == 1:
            createFolder()
        elif opcion == 2:
            accesFolder()
        elif opcion == 3:
            clean()
            print(config.activeWaterBody)
            pause()
        else:
            print("Programa finalizado...")
            break
    else:
        print("Opción invalida.")
        pause()
    clean()
