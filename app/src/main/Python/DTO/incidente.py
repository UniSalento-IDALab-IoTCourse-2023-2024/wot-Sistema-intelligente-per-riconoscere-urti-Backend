from datetime import datetime


class Incidente:
    def __init__(self):
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

    def to_dict(self):
        return {
            "date": self.data,
            "cliente_incidentato": self.cliente_incidentato
        }