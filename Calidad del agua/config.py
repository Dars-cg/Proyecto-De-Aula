#Creamos una clase global para manejar las configuraciones
#Atributos:
#   activeWaterBody
#   data_folder(Nombre de la carpeta de datos)
#   report_Folder(Nombre de la carpeta de reportes)
class Config:
    def __init__(self):
        self.activeWaterBody = None
        self.data_folder = "Datos"
        self.report_folder = "Reportes"

#Instanciamos el objeto config de la clase Config
config = Config()