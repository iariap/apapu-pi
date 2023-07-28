import datetime
import unittest

from model import CompaniaAerea, Paquete, Persona, RemitenteDebeSerClienteException

# Dado el siguiente Sistema:
# Una compañía Aérea se dedica al negocio de transporte de cargas aéreas entre diferentes orígenes y destinos.
# La compañía solo puede transportar paquetes de Clientes.
# Por cada paquete transportado la compañía aérea cobra 10$
# Debe existir un método que genere un reporte con el total de paquetes transportados y el total recaudado para un día determinado.
# Se pide:
# + Programar en Python las clases y responsabilidades del sistema, crear los testeos unitarios que consideren necesarios.
# + No utilizar ningún framework en la solución (mantener una solución sencilla).


class TestApp(unittest.TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.compania = CompaniaAerea()
        self.compania.clientes = [Persona(nombre="Juan"), Persona(nombre="Pedro"), Persona(nombre="Lucas")]
        self.compania.paquetes = [
            Paquete("Lima", "Arequipa", datetime.date(2023, 7, 1), self.compania.clientes[0]),
            Paquete("Lima", "Trujillo", datetime.date(2023, 7, 1), self.compania.clientes[1]),
            Paquete("Trujillo", "Lima", datetime.date(2023, 7, 2), self.compania.clientes[2]),
        ]

    def test_despachar_paquete_cliente(self):
        dia = datetime.date(2022, 7, 1)
        paquete = Paquete("Jujuy", "Catamarca", dia, remitente=self.compania.clientes[1])
        cantidad_paquetes_anterior = len(self.compania.paquetes)
        self.compania.transportar_paquete(paquete)
        self.assertEqual(cantidad_paquetes_anterior + 1, len(self.compania.paquetes))

    def test_despachar_paquete_no_cliente(self):
        dia = datetime.date(2022, 7, 1)
        paquete = Paquete("Jujuy", "Catamarca", dia, remitente=Persona(nombre="Pablo"))
        with self.assertRaises(RemitenteDebeSerClienteException):
            self.compania.transportar_paquete(paquete)

    def test_paquetes_de_dia_vacio(self):
        dia = datetime.date(2022, 7, 1)
        paquetes_de_dia = self.compania.get_paquetes_de_dia(dia)
        self.assertEqual(len(paquetes_de_dia), 0)

    def test_paquetes_de_dia(self):
        dia = datetime.date(2023, 7, 1)
        paquetes_de_dia = self.compania.get_paquetes_de_dia(dia)
        self.assertEqual(len(paquetes_de_dia), 2)
        paquete1, paquete2 = paquetes_de_dia
        self.assertEqual(paquete1.remitente, self.compania.clientes[0])
        self.assertEqual(paquete2.remitente, self.compania.clientes[1])

    def test_paquetes_transportados_en_dia_sin_actividad(self):
        dia = datetime.date(2022, 7, 1)
        paquetes_de_dia, recaudacion = self.compania.get_paquetes_transportados_en_dia(dia)
        self.assertEqual(len(paquetes_de_dia), 0)
        self.assertEqual(recaudacion, 0)

    def test_paquetes_transportados_en_dia_con_actividad_1(self):
        dia = datetime.date(2023, 7, 1)
        paquetes_de_dia, recaudacion = self.compania.get_paquetes_transportados_en_dia(dia)
        self.assertEqual(len(paquetes_de_dia), 2)
        self.assertEqual(recaudacion, self.compania.get_costo_envio_paquetes(paquetes_de_dia))

    def test_paquetes_transportados_en_dia_con_actividad_2(self):
        dia = datetime.date(2023, 7, 2)
        paquetes_de_dia, recaudacion = self.compania.get_paquetes_transportados_en_dia(dia)
        self.assertEqual(len(paquetes_de_dia), 1)
        self.assertEqual(recaudacion, self.compania.get_costo_envio_paquetes(paquetes_de_dia))


if __name__ == '__main__':
    unittest.main()
