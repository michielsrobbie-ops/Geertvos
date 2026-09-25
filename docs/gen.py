# Genereert de statische pagina's van geertvos.be (header/footer één keer gedefinieerd).
# Draaien vanuit docs/: python3 gen.py  → schrijft de html-bestanden in de projectmap.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site') if os.path.isdir(os.path.join(HERE, 'site')) else os.path.dirname(HERE)
DOMAIN = 'https://geertvos.be'
V = '20260925f'         # versie voor css/js — ophogen bij elke wijziging
# Nummers bevestigd door de klant (25 sept). Geen namen op de site, wel waarvoor je welk nummer belt.
TEL_TECH = '+32495460646'       # servicetechniekers (Lorenzo)
TEL_PROJ = '+32477416045'       # facilityprojecten (Pieter-Jan)
TEL_TECH_TXT = '+32 495 46 06 46'
TEL_PROJ_TXT = '+32 477 41 60 45'
MAIL = 'lorenzo.sterckx@electro-geertvos.be'   # bevestigd door Lorenzo (25 sept): alles gaat hiernaartoe

NAV = [('ons-verhaal', 'Ons verhaal')]


import json
def schema(slug, kruimel=None, service=None, faq=None):
    out = []
    if faq:
        out.append({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]})
    if kruimel:
        out.append({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
            {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},
            {"@type":"ListItem","position":2,"name":kruimel,"item":f"{DOMAIN}/{slug}/"}]})
    if service:
        out.append({"@context":"https://schema.org","@type":"Service","name":service[0],"description":service[1],
            "serviceType":service[0],"url":f"{DOMAIN}/{slug}/","areaServed":{"@type":"Place","name":"Limburg en de Kempen, België"},
            "provider":{"@type":"LocalBusiness","name":"BV Geert Vos","url":DOMAIN+"/"}})
    return ''.join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>\n' for o in out)

def head(title, desc, slug, extra=''):
    url = DOMAIN + '/' if slug == 'index' else f'{DOMAIN}/{slug}/'
    return f'''<!DOCTYPE html>
<html lang="nl-BE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/img/og-team.jpg">
<meta property="og:locale" content="nl_BE">
<meta name="theme-color" content="#141518">
<link rel="preload" href="/fonts/bricolage-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/style.css?v={V}">
{extra}
</head>
<body>
<a class="skip" href="#inhoud">Naar de inhoud</a>
'''

# (slug, tekst, niveau) — niveau 0 = pijler, 1 = onderdeel
DIENST_MENU = [('servicetechniekers', 'Servicetechniekers', 0), ('elektriciens', 'Elektriciens', 1), ('mechaniciens', 'Mechaniciens', 1),
  ('facilityprojecten', 'Facilityprojecten', 0), ('verhuizingen', 'Verhuizingen &amp; logistiek', 1),
  ('kabelmanagement', 'Kabelmanagement &amp; werkplekken', 1), ('verlichting', 'Verlichting', 1),
  ('/diensten/#extra', 'Extra diensten', 0), ('fietsenbeheer', 'Fietsenbeheer', 1), ('opslag', 'Opslag &amp; voorraad', 1)]

def header(slug):
    cur = ' aria-current="page"'
    dienst_slugs = [d[0] for d in DIENST_MENU if not d[0].startswith('/')] + ['diensten']
    sub = ''.join(f'<a href="{s if s.startswith("/") else "/" + s + "/"}" class="{"sub-kop" if n == 0 else "sub-kind"}"{cur if s == slug else ""}>{t}</a>' for s, t, n in DIENST_MENU)
    links = ''.join(f'<a href="/{s}/"{cur if s == slug else ""}>{t}</a>' for s, t in NAV)
    return f'''<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/" aria-label="BV Geert Vos, naar de startpagina"><img src="/img/logo-nav.svg" alt="BV Geert Vos" width="236" height="64"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu"><span></span>Menu</button>
    <nav class="nav" id="menu" aria-label="Hoofdmenu">
      <a href="/"{cur if slug == 'index' else ''}>Home</a>
      <div class="sub{' sub-actief' if slug in dienst_slugs else ''}">
        <a href="/diensten/" class="sub-link"{cur if slug == 'diensten' else ''}>Diensten</a><button class="sub-knop" type="button" aria-expanded="false" aria-label="Diensten openen"></button>
        <div class="sub-menu">{sub}</div>
      </div>
      {links}<a class="nav-vac" href="/vacatures/"{cur if slug == 'vacatures' else ''}>Vacatures</a><a class="nav-cta" href="/contact/">Contact</a></nav>
  </div>
</header>
'''

def kop(label, h1, lead, kruimel):
    return f'''<div class="kop">
  <div class="wrap">
    <div>
      <p class="kruimel"><a href="/">Home</a> / {kruimel}</p>
      <p class="label label-licht">{label}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
    </div>
    <img class="lampje" src="/img/bulb-wit.svg" alt="" width="120" height="134">
  </div>
  <div class="stroom"></div>
</div>
'''

CTA = f'''<div class="stroom"></div>
<div class="cta-band">
  <div class="wrap">
    <div>
      <p class="label">Contact</p>
      <h2>Zeg wat je nodig hebt.</h2>
      <p>Contacteer onze servicecoördinator. Wij zorgen voor een reactie binnen 24 uur.</p>
    </div>
    <div class="knoppen">
      <a class="btn btn-geel" href="/contact/">Contact</a>
      <a class="btn btn-licht tel-knop" href="tel:{TEL_TECH}"><small>Servicetechniekers</small>{TEL_TECH_TXT}</a>
      <a class="btn btn-licht tel-knop" href="tel:{TEL_PROJ}"><small>Projecten</small>{TEL_PROJ_TXT}</a>
    </div>
  </div>
</div>
'''

FOOT = f'''<footer class="site-foot">
  <div class="wrap">
    <div>
      <img src="/img/logo-nav.svg" alt="BV Geert Vos" width="258" height="70">
      <p>Servicetechniekers en facilityprojecten voor langdurige samenwerkingen, vanuit Meerhout. Al 30 jaar elke dag aanwezig bij Nike. Een hecht en bereikbaar team.</p>
    </div>
    <div>
      <p class="foot-kop">Diensten</p>
      <ul>
        <li><a href="/servicetechniekers/">Servicetechniekers</a></li>
        <li><a href="/elektriciens/">Elektriciens</a></li>
        <li><a href="/mechaniciens/">Mechaniciens</a></li>
        <li><a href="/facilityprojecten/">Facilityprojecten</a></li>
        <li><a href="/verhuizingen/">Verhuizingen en logistiek</a></li>
        <li><a href="/kabelmanagement/">Kabelmanagement en werkplekken</a></li>
        <li><a href="/verlichting/">Verlichting</a></li>
        <li><a href="/fietsenbeheer/">Fietsenbeheer</a></li>
        <li><a href="/opslag/">Opslag en voorraad</a></li>
      </ul>
    </div>
    <div>
      <p class="foot-kop">Bedrijf</p>
      <ul>
        <li><a href="/ons-verhaal/">Ons verhaal</a></li>
        <li><a href="/vacatures/">Vacatures</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacybeleid/">Privacybeleid</a></li>
      </ul>
    </div>
    <div>
      <p class="foot-kop">Contact</p>
      <address>BV Geert Vos<br>Bevrijdingslaan 256<br>2450 Meerhout, België<br>
      Servicetechniekers: <a href="tel:{TEL_TECH}">{TEL_TECH_TXT}</a><br>
      Projecten: <a href="tel:{TEL_PROJ}">{TEL_PROJ_TXT}</a><br>
      <a href="mailto:{MAIL}">{MAIL}</a></address>
    </div>
  </div>
  <div class="foot-onder">
    <span>© 2026 BV Geert Vos · BTW BE 0862.515.981</span>
    <span>Website door <a href="https://maxxmarketing.eu" rel="noopener">MaxxMarketing</a></span>
  </div>
</footer>
<script src="/js/main.js?v={V}"></script>
</body>
</html>
'''

def faq_blok(items, kop='Veelgestelde vragen', paper=True):
    return ('<section class="sec-paper">' if paper else '<section>') + '<div class="wrap"><div class="sec-kop"><p class="label">Vragen</p><h2>' + kop + '</h2></div><div class="faq">' + ''.join(
        f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in items) + '</div></div></section>'

def fig(src, alt, cap=''):
    return f'<figure><img src="{src}" alt="{alt}" loading="lazy" width="460" height="600"><figcaption>{cap or alt}</figcaption></figure>'

def voor_na(voor, na, cap):
    return (f'<div class="vergelijk" data-vergelijk><div class="vergelijk-beeld">'
            f'<img class="vergelijk-na" src="{na[0]}" alt="Na: {na[1]}" loading="lazy" width="460" height="600">'
            f'<div class="vergelijk-voor"><img src="{voor[0]}" alt="Voor: {voor[1]}" loading="lazy" width="460" height="600"></div>'
            f'<div class="vergelijk-lijn" aria-hidden="true"><span></span></div>'
            f'<span class="vergelijk-tag vergelijk-tag-voor" aria-hidden="true">Voor</span><span class="vergelijk-tag vergelijk-tag-na" aria-hidden="true">Na</span>'
            f'<input type="range" min="0" max="100" value="50" aria-label="Schuif tussen voor en na"></div>'
            f'<p class="voorna-cap">{cap}</p></div>')

WERK_ELEK = '''<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Werk in beeld</p><h2>Zo ziet ons werk eruit.</h2><p class="lead">Foto's van opdrachten die onze elektriciens uitvoerden: verlichting, lichtmasten en wat er gebeurt als kabelmanagement ontbreekt.</p></div>
    <p style="max-width:62ch;margin:-20px 0 28px">Voor-en-nafoto's van kabelmanagement staan op de pagina <a href="/kabelmanagement/">kabelmanagement en werkplekinrichting</a>.</p>
    <h3 class="gal-kop">Waarom kabelmanagement telt</h3>
    <p style="max-width:62ch;margin-bottom:20px">Slecht kabelmanagement leidt tot beschadigde kabels en stekkers, en uiteindelijk tot uitbranding. Dit zijn voorbeelden die we bij klanten aantroffen en herstelden.</p>
    <div class="galerij galerij-3">
      ''' + fig('/img/werk/kabel-geklemd-kast.webp', 'Kabel geklemd achter een metalen kast') + fig('/img/werk/uitgebrande-kabel.webp', 'Uitgebrande kabel na slecht kabelmanagement') + fig('/img/werk/uitgebrande-stekker.webp', 'Uitgebrande stekker') + '''
    </div>
    <h3 class="gal-kop">Verlichting en lichtmasten</h3>
    <div class="galerij galerij-4">
      ''' + fig('/img/werk/magazijn-verlichting-hoogwerker-1-hd.webp', 'Verlichting vervangen tussen magazijnstellingen met de hoogwerker') + fig('/img/werk/magazijn-verlichting-hoogwerker-2-hd.webp', 'Verlichting vervangen in een magazijn') + fig('/img/werk/straatverlichting-hoogwerker-2-hd.webp', 'Straatverlichting vervangen met de hoogwerker') + fig('/img/werk/lichtmasten-op-vrachtwagen.webp', 'Mobiele lichtmasten verplaatsen en verhuizen') + '''
    </div>
  </div>
</section>
'''

def team_strip(items, cls=''):
    return f'<div class="team-strip {cls}">' + ''.join(
        f'<figure><img src="{src}" alt="{alt}" loading="lazy" width="700" height="520"></figure>' for src, alt in items) + '</div>'

def ph(tekst, cls=''):
    return f'<div class="foto foto-ph {cls}"><span>{tekst}</span></div>'

def foto(src, alt, cls=''):
    return f'<div class="foto {cls}"><img src="{src}" alt="{alt}" loading="lazy" width="460" height="520"></div>'

pages = {}

