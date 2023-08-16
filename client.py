import xmpp
import slixmpp
import asyncio
from slixmpp.exceptions import IqError, IqTimeout

# Codigo del Cliente con referencia de https://slixmpp.readthedocs.io/en/latest/
# Codigo del Cliente con referencia de https://searchcode.com/file/58168360/examples/register_account.py/

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.name = jid.split('@')[0] # Se realiza el split para el username
        self.is_connected = False

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

    async def showContacts(self):
        user_roster = self.client_roster
        contacts = user_roster.keys()
        contact_list = list(contacts)

        if not contacts or contact_list[0] == self.boundjid.bare:
            print("\nNo tienes contactos")
            return
        else:
            for user in contacts:
                print("Usuario: ", user)
                user_presence = user_roster.presence(user)
                for answer, presence in user_presence.items():
                    if(presence['status']):
                        print("Estado: ", presence['status'])



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