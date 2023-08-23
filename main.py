# Oscar Fernando López Barrios
# Carné 20679
# Proyecto 1

# Se realizan los imports
from client import *
from client_functions import *
from delete_client import *

# Se hace el menu principal
while(True):
    print("\nBienvenido al Chat")
    print("\nTienes las siguienes opciones disponibles:\n")
    print("1) Registrar una nueva cuenta")
    print("2) Iniciar sesion con una cuenta")
    print("3) Eliminar cuenta del servidor")
    print("4) Salir")
    opcion = int(input("Ingrese la opcion que desees:"))

    # Opcion de crear cuenta
    if(opcion == 1):
        # Se toma el JID y la contraseña
        print("\nCreando nueva cuenta")
        jid = input("JID: ")
        password = input("Contraseña: ")
        # Si se pudo registrar se brinda el mensaje
        if register_user(jid, password):
            print("Registro completado")
        else:
            print("Registro no se pudo completar")
            
    # Opcion de ingresar sesion
    elif(opcion == 2):
        # Se toman los valores
        print("\nIngresando sesion")
        jid = input("JID: ")
        password = input("Contraseña: ")
        # Se crea el cliente
        client = Client(jid, password)
        client.connect(disable_starttls=True, use_ssl=False)
        client.process(forever=False)

    # Opcion de eliminar cuenta
    elif(opcion == 3):
        print("\nEliminando cuenta del servidor")
        # Se toman los valores
        jid = input("JID: ")
        password = input("Contraseña: ")
        # Se crea el cliente
        client = DeleteClient(jid, password)
        client.connect(disable_starttls=True, use_ssl=False)
        client.process(forever=False)
    # Opcion de salir del chat
    elif(opcion == 4):
        print("\nSaliendo del chat")
        break
    else:
        print("\nERROR opcion no valida\nIngresa otra opcion")