# ---------------------------------------------------------------- GEDEELDE BLOKKEN
DIENSTEN = [
  # slug, naam (kort, voor tegels), h1, label
  ('verhuizingen', 'Verhuizingen &amp; interne logistiek', 'Verhuizingen en interne logistiek', 'Facilityproject'),
  ('kabelmanagement', 'Kabelmanagement &amp; werkplekken', 'Kabelmanagement en werkplekinrichting', 'Facilityproject'),
  ('verlichting', 'Verlichting vervangen &amp; onderhouden', 'Verlichting vervangen en onderhouden', 'Facilityproject'),
]
FAC_TEGELS = [
  ('verhuizingen', '/img/team/verhuiswagen-laadlift.webp', 'Twee eigen verhuiswagens met laadlift.'),
  ('kabelmanagement', '/img/werk/kabelgoot-hd.webp', 'Werkplekken opbouwen, kabels wegwerken, bureaus en stoelen beheren.'),
  ('verlichting', '/img/werk/magazijn-verlichting-hoogwerker-2-hd.webp', 'Van kantoor tot magazijn en straat, met de hoogwerker.'),
]

EXTRA = [
  ('fietsenbeheer', 'Fietsenbeheer &amp; -onderhoud', 'Fietsenbeheer en -onderhoud', 'Extra dienst'),
  ('opslag', 'Opslag &amp; voorraadbeheer', 'Opslag en voorraadbeheer', 'Extra dienst'),
]
EXTRA_TEGELS = [
  ('fietsenbeheer', '/img/team/fietsen-aanhanger.webp', 'Met een echte fietsenmaker in dienst.'),
  ('opslag', '/img/team/opslag-rekken.webp', '300 palletplaatsen en een digitale inventaris.'),
]

def extra_html():
    return '<ul class="takken takken-2">' + ''.join(
        f'<li><a href="/{sl}/"><div class="tegel"><img src="{src}" alt="" loading="lazy" width="440" height="550"></div><h3>{nm}</h3><p>{tx}</p></a></li>'
        for (sl, src, tx), (_, nm, _, _) in zip(EXTRA_TEGELS, EXTRA)) + '</ul>'

def takken_html():
    return '<ul class="takken takken-3">' + ''.join(
        f'<li><a href="/{sl}/"><div class="tegel"><img src="{src}" alt="" loading="lazy" width="440" height="550"></div><h3>{nm}</h3><p>{tx}</p></a></li>'
        for (sl, src, tx), (_, nm, _, _) in zip(FAC_TEGELS, DIENSTEN)) + '</ul>'

def pijlers_html():
    return '''<div class="pijlers">
      <a class="pijler" href="/servicetechniekers/">
        <img src="/img/werk/werkstation-kabelmanagement-1-hd.webp" alt="" loading="lazy" width="440" height="591">
        <div class="in"><p class="label">Pijler 1</p><h3>Servicetechniekers</h3><p>Elektriciens en mechaniciens die wij voor langere tijd uitlenen aan je bedrijf, voor lange projecten.</p><span class="meer">Meer over servicetechniekers</span></div>
      </a>
      <a class="pijler" href="/facilityprojecten/">
        <img src="/img/werk/kabelgoot-hd.webp" alt="" loading="lazy" width="441" height="585">
        <div class="in"><p class="label">Pijler 2</p><h3>Facilityprojecten</h3><p>Verhuizingen en logistiek, kabelmanagement en werkplekken, verlichting. Enkel voor langere of grotere opdrachten.</p><span class="meer">Meer over facilityprojecten</span></div>
      </a>
    </div>'''

NIKE_NOOT = 'Dat is een vaste, langdurige samenwerking en geen dienst die we overal aanbieden. Het is wel de ervaring en de werkwijze waarop onze servicetechniekers en facilityprojecten steunen.'

FAQ_FAC = [
  ('Doen jullie ook kleine klussen?', 'Nee. Wij gaan enkel voor langere of grotere projecten. Voor een kleine of eenmalige klus zijn we niet de juiste partner.'),
  ('Hoe verloopt een project?', 'Onze servicecoördinator bekijkt met je wat er moet gebeuren en wanneer we kunnen starten. Een vast team en een ervaren teamlead plannen en voeren het project uit en volgen het op tot het 100% is afgewerkt.'),
  ('Kunnen jullie meerdere takken combineren?', 'Ja. Verhuizingen, werkplekken en verlichting combineren we in één project, met één team en één aanspreekpunt.'),
  ('Werken jullie ook voor andere klanten dan Nike?', 'Ja, voor bedrijven in Limburg en de Kempen. Bij Nike zijn we al bijna dertig jaar elke dag aanwezig met een volledig team. Die vaste samenwerking bieden we niet als losse dienst aan, maar de ervaring nemen we mee naar elk project.'),
  ('Doen jullie ook fietsenbeheer of opslag?', 'Ja, als extra dienst. Met een echte fietsenmaker in dienst en ongeveer 300 palletplaatsen. Lees meer op de pagina\'s Fietsenbeheer en Opslag.'),
]
FAQ_DIENSTEN = [
  ('Wat is het verschil tussen servicetechniekers en facilityprojecten?', 'Bij servicetechniekers lenen we elektriciens en mechaniciens uit aan je bedrijf, voor lange projecten. Bij facilityprojecten voeren wij zelf een project uit, zoals een verhuizing, het inrichten van werkplekken of het vervangen van verlichting, met ons eigen team.'),
  ('Werken jullie ook voor korte of kleine opdrachten?', 'Nee. Wij gaan enkel voor langdurige projecten. Bij servicetechniekers zoeken we eerst een langlopend project en werven we daarvoor het personeel aan. Facilityprojecten doen we enkel voor langere of grotere opdrachten.'),
  ('In welke regio werken jullie?', 'Vanuit Meerhout tot bij onze klanten in heel Limburg en de Kempen.'),
  ('Bieden jullie nog andere diensten aan?', 'Ja, twee extra diensten: fietsenbeheer, met een echte fietsenmaker in dienst, en opslag en voorraadbeheer, met ongeveer 300 palletplaatsen.'),
  ('Zijn jullie op zoek naar personeel?', 'Ja, steeds. Omdat we onze techniekers aanwerven voor langdurige projecten, zoeken we voortdurend nieuwe collega\'s. Bekijk de pagina Vacatures op onze website.'),
  ('Hoe snel krijg ik antwoord?', 'Contacteer onze servicecoördinator. Wij zorgen voor een reactie binnen 24 uur.'),
]

TEAM_HOME = [('/img/team/team-lunch.webp', 'Het team van Geert Vos samen aan tafel'),
  ('/img/team/team-gang.webp', 'Collega\'s van Geert Vos onderweg naar een opdracht'),
  ('/img/team/team-kerst.webp', 'Collega\'s van Geert Vos bij een evenement')]

# ---------------------------------------------------------------- HOME
pages['index'] = dict(
  title='Servicetechniekers en facilityprojecten | BV Geert Vos, Meerhout',
  desc='Al 30 jaar service en techniek waarop je kunt rekenen. Elektriciens en mechaniciens (servicetechniekers) en facilityprojecten voor langdurige samenwerkingen in Limburg en de Kempen.',
  extra='''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness","name":"BV Geert Vos","url":"https://geertvos.be/","logo":"https://geertvos.be/img/logo.svg","vatID":"BE0862515981",
"address":{"@type":"PostalAddress","streetAddress":"Bevrijdingslaan 256","postalCode":"2450","addressLocality":"Meerhout","addressRegion":"Antwerpen","addressCountry":"BE"},"foundingDate":"1996",
"areaServed":{"@type":"Place","name":"Limburg en de Kempen, België"},"email":"lorenzo.sterckx@electro-geertvos.be","contactPoint":[{"@type":"ContactPoint","telephone":"+32495460646","contactType":"servicetechniekers","areaServed":"BE","availableLanguage":"nl"},{"@type":"ContactPoint","telephone":"+32477416045","contactType":"projecten","areaServed":"BE","availableLanguage":"nl"}],"image":"https://geertvos.be/img/og-team.jpg",
"knowsAbout":["servicetechniekers","elektriciens","mechaniciens","facilityprojecten","interne verhuizingen","kabelmanagement","werkplekinrichting","verlichting"]}
</script>''',
  body=f'''
<main id="inhoud">
<section class="hero" aria-label="Intro">
  <div class="hero-licht"></div>
  <div class="wrap">
    <div class="hero-tekst">
      <p class="label label-licht">Service en techniek, Meerhout</p>
      <h1>Al 30 jaar service en techniek waarop je kunt rekenen.</h1>
      <p class="lead">Elektriciens en mechaniciens voor langdurige technische ondersteuning, facility en projecten. Vanuit Meerhout tot bij onze klanten in heel Limburg en de Kempen. Wij gaan enkel voor langdurige projecten.</p>
      <div class="hero-cta">
        <a class="btn btn-geel" href="/contact/">Contact</a>
        <a class="btn btn-licht" href="/diensten/">Onze diensten</a>
        <a class="btn btn-licht" href="/vacatures/">Vacatures</a>
      </div>
      <div class="hero-feit">
        <div><strong>30 jaar</strong>elke dag aanwezig bij Nike</div>
        <div><strong>2 pijlers</strong>servicetechniekers en facilityprojecten</div>
        <div><strong>Limburg &amp; de Kempen</strong>vanuit Meerhout</div>
      </div>
    </div>
    <div class="lamp" aria-hidden="true">
      <div class="gloed"></div>
      BULBSVG
    </div>
  </div>
  <div class="stroom hero-stroom"></div>
</section>

<section id="diensten">
  <div class="wrap">
    <div class="sec-kop">
      <p class="label">Onze twee pijlers</p>
      <h2>Servicetechniekers en facilityprojecten.</h2>
      <p class="lead">Twee diensten, allebei voor de lange termijn. Wij gaan enkel voor langdurige projecten: daar bouwen we ons team en onze planning rond, en daar zijn we sterk in.</p>
    </div>
    {pijlers_html()}
    <p style="margin-top:28px">Daarnaast bieden we twee extra diensten aan: <a href="/fietsenbeheer/">fietsenbeheer</a> en <a href="/opslag/">opslag en voorraadbeheer</a>.</p>
  </div>
</section>

<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop">
      <p class="label">Facilityprojecten</p>
      <h2>Drie takken, voor langere of grotere projecten.</h2>
      <p class="lead">Verhuizingen en logistiek, kabelmanagement en werkplekken, verlichting. Bijna dertig jaar ervaring, nu ook voor je bedrijf, maar enkel voor langere of grotere opdrachten.</p>
    </div>
    {takken_html()}
  </div>
</section>

<section>
  <div class="wrap twee">
    <div>
      <p class="label">Ons verhaal</p>
      <h2>Begonnen met een deurklink.</h2>
      <p class="lead" style="margin-top:16px">In 1996 herstelde Geert Vos als contractor een deur en een deurklink bij Nike. Vandaag zijn we daar nog altijd elke dag, met een volledig team.</p>
      <p style="margin-top:16px">{NIKE_NOOT}</p>
      <p style="margin-top:16px"><a class="btn btn-lijn" href="/ons-verhaal/">Lees ons verhaal</a> <a class="btn btn-lijn" href="/vacatures/" style="margin-left:8px">Vacatures</a></p>
      <div class="feiten">
        <div><strong>1996</strong>gestart bij Nike</div>
        <div><strong>2024</strong>servicetechniekers bij andere bedrijven</div>
        <div><strong>±11</strong>collega's dagelijks bij Nike</div>
      </div>
    </div>
    <ol class="tijd">
      <li><time>1996</time><p>Geert Vos start als contractor bij Nike. De eerste opdracht: een deur en een deurklink herstellen.</p></li>
      <li><time>De jaren erna</time><p>Lampen vervangen, meetings klaarzetten met tafels, stoelen, beamers en geluid. Het takenpakket en het team groeien mee.</p></li>
      <li><time>Vandaag</time><p>Elektrische bureaus, meubilair, interne verhuizingen en events. De beamers zijn grote mobiele schermen geworden.</p></li>
      <li><time>2024</time><p>Elektriciens en mechaniciens worden ook bij andere klanten ingezet, voor langdurige projecten. Zo groeit BV Geert Vos verder, naast de werking bij Nike.</p></li>
    </ol>
  </div>
</section>

<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop">
      <p class="label">Zo werken wij</p>
      <h2>Een hecht en bereikbaar team.</h2>
      <p class="lead">Dat is de sleutel van BV Geert Vos. Ook voor onze klanten: de verantwoordelijkheid leggen we hoog bij onszelf, en we zijn er wanneer je ons nodig hebt.</p>
    </div>
    {team_strip(TEAM_HOME)}
    <div class="waarden">
      <div><h3>Hecht en bereikbaar</h3><p>Een jong, hecht team met ervaren teamleads. Je weet bij wie je terecht kunt, en je krijgt binnen 24 uur een reactie.</p></div>
      <div><h3>Verantwoordelijkheid bij ons</h3><p>Onze techniekers werken zelfstandig, met de nodige certificaten, materialen en uitrusting. Wij volgen elke opdracht op tot ze 100% is afgewerkt en de werkplek proper is.</p></div>
      <div><h3>Enkel voor de lange termijn</h3><p>Wij gaan enkel voor langdurige projecten. Daar bouwen we samen met je aan, vaak voor vele jaren.</p></div>
    </div>
  </div>
</section>
</main>
''' + CTA)

