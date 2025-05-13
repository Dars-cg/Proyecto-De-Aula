import os
import option1
import option2
import option3
#========================
#Fin de las importaciones (os)

#Funciones para limpiar y hacer pausas en la consola usando la libreria os(Operative System).
def limpiarConsola():
    os.system('cls')#Clear console
def pausarConsola():
    os.system("pause")


#Función que nos imprime las opciones del menu 2
def menu2():
    print("======================================")
    print("SISTEMA DE ANÁLISIS DE CALIDAD DE AGUA     ")
    print("======================================")
    print("")
    print("1. Evaluación de la calidad del agua")
    print("2. Generacion De Graficas")
    print("3. Reportes")
    print("4. Deteccion de Causas Importantes")
    print("5. Volver al menú anterior")
    
    
#Ciclo principal en el que estamos corriendo constantemente el menu
#con la condición de que si la opción no está en el rango permitido
#no nos permite avanzar.
def ejecutarAplicacion():
    limpiarConsola()
    while True:
        menu2()
        opcion = int(input("Ingrese una opcion: "))
        limpiarConsola()
        if opcion >= 1 and opcion <= 5:
            if opcion == 1:
                option1.ejecutarOpcion1()
            elif opcion == 2:
                option2.ejecutarOpcion2()
            elif opcion == 3:
                option3.ejecutarOpcion3()
            elif opcion == 4:
                print("Opcion 4")
            else:
                print("Programa finalizado...")
                break
        else:
            print("Opción invalida.")
            pausarConsola()
        limpiarConsola()
