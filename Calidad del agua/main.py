import os
import option1
#========================
#Fin de las importaciones

#Funciones para limpiar y hacer pausas en la consola
def limpiar():
    os.system('cls')
def pausa():
    os.system("pause")

#Función que nos imprime las opciones del menu
def menu():
    print("Cuidado del agua.")
    print("1. Evaluación de la calidad del agua.")
    print("2. Generacion De Graficas.")
    print("3. Reportes.")
    print("4. Deteccion de Causas Importantes.")
    print("5. Salir.")

#Ciclo principal en el que estamos corriendo constantemente el menu
limpiar()
while True:
    menu()
    opcion = int(input("Ingrese una opcion: "))
    limpiar()
    if opcion >= 1 and opcion <= 5:
        if opcion == 1:
            option1.option1()
        elif opcion == 2:
            print("Opcion 2")
        elif opcion == 3:
            print("Opcion 3")
        elif opcion == 4:
            print("Opcion 4")
        else:
            print("Programa finalizado, chao pescao :3...")
            break
    limpiar()