# ---------------------------------------------------------------- SERVICETECHNIEKERS (pijler 1)
FAQ_SERVICE = [
  ('Wat zijn servicetechniekers?', 'Elektriciens en mechaniciens van BV Geert Vos die we voor langere tijd uitlenen aan een bedrijf, voor lange projecten. Ze werken zelfstandig op je locatie.'),
  ('Kunnen jullie ook een technieker voor één klus sturen?', 'Nee. Wij gaan enkel voor langdurige projecten. We zoeken eerst een langlopend project en werven daarvoor het personeel aan. Voor korte of eenmalige klussen zijn we niet de juiste partner.'),
  ('Wie zorgt voor certificaten, materiaal en uitrusting?', 'Wij. Onze techniekers komen met de nodige certificaten, materialen en uitrusting om hun opdracht zelfstandig en professioneel uit te voeren.'),
  ('In welke regio werken jullie?', 'Vanuit Meerhout tot bij onze klanten in heel Limburg en de Kempen.'),
  ('Wie volgt de techniekers op?', 'Ervaren teamleads van BV Geert Vos. Wij nemen de verantwoordelijkheid voor onze mensen en zijn bereikbaar als er iets is.'),
  ('Zijn jullie op zoek naar personeel?', 'Ja, steeds. Omdat we onze techniekers aanwerven voor langdurige projecten, zoeken we voortdurend nieuwe collega\'s. Bekijk de pagina Vacatures op onze website.'),
]
pages['servicetechniekers'] = dict(
  extra=schema('servicetechniekers', 'Servicetechniekers', ('Servicetechniekers', 'Elektriciens en mechaniciens die voor lange projecten aan bedrijven worden uitgeleend, met certificaten, materiaal en uitrusting.'), FAQ_SERVICE),
  title='Servicetechniekers: elektriciens en mechaniciens | BV Geert Vos',
  desc='Servicetechniekers voor lange projecten: elektriciens en mechaniciens die zelfstandig bij je bedrijf werken in Limburg en de Kempen. Met certificaten, materiaal en uitrusting.',
  body=kop('Pijler 1', 'Servicetechniekers', 'Elektriciens en mechaniciens die wij voor langere tijd uitlenen aan je bedrijf, voor lange projecten. Zelfstandig, met certificaten, materiaal en uitrusting.', 'Servicetechniekers') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee">
    <div>
      <h2>Techniekers die bij je project blijven.</h2>
      <p class="lead" style="margin-top:16px">Onder servicetechniekers verstaan we dat wij servicetechniekers uitlenen aan bedrijven, voor lange projecten. Zowel elektrisch als mechanisch.</p>
      <p style="margin-top:16px">Het is niet zo dat iedereen voor elke klus bij ons terecht kan. Wij gaan op zoek naar langdurige projecten en werven daarvoor zelf het personeel aan. Een korte of eenmalige klus doen we niet, een langlopend project bouwen we graag met je mee.</p>
      <p>Naar personeel zijn we dan ook steeds op zoek. Ben je zelf technieker? Bekijk onze <a href="/vacatures/">vacatures</a>.</p>
    </div>
    {foto('/img/werk/werkstation-kabelmanagement-2-hd.webp', 'Kabelmanagement aan een werkstation door Geert Vos')}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Twee vakgebieden</p><h2>Elektrisch en mechanisch.</h2></div>
    <div class="inzet">
      <div><h3>Elektriciens</h3><p>Verlichting, werkplekken en kabelmanagement, onderhoud en storingen. Zelfstandig en met de nodige certificaten.</p><p style="margin-top:16px"><a class="btn btn-lijn" href="/elektriciens/">Meer over onze elektriciens</a></p></div>
      <div><h3>Mechaniciens</h3><p>Mechanisch onderhoud, montage en herstellingen, 100% afgewerkt. Met eigen gereedschap en uitrusting.</p><p style="margin-top:16px"><a class="btn btn-lijn" href="/mechaniciens/">Meer over onze mechaniciens</a></p></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap twee">
    {foto('/img/werk/lichtmast-heftruck-hd.webp', 'Lichtmast verplaatsen met de heftruck', 'foto-hoog')}
    <div>
      <p class="label">Wat je mag verwachten</p>
      <h2>Zelfstandig, met opvolging.</h2>
      <ul class="punten">
        <li>Enkel voor langdurige projecten, bij dezelfde klant</li>
        <li>De nodige certificaten, materialen en uitrusting</li>
        <li>Zelfstandig werken, met opvolging door een ervaren teamlead</li>
        <li>Een hecht, bereikbaar team dat de verantwoordelijkheid neemt</li>
        <li>Een werkplek die proper en ordelijk achterblijft</li>
      </ul>
    </div>
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Werk in beeld</p><h2>Onze techniekers aan het werk.</h2></div>
    <div class="galerij galerij-4">
      {fig('/img/werk/straatverlichting-hoogwerker-4-hd.webp', 'Technieker aan het werk in de hoogwerker')}{fig('/img/werk/straatverlichting-hoogwerker-5-hd.webp', 'Verlichting vervangen met de hoogwerker')}{fig('/img/werk/magazijn-verlichting-hoogwerker-1-hd.webp', 'Verlichting vervangen tussen magazijnstellingen')}{fig('/img/werk/kabelgoot-hd.webp', 'Kabelmanagement in een magazijn')}
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Zo gaat het</p><h2>In drie stappen aan de slag.</h2></div>
    <ol class="stappen">
      <li><h3>Je contacteert onze servicecoördinator</h3><p>Die bekijkt met je welk profiel je nodig hebt, voor welk project, hoelang en waar. Je krijgt binnen 24 uur een reactie.</p></li>
      <li><h3>Wij zetten de juiste technieker in</h3><p>Met de nodige certificaten, materialen en uitrusting om zelfstandig te starten.</p></li>
      <li><h3>Onze teamleads volgen op</h3><p>Zodat de opdracht correct wordt uitgevoerd en 100% wordt afgewerkt.</p></li>
    </ol>
  </div>
</section>
''' + faq_blok(FAQ_SERVICE) + '</main>\n' + CTA)

# ---------------------------------------------------------------- ELEKTRICIENS / MECHANICIENS
def techniek_pagina(naam, enk, title, desc, lead, intro, werk, punten, faq, fotosrc, foto1, foto2, extra=''):
    f1 = foto(fotosrc, foto1) if fotosrc else ph(foto1)
    return dict(title=title, desc=desc, extra=extra, body=kop('Servicetechniekers', naam + ' voor langdurige projecten', lead, '<a href="/servicetechniekers/">Servicetechniekers</a> / ' + naam) + f'''
<main id="inhoud">
<section>
  <div class="wrap twee">
    <div>
      <h2>{intro[0]}</h2>
      <p class="lead" style="margin-top:16px">{intro[1]}</p>
      <p style="margin-top:16px">{intro[2]}</p>
      <p>{intro[3]}</p>
    </div>
    {f1}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Wat onze {naam.lower()} doen</p><h2>{werk[0]}</h2><p class="lead">{werk[1]}</p></div>
    <div class="waarden">{''.join(f'<div><h3>{k}</h3><p>{t}</p></div>' for k, t in werk[2])}</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Samenwerken</p><h2>Enkel voor langdurige projecten.</h2></div>
    <div class="inzet">
      <div><h3>Langdurig op je locatie</h3><p>Een {enk} die gedurende een langere periode bij dezelfde klant werkt, kent de site, de mensen en de installaties. Dat merk je in het werk: minder uitleg, minder fouten, meer gedaan.</p></div>
      <div><h3>Eerst het project, dan de mensen</h3><p>Wij gaan op zoek naar langdurige projecten en werven daarvoor zelf het personeel aan. Een korte of eenmalige klus doen we niet. Voor een langlopend project bouwen we graag met je mee.</p></div>
    </div>
  </div>
</section>
{WERK_ELEK if enk == 'elektricien' else ''}
<section class="sec-paper">
  <div class="wrap twee">
    {foto(*foto2.split('|'), 'foto-hoog') if '|' in foto2 else ph(foto2, 'foto-hoog')}
    <div>
      <p class="label">Wat je mag verwachten</p>
      <h2>Zelfstandig, met opvolging.</h2>
      <ul class="punten">{''.join(f'<li>{p}</li>' for p in punten)}</ul>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Zo gaat het</p><h2>In drie stappen aan de slag.</h2></div>
    <ol class="stappen">
      <li><h3>Je contacteert onze servicecoördinator</h3><p>Die bekijkt met je welk profiel je nodig hebt, voor hoelang en waar. Je krijgt binnen 24 uur een reactie.</p></li>
      <li><h3>Wij zetten de juiste {enk} in</h3><p>Met de nodige certificaten, materialen en uitrusting om zelfstandig te starten.</p></li>
      <li><h3>Onze teamleads volgen op</h3><p>Zodat de opdracht correct wordt uitgevoerd en 100% wordt afgewerkt.</p></li>
    </ol>
  </div>
</section>
''' + faq_blok(faq) + '</main>\n' + CTA)

FAQ_ELEK = [
  ('Werken jullie ook voor kortere opdrachten?', 'Nee. Wij gaan enkel voor langdurige projecten, waarbij een elektricien voor langere tijd bij dezelfde klant werkt. We zoeken eerst een langlopend project en werven daarvoor het personeel aan.'),
  ('Wie zorgt voor certificaten, materiaal en uitrusting?', 'Wij. Onze elektriciens komen met de nodige certificaten, materialen en uitrusting om hun opdracht zelfstandig en professioneel uit te voeren.'),
  ('In welke regio werken jullie?', 'Vanuit Meerhout tot bij onze klanten in heel Limburg en de Kempen. Contacteer onze servicecoördinator om te bekijken of je site binnen ons bereik ligt.'),
  ('Wie volgt de opdracht op?', 'Ervaren teamleads van BV Geert Vos. Wij nemen de verantwoordelijkheid voor onze mensen en zorgen dat de opdracht correct wordt opgevolgd en pas wordt afgesloten als ze 100% is afgewerkt.'),
  ('Zoeken jullie ook naar "elektrieker" of "elektrotechnieker"?', 'Zelfde vak, andere naam. Of je nu een elektrieker, elektrotechnieker of industrieel elektricien zoekt: contacteer onze servicecoördinator en beschrijf het werk, dan zoeken we het juiste profiel.'),
  ('Kan ik bij jullie als elektricien werken?', 'Ja, we zijn steeds op zoek naar nieuwe collega\'s voor langdurige projecten. Bekijk de pagina Vacatures op onze website.'),
]
FAQ_MECH = [
  ('Wat is het verschil met een onderhoudstechnieker?', 'Weinig. Onze mechaniciens doen mechanisch onderhoud, montage en herstellingen; velen noemen dat een onderhoudstechnieker of mecanicien. Beschrijf het werk, wij matchen het profiel.'),
  ('Kan een mechanicien langere tijd bij ons werken?', 'Dat is precies waar we ons op richten: een technieker die gedurende een langere periode bij dezelfde klant werkt en je installaties leert kennen. Voor korte of eenmalige klussen zijn we niet de juiste partner.'),
  ('Brengen jullie eigen gereedschap mee?', 'Ja. Onze mechaniciens beschikken over de nodige certificaten, materialen en uitrusting om zelfstandig te werken.'),
  ('Hoe zorgen jullie voor kwaliteit?', 'Orde, stiptheid en kwaliteit zijn onze belangrijkste waarden. Ervaren teamleads volgen elke opdracht op, wij nemen de verantwoordelijkheid voor onze mensen, en we laten de werkplek proper en ordelijk achter.'),
  ('Hoe start ik?', 'Contacteer onze servicecoördinator. Die bekijkt met je welk profiel je nodig hebt, voor hoelang en waar, en wanneer we kunnen starten. Je krijgt binnen 24 uur een reactie.'),
  ('Kan ik bij jullie als mechanicien werken?', 'Ja, we zijn steeds op zoek naar nieuwe collega\'s voor langdurige projecten. Bekijk de pagina Vacatures op onze website.'),
]

pages['elektriciens'] = techniek_pagina('Elektriciens', 'elektricien',
  extra=schema('elektriciens', 'Elektriciens', ('Elektriciens', 'Elektriciens die voor langere periodes bij je bedrijf werken, met certificaten, materiaal en uitrusting.'), FAQ_ELEK),
  title='Elektricien inhuren voor langdurige projecten | BV Geert Vos',
  desc='Ervaren elektriciens voor langdurige projecten bij je bedrijf in Limburg en de Kempen. Met certificaten, materiaal en uitrusting. Contacteer onze servicecoördinator.',
  lead='Ervaren elektriciens die wij voor langere periodes bij je bedrijf inzetten, voor lange projecten. Vanuit Meerhout, in heel Limburg en de Kempen.',
  intro=('Een elektricien die je site kent.', 'Bij onze technische dienstverlening stellen we elektriciens tewerk op de locatie van onze klanten. Ze werken er zelfstandig, met de certificaten, het materiaal en de uitrusting die hun opdracht vraagt.',
         'Elektrisch werk zit al sinds 1996 in ons DNA: het begon bij Nike met lampen vervangen en groeide uit tot het dagelijks beheer van verlichting, kabelmanagement en elektrische bureaus op een volledige site. Sinds 2024 zetten we die ervaring ook in bij andere bedrijven.',
         'Of je nu zoekt naar een elektricien, een elektrieker of een elektrotechnieker: je krijgt iemand die niet na een paar weken weer weg is, en die je niet elke keer opnieuw hoeft uit te leggen hoe je gebouw in elkaar zit.'),
  werk=('Elektrisch werk op je site, dag na dag.', 'Wat een elektricien van Geert Vos bij je doet, hangt af van je site. Dit is het soort werk dat we al jaren dagelijks uitvoeren.', [
        ('Verlichting', 'Lampen en armaturen vervangen, verlichting onderhouden en aanpassen in kantoren, gangen en werkruimtes.'),
        ('Werkplekken en kabelmanagement', 'Werkplekken aansluiten, elektrische bureaus beheren, kabels netjes en veilig wegwerken.'),
        ('Onderhoud en storingen', 'Kleine herstellingen en onderhoud aan elektrische installaties, zodat alles blijft werken.'),
        ('Lichtmasten en straatverlichting', 'Mobiele lichtmasten verplaatsen en verhuizen, straatverlichting vervangen met de hoogwerker.')]),
  punten=['De nodige certificaten voor het werk dat je vraagt', 'Eigen materiaal en uitrusting, klaar om te starten', 'Zelfstandig werken, met opvolging door een ervaren teamlead', 'Een werkplek die proper en ordelijk achterblijft', 'Vriendelijk, flexibel en met een positieve ingesteldheid'],
  faq=FAQ_ELEK,
  fotosrc='/img/werk/werkstation-kabelmanagement-2-hd.webp', foto1='Kabelmanagement aan een werkstation door Geert Vos', foto2='/img/werk/straatverlichting-hoogwerker-1-hd.webp|Straatverlichting vervangen met de hoogwerker')

pages['mechaniciens'] = techniek_pagina('Mechaniciens', 'mechanicien',
  extra=schema('mechaniciens', 'Mechaniciens', ('Mechaniciens', 'Mechaniciens en onderhoudstechniekers die voor langere periodes bij je bedrijf werken, met certificaten, materiaal en uitrusting.'), FAQ_MECH),
  title='Mechanicien inhuren voor langdurige projecten | BV Geert Vos',
  desc='Mechaniciens en onderhoudstechniekers voor langdurige projecten bij je bedrijf in Limburg en de Kempen. Zelfstandig, eigen materiaal. Contacteer onze servicecoördinator.',
  lead='Mechaniciens die wij voor langere periodes bij je bedrijf inzetten, voor lange projecten. Vanuit Meerhout, in heel Limburg en de Kempen.',
  intro=('Mechanisch werk dat 100% wordt afgewerkt.', 'Onze mechaniciens werken op de locatie van onze klanten, zelfstandig en met de certificaten, het materiaal en de uitrusting die de opdracht vraagt.',
         'Mechanisch onderhoud doen we al bijna dertig jaar, elke dag: bureaustoelen en elektrische bureaus herstellen, meubilair in breakrooms en restaurants onderhouden, fietsen nakijken met een eigen fietsenmaker, verhuiswagens met laadlift inzetten. Handen die gewend zijn om dingen weer in orde te maken.',
         'Noem het een mechanicien, mecanicien of onderhoudstechnieker: je krijgt iemand die je installaties leert kennen en die pas klaar is als het werk écht af is, met een propere werkplek achteraf.'),
  werk=('Onderhouden, monteren, herstellen.', 'Wat een mechanicien van Geert Vos bij je doet, hangt af van je site. Dit is het soort werk dat we al jaren dagelijks uitvoeren.', [
        ('Mechanisch onderhoud', 'Periodiek onderhoud en kleine herstellingen aan installaties en uitrusting, voor ze een probleem worden.'),
        ('Montage en demontage', 'Meubilair, werkplekken en opstellingen opbouwen, verplaatsen en afbreken. Twee eigen verhuiswagens met laadlift.'),
        ('Storingen', 'Als iets vastloopt: kijken, herstellen, en zorgen dat het niet terugkomt.'),
        ('Fietsen en materieel', 'Beheer en onderhoud van een fietsenvloot door een echte fietsenmaker; beheer van magazijn en voorraad.')]),
  punten=['De nodige certificaten voor het werk dat je vraagt', 'Eigen gereedschap en uitrusting, klaar om te starten', 'Zelfstandig werken, met opvolging door een ervaren teamlead', 'Een werkplek die proper en ordelijk achterblijft', 'Vriendelijk, flexibel en met een positieve ingesteldheid'],
  faq=FAQ_MECH,
  fotosrc='/img/werk/lichtmast-heftruck-hd.webp', foto1='Lichtmast verplaatsen met de heftruck', foto2='/img/team/team-keuken-2.webp|Collega\'s monteren keukenkasten met een ladder')


def dienst_pagina(slug, naam, h1, label, title, desc, lead, intro, werk, punten, faq, fotosrc, alt, foto2, galerij='', extra=False):
    andere = ''.join(f'<li><a href="/{sl}/">{nm}</a></li>' for sl, nm, _, _ in DIENSTEN + EXTRA if sl != slug)
    hub = f'<a href="/diensten/">Diensten</a> / {h1}' if extra else f'<a href="/facilityprojecten/">Facilityprojecten</a> / {h1}'
    stap_h2, stap_lead, stap_1 = (('Van vraag tot afgewerkte opdracht.', 'Een vast aanspreekpunt en een reactie binnen 24 uur.', 'Aanvraag komt binnen') if extra
                                  else ('Van vraag tot afgewerkt project.', 'Wij gaan enkel voor langere of grotere opdrachten.', 'Project komt binnen'))
    return dict(title=title, desc=desc,
      extra=schema(slug, h1, (h1, desc), faq),
      body=kop(label, h1, lead, hub) + f'''
<main id="inhoud">
<section>
  <div class="wrap twee">
    <div>
      <h2>{intro[0]}</h2>
      <p class="lead" style="margin-top:16px">{intro[1]}</p>
      <p style="margin-top:16px">{intro[2]}</p>
      <p>{intro[3]}</p>
    </div>
    {foto(fotosrc, alt) if fotosrc else ph(alt)}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Wat we doen</p><h2>{werk[0]}</h2><p class="lead">{werk[1]}</p></div>
    <div class="waarden">{''.join(f'<div><h3>{k}</h3><p>{t}</p></div>' for k, t in werk[2])}</div>
  </div>
</section>
{galerij}
<section{'' if galerij else ' class="sec-paper"'}>
  <div class="wrap twee">
    {foto(*foto2.split('|'), 'foto-hoog') if '|' in foto2 else ph(foto2, 'foto-hoog')}
    <div>
      <p class="label">Wat je mag verwachten</p>
      <h2>Geregeld, en proper achtergelaten.</h2>
      <ul class="punten">{''.join(f'<li>{p}</li>' for p in punten)}</ul>
    </div>
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Zo gaat het</p><h2>{stap_h2}</h2><p class="lead">{stap_lead}</p></div>
    <ol class="stappen">
      <li><h3>{stap_1}</h3><p>Je contacteert onze servicecoördinator, die met je bekijkt wat er nodig is en wanneer we kunnen starten. Je krijgt binnen 24 uur een reactie.</p></li>
      <li><h3>Team en materiaal ingepland</h3><p>Onze teamleads plannen de juiste mensen in, met het materiaal, de wagens en de uitrusting die de klus vraagt.</p></li>
      <li><h3>Uitgevoerd en afgewerkt</h3><p>Pas klaar als het 100% af is en de werkplek proper en ordelijk is. De teamlead volgt het op.</p></li>
    </ol>
  </div>
</section>
''' + faq_blok(faq) + f'''
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Ook van ons</p><h2>Onze andere diensten.</h2></div>
    <ul class="andere">{andere}<li><a href="/servicetechniekers/">Servicetechniekers</a></li></ul>
  </div>
</section>
</main>
''' + CTA)

GAL_VERHUIS = '''<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Werk in beeld</p><h2>Zo ziet een project eruit.</h2></div>
    <div class="galerij galerij-4">
      ''' + fig('/img/team/team-keuken-1.webp', 'Collega\'s bouwen een keuken op in een kantoorruimte') + fig('/img/team/team-keuken-2.webp', 'Kasten monteren met de ladder') + fig('/img/team/luidspreker-meeting.webp', 'Een mobiele geluidsinstallatie klaarzetten voor een meeting') + fig('/img/team/team-gang.webp', 'Ons team onderweg naar een opdracht') + '''
    </div>
  </div>
</section>
'''
# --- 1 Verhuizingen
pages['verhuizingen'] = dienst_pagina('verhuizingen', DIENSTEN[0][1], DIENSTEN[0][2], DIENSTEN[0][3],
  title='Interne verhuizingen en logistiek | BV Geert Vos, Meerhout',
  desc='Interne verhuizingen en logistiek als project voor bedrijven in Limburg en de Kempen, voor langere of grotere opdrachten. Twee eigen verhuiswagens met laadlift.',
  lead='Afdelingen verhuizen, werkplekken verplaatsen, meetings en events opbouwen: interne verhuizingen en logistiek als project, voor langere of grotere opdrachten.',
  intro=('Verhuizen zonder dat de rest stilvalt.', 'Een interne verhuizing lijkt klein tot je ze moet organiseren: bureaus, stoelen, kasten, schermen, dozen, en iedereen die de volgende ochtend gewoon wil kunnen werken. Wij doen dit al bijna dertig jaar, elke dag.',
         'Daarvoor beschikken we over twee eigen verhuiswagens met laadlift, zodat materiaal veilig en ergonomisch geladen en gelost wordt. Geen getil over drempels, geen beschadigde kasten, geen rugklachten.',
         'Ook meetings en evenementen zetten we klaar: tafels, stoelen, geluid en de grote mobiele schermen die de beamers van vroeger hebben vervangen. En na afloop ruimen we alles weer op.'),
  werk=('Van dozen tot complete afdelingen.', 'Wat we bij Nike al bijna dertig jaar dagelijks uitvoeren, zetten we in voor je project.', [
        ('Interne verhuizingen', 'Werkplekken, afdelingen en meubilair verplaatsen binnen het gebouw of tussen gebouwen. Gepland rond je werking, zodat niemand stilvalt.'),
        ('Twee verhuiswagens met laadlift', 'Eigen wagens, dus geen wachten op een externe transporteur. Veilig en ergonomisch laden en lossen.'),
        ('Meetings en evenementen', 'Opstellingen klaarzetten met tafels, stoelen, geluidsinstallatie en grote mobiele schermen. Na afloop weer afgebroken en opgeruimd.'),
        ('Logistieke ondersteuning', 'Materiaal ophalen, leveren, verdelen en terugbrengen. Ook lichtmasten en ander zwaar materieel verplaatsen we, met heftruck als het moet.')]),
  punten=['Enkel voor langere of grotere projecten, met een vast team', 'Twee eigen verhuiswagens met laadlift', 'Ervaren ploeg die dagelijks verhuist', 'Gepland rond je werking, ook buiten de kantooruren als dat nodig is', 'Meubilair en materiaal veilig en zonder schade verplaatst', 'Alles weer proper en ordelijk achtergelaten'],
  faq=[
    ('Verhuizen jullie ook tussen twee gebouwen?', 'Ja. Met onze eigen verhuiswagens met laadlift verplaatsen we materiaal veilig tussen locaties, niet alleen binnen één gebouw.'),
    ('Kunnen jullie een meeting of event opbouwen?', 'Ja. Meetings en evenementen klaarzetten met tafels, stoelen, geluid en grote mobiele schermen doen we al sinds 1996, en na afloop ruimen we alles weer op.'),
    ('Doen jullie ook één kleine verhuizing?', 'Nee. Wij gaan enkel voor langere of grotere projecten. Voor een kleine of eenmalige verhuizing zijn we niet de juiste partner.'),
    ('Hoe snel kunnen jullie een verhuisproject inplannen?', 'Dat hangt af van de omvang. Contacteer onze servicecoördinator: die bekijkt met je wat er moet gebeuren en wanneer we de ploeg en de wagens kunnen inzetten. Je krijgt binnen 24 uur een reactie.'),
    ('Wat als er iets beschadigd raakt?', 'Daarom werken we met laadliften, ervaren mensen en een teamlead die opvolgt. Een opdracht is voor ons pas klaar als ze 100% correct is afgewerkt.'),
  ],
  fotosrc='/img/team/verhuiswagen-laadlift.webp', alt='Verhuiswagen met laadlift van Geert Vos',
  foto2='/img/werk/lichtmast-heftruck-hd.webp|Mobiele lichtmast verplaatsen met de heftruck', galerij=GAL_VERHUIS)

# --- 2 Kabelmanagement
GAL_KABEL = '''<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Voor en na</p><h2>Zo ziet goed kabelmanagement eruit.</h2></div>
    <div class="galerij galerij-2">
      ''' + voor_na(('/img/werk/kabelmanagement-voor.webp', 'losse, hangende kabels'), ('/img/werk/kabelmanagement-na.webp', 'kabels gebundeld en weggewerkt'), 'Werkplekbekabeling opnieuw gelegd en gebundeld.') + voor_na(('/img/werk/werkstation-kabels-voor.webp', 'kabels los onder een werkstation'), ('/img/werk/werkstation-kabels-na.webp', 'werkstation met opgeruimde bekabeling'), 'Werkstation: alle kabels geleid en vastgezet.') + '''
    </div>
    <h3 class="gal-kop">Wat er gebeurt als het niet gebeurt</h3>
    <p style="max-width:62ch;margin-bottom:20px">Kabels die klem zitten, geplet worden of los over de vloer lopen, raken beschadigd. Het eindigt met uitgebrande stekkers en kabels. Dit zijn voorbeelden die we bij klanten aantroffen en herstelden.</p>
    <div class="galerij galerij-3">
      ''' + fig('/img/werk/kabel-geklemd-kast.webp', 'Kabel geklemd achter een metalen kast') + fig('/img/werk/uitgebrande-kabel.webp', 'Uitgebrande kabel na slecht kabelmanagement') + fig('/img/werk/uitgebrande-stekker.webp', 'Uitgebrande stekker') + '''
    </div>
  </div>
</section>
'''
pages['kabelmanagement'] = dienst_pagina('kabelmanagement', DIENSTEN[1][1], DIENSTEN[1][2], DIENSTEN[1][3],
  title='Kabelmanagement en werkplekinrichting | BV Geert Vos, Meerhout',
  desc='Werkplekken opbouwen en aanpassen, kabels netjes en veilig wegwerken, elektrische bureaus en meubilair beheren. Als project voor bedrijven in Limburg en de Kempen.',
  lead='Werkplekken opbouwen, verplaatsen en aanpassen, met kabels die netjes en veilig zijn weggewerkt. Plus het beheer van elektrische bureaus, stoelen en meubilair, voor langere of grotere projecten.',
  intro=('Een werkplek die werkt, en er ook zo uitziet.', 'Werkplekaanpassingen komen bij Nike dagelijks binnen via het ticketsysteem: een nieuwe collega, een team dat verhuist, een bureau dat anders moet staan. Wij bouwen op, sluiten aan en werken de kabels weg.',
         'We beheren en onderhouden er ook de elektrische bureaus, de bureaustoelen en een groot deel van het meubilair in breakrooms en restaurants. Kapot? Wij herstellen het. Versleten? Wij vervangen het.',
         'Kabelmanagement is geen cosmetica. Losse en geplette kabels raken beschadigd en leiden tot uitgebrande stekkers. Netjes weggewerkt is dus ook veilig weggewerkt.'),
  werk=('Van kabelgoot tot bureaustoel.', 'Alles wat een werkplek nodig heeft om te werken, elke dag opnieuw.', [
        ('Werkplekken opbouwen en aanpassen', 'Nieuwe werkplekken opbouwen, bestaande verplaatsen of aanpassen. Bureau, stoel, scherm, stroom en data: klaar om te gebruiken.'),
        ('Kabelmanagement', 'Kabels leiden, bundelen en vastzetten in goten en onder bureaus. Netjes, veilig en makkelijk aan te passen als er iets verandert.'),
        ('Elektrische bureaus en stoelen', 'Beheer, onderhoud en herstelling van elektrische zit-stabureaus en bureaustoelen.'),
        ('Meubilair breakrooms en restaurants', 'Tafels, stoelen en ander meubilair in gemeenschappelijke ruimtes onderhouden, herstellen en vervangen.')]),
  punten=['Enkel voor langere of grotere projecten', 'Werkplek klaar om te gebruiken, inclusief stroom en data', 'Kabels weggewerkt volgens de regels van de kunst', 'Herstelling van elektrische bureaus en stoelen in eigen beheer', 'Een bereikbaar team, met reactie binnen 24 uur', 'Werkplek proper en ordelijk achtergelaten'],
  faq=[
    ('Doen jullie ook kleine aanpassingen, zoals één bureau verplaatsen?', 'Nee. Wij werken in projecten: een reeks werkplekken, een hele afdeling of een gebouw. Voor één los bureau zijn we niet de juiste partner.'),
    ('Herstellen jullie elektrische bureaus?', 'Ja, beheer en onderhoud van elektrische bureaus en bureaustoelen maakt deel uit van onze projecten voor werkplekinrichting.'),
    ('Waarom is kabelmanagement belangrijk?', 'Losse of geplette kabels raken beschadigd en kunnen uitbranden. Netjes weggewerkte kabels zijn veiliger, gaan langer mee en zijn makkelijker aan te passen.'),
    ('Kunnen jullie een hele afdeling inrichten?', 'Ja. Samen met onze verhuisploeg en onze elektriciens richten we complete afdelingen in, van meubilair tot bekabeling.'),
  ],
  fotosrc='/img/werk/kabelgoot-magazijn-hd.webp', alt='Kabelgoten met netjes weggewerkte kabels in een magazijn',
  foto2='/img/werk/werkstation-kabelmanagement-2-hd.webp|Afgewerkt kabelmanagement aan een werkstation', galerij=GAL_KABEL)

# --- 3 Verlichting
GAL_LICHT = '''<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Werk in beeld</p><h2>Van magazijn tot straat.</h2></div>
    <div class="galerij galerij-4">
      ''' + fig('/img/werk/magazijn-verlichting-hoogwerker-1-hd.webp', 'Verlichting vervangen tussen magazijnstellingen met de hoogwerker') + fig('/img/werk/magazijn-verlichting-hoogwerker-2-hd.webp', 'Verlichting vervangen in een magazijn') + fig('/img/werk/straatverlichting-hoogwerker-1-hd.webp', 'Straatverlichting vervangen met de hoogwerker') + fig('/img/werk/straatverlichting-hoogwerker-3-hd.webp', 'Onze bestelwagen en hoogwerker op een parking') + fig('/img/werk/straatverlichting-hoogwerker-4-hd.webp', 'Technieker in de korf van de hoogwerker') + fig('/img/werk/straatverlichting-hoogwerker-5-hd.webp', 'Lamp vervangen op grote hoogte') + fig('/img/werk/straatverlichting-hoogwerker-2-hd.webp', 'Straatlamp vervangen met de hoogwerker') + fig('/img/werk/lichtmast-heftruck-hd.webp', 'Mobiele lichtmast verplaatsen met de heftruck') + '''
    </div>
  </div>
</section>
'''
pages['verlichting'] = dienst_pagina('verlichting', DIENSTEN[2][1], DIENSTEN[2][2], DIENSTEN[2][3],
  title='Verlichting vervangen en onderhouden | BV Geert Vos, Meerhout',
  desc='Lampen en armaturen vervangen in kantoren en magazijnen, straatverlichting met de hoogwerker, lichtmasten verplaatsen. Voor langere projecten bij bedrijven in Limburg en de Kempen.',
  lead='Lampen vervangen was in 1996 een van onze allereerste opdrachten. Vandaag vervangen en onderhouden we verlichting als project, van kantoor tot magazijn en van parking tot straat, voor langere of grotere opdrachten.',
  intro=('Alles blijft branden.', 'Een defecte lamp lijkt een detail, tot het er tien zijn in een magazijngang of op een parking. Wij vervangen en onderhouden verlichting zodat je er niet aan hoeft te denken.',
         'In kantoren, gangen en werkruimtes doen we dat vanop de ladder. In magazijnen met hoge stellingen en buiten aan straatverlichting werken we met de hoogwerker. Mobiele lichtmasten verplaatsen en verhuizen we met de heftruck en onze eigen wagens.',
         'Het werk gebeurt door onze eigen elektriciens, met de certificaten en de uitrusting die erbij horen. Gepland als onderhoud, binnen een langlopend project.'),
  werk=('Binnen, buiten en in de hoogte.', 'Verlichting in al zijn vormen, uitgevoerd door onze eigen elektriciens.', [
        ('Kantoren en werkruimtes', 'Lampen en armaturen vervangen en onderhouden in kantoren, gangen, breakrooms en werkplaatsen.'),
        ('Magazijnen', 'Verlichting vervangen tussen en boven hoge stellingen, met de hoogwerker. Veilig en zonder het magazijn stil te leggen.'),
        ('Straat- en buitenverlichting', 'Straatverlichting en parkingverlichting vervangen met de hoogwerker.'),
        ('Lichtmasten', 'Mobiele lichtmasten verplaatsen, verhuizen en opstellen, met heftruck en eigen wagens.')]),
  punten=['Enkel voor langere of grotere projecten', 'Eigen elektriciens met de nodige certificaten', 'Hoogwerker voor magazijnen en buitenverlichting', 'Geplande onderhoudsrondes binnen een langlopend project', 'Lichtmasten verplaatst met eigen materieel', 'Werkplek proper achtergelaten, oude lampen afgevoerd'],
  faq=[
    ('Vervangen jullie ook verlichting op grote hoogte?', 'Ja. Voor magazijnen met hoge stellingen en voor straatverlichting werken we met de hoogwerker.'),
    ('Komen jullie één lamp vervangen?', 'Nee. Wij gaan enkel voor langere of grotere projecten, zoals het onderhoud van verlichting in een heel gebouw of magazijn.'),
    ('Kunnen jullie een onderhoudsronde inplannen?', 'Ja. Veel klanten laten ons de verlichting periodiek nakijken en vervangen, zodat er minder uitval is tussendoor.'),
    ('Wie voert het werk uit?', 'Onze eigen elektriciens, met de certificaten, het materiaal en de uitrusting die erbij horen.'),
    ('Verplaatsen jullie ook lichtmasten?', 'Ja. Mobiele lichtmasten verplaatsen en verhuizen we met de heftruck en onze eigen wagens.'),
  ],
  fotosrc='/img/werk/magazijn-verlichting-hoogwerker-2-hd.webp', alt='Verlichting vervangen in een magazijn met de hoogwerker',
  foto2='/img/werk/straatverlichting-hoogwerker-2-hd.webp|Straatverlichting vervangen met de hoogwerker', galerij=GAL_LICHT)


# --- 4 Fietsenbeheer
pages['fietsenbeheer'] = dienst_pagina('fietsenbeheer', EXTRA[0][1], EXTRA[0][2], EXTRA[0][3],
  title='Fietsenbeheer en fietsonderhoud voor bedrijven | BV Geert Vos',
  desc='Beheer en onderhoud van bedrijfsfietsen door een echte fietsenmaker in dienst. Herstellingen, nazicht en beheer van de vloot, voor bedrijven in Limburg en de Kempen.',
  lead='Een bedrijf met veel fietsen heeft veel onderhoud. Als extra dienst nemen wij het beheer over, met een echte fietsenmaker in dienst.',
  intro=('Een fietsenmaker op je site.', 'Bedrijfsfietsen, dienstfietsen, fietsen om over een grote site te rijden: ze worden intensief gebruikt en moeten het blijven doen. Daarom hebben we een echte fietsenmaker in dienst, geen collega die het er even bij doet.',
         'Hij staat in voor het beheer en onderhoud van de vloot: nazicht, herstellingen, banden, remmen, kettingen, verlichting. Fietsen die niet meer te redden zijn, gaan eruit; nieuwe komen erbij.',
         'Daarnaast beheert hij mee onze opslagruimte, dus onderdelen en reservefietsen liggen klaar en zijn terug te vinden.'),
  werk=('Alles wat een vloot nodig heeft.', 'Van dagelijks onderhoud tot het beheer van de hele fietsenvloot.', [
        ('Beheer van de vloot', 'Overzicht van alle fietsen: welke er zijn, waar ze staan, wat de staat is en wanneer ze onderhoud nodig hebben.'),
        ('Onderhoud', 'Periodiek nazicht van banden, remmen, ketting, versnellingen en verlichting, zodat de fietsen veilig blijven.'),
        ('Herstellingen', 'Platte band, kapotte ketting, losse trapper: hersteld door een vakman, snel weer inzetbaar.'),
        ('Onderdelen en reserve', 'Onderdelen en reservefietsen op voorraad in ons magazijn, digitaal bijgehouden.')]),
  punten=['Een echte fietsenmaker in dienst', 'Beheer én onderhoud van de hele vloot', 'Onderdelen en reservefietsen op voorraad', 'Herstellingen ter plaatse of in ons atelier', 'Overzicht van de staat van elke fiets'],
  faq=[
    ('Wie doet het onderhoud?', 'Een echte fietsenmaker die bij BV Geert Vos in dienst is. Hij staat ook mee in voor het beheer van onze opslagruimte.'),
    ('Beheren jullie ook de hele vloot?', 'Ja. Naast onderhoud en herstellingen houden we bij welke fietsen er zijn, in welke staat ze zijn en wanneer ze nazicht nodig hebben.'),
    ('Hebben jullie onderdelen op voorraad?', 'Ja. Onderdelen en reservefietsen liggen in ons magazijn en worden bijgehouden in onze digitale inventaris.'),
    ('Kunnen jullie starten met een bestaande vloot?', 'Zeker. We beginnen met een nazicht van alle fietsen en een overzicht van wat er moet gebeuren.'),
  ],
  fotosrc='/img/team/fietsen-aanhanger.webp', alt='Bedrijfsfietsen op een aanhangwagen naast een bestelwagen',
  foto2='/img/team/fietsen-opslag.webp|Fietsen en materiaal in onze opslagruimte', extra=True)

# --- 5 Opslag
pages['opslag'] = dienst_pagina('opslag', EXTRA[1][1], EXTRA[1][2], EXTRA[1][3],
  title='Opslag en voorraadbeheer, 300 palletplaatsen | BV Geert Vos',
  desc='Opslagruimte met ongeveer 300 palletplaatsen en een digitale inventaris die dagelijks wordt bijgewerkt. Opslag en voorraadbeheer voor bedrijven in Limburg en de Kempen.',
  lead='Als extra dienst: ongeveer 300 palletplaatsen en een digitale inventaris die elke dag wordt bijgewerkt. Je weet altijd wat er ligt en waar.',
  intro=('Wat je niet dagelijks nodig hebt, ligt bij ons klaar.', 'Meubilair dat tijdelijk weg moet, materiaal voor events, reserveonderdelen, seizoensmateriaal: het moet ergens naartoe, en het moet terug te vinden zijn als je het nodig hebt.',
         'Wij beschikken over een opslagruimte met ongeveer 300 palletplaatsen. Alles wat binnenkomt, wordt geregistreerd in een digitale inventaris die dagelijks wordt bijgewerkt. Geen zoekwerk, geen dubbele aankopen.',
         'Onze fietsenmaker staat mee in voor het beheer van het magazijn, en onze verhuiswagens met laadlift brengen en halen wat je nodig hebt.'),
  werk=('Opslaan, bijhouden, leveren.', 'Meer dan een loods: een voorraad die beheerd wordt.', [
        ('300 palletplaatsen', 'Droge, geordende opslag voor meubilair, materiaal en reserveonderdelen.'),
        ('Digitale inventaris', 'Elke pallet en elk stuk geregistreerd, dagelijks bijgewerkt. Je weet wat er ligt zonder te gaan kijken.'),
        ('In- en uitslag', 'Materiaal ophalen, opslaan en terugbrengen met onze eigen verhuiswagens met laadlift.'),
        ('Beheer door een vast aanspreekpunt', 'Eén persoon die het magazijn kent en weet waar alles ligt.')]),
  punten=['Ongeveer 300 palletplaatsen', 'Digitale inventaris, dagelijks bijgewerkt', 'Transport met eigen verhuiswagens', 'Vast aanspreekpunt voor het magazijn', 'Combineerbaar met verhuizingen en werkplekinrichting'],
  faq=[
    ('Hoeveel opslagruimte hebben jullie?', 'Ongeveer 300 palletplaatsen.'),
    ('Hoe weet ik wat er van mij ligt?', 'Alles wordt bijgehouden in een digitale inventaris die dagelijks wordt bijgewerkt. Vraag het aan ons vast aanspreekpunt en je krijgt het overzicht.'),
    ('Halen en brengen jullie ook?', 'Ja, met onze eigen verhuiswagens met laadlift.'),
    ('Kunnen jullie tijdelijke opslag doen tijdens een verhuizing?', 'Ja. Dat combineren we vaak: meubilair tijdelijk bij ons, en terug op zijn plaats als de nieuwe ruimte klaar is.'),
  ],
  fotosrc='/img/team/opslag-rekken.webp', alt='Opslagrekken met pallets, kasten en lockers',
  foto2='/img/team/fietsen-opslag.webp|Opslagruimte met stellingen, fietsen en materiaal', extra=True)


# ---------------------------------------------------------------- FACILITYPROJECTEN (pijler 2)
pages['facilityprojecten'] = dict(
  extra=schema('facilityprojecten', 'Facilityprojecten', ('Facilityprojecten', 'Interne verhuizingen en logistiek, kabelmanagement en werkplekinrichting en verlichting, voor langere of grotere projecten.'), FAQ_FAC),
  title='Facilityprojecten in Limburg en de Kempen | BV Geert Vos, Meerhout',
  desc='Facilityprojecten voor langere of grotere opdrachten: verhuizingen en logistiek, kabelmanagement en werkplekken, verlichting. Voor bedrijven in Limburg en de Kempen.',
  body=kop('Pijler 2', 'Facilityprojecten', 'Verhuizingen en logistiek, kabelmanagement en werkplekken, verlichting. Enkel voor langere of grotere opdrachten voor bedrijven in Limburg en de Kempen.', 'Facilityprojecten') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee">
    <div>
      <h2>Projecten, geen klusjes.</h2>
      <p class="lead" style="margin-top:16px">Het projectmatige werk doen we enkel voor langere of grotere opdrachten voor bedrijven. Dat kan voor de takken verhuizingen en logistiek, kabelmanagement en werkplekken, en verlichting.</p>
      <p style="margin-top:16px">Een grote interne verhuizing, een reeks werkplekken die ingericht moeten worden, verlichting die in een heel gebouw of magazijn wordt vervangen: zulke projecten plannen we met een vast team en een ervaren teamlead die opvolgt.</p>
      <p>Een hecht en bereikbaar team, en de verantwoordelijkheid hoog bij onszelf: zo willen we werken voor onze klanten.</p>
    </div>
    {foto('/img/team/team-keuken-1.webp', 'Medewerkers bouwen een keuken op in een kantoorruimte', 'foto-hoog')}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Drie takken</p><h2>Waar we projecten voor uitvoeren.</h2><p class="lead">Elke tak heeft een eigen pagina met wat we precies doen, foto's en veelgestelde vragen.</p></div>
    {takken_html()}
  </div>
</section>
<section>
  <div class="wrap twee">
    <div>
      <p class="label">Onze ervaring</p>
      <h2>Dertig jaar facility bij Nike.</h2>
      <p class="lead" style="margin-top:16px">Bij Nike doen we al bijna dertig jaar alle facility-werk. Onze medewerkers en teamleads plannen en voeren dagelijks opdrachten uit die binnenkomen via een online ticketsysteem.</p>
      <p style="margin-top:16px">Die opdrachten zijn zeer uiteenlopend: van werkplekaanpassingen, kabelmanagement en verlichting tot verhuizingen, meetingopstellingen, meubilair en logistieke ondersteuning.</p>
      <p>{NIKE_NOOT}</p>
      <p style="margin-top:16px"><a class="btn btn-lijn" href="/ons-verhaal/">Lees ons verhaal</a></p>
    </div>
    {foto('/img/team/team-gang.webp', 'Ons team onderweg naar een opdracht', 'foto-hoog')}
  </div>
</section>
''' + faq_blok(FAQ_FAC) + '</main>\n' + CTA)

