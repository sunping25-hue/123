"""Tests for mcw-onepage-site: calculator maths + content guardrails. Run: python3 -m pytest tests/test_mcw_onepage.py  (or python3 tests/test_mcw_onepage.py)"""
import json, re, subprocess, pathlib, unittest
SITE = pathlib.Path(__file__).resolve().parent.parent / "mcw-onepage-site"
TEXT_FILES = ["index.html", "app.js", "calc.js", "config.js", "style.css"]

def node_compute(inp):
    js = f"const c=require({json.dumps(str(SITE/'calc.js'))});console.log(JSON.stringify(c.compute({json.dumps(inp)})))"
    return json.loads(subprocess.check_output(["node", "-e", js]))

class Calc(unittest.TestCase):
    def test_basic(self):
        r = node_compute(dict(machines=6, rent=40000, turns=5, price=100, utilities=30000, investment=2000000))
        self.assertTrue(r["ok"]); self.assertEqual(r["dayRev"], 3000); self.assertEqual(r["monthRev"], 90000)
        self.assertEqual(r["yearRev"], 1080000); self.assertEqual(r["monthNet"], 20000); self.assertEqual(r["yearNet"], 240000)
        self.assertAlmostEqual(r["dayNet"], 20000/30); self.assertAlmostEqual(r["payback"], 100)
    def test_loss_no_payback(self):
        r = node_compute(dict(machines=1, rent=50000, turns=1, price=50, utilities=10000, investment=100))
        self.assertTrue(r["ok"]); self.assertIsNone(r["payback"])
    def test_invalid(self):
        for bad in [dict(machines=0), dict(machines=13), dict(rent=""), dict(price=-1), dict(investment=None)]:
            inp = dict(machines=3, rent=1, turns=1, price=1, utilities=1, investment=1); inp.update(bad)
            self.assertFalse(node_compute(inp)["ok"], bad)

class Content(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all = "".join((SITE/f).read_text(encoding="utf-8") for f in TEXT_FILES)
        cls.html = (SITE/"index.html").read_text(encoding="utf-8")
    def test_forbidden(self):
        for s in ["@mcw17", "台灣製造", "0973688139", "藍光", "photos_original_for_dev", "保證回本", "限時", "名額有限", "第一品牌"]:
            self.assertNotIn(s, self.all, s)
    def test_no_superlative(self):
        self.assertIsNone(re.search(r"最", self.html))
    def test_only_amount_150(self):
        amounts = re.findall(r"\d[\d,]*\s*(?:萬|元)", re.sub(r"<script.*?</script>", "", self.html, flags=re.S))
        self.assertEqual(sorted(set(a.replace(" ", "") for a in amounts)), ["150萬"], amounts)
    def test_contacts(self):
        for s in ["@mcw27", "07-788-1902", "0970-622-778", "mcw17", "高雄市大寮區大寮路474巷20之2號", "科嘉國際有限公司"]:
            self.assertIn(s, self.html)
    def test_jsonld(self):
        blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', self.html, re.S)
        data = [json.loads(b) for b in blocks]
        faq = [d for d in data if d.get("@type") == "FAQPage"]
        self.assertTrue(faq and len(faq[0]["mainEntity"]) >= 5)
    def test_no_ai_qa(self):
        self.assertNotRegex(self.all.lower(), r"openai|anthropic|api[_-]?key")
    def test_images_size(self):
        for p in (SITE/"img").iterdir():
            lim = 400_000 if p.name.startswith("hero") else 300_000
            self.assertLessEqual(p.stat().st_size, lim, p.name)

if __name__ == "__main__":
    unittest.main()
