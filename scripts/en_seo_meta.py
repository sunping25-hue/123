#!/usr/bin/env python3
"""English SEO head metadata: titles, descriptions, canonical, hreflang, OG/Twitter, Product JSON-LD.
Edits only <head> tags with targeted regex; body markup untouched."""
import json, re, html
from pathlib import Path
SITE = Path(__file__).resolve().parents[1] / 'shinox-v2-site'
O = 'https://www.shinox-wash.com'
OG_IMG = O + '/og-image.jpg'

META = {
 'index.html': ('Self-Service Car Wash Equipment & Touchless Machines | ShinoX',
  'ShinoX self-service car wash equipment, 9-in-1 coin-operated control boxes and B2 / M9 touchless automatic car wash machines, plus site planning for new car washes.'),
 'about.html': ('About ShinoX | Car Wash Equipment & Site Integration',
  'ShinoX focuses on car wash equipment, systems integration and complete site development for car wash entrepreneurs and operators, from equipment selection to bay layout.'),
 'business.html': ('Start a Car Wash Business: Self-Service Site Planning | ShinoX',
  'Planning a car wash business startup? ShinoX helps you review site conditions, wash bay numbers, vehicle circulation, equipment and construction. Book a free site survey.'),
 'contact.html': ('Contact ShinoX | Car Wash Equipment Enquiries & Site Survey',
  'Contact ShinoX about touchless car wash machines and self-service car wash equipment: Tel/WhatsApp +886 979 666 302, LINE @shinox, or email. Ask for a free site survey.'),
 'faq.html': ('Car Wash Equipment FAQ: Costs, Payback, B2 & M9 | ShinoX',
  'Answers on starting a self-service car wash: costs, non-guaranteed payback, site size, B2 and M9 touchless car wash machines, financing, repairs and machine viewings.'),
 'news.html': ('News & Car Wash Technology | ShinoX',
  'ShinoX news: car wash technology, vehicle length detection, license plate recognition and payments, technical support and new wash concepts.'),
 'news-beyond-the-machine.html': ('Car Wash Technical Support & Business Guidance | ShinoX',
  'A car wash machine is the start of a business. ShinoX support covers equipment introduction, opening preparations and day-to-day car wash operations.'),
 'news-japanese-future-wash.html': ('Japanese Future Wash Concept (Coming Soon) | ShinoX',
  'ShinoX is developing a car wash concept that combines European-style wash bay planning with the careful, user-focused spirit of Japanese car care. Coming soon.'),
 'news-smart-wash.html': ('License Plate Recognition & Payments for Car Washes | ShinoX',
  'ShinoX connects license plate recognition, membership and digital payment options to support a smoother unattended car wash experience, from arrival to wash start.'),
 'news-vehicle-length.html': ('Vehicle Length Detection for Automatic Car Washes | ShinoX',
  'The ShinoX automatic car wash system detects vehicle length with a sensor and sends it to the control system, so the wash range follows each car\u2019s length.'),
 'products.html': ('Car Wash Equipment: Touchless & Self-Service Systems | ShinoX',
  'Browse ShinoX car wash equipment: B2 and M9 touchless car wash machines, 9-in-1 self-service control boxes, cloud top-up kiosks, payment terminals and peripherals.'),
 'projects.html': ('Car Wash Projects & Site Planning | ShinoX',
  'ShinoX car wash projects: site planning, vehicle circulation and equipment configuration. Only authorized and verified sites are published.'),
 'products/wash-1.html': ('B2 Dual-Arm Touchless Automatic Car Wash Machine | ShinoX',
  'ShinoX B2 dual-arm 360\u00b0 touchless automatic car wash machine: about 2 min 30 s and about 100 L of water per car, 7-in-1 wash functions and ultrasonic vehicle sensing.'),
 'products/wash-2.html': ('M9 Single-Arm 360\u00b0 Touchless Car Wash Machine | ShinoX',
  'ShinoX M9 single-arm 360\u00b0 touchless car wash machine in Standard, Plus and Premium versions: quick wash about 2 min, deep wash about 6 min, ready for 24-hour use.'),
 'products/self-3.html': ('9-in-1 Self-Service Car Wash Control Box | ShinoX',
  'ShinoX 9-in-1 control box for self-service car wash bays: wet and dry zone functions, coins, stored-value cards, mobile payments and cloud membership points.'),
 'products/self-1.html': ('Water Softening & Filtration for Car Wash Sites | ShinoX',
  'Plan water softening and filtration for a self-service car wash: review water quality and local supply with ShinoX before selecting equipment.'),
 'products/self-2.html': ('Car Wash Wastewater Recycling Planning | ShinoX',
  'Plan car wash wastewater treatment and recycling with ShinoX alongside your site\u2019s pipework, drainage and applicable requirements.'),
 'products/self-4.html': ('Card Sales & Recharge Machine for Car Washes | ShinoX',
  'Fit card sales and recharging into the self-service car wash customer journey. Review equipment arrangements and on-site usage flow with ShinoX.'),
 'products/self-5.html': ('Cloud Top-up Kiosk (Mobile Wallet) for Car Washes | ShinoX',
  'ShinoX cloud top-up kiosk for self-service car washes: cash top-up and QR Code member login, mobile payment, cloud back-office reports and an optional coin changer.'),
 'products/self-6.html': ('Touchscreen Cloud Payment Terminal for Car Washes | ShinoX',
  'Touchscreen cloud payment terminal for self-service car wash sites. Review the interface and payment flow with ShinoX; integration depends on the product version.'),
 'products/self-7.html': ('1-1 Coin Box for Self-Service Car Wash Equipment | ShinoX',
  'Plan a 1-1 coin box for self-service car wash equipment. Discuss coin box configuration and integration conditions with ShinoX.'),
 'products/peripheral-1.html': ('Vacuum Unit for Self-Service Car Wash Sites | ShinoX',
  'Make interior cleaning part of your self-service car wash. Discuss vacuum unit selection and placement within your site layout with ShinoX.'),
 'products/peripheral-2.html': ('Coin-Operated Ozone Machine for Car Washes | ShinoX',
  'Coin-operated ozone machine for car wash sites. Discuss its purpose, operation and safety conditions with ShinoX before configuration.'),
 'products/peripheral-3.html': ('Coin-Operated Air Gun for Car Wash Sites | ShinoX',
  'Coin-operated air gun for self-service car washes. Discuss air supply, coin payment and placement around your operating needs with ShinoX.'),
 'products/peripheral-4.html': ('Coin-Operated Water Blower for Car Washes | ShinoX',
  'Coin-operated water blower for the drying step of a self-service car wash. Plan placement, charging and site layout with ShinoX.'),
 'products/peripheral-5.html': ('Compartment Vending Machine for Car Wash Sites | ShinoX',
  'Add compartment vending to your car wash site. Discuss the intended items and on-site service arrangements with ShinoX.'),
 'products/peripheral-6.html': ('Parts Vending Machine for Car Wash Sites | ShinoX',
  'Parts vending machine for car wash sites: start with the parts you intend to sell, then review equipment configuration and daily management with ShinoX.'),
}
PRODUCT_NAME = {'products/wash-1.html':'ShinoX B2 Dual-Arm Touchless Automatic Car Wash Machine',
                'products/wash-2.html':'ShinoX M9 Single-Arm 360° Touchless Car Wash Machine',
                'products/self-3.html':'ShinoX 9-in-1 Car Wash Control Box'}
