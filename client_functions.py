# Oscar Fernando López Barrios
# Carné 20679
# Proyecto 1

import xmpp

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