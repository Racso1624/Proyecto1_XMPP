import logging
import xmpp
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

# Codigo referenciado de https://slixmpp.readthedocs.io/en/latest/

class Client(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.username = jid.split('@')[0] # Se realiza el split para el username
        self.user_connected = False
        self.nickname = ""
        self.chat = ""
        self.room = ""

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()

def register_user(user_jid, password):
    # Se toma el jid
    jid = xmpp.JID(user_jid)
    # Se crea el cliente y se conecta
    user_account = xmpp.Client(jid.getDomain(), debug=[])
    user_account.connect()
    return xmpp.features.register(user_account, jid.getDomain(), {
        'username': jid.getNode(),
        'password': password
    })
    