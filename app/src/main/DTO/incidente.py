from datetime import datetime


class Incidente:
    def __init__(self):
        self.id = None
        self.data = None
        self.cliente_incidentato = None

    def get_data(self):
        return self.data

    def set_data(self):
        self.data = datetime.now()

    def get_cliente_incidentato(self):
        return self.cliente_incidentato

    def set_cliente_incidentato(self, value):
        self.cliente_incidentato = value

    def set_id(self, value):
        self.id = value

    def get_id(self):
        return self.id

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.data,
            "cliente_incidentato": self.cliente_incidentato
        }