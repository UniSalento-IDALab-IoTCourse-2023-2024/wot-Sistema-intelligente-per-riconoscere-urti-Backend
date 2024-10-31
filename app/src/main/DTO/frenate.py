from datetime import datetime


class Frenate:
    def __init__(self):
        self.id = None
        self.data = None
        self.cliente = None

    def get_data(self):
        return self.data

    def set_data(self):
        self.data = datetime.now()

    def get_cliente(self):
        return self.cliente

    def set_id(self, value):
        self.id = value

    def get_id(self):
        return self.id

    def set_cliente(self, value):
        self.cliente = value

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.data,
            "cliente": self.cliente
        }