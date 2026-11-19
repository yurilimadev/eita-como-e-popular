import csv
import os
import unittest
from assets.style import carregar_html_header, carregar_html_popup, carregar_html_resumo


class TestMunicipiosAlinhamento(unittest.TestCase):
    def setUp(self):
        with open('data/municipios_2025.csv', encoding='utf-8') as f:
            self.rows = list(csv.DictReader(f))

    def test_total_municipios_2025(self):
        self.assertEqual(len(self.rows), 5571)

    def test_sem_campos_vazios(self):
        for i, row in enumerate(self.rows):
            for col in ('id', 'cidade', 'estado', '2025', 'latitude', 'longitude'):
                self.assertTrue(row[col], f"Linha {i} com coluna {col} vazia")

    def test_primeira_e_ultima_cidade_alinhadas(self):
        primeira = self.rows[0]
        self.assertEqual(primeira['id'], '1100015')
        self.assertEqual(primeira['cidade'], "Alta Floresta D'Oeste")
        self.assertEqual(primeira['estado'], 'RO')
        self.assertAlmostEqual(float(primeira['latitude']), -11.9291869, places=5)
        self.assertAlmostEqual(float(primeira['longitude']), -61.9942423, places=5)

        ultima = self.rows[-1]
        self.assertEqual(ultima['id'], '5300108')
        self.assertEqual(ultima['cidade'], 'Brasília')
        self.assertEqual(ultima['estado'], 'DF')
        self.assertAlmostEqual(float(ultima['latitude']), -15.7975154, places=5)
        self.assertAlmostEqual(float(ultima['longitude']), -47.8918874, places=5)

    def test_sem_coordenadas_duplicadas_ou_centro_brasil(self):
        coords = [(float(r['latitude']), float(r['longitude'])) for r in self.rows]
        self.assertEqual(len(coords), len(set(coords)))
        self.assertNotIn((-14.235004, -51.92528), coords)

    def test_templates_html_e_mascotes(self):
        header = carregar_html_header()
        self.assertIn('IBGE 2025', header)

        resumo = carregar_html_resumo(1234, 22.15, 'Curitiba', 'PR', 1800000)
        self.assertIn('1.234', resumo)
        self.assertIn('22,1%', resumo)
        self.assertIn('Curitiba - PR', resumo)

        popup = carregar_html_popup('abc123', 'https://github.com/yurilimadev/eita-como-e-popular')
        self.assertIn('data:image/png;base64,abc123', popup)

        for img in ('assets/mascote-sucesso.png', 'assets/mascote-poucos-seguidores.png', 'assets/mascote-mapa.png'):
            self.assertTrue(os.path.exists(img), f"Imagem ausente: {img}")


if __name__ == '__main__':
    unittest.main()