NOINDEX = {'404.html':'404.html','privacy.html':'privacy.html','privacy/index.html':'privacy.html','terms.html':'terms.html','terms/index.html':'terms.html'}
ORG_LD = None

ALT_RE = re.compile(r'[ \t]*<link\b(?=[^>]*\brel=["\']alternate["\'])(?=[^>]*\bhreflang=)[^>]*>\n?', re.I)
CANON_RE = re.compile(r'[ \t]*<link\b(?=[^>]*\brel=["\']canonical["\'])[^>]*>\n?', re.I)
OG_RE = re.compile(r'[ \t]*<meta\b(?=[^>]*\b(?:property|name)=["\'](?:og:|twitter:))[^>]*>\n?', re.I)
TITLE_RE = re.compile(r'<title>.*?</title>', re.S)
DESC_RE = re.compile(r'<meta\b(?=[^>]*\bname=["\']description["\'])[^>]*>', re.I)

def esc(s): return html.escape(s, quote=True)

def links(target, lang_self, zh_path, en_path):
    return ''.join([
      f'<link rel="canonical" href="{O}/{target}">',
      f'<link rel="alternate" hreflang="zh-Hant" href="{O}/{zh_path}">',
      f'<link rel="alternate" hreflang="en" href="{O}/{en_path}">',
      f'<link rel="alternate" hreflang="x-default" href="{O}/{en_path}">'])