# ---------------------------------------------------------------- DIENSTEN (overzicht)
pages['diensten'] = dict(
  extra=schema('diensten', 'Diensten', None, None),
  title='Onze diensten: servicetechniekers en facilityprojecten | BV Geert Vos',
  desc='Twee diensten voor langdurige projecten: servicetechniekers (elektriciens en mechaniciens) en facilityprojecten (verhuizingen, werkplekken, verlichting). Limburg en de Kempen.',
  body=kop('Twee diensten', 'Onze diensten', 'Wij bieden twee diensten aan: servicetechniekers en facilityprojecten, allebei voor langdurige projecten. Daarnaast twee extra diensten: fietsenbeheer en opslag.', 'Diensten') + f'''
<main id="inhoud">
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Twee pijlers</p><h2>Servicetechniekers en facilityprojecten.</h2><p class="lead">Wij gaan enkel voor langdurige projecten. Daar bouwen we ons team, onze planning en onze klantrelaties rond.</p></div>
    {pijlers_html()}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Het verschil</p><h2>Twee manieren van werken.</h2></div>
    <div class="inzet">
      <div>
        <h3>Servicetechniekers</h3>
        <p>Wij lenen servicetechniekers uit aan bedrijven voor lange projecten, zowel elektrisch als mechanisch. Niet iedereen kan voor elke klus bij ons terecht: wij gaan op zoek naar langdurige projecten en werven daar zo het personeel voor aan. Naar personeel zijn we dan ook steeds op zoek.</p>
        <p style="margin-top:16px"><a href="/servicetechniekers/">Servicetechniekers</a> · <a href="/elektriciens/">Elektriciens</a> · <a href="/mechaniciens/">Mechaniciens</a> · <a href="/vacatures/">Vacatures</a></p>
      </div>
      <div>
        <h3>Facilityprojecten</h3>
        <p>Het projectmatige werk doen we enkel voor langere of grotere opdrachten voor bedrijven. Dat kan voor de takken verhuizingen en logistiek, kabelmanagement en werkplekken, en verlichting.</p>
        <p style="margin-top:16px"><a href="/facilityprojecten/">Facilityprojecten</a> · <a href="/verhuizingen/">Verhuizingen</a> · <a href="/kabelmanagement/">Kabelmanagement</a> · <a href="/verlichting/">Verlichting</a></p>
      </div>
    </div>
  </div>
</section>
<section id="extra">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Extra diensten</p><h2>Fietsenbeheer en opslag.</h2><p class="lead">Naast onze twee pijlers bieden we twee extra diensten aan.</p></div>
    {extra_html()}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap twee">
    <div>
      <p class="label">Onze ervaring</p>
      <h2>Al 30 jaar elke dag bij Nike.</h2>
      <p class="lead" style="margin-top:16px">Bij Nike doen we al bijna dertig jaar alle facility-werk, van verhuizingen en werkplekken tot verlichting en meubilair.</p>
      <p style="margin-top:16px">{NIKE_NOOT}</p>
      <p style="margin-top:16px"><a class="btn btn-lijn" href="/ons-verhaal/">Lees ons verhaal</a></p>
    </div>
    {foto('/img/team/team-gang.webp', 'Ons team onderweg naar een opdracht', 'foto-hoog')}
  </div>
</section>
''' + faq_blok(FAQ_DIENSTEN, paper=False) + '</main>\n' + CTA)

