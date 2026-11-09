import unittest
from decimal import Decimal

from calculadora import calcular_preco_para_repasse, calcular_repasse


class TestCalculadora(unittest.TestCase):
    def test_empadao_amora_preco_exato_e_arredondado(self):
        exato, sugerido = calcular_preco_para_repasse(
            Decimal("12"), Decimal("12"), Decimal("3.2"), Decimal("3.99"), Decimal("0.10")
        )
        self.assertEqual(exato, Decimal("18.86"))
        self.assertEqual(sugerido, Decimal("18.90"))

    def test_repasse_por_distancia(self):
        preco = Decimal("18.90")
        self.assertEqual(calcular_repasse(preco, Decimal("12"), Decimal("3.2"), Decimal("3.99")), Decimal("12.04"))
        self.assertEqual(calcular_repasse(preco, Decimal("12"), Decimal("3.2"), Decimal("5.99")), Decimal("10.04"))
        self.assertEqual(calcular_repasse(preco, Decimal("12"), Decimal("3.2"), Decimal("7.99")), Decimal("8.04"))
        self.assertEqual(calcular_repasse(preco, Decimal("12"), Decimal("3.2"), Decimal("9.99")), Decimal("6.04"))

    def test_nao_aceita_percentual_de_100_ou_mais(self):
        with self.assertRaises(ValueError):
            calcular_preco_para_repasse(
                Decimal("12"), Decimal("80"), Decimal("20"), Decimal("3.99")
            )


if __name__ == "__main__":
    unittest.main()
