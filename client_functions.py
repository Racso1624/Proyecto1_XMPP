# Oscar Fernando López Barrios
# Carné 20679
# Proyecto 1

# Se importa libreria
import xmpp

# Se realiza el registro del usuario
def register_user(user_jid, password):
    # Obtiene el JID
    jid = xmpp.JID(user_jid)
    # Se crea el cliente y se conecta
    user_account = xmpp.Client(jid.getDomain(), debug=[])
    user_account.connect()
    # Se devuelve el mensaje de conexion
    return xmpp.features.register(user_account, jid.getDomain(), {
        'username': jid.getNode(),
        'password': password
    })