# ---------------------------------------------------------------- ONS VERHAAL
pages['ons-verhaal'] = dict(
  extra=schema('ons-verhaal', 'Ons verhaal'),
  title='Ons verhaal: sinds 1996 bij Nike | BV Geert Vos, Meerhout',
  desc='Begonnen in 1996 met een deur en een deurklink bij Nike. Vandaag elke dag een volledig team ter plaatse, sinds 2024 ook servicetechniekers elders.',
  body=kop('Sinds 1996', 'Ons verhaal', 'Het begon ongeveer dertig jaar geleden met een kleine opdracht. Vandaag is het een samenwerking die nog altijd bestaat, en de basis voor onze servicetechniekers en facilityprojecten.', 'Ons verhaal') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee">
    <div>
      <h2>1996: een deur en een deurklink.</h2>
      <p class="lead" style="margin-top:16px">Geert Vos begon in 1996 als contractor bij Nike. Wat begon met het herstellen van een deur en een deurklink, groeide stap voor stap uit tot een samenwerking die vandaag nog steeds bestaat.</p>
      <p style="margin-top:16px">In het begin ging het onder andere om het vervangen van lampen en het klaarzetten van meetings met tafels, stoelen, beamers en geluidsinstallaties. Doorheen de jaren kregen we steeds meer verantwoordelijkheden, en groeide zowel het takenpakket als ons team.</p>
      <p>Vandaag beheren en onderhouden we onder andere elektrische bureaus, bureaustoelen en een groot deel van het meubilair in breakrooms en restaurants. We ondersteunen nog steeds meetings en evenementen. De vroegere beamers hebben ondertussen plaatsgemaakt voor grote mobiele schermen.</p>
    </div>
    {foto('/img/team/team-gang.webp', 'Ons team onderweg naar een opdracht', 'foto-hoog')}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap twee">
    <ol class="tijd">
      <li><time>1996</time><p>Geert Vos start als contractor bij Nike. Eerste opdracht: een deur en een deurklink.</p></li>
      <li><time>De jaren erna</time><p>Lampen vervangen, meetings klaarzetten. Meer verantwoordelijkheden, een groter team.</p></li>
      <li><time>Vandaag</time><p>Elke dag een volledig team bij Nike: meubilair, verhuizingen en events, met twee eigen verhuiswagens met laadlift.</p></li>
      <li><time>2024</time><p>Servicetechniekers (elektriciens en mechaniciens) worden ook bij andere klanten ingezet, voor langdurige projecten. Zo groeit BV Geert Vos verder, naast de werking bij Nike.</p></li>
    </ol>
    <div>
      <p class="label">Werking bij Nike</p>
      <h2>Elke dag een ticket, elke dag geregeld.</h2>
      <p class="lead" style="margin-top:16px">Bij Nike werken we met een online ticketsysteem waarin dagelijks opdrachten binnenkomen. Onze medewerkers en teamleads zorgen voor de planning en de uitvoering.</p>
      <p style="margin-top:16px">Die opdrachten zijn zeer uiteenlopend: van werkplekaanpassingen, kabelmanagement en verlichting tot verhuizingen, meetingopstellingen, meubilair en logistieke ondersteuning.</p>
      <p>Dat we hier na bijna dertig jaar nog steeds dagelijks met een volledig team actief zijn, zegt volgens ons veel over de samenwerking en het vertrouwen dat doorheen de jaren is opgebouwd.</p>
      <p>{NIKE_NOOT}</p>
      <p>Los daarvan bieden we ook twee extra diensten aan: <a href="/fietsenbeheer/">fietsenbeheer</a>, met een echte fietsenmaker in dienst, en <a href="/opslag/">opslag en voorraadbeheer</a>, met ongeveer 300 palletplaatsen en een digitale inventaris die dagelijks wordt bijgewerkt.</p>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-kop">
      <p class="label">Wie wij zijn</p>
      <h2>Een hecht en bereikbaar team.</h2>
      <p class="lead">Dat is de sleutel van BV Geert Vos. Ook voor onze klanten: de verantwoordelijkheid leggen we hoog bij onszelf. We zijn een jong team waarin veel collega's ook buiten het werk goed met elkaar overeenkomen, binnen een duidelijke organisatie met ervaren teamleads.</p>
    </div>
    <div class="waarden">
      <div><h3>Hecht en bereikbaar</h3><p>Je weet bij wie je terecht kunt, en je krijgt binnen 24 uur een reactie.</p></div>
      <div><h3>Verantwoordelijkheid bij ons</h3><p>Onze teamleads volgen elke opdracht op. Wij nemen de verantwoordelijkheid, ook voor het resultaat bij de klant.</p></div>
      <div><h3>Orde, stiptheid, kwaliteit</h3><p>Onze belangrijkste waarden. Een opdracht is pas klaar wanneer ze 100% afgewerkt is, en de werkplek proper en ordelijk achterblijft.</p></div>
      <div><h3>Vriendelijk, flexibel, positief</h3><p>Onze manier van werken. Daardoor vertrouwen klanten ons, en groeien samenwerkingen uit tot vele jaren, niet enkel weken of maanden.</p></div>
    </div>
    <div class="drie" style="margin-top:56px">
      {foto('/img/team/team-lunch.webp', 'Het team van Geert Vos samen aan tafel')}
      {foto('/img/team/verhuiswagen-laadlift.webp', 'Verhuiswagen met laadlift', 'foto-truck')}
      {foto('/img/team/opslag-rekken.webp', 'Ons magazijn met opslagrekken')}
    </div>
  </div>
</section>
</main>
''' + CTA)



# ---------------------------------------------------------------- VACATURES
TEAM_VAC = [('/img/team/team-lunch.webp', 'Het team van Geert Vos samen aan tafel'),
  ('/img/team/team-kerst.webp', 'Collega\'s van Geert Vos bij een evenement')]
VACATURE_JSON = json.dumps({
  "@context": "https://schema.org", "@type": "JobPosting",
  "title": "Service Technieker",
  "description": "Elektromechanisch onderhoud uitvoeren en storingen oplossen aan machines en installaties bij klanten in de regio Lommel - Genk en de Kempen. Voltijd in loondienst, vast contract mogelijk, met bedrijfsbus, GSM en maaltijdcheques. Minimaal 5 jaar aantoonbare ervaring als technieker onderhoud en storingen, VCA en rijbewijs B, bereid om in 2 of 3 ploegen te werken.",
  "datePosted": "2026-09-25", "employmentType": "FULL_TIME",
  "hiringOrganization": {"@type": "Organization", "name": "BV Geert Vos", "sameAs": DOMAIN + "/"},
  "jobLocation": {"@type": "Place", "address": {"@type": "PostalAddress", "addressLocality": "Lommel", "addressRegion": "Limburg", "addressCountry": "BE"}},
}, ensure_ascii=False)

def kv(k, v, klein):
    return f'<div><span class="vf-k">{k}</span><strong>{v}</strong><small>{klein}</small></div>'

pages['vacatures'] = dict(
  extra=schema('vacatures', 'Vacatures') + f'<script type="application/ld+json">{VACATURE_JSON}</script>\n',
  title='Vacature Service Technieker | BV Geert Vos, Meerhout',
  desc='Vacature service technieker in regio Lommel - Genk en de Kempen: elektromechanisch onderhoud en storingen, voltijd in loondienst, met bedrijfsbus en maaltijdcheques. Solliciteer online.',
  body=kop('Vacatures', 'Vacatures', 'Wij zoeken een service technieker voor onderhoud en storingen aan machines en installaties in regio Lommel - Genk en de Kempen.', 'Vacatures') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee">
    <div>
      <p class="label">Open vacature</p>
      <h2>Service Technieker</h2>
      <p class="lead" style="margin-top:16px">Je lost storingen op en voert elektromechanisch onderhoud uit aan machines en installaties bij onze klanten in de regio. Veel verschillende opdrachten, veel afwisseling, en werk dat je deels zelf kunt kiezen.</p>
      <p style="margin-top:16px">We zijn een familiebedrijf met een fijn team, korte lijnen en een leuke sfeer. Bij ons telt kwaliteit boven kwantiteit.</p>
      <p style="margin-top:24px"><a class="btn btn-geel" href="#solliciteren">Solliciteer nu</a> <a class="btn btn-lijn tel" href="tel:{TEL_TECH}" style="margin-left:8px">Liever bellen? {TEL_TECH_TXT}</a></p>
    </div>
    {foto('/img/team/team-gang.webp', 'Ons team onderweg naar een opdracht', 'foto-hoog')}
  </div>
</section>

<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">In het kort</p><h2>Wat, waar en hoe.</h2></div>
    <div class="vac-feiten">
      {kv('Locatie', 'Regio Lommel - Genk', 'In Limburg en de Kempen. Je woont op maximaal 45 minuten reistijd.')}
      {kv('Contract', 'Loondienst', 'Vast contract mogelijk')}
      {kv('Uren', 'Voltijd', 'In 2 of 3 ploegen')}
      {kv('Loon', 'Tot € 4.000 bruto', 'Op basis van je ervaring')}
      {kv('Vervoer', 'Bedrijfsbus mogelijk', 'Bus van de zaak')}
      {kv("Extra's", 'GSM en maaltijdcheques', 'En modern, goed materieel')}
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Wat ga je doen</p><h2>Veel variatie, elke dag.</h2><p class="lead">Elektromechanisch onderhoud en storingen oplossen aan machines en installaties. Veel verschillende opdrachten, dus geen dag is hetzelfde.</p></div>
    <ul class="punten" style="max-width:62ch;margin-bottom:64px">
      <li>Elektromechanisch onderhoud uitvoeren aan machines en installaties</li>
      <li>Storingen opsporen en oplossen, met schema's als houvast</li>
      <li>Werken bij onze klanten in de regio, met veel afwisseling in projecten</li>
    </ul>
    <div class="sec-kop"><p class="label">Wie zoeken we</p><h2>Ervaring, en de juiste papieren.</h2></div>
    <div class="inzet">
      <div>
        <h3>Dit heb je minimaal</h3>
        <ul class="punten">
          <li>5 jaar aantoonbare werkervaring als technieker onderhoud en storingen</li>
          <li>Bereid om in 2 of 3 ploegen te werken</li>
          <li>Vloeiend Nederlands, mondeling en schriftelijk</li>
          <li>Rijbewijs B</li>
          <li>VCA</li>
        </ul>
      </div>
      <div>
        <h3>Dit is een pluspunt</h3>
        <ul class="punten">
          <li>Diploma elektromechanica, of een richting elektra of mechanica</li>
          <li>Ruime ervaring met machines en installaties</li>
          <li>Schema's kunnen lezen en storingen zelfstandig oplossen</li>
          <li>Rolbrugattest en heftruckattest</li>
          <li>Elektrische bekwaamheid, een belangrijk extra</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Waarom bij ons</p><h2>Werken bij een familiebedrijf.</h2></div>
    {team_strip(TEAM_VAC, 'team-strip-2')}
    <div class="waarden waarden-3">
      <div><h3>Vast contract mogelijk</h3><p>Voltijd in loondienst, met de mogelijkheid op een vast contract.</p></div>
      <div><h3>Korte reistijden</h3><p>Alle opdrachten zitten in de regio, dus je bent snel weer thuis.</p></div>
      <div><h3>Eigen inbreng</h3><p>Je kunt werk kiezen dat bij je past.</p></div>
      <div><h3>Kwaliteit boven kwantiteit</h3><p>Bij ons telt goed werk meer dan snel werk. Een opdracht is pas klaar als ze 100% af is.</p></div>
      <div><h3>Fijn team, leuke sfeer</h3><p>Een familiebedrijf met korte lijnen en collega's die ook buiten het werk goed met elkaar overeenkomen.</p></div>
      <div><h3>Modern materieel</h3><p>Goed en modern materieel, een bedrijfsbus, GSM en maaltijdcheques.</p></div>
    </div>
  </div>
</section>

<section id="solliciteren">
  <div class="wrap twee" style="align-items:start">
    <div>
      <p class="label">Solliciteren</p>
      <h2>Een paar vragen en je cv.</h2>
      <p class="lead" style="margin-top:16px">Vul het formulier in en voeg je cv toe, of typ je werkervaring uit. Een motivatiebrief is niet nodig. We antwoorden persoonlijk.</p>
      <p style="margin-top:16px">Liever bellen? Bel ons op <a class="tel" href="tel:{TEL_TECH}">{TEL_TECH_TXT}</a>.</p>
    </div>
    <form data-gv action="https://formsubmit.co/{MAIL}" method="POST" enctype="multipart/form-data">
      <input type="hidden" name="_subject" value="Sollicitatie Service Technieker via geertvos.be">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="https://geertvos.be/bedankt/">
      <input type="hidden" name="Vacature" value="Service Technieker">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
      <div class="veld-2">
        <div class="veld"><label for="s-naam">Naam</label><input id="s-naam" name="Naam" required autocomplete="name"></div>
        <div class="veld"><label for="s-tel">Telefoon</label><input id="s-tel" type="tel" name="Telefoon" required autocomplete="tel"></div>
      </div>
      <div class="veld-2">
        <div class="veld"><label for="s-email">E-mail</label><input id="s-email" type="email" name="E-mail" required autocomplete="email"></div>
        <div class="veld"><label for="s-woonplaats">Woonplaats</label><input id="s-woonplaats" name="Woonplaats" required autocomplete="address-level2"></div>
      </div>
      <div class="veld-2">
        <div class="veld"><label for="s-diploma">Opleiding of diploma</label><input id="s-diploma" name="Opleiding" placeholder="bv. elektromechanica"></div>
        <div class="veld"><label for="s-ervaring">Ervaring als onderhoudstechnieker</label>
          <select id="s-ervaring" name="Ervaring"><option>Minder dan 5 jaar</option><option>5 tot 10 jaar</option><option>Meer dan 10 jaar</option></select></div>
      </div>
      <div class="veld"><span class="veld-kop">Wat heb je al?</span>
        <div class="checks">
          <label><input type="checkbox" name="Rijbewijs B" value="Ja"> Rijbewijs B</label>
          <label><input type="checkbox" name="VCA" value="Ja"> VCA</label>
          <label><input type="checkbox" name="Rolbrugattest" value="Ja"> Rolbrugattest</label>
          <label><input type="checkbox" name="Heftruckattest" value="Ja"> Heftruckattest</label>
          <label><input type="checkbox" name="Elektrische bekwaamheid" value="Ja"> Elektrische bekwaamheid</label>
        </div></div>
      <div class="veld-2">
        <div class="veld"><label for="s-ploeg">Bereid om in 2 of 3 ploegen te werken?</label>
          <select id="s-ploeg" name="Ploegen"><option>Ja</option><option>Nee</option></select></div>
        <div class="veld"><label for="s-vanaf">Beschikbaar vanaf</label><input id="s-vanaf" name="Beschikbaar vanaf" placeholder="bv. direct, of 1 november"></div>
      </div>
      <div class="veld cv-blok">
        <span class="veld-kop">Je cv of je ervaring</span>
        <p class="veld-uitleg">Voeg je cv toe. Heb je geen cv? Typ dan hieronder gewoon je werkervaring uit. Eén van de twee is genoeg, een motivatiebrief is niet nodig.</p>
        <label class="cv-upload" for="s-cv"><span class="cv-titel">Upload je cv</span><span class="cv-sub">Pdf of Word</span><input id="s-cv" type="file" name="attachment" accept=".pdf,.doc,.docx"></label>
        <label for="s-ervaring-tekst">Geen cv? Typ je werkervaring uit</label>
        <textarea id="s-ervaring-tekst" name="Werkervaring" data-of-cv placeholder="Bij welke bedrijven werkte je, van wanneer tot wanneer, en wat deed je daar? Aan welke machines en installaties heb je gewerkt?"></textarea>
      </div>
      <p class="form-fout" role="alert" hidden>Voeg je cv toe, of typ je werkervaring uit. Eén van de twee is nodig.</p>
      <div><button class="btn btn-geel" type="submit">Verstuur sollicitatie</button></div>
      <p class="form-noot">We gebruiken je gegevens en cv alleen voor deze sollicitatie. Zie ons <a href="/privacybeleid/">privacybeleid</a>.</p>
    </form>
  </div>
</section>
</main>
''' + CTA)

