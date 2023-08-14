import logging
from slixmpp import ClientXMPP

# Codigo referenciado de https://slixmpp.readthedocs.io/en/latest/

class RegisterUser(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def register(self, iq):
        response = self.Iq()
        response['type'] = 'set'
        response['register']['username'] = self.boundjid.user
        response['register']['password'] = self.password
        print(response)

        try:
            response.send(now=True)
            logging.info("Usuario registrado correctamente.")
        except IqError as err:
            logging.error("Error al registrar el usuario: %s" % err.iq['error']['text'])
        except IqTimeout:
            logging.error("Tiempo de espera agotado al registrar el usuario.")