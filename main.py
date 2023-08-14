# Oscar Fernando López Barrios
# Carné 20679
# Proyecto 1

import slixmpp
import logging

from user_register import *
while(True):
    print("Bienvenido al Chat")
    print("\nTienes las siguienes opciones disponibles:\n")
    print("1) Registrar una nueva cuenta")
    print("2) Iniciar sesion con una cuenta")
    print("3) Eliminar cuenta del servidor")
    print("4) Salir")
    opcion = int(input("Ingrese la opcion que desees:"))

    if(opcion == 1):
        print("\nCreando nueva cuenta")
        jid = input("JID: ")
        password = input("Contraseña: ")

        xmpp = RegisterUser(jid, password)
        xmpp.register_plugin('xep_0030')  # Service Discovery
        xmpp.register_plugin('xep_0004')  # Data Forms
        xmpp.register_plugin('xep_0066')  # Out-of-band Data
        xmpp.register_plugin('xep_0077')  # In-band Registration

        if xmpp.connect():
            xmpp.process(block=True)
            print("Proceso completado")
        else:
            print("No se pudo conectar.")

    elif(opcion == 2):
        print("\nIngresando sesion")
    elif(opcion == 3):
        print("\nEliminando cuenta del servidor")
    elif(opcion == 4):
        print("\nSaliendo del chat")
        break
    else:
        print("\nERROR opcion no valida\nIngresa otra opcion\n")