from datetime import date
from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Persona:
    id: str = field(default_factory=lambda: str(uuid4()), init=False)
    nombre: str


@dataclass
class Paquete:
    origen: str
    destino: str
    fecha: date
    remitente: Persona


ListaPaquetes = list[Paquete]
ListaPersonas = list[Persona]
COSTO_POR_PAQUETE = 10


class RemitenteDebeSerClienteException(Exception):
    ...


class CompaniaAerea:
    def __init__(self) -> None:
        self.paquetes: ListaPaquetes = []
        self.clientes: ListaPersonas = []

    def transportar_paquete(self, paquete: Paquete):
        if paquete.remitente.id in [cliente.id for cliente in self.clientes]:
            self.paquetes.append(paquete)
        else:
            raise RemitenteDebeSerClienteException(
                f"El remitente {paquete.remitente.nombre} no es cliente de la compania. La compania solo puede transportar paquetes de clientes."
            )

    def get_paquetes_de_dia(self, dia: date) -> ListaPaquetes:
        "retorna los paquetes que hayan sido registrados para cierto dia"
        return [paquete for paquete in self.paquetes if paquete.fecha == dia]

    def get_paquetes_transportados_en_dia(self, dia: date):
        "retorna los paquetes que hayan sido registrados para cierto dia y lo recaudado en ese dia"
        paquetes_de_dia = self.get_paquetes_de_dia(dia)
        return paquetes_de_dia, self.get_costo_envio_paquetes(paquetes_de_dia)

    def get_costo_envio_paquetes(self, paquetes):
        """Dada una lista de paquetes calcula el costo de envio de esos paquetes.
        Por cada paquete transportado la compañía aérea cobra 10$"""
        return COSTO_POR_PAQUETE * len(paquetes)
