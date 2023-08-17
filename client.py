import xmpp
import slixmpp
import asyncio
from slixmpp.exceptions import IqError, IqTimeout
from aioconsole import ainput
from aioconsole.stream import aprint
import base64

# Codigo del Cliente con referencia de https://slixmpp.readthedocs.io/en/latest/
# Codigo del Cliente con referencia de https://searchcode.com/file/58168360/examples/register_account.py/

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.name = jid.split('@')[0] # Se realiza el split para el username
        self.is_connected = False
        self.contact_chat = ""

        #Plugins obtenidos por ChatGPT
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0199') # Ping
        self.register_plugin('xep_0045') # MUC
        self.register_plugin('xep_0085') # Notifications
        self.register_plugin('xep_0004') # Data Forms
        self.register_plugin('xep_0060') # PubSub
        self.register_plugin('xep_0066') # Out of Band Data
        self.register_plugin('xep_0363') # HTTP File Upload

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.receiveMessage)

    async def start(self, event):
        try:
            self.send_presence()
            await self.get_roster()
            self.is_connected = True
            print("\nConectado al servidor")

            asyncio.create_task(self.menu())

        except IqError as err:
            self.is_connected = False
            print(f"Error: {err.iq['error']['text']}")
            self.disconnect()
        except IqTimeout:
            self.is_connected = False
            print('Error: El servidor toma mucho tiempo para responder')
            self.disconnect()

    async def receiveMessage(self, message):
        if(message['type'] == "chat"):
            contact_name = str(message['from']).split('@')[0]
            # Codigo con algoritmo brindado por medio de ChatGPT
            if(message['body'].startswith("file://")):
                file_information = message['body'][7:].split("://")
                file_extension = file_information[0]
                file_data = file_information[1]

                try:
                    data_decoded = base64.b64decode(file_data)
                    with open("file_received_from_" + contact_name + "." + file_extension, "wb") as file:
                        file.write(data_decoded)
                    print("Archivo recibido y descargado")
                except Exception as err:
                    print("Error al decodificar la informacion del archivo")
            else:
                if(contact_name == self.contact_chat.split('@')[0]):
                    print("\nMensaje de " + contact_name + ": " + message['body'])
                else:
                    print("\nMensaje de otra conversacion de " + contact_name + ": " + message['body'])

    async def menu(self):
        while self.is_connected:
            print("\nTienes las siguienes opciones disponibles para utilizar en el chat:\n")
            print("1) Mostrar todos los contactos y su estado")
            print("2) Agregar un usuario a los contactos")
            print("3) Mostrar detalles de contacto de un usuario")
            print("4) Comunicación 1 a 1 con cualquier usuario/contacto")
            print("5) Participar en conversaciones grupales")
            print("6) Definir mensaje de presencia")
            print("7) Enviar/recibir notificaciones")
            print("8) Enviar/recibir archivos")
            opcion = int(input("Ingrese la opcion que desees:"))

            if(opcion == 1):
                await self.showContacts()
            elif(opcion == 2):
                await self.addContact()
            elif(opcion == 3):
                await self.showContact()
            elif(opcion == 4):
                await self.sendMessage()

    async def showContacts(self):
        user_roster = self.client_roster
        contacts = user_roster.keys()
        contact_list = list(contacts)

        # Solucion brindada por ChatGPT
        if len(contact_list) == 1 and contact_list[0] == self.boundjid.bare:
            print("\nNo tienes contactos")
            return
        else:
            print("\nLista de usuarios")
            for user in contacts:
                if(user != self.boundjid.bare):
                    print("Usuario: ", user)
                    user_presence = user_roster.presence(user)
                    print(user_presence)
                    for answer, presence in user_presence.items():
                        if(presence['status']):
                            print("Estado: ", presence['status'])

    async def addContact(self):
        contact_jid = input("Ingresa el JID del contacto para agregar: ")
        try:
            self.send_presence_subscription(pto = contact_jid)
            print(f"Solicitud enviada existosamente a {contact_jid}")
            await self.get_roster()
        except IqError as err:
            print(f"Error enviando la solicitud: {err.iq['error']['text']}")
        except IqTimeout:
            print("No hay respuesta del servidor")

    async def showContact(self):
        contact_jid = input("Ingresa el JID del contacto para buscar: ")
        user_roster = self.client_roster
        contacts = user_roster.keys()
        contact_list = list(contacts)

        if(contact_jid not in contact_list):
            print("El usuario no se encuentra agregado como contacto")
        else:
            print("Usuario: ", contact_jid)
            user_presence = user_roster.presence(contact_jid)
            print(user_presence)
            for answer, presence in user_presence.items():
                print(presence)
                if(presence['status']):
                    print("Estado: ", presence['status'])

    async def sendMessage(self):
        contact_jid = await ainput("Ingresa el JID del contacto para enviar mensaje: ")
        self.contact_chat = contact_jid

        await aprint("Mensaje para", contact_jid.split("@")[0])
        await aprint("Si deseas salir escribe: exit chat")

        user_chatting = True
        while user_chatting:
            message = await ainput("Escribe el mensaje: ")
            print(message)
            if(message == "exit chat"):
                user_chatting = False
                self.contact_chat = ""
            else:
                self.send_message(mto=contact_jid, mbody=message, mtype='chat') 

def register_user(user_jid, password):
    # Se toma el jid
    jid = xmpp.JID(user_jid)
    # Se crea el cliente y se conecta
    user_account = xmpp.Client(jid.getDomain(), debug=[])
    user_account.connect()
    # Se devuelve la indicacion si se logro registrar
    return xmpp.features.register(user_account, jid.getDomain(), {
        'username': jid.getNode(),
        'password': password
    })