import os

#Funciones para limpiar y hacer pausas en la consola
def limpiar():
    os.system('cls')
def pausa():
    os.system("pause")

def menuOp1():
    print("Evaluación de calidad del agua.")
    print("1. igresar datos manualmente")
    print("2. importar archivos de datos")
    print("3. volver atras")

     
def option1():
    while True:
        menuOp1()
        option = int(input("ingrese una opcion: "))
        if option == 1:
            print("Opcion 1")
            limpiar()
        elif option == 2:
            print("option 2")
            limpiar()
        else:
            print("option 3")
            break
        
