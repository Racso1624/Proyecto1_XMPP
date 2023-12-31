# Oscar Fernando López Barrios
# Carné 20679
# Proyecto 1

import slixmpp
import asyncio
from slixmpp.exceptions import IqError, IqTimeout
import base64
from aioconsole import ainput
from aioconsole.stream import aprint

# Codigo del Cliente con referencia de https://slixmpp.readthedocs.io/en/latest/
# Codigo del Cliente con referencia de https://searchcode.com/file/58168360/examples/register_account.py/
# https://slixmpp.readthedocs.io/en/latest/api/clientxmpp.html

# Se crea la clase Cliente
class Client(slixmpp.ClientXMPP):
    # Se hace el init
    def __init__(self, jid, password):
        super().__init__(jid, password)

        # Se crean las variables globales del Cliente
        self.name = jid.split('@')[0] # Se realiza el split para el username
        self.is_connected = False
        self.chat = ""
        self.room_nickname = ""
        self.room = ""

        #Plugins obtenidos por ChatGPT
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0066') # Out of Band Data
        self.register_plugin('xep_0363') # HTTP File Upload
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0085') # Notifications

        # Se realiza el handler de los eventos que se realicen durante el chat
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.receiveMessage)
        self.add_event_handler("groupchat_message", self.receivechatroomMessage)
    
    # Se crea la funcion Handler de Star
    async def start(self, event):
        try:
            # Se conecta al server
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            print("\nConectado al servidor")

            asyncio.create_task(self.menu())

        # Si pasa lo contrario se brinda el error
        except IqError as err:
            self.is_connected = False
            print(f"Error: {err.iq['error']['text']}")
            self.disconnect()
        except IqTimeout:
            self.is_connected = False
            print('Error: El servidor toma mucho tiempo para responder')
            self.disconnect()

    # Se crea la funcion Handler para recibir mensajes
    async def receiveMessage(self, message):
        # Si el mensaje es de tipo chat se toma
        if(message['type'] == "chat"):
            # Se obtiene el nombre del contacto
            contact_name = str(message['from']).split('@')[0]
            # Codigo con algoritmo brindado por medio de ChatGPT
            # Si el mensaje es file
            if(message['body'].startswith("file://")):
                # Se obtiene la informacion del archivo
                file_information = message['body'][7:].split("://")
                # Se obtiene la extension
                file_extension = file_information[0]
                # Se obtienen los datos
                file_data = file_information[1]
                
                # Se intenta decodificar
                try:
                    data_decoded = base64.b64decode(file_data)
                    with open("file_received_from_" + contact_name + "." + file_extension, "wb") as file:
                        file.write(data_decoded)
                    print("Archivo recibido y descargado")
                # Si no brinda error
                except Exception as err:
                    print("Error al decodificar la informacion del archivo")
            else:
                # Si es otro tipo de mensaje solo se muestra
                if(contact_name == self.chat.split('@')[0]):
                    print("\nMensaje de " + contact_name + ": " + message['body'])
                else:
                    print("\nMensaje de otra conversacion de " + contact_name + ": " + message['body'])
    
    # Recibir mensaje de chat de grupo
    async def receivechatroomMessage(self, message=''):
        # Se obtiene el nombre del usuario
        group_user = message['mucnick'] 
        if group_user != self.boundjid.user:
            # Se realiza la impresion del mensaje
            if(self.room in str(message['from'])):
                print("Mensaje de " + group_user + ": " + message['body'])
            else:
                print("Nuevo mensaje del usuario " + group_user + " en la sala de chat " + self.room.split('@')[0] + ": " + message['body'])

    # Menu de opciones dentro del chat
    async def menu(self):
        while(self.is_connected):
            print("\nTienes las siguienes opciones disponibles para utilizar en el chat:\n")
            print("1) Mostrar todos los contactos y su estado")
            print("2) Agregar un usuario a los contactos")
            print("3) Mostrar detalles de contacto de un usuario")
            print("4) Comunicación 1 a 1 con cualquier usuario/contacto")
            print("5) Participar en conversaciones grupales")
            print("6) Definir mensaje de presencia")
            print("7) Enviar archivos")
            print("8) Cerrar sesión")
            opcion = int(input("Ingrese la opcion que desees:"))

            # Dependiendo de la opcion se realiza una accion
            if(opcion == 1):
                await self.showContacts()
            elif(opcion == 2):
                await self.addContact()
            elif(opcion == 3):
                await self.showContact()
            elif(opcion == 4):
                await self.sendMessage()
            elif(opcion == 5):
                await self.groupchatMenu()
            elif(opcion == 6):
                await self.setPresence()
            elif(opcion == 7):
                user_jid = input("Ingresa el JID del usuario que deseas: ")
                path = input("Ingresa la ruta del archivo: ")
                await self.sendFiles(user_jid, path)
            elif(opcion == 8):
                # Se desconecta para cerrar sesion
                self.disconnect()
                self.is_connected = False

    # Menu para el groupchat
    async def groupchatMenu(self):
        menu_var = True
        # Se pregunta la opcion deseada
        while(menu_var):
            print("\nTienes las siguienes opciones disponibles para utilizar en el chat:\n")
            print("1) Crear una sala")
            print("2) Unirse a una sala")
            print("3) Salir")
            opcion = int(input("Ingrese la opcion que desees:"))

            # Se realizan las opciones de las salas de chat
            if(opcion == 1):
                roomname = input("Ingresa el nombre para la sala de chat: ")
                await self.createChatRoom(roomname)
            elif(opcion == 2):
                roomname = input("Ingresa el nombre de la sala de chat: ")
                await self.joinChatRoom(roomname)
            elif(opcion == 3):
                menu_var = False

    # Funcion para mostrar contactos
    async def showContacts(self):
        # Se obtienen los valores de los contactos
        user_roster = self.client_roster
        contacts = user_roster.keys()
        contact_list = list(contacts)

        # Solucion brindada por ChatGPT
        if(len(contact_list) == 1 and contact_list[0] == self.boundjid.bare):
            print("\nNo tienes contactos")
            return
        # Se imprimen los contactos
        else:
            print("\nLista de usuarios")
            for user in contacts:
                if(user != self.boundjid.bare):
                    print("Usuario: ", user)
                    user_presence = user_roster.presence(user)
                    if(user_presence != {}):
                        # Se imprime el estado
                        for answer, presence in user_presence.items():
                            if(presence['show'] == ''):
                                print("Estado: Disponible")
                            elif(presence['show'] == 'away'):
                                print("Estado: Ausente")
                            elif(presence['show'] == 'dnd'):
                                print("Estado: Ocupado")
                            elif(presence['show'] == 'xa'):
                                print("Estado: No Disponible")
                    else:
                        print("Estado: Desconectado")

    # Se añade contactos
    async def addContact(self):
        # Se ingresa el JID para el contacto
        contact_jid = input("Ingresa el JID del contacto para agregar: ")
        try:
            # Se solicita
            self.send_presence_subscription(pto = contact_jid)
            print(f"Solicitud enviada existosamente a {contact_jid}")
            await self.get_roster()
        except IqError as err:
            print(f"Error enviando la solicitud: {err.iq['error']['text']}")
        except IqTimeout:
            print("No hay respuesta del servidor")

    # Se muestra un contacto
    async def showContact(self):
        # Se ingresa el contacto y se regresa la lista
        contact_jid = input("Ingresa el JID del contacto para buscar: ")
        user_roster = self.client_roster
        contacts = user_roster.keys()
        contact_list = list(contacts)
        # Se revisa que el contacto se encuentra en la lista
        if(contact_jid not in contact_list):
            print("El usuario no se encuentra agregado como contacto")
        # Se imprime la información
        else:
            print("Usuario: ", contact_jid)
            user_presence = user_roster.presence(contact_jid)
            if(user_presence != {}):
                for answer, presence in user_presence.items():
                    if(presence['show'] == ''):
                        print("Estado: Disponible")
                    elif(presence['show'] == 'away'):
                        print("Estado: Ausente")
                    elif(presence['show'] == 'dnd'):
                        print("Estado: Ocupado")
                    elif(presence['show'] == 'xa'):
                        print("Estado: No Disponible")
            else:
                print("Estado: Desconectado")

    # Se crea funcion para enviar mensaje
    async def sendMessage(self):
        # Se ingresa el jid para el contacto
        contact_jid = await ainput("Ingresa el JID del contacto para enviar mensaje: ")
        self.chat = contact_jid

        await aprint("Mensaje para: ", contact_jid.split("@")[0])
        await aprint("Si deseas salir escribe: exit chat")

        # Se hace un ciclo para mandar mensajes
        user_chatting = True
        while user_chatting:
            message = await ainput("Escribe el mensaje: ")
            print(message)
            if(message == "exit chat"):
                user_chatting = False
                self.chat = ""
            else:
                # Se envia mensaje
                self.send_message(mto=contact_jid, mbody=message, mtype='chat') 

    # Referencia de https://xmpp.org/extensions/xep-0045.html#terms-rooms
    # Referencia de https://slixmpp.readthedocs.io/en/latest/getting_started/muc.html
    # Referencia de https://xmpp.org/registrar/formtypes.html
    # Codigo con ayuda de ChatGPT
    # Se crea la clase para crear chat rooms
    async def createChatRoom(self, name_room):
        try:
            # Se crea el chat grupal
            name_room = name_room + "@conference.alumchat.xyz"
            self.plugin['xep_0045'].join_muc(name_room, self.boundjid.user)
            
            # Se espera debido a que de lo contrario brinda error al crearlo
            await asyncio.sleep(2)

            # Se crea el form para el chat grupal
            form = self.plugin['xep_0004'].make_form(ftype='submit', title='ChatRoom Configuration')
            form['muc#roomconfig_roomname'] = name_room
            form['muc#roomconfig_roomdesc'] = 'Sala de chat de usuario AlumChat'
            form['muc#roomconfig_roomowners'] = [self.boundjid.user]
            form['muc#roomconfig_maxusers'] = '50'
            form['muc#roomconfig_publicroom'] = '1'
            form['muc#roomconfig_persistentroom'] = '1'
            form['muc#roomconfig_enablelogging'] = '1'
            form['muc#roomconfig_changesubject'] = '1'
            form['muc#roomconfig_membersonly'] = '0'
            form['muc#roomconfig_allowinvites'] = '0'
            form['muc#roomconfig_whois'] = 'anyone'

            # Se crea la sala del chat
            await self.plugin['xep_0045'].set_room_config(name_room, config=form)
            print("Se creo la sala de chat: ", name_room)
            self.send_message(mto=name_room, mbody="Bienvenidos a la sala: " + name_room, mtype='groupchat')
        # Se imprimen los errores
        except IqError as err:
            print("Error para crear la sala de chat")
        except IqTimeout:
            print("Tiempo de espera maximo para la creacion de la sala")


    # Referencia de https://xmpp.org/extensions/xep-0045.html#terms-rooms
    # Referencia de https://slixmpp.readthedocs.io/en/latest/getting_started/muc.html
    # Codigo con ayuda de ChatGPT
    # Se crea la funcion para unirse a una sala de chat
    async def joinChatRoom(self, name_room):
        # Se ingresa el nombre de la sala
        name_room = name_room + "@conference.alumchat.xyz"
        self.room = name_room 
        self.room_nickname = self.boundjid.user 

        # Unirse a la sala de chat
        try:
            await self.plugin['xep_0045'].join_muc(name_room, self.room_nickname)
        except IqError as err:
            print(f"Error al unirse {err.iq['error']['text']}")
        except IqTimeout:
            print("No hay respuesta del servidor")
            return None

        await aprint("Mensajes de la Sala de Chat: ", name_room)
        await aprint("Para salir del chat escribe: exit chat")

        # Se crea el ciclo para enviar mensajes
        user_chatting = True
        while user_chatting:
            message = await ainput("Escribe el mensaje: ")
            if(message == "exit chat"):
                # Se sale del chat room
                user_chatting = False
                self.chat = ""
                self.plugin['xep_0045'].leave_muc(self.room, self.room)
                self.room = ""
                self.room_nickname = ""
            else:
                # Se envian mensajes
                self.send_message(self.room, message, mtype='groupchat')

    # Se utiliza la funcion para añadir la presencia
    async def setPresence(self):
        status, status_message = self.presenceMenu()
        self.status = status
        self.status_message = status_message
        self.send_presence(pshow=self.status, pstatus=self.status_message) 
        await self.get_roster() 

    # Se crea el menu de presencia del usuario
    def presenceMenu(self):
        print("Estados disponibles: ")
        print("1) Disponible")
        print("2) Ausente")
        print("3) No Disponible")
        print("4) Ocupado")
        option = int(input("Ingresa el estado que desees: "))

        if(option == 1):
            return '', 'Disponible'
        elif(option == 2):
            return 'away', 'Ausente'
        elif(option == 3):
            return 'xa', 'No Disponible'
        elif(option == 2):
            return 'dnd', 'Ocupado'


    # Codigo con ayuda de ChatGPT
    # Se crea la funcion para enviar archios
    async def sendFiles(self, contact_jid, file_path):
        # Se obtienen las extensiones
        file_extension = file_path.split(".")[-1]

        with open(file_path, "rb") as file: 
            file_data = file.read()
        # Se codifica la data del archivo
        encoded_data = base64.b64encode(file_data).decode()
        message =  message = f"file://{file_extension}://{encoded_data}" 
        # Se envia la data
        self.send_message(mto=contact_jid, mbody=message, mtype='chat')