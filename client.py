# Oscar Fernando López Barrios
# Carné 20679
# Proyecto 1

import slixmpp
import asyncio
from slixmpp.exceptions import IqError, IqTimeout
import base64
from client_functions import *

# Codigo del Cliente con referencia de https://slixmpp.readthedocs.io/en/latest/
# Codigo del Cliente con referencia de https://searchcode.com/file/58168360/examples/register_account.py/

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.name = jid.split('@')[0] # Se realiza el split para el username
        self.is_connected = False
        self.chat = ""
        self.room_nickname = ""
        self.chatroom = ""

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

            asyncio.create_task(menu(self))

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

    async def createChatRoom(self, name_room):
        try:
            print(name_room)
            name_room = f"{name_room}@conference.alumchat.xyz"
            print(name_room)
            self.plugin['xep_0045'].join_muc(name_room, self.boundjid.user)

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