def og(title, desc, url):
    return ''.join([
      '<meta property="og:locale" content="en_US">','<meta property="og:locale:alternate" content="zh_TW">',
      '<meta property="og:type" content="website">','<meta property="og:site_name" content="ShinoX Car Wash Systems">',
      f'<meta property="og:title" content="{esc(title)}">',f'<meta property="og:description" content="{esc(desc)}">',
      f'<meta property="og:url" content="{url}">',f'<meta property="og:image" content="{OG_IMG}">',
      '<meta property="og:image:width" content="1200">','<meta property="og:image:height" content="630">',
      '<meta property="og:image:alt" content="ShinoX Car Wash Systems">',
      '<meta name="twitter:card" content="summary_large_image">',f'<meta name="twitter:title" content="{esc(title)}">',
      f'<meta name="twitter:description" content="{esc(desc)}">',f'<meta name="twitter:image" content="{OG_IMG}">'])

def head_edit(text, fn):
    i = text.lower().find('</head>'); head, rest = text[:i], text[i:]
    return fn(head) + rest

def en_page(rel, title, desc, noindex_target=None):
    p = SITE/'en'/rel; t = p.read_text()
    canon = 'en/'+(noindex_target or rel); zh = noindex_target or rel
    def fn(h):
        h = ALT_RE.sub('', h); h = CANON_RE.sub('', h); h = OG_RE.sub('', h)
        if title:
            h = TITLE_RE.sub('<title>'+esc(title).replace('&#x27;',"'")+'</title>', h, count=1)
            if DESC_RE.search(h): h = DESC_RE.sub('<meta name="description" content="'+esc(desc)+'">', h, count=1)
            else: h = h.replace('</title>', '</title><meta name="description" content="'+esc(desc)+'">', 1)
        else:
            m = TITLE_RE.search(h); title_ = html.unescape(m.group()[7:-8]) if m else 'ShinoX'
            d = DESC_RE.search(h); desc_ = html.unescape(re.search(r'content="([^"]*)"', d.group()).group(1)) if d else title_
            return h + links(canon, 'en', zh, canon) + og(title_, desc_, O+'/'+canon)
        h = h + links(canon, 'en', zh, canon) + og(title, desc, O+'/'+canon)
        if 'application/ld+json' not in h and ORG_LD: h += ORG_LD
        return h
    t = head_edit(t, fn)
    if rel in PRODUCT_NAME:
        def fix(m):
            j = json.loads(m.group(2))
            for n in j.get('@graph', []):
                if n.get('@type') == 'Product':
                    n['name'] = PRODUCT_NAME[rel]; n['description'] = desc
                if n.get('@type') == 'BreadcrumbList': n['itemListElement'][-1]['name'] = PRODUCT_NAME[rel]
            return m.group(1)+json.dumps(j, ensure_ascii=False)+m.group(3)
        t = re.sub(r'(<script type="application/ld\+json">)(.*?)(</script>)', lambda m: fix(m) if '"Product"' in m.group(2) else m.group(), t, flags=re.S)
    p.write_text(t)

def zh_page(rel, noindex_target=None):
    p = SITE/rel
    if not p.exists(): return
    zh = noindex_target or rel; en = 'en/'+zh
    t = p.read_text()
    p.write_text(head_edit(t, lambda h: CANON_RE.sub('', ALT_RE.sub('', h)) + links(zh, 'zh', zh, en)))

def main():
    global ORG_LD
    src = (SITE/'en/news.html').read_text()
    ORG_LD = re.search(r'<script type="application/ld\+json">.*?</script>', src, re.S).group()
    for rel,(ti,de) in META.items(): en_page(rel, ti, de); zh_page(rel)
    for rel,tgt in NOINDEX.items(): en_page(rel, None, None, tgt); zh_page(rel, tgt)
if __name__ == '__main__': main()
