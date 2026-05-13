USUARIOS = {

    "admin": {
        "password": "1234",
        "rol": "admin"
    },

    "docente": {
        "password": "abcd",
        "rol": "docente"
    }
}


def login(usuario, password):

    if usuario in USUARIOS:

        if USUARIOS[usuario]["password"] == password:

            return {
                "autenticado": True,
                "rol": USUARIOS[usuario]["rol"]
            }

    return {
        "autenticado": False,
        "rol": None
    }