# ---------------------------------------------------------------- CONTACT
pages['contact'] = dict(
  extra=schema('contact', 'Contact'),
  title='Contact | BV Geert Vos, Meerhout',
  desc='Neem contact op met BV Geert Vos, Bevrijdingslaan 256 in Meerhout. Bel onze servicecoördinator of stuur een bericht. Wij reageren binnen 24 uur.',
  body=kop('Neem contact op', 'Contact', 'Contacteer onze servicecoördinator. Wij zorgen voor een reactie binnen 24 uur.', 'Contact') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee" style="align-items:start">
    <div>
      <div class="bel-kaart">
        <strong>Bel ons</strong>
        <p class="rol">Voor servicetechniekers en vacatures</p>
        <a class="tel" href="tel:{TEL_TECH}">{TEL_TECH_TXT}</a>
        <p class="rol" style="margin-top:20px">Voor alle projecten</p>
        <a class="tel" href="tel:{TEL_PROJ}">{TEL_PROJ_TXT}</a>
      </div>
      <h2 style="margin-top:40px;font-size:26px">BV Geert Vos</h2>
      <address style="font-style:normal;line-height:1.8;margin-top:8px;color:var(--grijs)">Bevrijdingslaan 256<br>2450 Meerhout, België<br>BTW BE 0862.515.981<br><a href="mailto:{MAIL}">{MAIL}</a></address>
      <p style="margin-top:14px"><a href="https://www.google.com/maps/search/?api=1&query=Bevrijdingslaan+256+2450+Meerhout" rel="noopener" target="_blank">Route via Google Maps</a></p>
    </div>
    <div>
      <h2 style="font-size:40px;margin-bottom:20px">Stuur een bericht</h2>
      <form data-gv action="https://formsubmit.co/{MAIL}" method="POST">
        <input type="hidden" name="_subject" value="Nieuw bericht via geertvos.be">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_next" value="https://geertvos.be/bedankt/">
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
        <div class="veld-2">
          <div class="veld"><label for="naam">Naam</label><input id="naam" name="Naam" required autocomplete="name"></div>
          <div class="veld"><label for="bedrijf">Bedrijf</label><input id="bedrijf" name="Bedrijf" autocomplete="organization"></div>
        </div>
        <div class="veld-2">
          <div class="veld"><label for="email">E-mail</label><input id="email" type="email" name="E-mail" required autocomplete="email"></div>
          <div class="veld"><label for="tel">Telefoon</label><input id="tel" type="tel" name="Telefoon" autocomplete="tel"></div>
        </div>
        <div class="veld"><label for="dienst">Waarover gaat het?</label>
          <select id="dienst" name="Dienst">
            <option>Servicetechniekers: elektriciens</option><option>Servicetechniekers: mechaniciens</option><option>Facilityproject: verhuizingen en logistiek</option><option>Facilityproject: kabelmanagement en werkplekken</option><option>Facilityproject: verlichting</option><option>Extra dienst: fietsenbeheer</option><option>Extra dienst: opslag en voorraadbeheer</option><option>Iets anders</option>
          </select></div>
        <div class="veld"><label for="bericht">Bericht</label><textarea id="bericht" name="Bericht" required></textarea></div>
        <div><button class="btn btn-geel" type="submit">Verstuur bericht</button></div>
        <p class="form-noot">We gebruiken je gegevens alleen om te antwoorden. Zie ons <a href="/privacybeleid/">privacybeleid</a>.</p>
      </form>
    </div>
  </div>
</section>
</main>
''')

pages['bedankt'] = dict(
  title='Bedankt voor je bericht | BV Geert Vos',
  desc='Je bericht is verstuurd. Wij reageren binnen 24 uur.',
  extra='<meta name="robots" content="noindex">',
  body=kop('Contact', 'Bedankt', 'Je bericht is aangekomen. Wij reageren binnen 24 uur.', 'Contact') + f'''
<main id="inhoud"><section><div class="wrap"><p class="lead">Dringend? Bel voor servicetechniekers <a class="tel" href="tel:{TEL_TECH}">{TEL_TECH_TXT}</a> of voor projecten <a class="tel" href="tel:{TEL_PROJ}">{TEL_PROJ_TXT}</a>.</p><p style="margin-top:24px"><a class="btn btn-ink" href="/">Terug naar de startpagina</a></p></div></section></main>
''')

pages['404'] = dict(
  title='Pagina niet gevonden | BV Geert Vos',
  desc='Deze pagina bestaat niet (meer).',
  extra='<meta name="robots" content="noindex">',
  body=kop('Fout 404', 'Niet gevonden', 'Deze pagina bestaat niet of is verhuisd. Misschien zoek je een van onze diensten?', 'Niet gevonden') + f'''
<main id="inhoud"><section><div class="wrap"><p class="lead"><a href="/servicetechniekers/">Servicetechniekers</a> · <a href="/facilityprojecten/">Facilityprojecten</a> · <a href="/vacatures/">Vacatures</a> · <a href="/contact/">Contact</a></p><p style="margin-top:24px"><a class="btn btn-ink" href="/">Naar de startpagina</a></p></div></section></main>
''')

# ---------------------------------------------------------------- PRIVACY
pages['privacybeleid'] = dict(
  title='Privacybeleid | BV Geert Vos',
  desc='Hoe BV Geert Vos omgaat met je persoonsgegevens op geertvos.be.',
  body=kop('Juridisch', 'Privacybeleid', 'Kort en zonder kleine lettertjes: welke gegevens we verwerken, waarom, en hoelang.', 'Privacybeleid') + f'''
<main id="inhoud"><section><div class="wrap prose">
<p>BV Geert Vos, Bevrijdingslaan 256, 2450 Meerhout (BTW BE 0862.515.981) is verantwoordelijk voor de verwerking van persoonsgegevens op deze website. Vragen? Mail naar <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>Contact- en sollicitatieformulier</h2>
<p>Als je een formulier invult, verwerken we je naam, e-mailadres, en wat je verder invult (bedrijf, telefoonnummer, bericht, en bij een sollicitatie ook woonplaats, ervaring, certificaten en cv). We gebruiken die gegevens alleen om je vraag te beantwoorden en bewaren ze zolang dat nodig is voor de opvolging. Het formulier wordt technisch verzonden via FormSubmit, die het bericht als e-mail aan ons bezorgt.</p>
<h2>Cookies</h2>
<p>Deze website gebruikt geen cookies, geen tracking en geen analysediensten van derden. De lettertypes worden vanaf onze eigen server geladen.</p>
<h2>Je rechten</h2>
<p>Je hebt het recht om je gegevens in te kijken, te laten verbeteren of te laten verwijderen. Stuur daarvoor een mail naar <a href="mailto:{MAIL}">{MAIL}</a>. Je kunt ook een klacht indienen bij de Gegevensbeschermingsautoriteit (gegevensbeschermingsautoriteit.be).</p>
<p class="grijs" style="margin-top:32px">Laatst bijgewerkt: september 2026.</p>
</div></section></main>
''')

# ---------------------------------------------------------------- schrijven
bulb = open(os.path.join(OUT, 'img', 'bulb.svg')).read()
for slug, p in pages.items():
    html = head(p['title'], p['desc'], slug, p.get('extra', '')) + header(slug) + p['body'].replace('BULBSVG', bulb) + FOOT
    open(os.path.join(OUT, f'{slug}.html'), 'w').write(html)
    print(slug, len(html))

urls = ['', 'diensten/', 'servicetechniekers/', 'elektriciens/', 'mechaniciens/', 'facilityprojecten/', 'verhuizingen/', 'kabelmanagement/', 'verlichting/', 'fietsenbeheer/', 'opslag/', 'ons-verhaal/', 'vacatures/', 'contact/', 'privacybeleid/']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
