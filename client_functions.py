# Oscar Fernando López Barrios
# Carné 20679
# Proyecto 1

import xmpp
from aioconsole import ainput
from aioconsole.stream import aprint
from slixmpp.exceptions import IqError, IqTimeout
import asyncio

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

async def menu(self):
    while(self.is_connected):
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
            await showContacts(self)
        elif(opcion == 2):
            await addContact(self)
        elif(opcion == 3):
            await showContact(self)
        elif(opcion == 4):
            await sendMessage(self)
        elif(opcion == 5):
            await groupchatMenu(self)
        elif(opcion == 6):
            await sendMessage(self)

async def groupchatMenu(self):
    menu_var = True
    while(menu_var):
        print("\nTienes las siguienes opciones disponibles para utilizar en el chat:\n")
        print("1) Crear una sala")
        print("2) Unirse a una sala")
        print("3) Salir")
        opcion = int(input("Ingrese la opcion que desees:"))

        if(opcion == 1):
            roomname = input("Ingresa el nombre para la sala de chat: ")
            await createChatRoom(self, roomname)
        elif(opcion == 2):
            roomname = input("Ingresa el nombre de la sala de chat: ")
            await joinChatRoom(self)
        elif(opcion == 3):
            menu_var = False

async def showContacts(self):
    user_roster = self.client_roster
    contacts = user_roster.keys()
    contact_list = list(contacts)

    # Solucion brindada por ChatGPT
    if(len(contact_list) == 1 and contact_list[0] == self.boundjid.bare):
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

    await aprint("Mensaje para: ", contact_jid.split("@")[0])
    await aprint("Si deseas salir escribe: exit chat")

    user_chatting = True
    while user_chatting:
        message = await ainput("Escribe el mensaje: ")
        print(message)
        if(message == "exit chat"):
            user_chatting = False
            self.chat = ""
        else:
            self.send_message(mto=contact_jid, mbody=message, mtype='chat') 

# Referencia de https://xmpp.org/extensions/xep-0045.html#terms-rooms
# Referencia de https://slixmpp.readthedocs.io/en/latest/getting_started/muc.html
# Codigo con ayuda de ChatGPT
async def createChatRoom(self, name_room):
    try:
        print(name_room)
        name_room = f"{name_room}@conference.alumchat.xyz"
        print(name_room)
        self.plugin['xep_0045'].join_muc(name_room, self.boundjid.user)
        
        # Se espera debido a que de lo contrario brinda error al crearlo
        await asyncio.sleep(1)

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

        await self.plugin['xep_0045'].set_room_config(name_room, config=form)
        print("Se creo la sala de chat: ", name_room)
        self.send_message(mto=name_room, mbody="Bienvenidos a la sala: " + name_room, mtype='groupchat')
        
    except IqError as err:
        print("Error para crear la sala de chat")
    except IqTimeout:
        print("Tiempo de espera maximo para la creacion de la sala")


# Referencia de https://xmpp.org/extensions/xep-0045.html#terms-rooms
# Referencia de https://slixmpp.readthedocs.io/en/latest/getting_started/muc.html
# Codigo con ayuda de ChatGPT
async def joinChatRoom(self, name_room):
    self.chatroom = name_room 
    self.room_nickname = self.boundjid.user 

    print("Mensajes de la sala: ")

    try:
        await self.plugin['xep_0045'].join_muc(name_room, self.room_nickname)
    except IqError as err:
        print(f"Error al entrar a la sala de chat: {err.iq['error']['text']}")
    except IqTimeout:
        print("Sin respuesta del servidor")
        return

    await aprint("Mensajes de la Sala de Chat: ", self.chatroom.split("@")[0])
    await aprint("Para salir del chat escribe: exit chat")

    user_chatting = True
    while user_chatting:
        message = await ainput("Escribe el mensaje: ")
        if(message == "exit chat"):
            user_chatting = False
            self.chat = ""
            exitChatRoom(self)
        else:
            self.send_message(self.room, message, mtype='groupchat')

# Referencia de https://xmpp.org/extensions/xep-0045.html#terms-rooms
# Referencia de https://slixmpp.readthedocs.io/en/latest/getting_started/muc.html
def exitChatRoom(self):
    self['xep_0045'].leave_muc(self.chatroom, self.room_nickname)
    self.chatroom = ""
    self.room_nickname = ""