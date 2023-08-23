import slixmpp
from slixmpp.xmlstream.stanzabase import ET
from slixmpp.exceptions import IqError, IqTimeout

class DeleteClient(slixmpp.ClientXMPP):

    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.add_event_handler("session_start", self.start)
        
    async def start(self, event):
        self.send_presence()
        await self.get_roster()
        await self.unregister()
        self.disconnect()
        
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