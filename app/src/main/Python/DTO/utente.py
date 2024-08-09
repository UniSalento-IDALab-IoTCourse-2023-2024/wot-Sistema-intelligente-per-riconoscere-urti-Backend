# Assuming this is the structure of the Utente class
class Utente:
    def __init__(self):
        self.nome = None
        self.cognome = None
        self.numero_telefono = None
        self.username = None
        self.email = None
        self.password = None

    def set_nome(self, nome):
        self.nome = nome

    def set_cognome(self, cognome):
        self.cognome = cognome

    def set_numero_telefono(self, numero_telefono):
        self.numero_telefono = numero_telefono

    def set_username(self, username):
        self.username = username

    def set_email(self, email):
        self.email = email

    def set_password(self, password):
        self.password = password

    def get_nome(self):
        return self.nome

    def get_cognome(self):
        return self.cognome

    def get_numero_telefono(self):
        return self.numero_telefono

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def to_dict(self):
        return {
            "nome": self.nome,
            "cognome": self.cognome,
            "numero_telefono": self.numero_telefono,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
