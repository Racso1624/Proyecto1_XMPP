# Oscar Fernando López Barrios
# Carné 20679
# Proyecto 1

# Se realizan los imports
import slixmpp
from slixmpp.xmlstream.stanzabase import ET
from slixmpp.exceptions import IqError, IqTimeout

# Codigo con ayuda de ChatGPT
# Se realiza la Clase 
class DeleteClient(slixmpp.ClientXMPP):
    # Se realiza el init de la clase
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.add_event_handler("session_start", self.start)
    # Se realiza el start
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.unregister()
        self.disconnect()
    # Se realiza el desregistro para el usuario
    async def unregister(self):
        server_response = self.Iq()
        server_response['type'] = 'set'
        server_response['from'] = self.boundjid.user
        fragment = ET.fromstring("<query xmlns='jabber:iq:register'><remove/></query>")
        server_response.append(fragment)
        
        try:
            await server_response.send()
            print(f"Se elimino la cuenta: {self.boundjid.jid}")
        except IqError as err:
            print(f"Error al eliminar la cuenta: {err.iq['error']['text']}")
            self.disconnect()
        except IqTimeout:
            print("No hay respuesta del servidor")
            self.disconnect()