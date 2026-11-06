import unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1]/'shinox-v2-site'
class RevenueCalc(unittest.TestCase):
    def test_markup_and_formula(self):
        for f in ['index.html','en/index.html']:
            h=(S/f).read_text()
            for id_ in ['revcalc-customers','revcalc-month','revcalc-year','investment-tools']:self.assertIn(f'id="{id_}"',h)
            self.assertIn('revenue-calc.js',h)
        js=(S/'revenue-calc.js').read_text()
        self.assertIn('DAYS = 30, MONTHS = 12',js);self.assertIn('revcalc-ticket',js)
        for f in ['index.html']:
            h=(S/f).read_text()
            for v in (250,350,450,550,650):self.assertIn(f'<option value="{v}"',h)
            self.assertIn('<option value="250" selected>',h)
        self.assertEqual(100*250*30,750000);self.assertEqual(750000*12,9000000)

class RevenueCalcCurrency(unittest.TestCase):
    def test_en_usd_zh_ntd(self):
        en=(S/'en/index.html').read_text();zh=(S/'index.html').read_text()
        self.assertIn('data-currency="US$"',en);self.assertNotIn('>NT$250<',en)
        for v in (8,11,14,17,20):self.assertIn(f'<option value="{v}"',en)
        self.assertIn('<option value="8" selected>US$8</option>',en);self.assertIn('Figures in US$ for reference only.',en)
        self.assertNotIn('data-currency',zh);self.assertIn('<option value="250" selected>NT$250</option>',zh)
        self.assertEqual(100*8*30,24000);self.assertEqual(24000*12,288000)
