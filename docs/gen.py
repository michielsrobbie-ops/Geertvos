# Genereert de statische pagina's van geertvos.be (header/footer één keer gedefinieerd).
# Draaien vanuit docs/: python3 gen.py  → schrijft de html-bestanden in de projectmap.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site') if os.path.isdir(os.path.join(HERE, 'site')) else os.path.dirname(HERE)
DOMAIN = 'https://geertvos.be'
V = '20260910b'         # versie voor css/js — ophogen bij elke wijziging
TEL_LORENZO = '+32400000000'   # TIJDELIJK — echte nummer Lorenzo invullen
TEL_PJ = '+32400000001'        # TIJDELIJK — echte nummer Pieter-Jan invullen
TEL_LORENZO_TXT = '+32 400 00 00 00'
TEL_PJ_TXT = '+32 400 00 00 01'
MAIL = 'info@geertvos.be'   # TODO: bevestigen bij klant

NAV = [('ons-verhaal', 'Ons verhaal'), ('werken-bij', 'Werken bij')]


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
            "serviceType":service[0],"url":f"{DOMAIN}/{slug}/","areaServed":{"@type":"Place","name":"Kempen, België"},
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
<meta property="og:image" content="{DOMAIN}/img/og.jpg">
<meta property="og:locale" content="nl_BE">
<meta name="theme-color" content="#141518">
<link rel="preload" href="/fonts/bricolage-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/style.css?v={V}">
{extra}
</head>
<body>
<a class="skip" href="#inhoud">Naar de inhoud</a>
'''

DIENST_MENU = [('elektriciens', 'Elektriciens'), ('mechaniciens', 'Mechaniciens'), ('verhuizingen', 'Verhuizingen &amp; logistiek'),
  ('kabelmanagement', 'Kabelmanagement &amp; werkplekken'), ('verlichting', 'Verlichting'), ('fietsenbeheer', 'Fietsenbeheer'), ('opslag', 'Opslag &amp; voorraad')]

def header(slug):
    cur = ' aria-current="page"'
    dienst_slugs = [d[0] for d in DIENST_MENU] + ['diensten', 'facility-diensten']
    sub = ''.join(f'<a href="/{s}/"{cur if s == slug else ""}>{t}</a>' for s, t in DIENST_MENU)
    links = ''.join(f'<a href="/{s}/"{cur if s == slug else ""}>{t}</a>' for s, t in NAV)
    return f'''<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/" aria-label="BV Geert Vos, naar de startpagina"><img src="/img/logo-nav.svg" alt="BV Geert Vos" width="236" height="64"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu"><span></span>Menu</button>
    <nav class="nav" id="menu" aria-label="Hoofdmenu">
      <a href="/"{cur if slug == 'index' else ''}>Home</a>
      <div class="sub{' sub-actief' if slug in dienst_slugs else ''}">
        <a href="/diensten/" class="sub-link"{cur if slug == 'diensten' else ''}>Diensten</a><button class="sub-knop" type="button" aria-expanded="false" aria-label="Diensten openen"></button>
        <div class="sub-menu">{sub}<a href="/facility-diensten/" class="sub-alle">Alle facility-diensten</a></div>
      </div>
      {links}<a class="nav-cta" href="/contact/">Contact</a></nav>
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
      <h2>Zeg wat u nodig hebt.</h2>
      <p>Lorenzo bekijkt samen met u wat er moet gebeuren en wanneer we kunnen starten.</p>
    </div>
    <div class="knoppen">
      <a class="btn btn-geel" href="/contact/">Contact</a>
      <a class="btn btn-licht tel" href="tel:{TEL_LORENZO}">{TEL_LORENZO_TXT}</a>
    </div>
  </div>
</div>
'''

FOOT = f'''<footer class="site-foot">
  <div class="wrap">
    <div>
      <img src="/img/logo-nav.svg" alt="BV Geert Vos" width="258" height="70">
      <p>Elektriciens, mechaniciens en facility-diensten vanuit Meerhout. Sinds 1996 dagelijks aan het werk bij Nike, sinds 2024 ook bij andere bedrijven.</p>
    </div>
    <div>
      <p class="foot-kop">Diensten</p>
      <ul>
        <li><a href="/elektriciens/">Elektriciens</a></li>
        <li><a href="/mechaniciens/">Mechaniciens</a></li>
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
        <li><a href="/werken-bij/">Werken bij Geert Vos</a></li>
        <li><a href="/contact/">Contact</a></li>
        <li><a href="/privacybeleid/">Privacybeleid</a></li>
      </ul>
    </div>
    <div>
      <p class="foot-kop">Contact</p>
      <address>BV Geert Vos<br>Bevrijdingslaan 256<br>2450 Meerhout, België<br>
      <a href="tel:{TEL_LORENZO}">{TEL_LORENZO_TXT}</a><br>
      <a href="tel:{TEL_PJ}">{TEL_PJ_TXT}</a><br>
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

def faq_blok(items, kop='Veelgestelde vragen'):
    return '<section class="sec-paper"><div class="wrap"><div class="sec-kop"><p class="label">Vragen</p><h2>' + kop + '</h2></div><div class="faq">' + ''.join(
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
      ''' + fig('/img/werk/magazijn-verlichting-hoogwerker-1.webp', 'Verlichting vervangen tussen magazijnstellingen met de hoogwerker') + fig('/img/werk/magazijn-verlichting-hoogwerker-2.webp', 'Verlichting vervangen in een magazijn') + fig('/img/werk/straatverlichting-hoogwerker-2.webp', 'Straatverlichting vervangen met de hoogwerker') + fig('/img/werk/lichtmasten-op-vrachtwagen.webp', 'Mobiele lichtmasten verplaatsen en verhuizen') + '''
    </div>
  </div>
</section>
'''

def ph(tekst, cls=''):
    return f'<div class="foto foto-ph {cls}"><span>{tekst}</span></div>'

def foto(src, alt, cls=''):
    return f'<div class="foto {cls}"><img src="{src}" alt="{alt}" loading="lazy" width="460" height="520"></div>'

pages = {}

# ---------------------------------------------------------------- HOME
pages['index'] = dict(
  title='Elektriciens, mechaniciens en facility | BV Geert Vos',
  desc='Elektriciens en mechaniciens voor langere tijd bij uw bedrijf, plus verhuizingen, werkplekken, verlichting, fietsen en opslag. Meerhout, sinds 1996 bij Nike.',
  extra='''<script type="application/ld+json">
{"@context":"https://schema.org","@type":"LocalBusiness","name":"BV Geert Vos","url":"https://geertvos.be/","logo":"https://geertvos.be/img/logo.svg","vatID":"BE0862515981",
"address":{"@type":"PostalAddress","streetAddress":"Bevrijdingslaan 256","postalCode":"2450","addressLocality":"Meerhout","addressRegion":"Antwerpen","addressCountry":"BE"},"foundingDate":"1996",
"areaServed":{"@type":"Place","name":"Kempen, België"},"email":"info@geertvos.be","image":"https://geertvos.be/img/og.jpg",
"knowsAbout":["elektriciens","mechaniciens","facility management","interne verhuizingen","kabelmanagement","werkplekinrichting","verlichting","fietsenbeheer","opslag"]}
</script>''',
  body=f'''
<main id="inhoud">
<section class="hero" aria-label="Intro">
  <div class="hero-licht"></div>
  <div class="wrap">
    <div class="hero-tekst">
      <p class="label label-licht">Techniek en facility, Meerhout</p>
      <h1>Techniekers die blijven.</h1>
      <p class="lead">Elektriciens en mechaniciens die voor langere tijd bij uw bedrijf aan de slag gaan, en alle facility-werk eromheen: verhuizingen, werkplekken, verlichting, fietsen en opslag. Vanuit Meerhout, al bijna dertig jaar elke dag bij Nike.</p>
      <div class="hero-cta">
        <a class="btn btn-geel" href="/contact/">Contact</a>
        <a class="btn btn-licht" href="/diensten/">Onze diensten</a>
      </div>
      <div class="hero-feit">
        <div><strong><span class="teller" data-sinds="1996-01-01">0</span> dagen</strong>aan het werk bij Nike, sinds 1996</div>
        <div><strong>7 diensten</strong>techniek en facility, één aanspreekpunt</div>
        <div><strong>Meerhout</strong>Kempen, België</div>
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
      <h2>Twee pijlers, één manier van werken.</h2>
      <p class="lead">Sinds 2024 stellen we elektriciens en mechaniciens tewerk bij andere bedrijven in de Kempen en omstreken. Ze werken er zelfstandig, met de certificaten, het materiaal en de uitrusting die de opdracht vraagt, en bij voorkeur voor lange tijd bij dezelfde klant. Elektrieker, onderhoudstechnieker, mecanicien: zeg wat u nodig hebt, wij zoeken het profiel.</p>
    </div>
    <div class="pijlers">
      <a class="pijler" href="/elektriciens/">
        <img src="/img/werk/werkstation-kabelmanagement-1.webp" alt="" loading="lazy" width="440" height="591">
        <div class="in"><p class="label">Pijler 1</p><h3>Elektriciens</h3><p>Voor langdurige samenwerkingen op uw locatie, of voor een kortere technische opdracht.</p><span class="meer">Meer over onze elektriciens</span></div>
      </a>
      <a class="pijler" href="/mechaniciens/">
        <img src="/img/werk/lichtmast-verplaatsen-heftruck.webp" alt="" loading="lazy" width="347" height="557">
        <div class="in"><p class="label">Pijler 2</p><h3>Mechaniciens</h3><p>Mechanisch werk dat 100% wordt afgewerkt, met opvolging door ervaren teamleads.</p><span class="meer">Meer over onze mechaniciens</span></div>
      </a>
    </div>
  </div>
</section>

<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop">
      <p class="label">Facility &amp; logistiek</p>
      <h2>Wat we al bijna dertig jaar elke dag doen.</h2>
      <p class="lead">Bij Nike komen dagelijks opdrachten binnen via een online ticketsysteem. Onze medewerkers en teamleads plannen en voeren ze uit. Vijf takken, één team.</p>
    </div>
    <ul class="takken">
      <li><a href="/verhuizingen/"><div class="tegel"><img src="/img/foto/ph-verhuizingen.jpg" alt="" loading="lazy" width="460" height="520"></div><h3>Verhuizingen &amp; interne logistiek</h3><p>Twee eigen verhuiswagens met laadlift.</p></a></li>
      <li><a href="/kabelmanagement/"><div class="tegel"><img src="/img/werk/kabelgoot-kabelmanagement.webp" alt="" loading="lazy" width="441" height="585"></div><h3>Kabelmanagement &amp; werkplekinrichting</h3><p>Elektrische bureaus, stoelen, meubilair, netjes aangesloten.</p></a></li>
      <li><a href="/verlichting/"><div class="tegel"><img src="/img/werk/magazijn-verlichting-hoogwerker-2.webp" alt="" loading="lazy" width="435" height="596"></div><h3>Verlichting vervangen &amp; onderhouden</h3><p>Waar het in 1996 mee begon.</p></a></li>
      <li><a href="/fietsenbeheer/"><div class="tegel"><img src="/img/foto/ph-fietsen.jpg" alt="" loading="lazy" width="460" height="520"></div><h3>Fietsenbeheer &amp; -onderhoud</h3><p>Met een echte fietsenmaker in dienst.</p></a></li>
      <li><a href="/opslag/"><div class="tegel"><img src="/img/werk/magazijn-verlichting-hoogwerker-1.webp" alt="" loading="lazy" width="447" height="590"></div><h3>Opslag &amp; voorraadbeheer</h3><p>300 palletplaatsen, digitale inventaris.</p></a></li>
    </ul>
  </div>
</section>

<section>
  <div class="wrap twee">
    <div>
      <p class="label">Ons verhaal</p>
      <h2>Begonnen met een deurklink.</h2>
      <p class="lead" style="margin-top:16px">In 1996 herstelde Geert Vos als contractor een deur en een deurklink bij Nike. Vandaag zijn we daar nog altijd elke dag, met een volledig team.</p>
      <p style="margin-top:16px"><a class="btn btn-lijn" href="/ons-verhaal/">Lees ons verhaal</a> <a class="btn btn-lijn" href="/werken-bij/" style="margin-left:8px">Werken bij Geert Vos</a></p>
      <div class="feiten">
        <div><strong>1996</strong>gestart bij Nike</div>
        <div><strong>2024</strong>tweede pijler: techniekers bij andere bedrijven</div>
        <div><strong>300</strong>palletplaatsen</div>
      </div>
    </div>
    <ol class="tijd">
      <li><time>1996</time><p>Geert Vos start als contractor bij Nike. De eerste opdracht: een deur en een deurklink herstellen.</p></li>
      <li><time>De jaren erna</time><p>Lampen vervangen, meetings klaarzetten met tafels, stoelen, beamers en geluid. Het takenpakket en het team groeien mee.</p></li>
      <li><time>Vandaag</time><p>Elektrische bureaus, meubilair, interne verhuizingen, fietsen, opslag en events. De beamers zijn grote mobiele schermen geworden.</p></li>
      <li><time>2024</time><p>Elektriciens en mechaniciens worden ook bij andere klanten tewerkgesteld. De tweede pijler van BV Geert Vos.</p></li>
    </ol>
  </div>
</section>

<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop">
      <p class="label">Zo werken wij</p>
      <h2>Klaar is pas klaar als het 100% af is.</h2>
      <p class="lead">Orde, stiptheid en kwaliteit. En na afloop een werkplek die proper en ordelijk achterblijft. Daarom werken klanten niet enkele weken met ons, maar vele jaren.</p>
    </div>
    <div class="waarden">
      <div><h3>Vriendelijk en flexibel</h3><p>Een positieve ingesteldheid op de werkvloer. Onze mensen komen graag, en dat merkt u.</p></div>
      <div><h3>Zelfstandig, met opvolging</h3><p>Elke technieker heeft de certificaten, het materiaal en de uitrusting om zelfstandig te werken. Ervaren teamleads volgen elke opdracht correct op.</p></div>
      <div><h3>Voor de lange termijn</h3><p>We richten ons op samenwerkingen waarbij onze techniekers voor langere periodes bij dezelfde klant werken. Kortere opdrachten doen we er graag bij.</p></div>
    </div>
  </div>
</section>
</main>
''' + CTA)

# ---------------------------------------------------------------- ELEKTRICIENS / MECHANICIENS
def techniek_pagina(naam, enk, title, desc, lead, intro, werk, punten, faq, fotosrc, foto1, foto2, extra=''):
    f1 = foto(fotosrc, foto1) if fotosrc else ph(foto1)
    return dict(title=title, desc=desc, extra=extra, body=kop('Pijler ' + ('1' if enk == 'elektricien' else '2'), naam + ' in de Kempen', lead, naam) + f'''
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
    <div class="sec-kop"><p class="label">Samenwerken</p><h2>Twee manieren om samen te werken.</h2></div>
    <div class="inzet">
      <div><h3>Langdurig op uw locatie</h3><p>Onze focus. Een {enk} die gedurende een langere periode bij dezelfde klant werkt, kent de site, de mensen en de installaties. Dat merkt u in het werk: minder uitleg, minder fouten, meer gedaan.</p></div>
      <div><h3>Kortere technische opdrachten</h3><p>Ook voor een afgebakende opdracht komen we langs. Zelfde mensen, zelfde manier van werken, ander tempo.</p></div>
    </div>
  </div>
</section>
{WERK_ELEK if enk == 'elektricien' else ''}
<section class="sec-paper">
  <div class="wrap twee">
    {foto(*foto2.split('|'), 'foto-hoog') if '|' in foto2 else ph(foto2, 'foto-hoog')}
    <div>
      <p class="label">Wat u mag verwachten</p>
      <h2>Zelfstandig, met opvolging.</h2>
      <ul class="punten">{''.join(f'<li>{p}</li>' for p in punten)}</ul>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Zo gaat het</p><h2>In drie stappen aan de slag.</h2></div>
    <ol class="stappen">
      <li><h3>U belt Lorenzo</h3><p>Hij bekijkt met u welk profiel u nodig hebt, voor hoelang en waar.</p></li>
      <li><h3>Wij zetten de juiste {enk} in</h3><p>Met de nodige certificaten, materialen en uitrusting om zelfstandig te starten.</p></li>
      <li><h3>Onze teamleads volgen op</h3><p>Zodat de opdracht correct wordt uitgevoerd en 100% wordt afgewerkt.</p></li>
    </ol>
  </div>
</section>
''' + faq_blok(faq) + '</main>\n' + CTA)

FAQ_ELEK = [
  ('Werken jullie ook voor kortere opdrachten?', 'Ja. Onze focus ligt op langdurige samenwerkingen, waarbij een elektricien voor langere tijd bij dezelfde klant werkt, maar kortere technische opdrachten voeren we ook uit.'),
  ('Wie zorgt voor certificaten, materiaal en uitrusting?', 'Wij. Onze elektriciens komen met de nodige certificaten, materialen en uitrusting om hun opdracht zelfstandig en professioneel uit te voeren.'),
  ('In welke regio werken jullie?', 'Vanuit Meerhout in de Kempen. Onze techniekers werken op de locatie van de klant; bel Lorenzo om te bekijken of uw site binnen ons bereik ligt.'),
  ('Wie volgt de opdracht op?', 'Ervaren teamleads van BV Geert Vos. Zij zorgen dat de opdracht correct wordt opgevolgd en pas wordt afgesloten als ze 100% is afgewerkt.'),
  ('Zoeken jullie ook naar "elektrieker" of "elektrotechnieker"?', 'Zelfde vak, andere naam. Of u nu een elektrieker, elektrotechnieker of industrieel elektricien zoekt: bel Lorenzo en beschrijf het werk, dan zoeken we het juiste profiel.'),
]
FAQ_MECH = [
  ('Wat is het verschil met een onderhoudstechnieker?', 'Weinig. Onze mechaniciens doen mechanisch onderhoud, montage en herstellingen; velen noemen dat een onderhoudstechnieker of mecanicien. Beschrijf het werk, wij matchen het profiel.'),
  ('Kan een mechanicien langere tijd bij ons werken?', 'Dat is precies waar we ons op richten: een technieker die gedurende een langere periode bij dezelfde klant werkt en uw installaties leert kennen. Kortere opdrachten doen we er graag bij.'),
  ('Brengen jullie eigen gereedschap mee?', 'Ja. Onze mechaniciens beschikken over de nodige certificaten, materialen en uitrusting om zelfstandig te werken.'),
  ('Hoe zorgen jullie voor kwaliteit?', 'Orde, stiptheid en kwaliteit zijn onze belangrijkste waarden. Ervaren teamleads volgen elke opdracht op, en we laten de werkplek proper en ordelijk achter.'),
  ('Hoe start ik?', 'Bel Lorenzo. Hij bekijkt met u welk profiel u nodig hebt, voor hoelang en waar, en wanneer we kunnen starten.'),
]

pages['elektriciens'] = techniek_pagina('Elektriciens', 'elektricien',
  extra=schema('elektriciens', 'Elektriciens', ('Elektriciens', 'Elektriciens die voor langere periodes of een kortere opdracht bij uw bedrijf werken, met certificaten, materiaal en uitrusting.'), FAQ_ELEK),
  title='Elektricien inhuren in de Kempen | BV Geert Vos, Meerhout',
  desc='Ervaren elektriciens voor langere periodes bij uw bedrijf in de Kempen, of voor een kortere opdracht. Met certificaten, materiaal en uitrusting. Bel Lorenzo.',
  lead='Ervaren elektriciens die voor langere periodes bij uw bedrijf werken, of een kortere elektrische opdracht komen afwerken. Vanuit Meerhout, voor bedrijven in de Kempen en omstreken.',
  intro=('Een elektricien die uw site kent.', 'Bij onze technische dienstverlening stellen we elektriciens tewerk op de locatie van onze klanten. Ze werken er zelfstandig, met de certificaten, het materiaal en de uitrusting die hun opdracht vraagt.',
         'Elektrisch werk zit al sinds 1996 in ons DNA: het begon bij Nike met lampen vervangen en groeide uit tot het dagelijks beheer van verlichting, kabelmanagement en elektrische bureaus op een volledige site. Sinds 2024 zetten we die ervaring ook in bij andere bedrijven.',
         'Of u nu zoekt naar een elektricien, een elektrieker of een elektrotechnieker: u krijgt iemand die niet na een paar weken weer weg is, en die u niet elke keer opnieuw hoeft uit te leggen hoe uw gebouw in elkaar zit.'),
  werk=('Elektrisch werk op uw site, dag na dag.', 'Wat een elektricien van Geert Vos bij u doet, hangt af van uw site. Dit is het soort werk dat we al jaren dagelijks uitvoeren.', [
        ('Verlichting', 'Lampen en armaturen vervangen, verlichting onderhouden en aanpassen in kantoren, gangen en werkruimtes.'),
        ('Werkplekken en kabelmanagement', 'Werkplekken aansluiten, elektrische bureaus beheren, kabels netjes en veilig wegwerken.'),
        ('Onderhoud en storingen', 'Kleine herstellingen en onderhoud aan elektrische installaties, zodat alles blijft werken.'),
        ('Lichtmasten en straatverlichting', 'Mobiele lichtmasten verplaatsen en verhuizen, straatverlichting vervangen met de hoogwerker.')]),
  punten=['De nodige certificaten voor het werk dat u vraagt', 'Eigen materiaal en uitrusting, klaar om te starten', 'Zelfstandig werken, met opvolging door een ervaren teamlead', 'Een werkplek die proper en ordelijk achterblijft', 'Vriendelijk, flexibel en met een positieve ingesteldheid'],
  faq=FAQ_ELEK,
  fotosrc='/img/werk/werkstation-kabelmanagement-2.webp', foto1='Kabelmanagement aan een werkstation door Geert Vos', foto2='/img/werk/straatverlichting-hoogwerker-1.webp|Straatverlichting vervangen met de hoogwerker')

pages['mechaniciens'] = techniek_pagina('Mechaniciens', 'mechanicien',
  extra=schema('mechaniciens', 'Mechaniciens', ('Mechaniciens', 'Mechaniciens en onderhoudstechniekers die voor langere periodes of een kortere opdracht bij uw bedrijf werken, met certificaten, materiaal en uitrusting.'), FAQ_MECH),
  title='Mechanicien inhuren in de Kempen | BV Geert Vos, Meerhout',
  desc='Mechaniciens en onderhoudstechniekers voor langere periodes bij uw bedrijf in de Kempen, of een kortere opdracht. Zelfstandig, eigen materiaal. Bel Lorenzo.',
  lead='Mechaniciens die voor langere periodes bij uw bedrijf werken, of een kortere mechanische opdracht komen afwerken. Vanuit Meerhout, voor bedrijven in de Kempen en omstreken.',
  intro=('Mechanisch werk dat 100% wordt afgewerkt.', 'Onze mechaniciens werken op de locatie van onze klanten, zelfstandig en met de certificaten, het materiaal en de uitrusting die de opdracht vraagt.',
         'Mechanisch onderhoud doen we al bijna dertig jaar, elke dag: bureaustoelen en elektrische bureaus herstellen, meubilair in breakrooms en restaurants onderhouden, fietsen nakijken met een eigen fietsenmaker, verhuiswagens met laadlift inzetten. Handen die gewend zijn om dingen weer in orde te maken.',
         'Noem het een mechanicien, mecanicien of onderhoudstechnieker: u krijgt iemand die uw installaties leert kennen en die pas klaar is als het werk écht af is, met een propere werkplek achteraf.'),
  werk=('Onderhouden, monteren, herstellen.', 'Wat een mechanicien van Geert Vos bij u doet, hangt af van uw site. Dit is het soort werk dat we al jaren dagelijks uitvoeren.', [
        ('Mechanisch onderhoud', 'Periodiek onderhoud en kleine herstellingen aan installaties en uitrusting, voor ze een probleem worden.'),
        ('Montage en demontage', 'Meubilair, werkplekken en opstellingen opbouwen, verplaatsen en afbreken. Twee eigen verhuiswagens met laadlift.'),
        ('Storingen', 'Als iets vastloopt: kijken, herstellen, en zorgen dat het niet terugkomt.'),
        ('Fietsen en materieel', 'Beheer en onderhoud van een fietsenvloot door een echte fietsenmaker; beheer van magazijn en voorraad.')]),
  punten=['De nodige certificaten voor het werk dat u vraagt', 'Eigen gereedschap en uitrusting, klaar om te starten', 'Zelfstandig werken, met opvolging door een ervaren teamlead', 'Een werkplek die proper en ordelijk achterblijft', 'Vriendelijk, flexibel en met een positieve ingesteldheid'],
  faq=FAQ_MECH,
  fotosrc='/img/werk/lichtmast-verplaatsen-heftruck.webp', foto1='Lichtmast verplaatsen met de heftruck', foto2='/img/werk/lichtmasten-op-vrachtwagen.webp|Lichtmasten geladen op de vrachtwagen')

# ---------------------------------------------------------------- FACILITY (overzicht + 5 dienstpagina's)
DIENSTEN = [
  # slug, naam (kort, voor tegels/menu), h1, label
  ('verhuizingen', 'Verhuizingen &amp; interne logistiek', 'Verhuizingen en interne logistiek', 'Tak 1'),
  ('kabelmanagement', 'Kabelmanagement &amp; werkplekinrichting', 'Kabelmanagement en werkplekinrichting', 'Tak 2'),
  ('verlichting', 'Verlichting vervangen &amp; onderhouden', 'Verlichting vervangen en onderhouden', 'Tak 3'),
  ('fietsenbeheer', 'Fietsenbeheer &amp; -onderhoud', 'Fietsenbeheer en -onderhoud', 'Tak 4'),
  ('opslag', 'Opslag &amp; voorraadbeheer', 'Opslag en voorraadbeheer', 'Tak 5'),
]

def dienst_pagina(slug, naam, h1, label, title, desc, lead, intro, werk, punten, faq, fotosrc, alt, foto2, galerij=''):
    andere = ''.join(f'<li><a href="/{sl}/">{nm}</a></li>' for sl, nm, _, _ in DIENSTEN if sl != slug)
    return dict(title=title, desc=desc,
      extra=schema(slug, h1, (h1, desc), faq),
      body=kop(label + ' · Facility &amp; logistiek', h1, lead, f'<a href="/facility-diensten/">Facility</a> / {h1}') + f'''
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
      <p class="label">Wat u mag verwachten</p>
      <h2>Geregeld, en proper achtergelaten.</h2>
      <ul class="punten">{''.join(f'<li>{p}</li>' for p in punten)}</ul>
    </div>
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Zo gaat het</p><h2>Van vraag tot afgewerkte opdracht.</h2></div>
    <ol class="stappen">
      <li><h3>Opdracht komt binnen</h3><p>Via het ticketsysteem, een mail of een telefoontje naar Lorenzo. Hij bekijkt wat er nodig is en wanneer.</p></li>
      <li><h3>Team en materiaal ingepland</h3><p>Onze teamleads plannen de juiste mensen in, met het materiaal, de wagens en de uitrusting die de klus vraagt.</p></li>
      <li><h3>Uitgevoerd en afgewerkt</h3><p>Pas klaar als het 100% af is en de werkplek proper en ordelijk is. De teamlead volgt het op.</p></li>
    </ol>
  </div>
</section>
''' + faq_blok(faq) + f'''
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Ook van ons</p><h2>Onze andere facility-diensten.</h2></div>
    <ul class="andere">{andere}<li><a href="/elektriciens/">Elektriciens</a></li><li><a href="/mechaniciens/">Mechaniciens</a></li></ul>
  </div>
</section>
</main>
''' + CTA)

# --- 1 Verhuizingen
pages['verhuizingen'] = dienst_pagina('verhuizingen', DIENSTEN[0][1], DIENSTEN[0][2], DIENSTEN[0][3],
  title='Interne verhuizingen en logistiek | BV Geert Vos, Meerhout',
  desc='Interne verhuizingen, meetingopstellingen en logistiek voor bedrijven in de Kempen. Twee eigen verhuiswagens met laadlift. Al bijna 30 jaar dagelijks bij Nike.',
  lead='Afdelingen verhuizen, werkplekken verplaatsen, meetings en events opbouwen: interne verhuizingen en logistieke opdrachten zijn een groot deel van ons dagelijks werk.',
  intro=('Verhuizen zonder dat de rest stilvalt.', 'Een interne verhuizing lijkt klein tot je ze moet organiseren: bureaus, stoelen, kasten, schermen, dozen, en iedereen die de volgende ochtend gewoon wil kunnen werken. Wij doen dit al bijna dertig jaar, elke dag.',
         'Daarvoor beschikken we over twee eigen verhuiswagens met laadlift, zodat materiaal veilig en ergonomisch geladen en gelost wordt. Geen getil over drempels, geen beschadigde kasten, geen rugklachten.',
         'Ook meetings en evenementen zetten we klaar: tafels, stoelen, geluid en de grote mobiele schermen die de beamers van vroeger hebben vervangen. En na afloop ruimen we alles weer op.'),
  werk=('Van dozen tot complete afdelingen.', 'Wat we bij Nike dagelijks uitvoeren, doen we ook voor uw bedrijf.', [
        ('Interne verhuizingen', 'Werkplekken, afdelingen en meubilair verplaatsen binnen het gebouw of tussen gebouwen. Gepland rond uw werking, zodat niemand stilvalt.'),
        ('Twee verhuiswagens met laadlift', 'Eigen wagens, dus geen wachten op een externe transporteur. Veilig en ergonomisch laden en lossen.'),
        ('Meetings en evenementen', 'Opstellingen klaarzetten met tafels, stoelen, geluidsinstallatie en grote mobiele schermen. Na afloop weer afgebroken en opgeruimd.'),
        ('Logistieke ondersteuning', 'Materiaal ophalen, leveren, verdelen en terugbrengen. Ook lichtmasten en ander zwaar materieel verplaatsen we, met heftruck als het moet.')]),
  punten=['Twee eigen verhuiswagens met laadlift', 'Ervaren ploeg die dagelijks verhuist', 'Gepland rond uw werking, ook buiten de kantooruren als dat nodig is', 'Meubilair en materiaal veilig en zonder schade verplaatst', 'Alles weer proper en ordelijk achtergelaten'],
  faq=[
    ('Verhuizen jullie ook tussen twee gebouwen?', 'Ja. Met onze eigen verhuiswagens met laadlift verplaatsen we materiaal veilig tussen locaties, niet alleen binnen één gebouw.'),
    ('Kunnen jullie een meeting of event opbouwen?', 'Ja. Meetings en evenementen klaarzetten met tafels, stoelen, geluid en grote mobiele schermen doen we al sinds 1996, en na afloop ruimen we alles weer op.'),
    ('Hoe snel kunnen jullie een verhuizing inplannen?', 'Dat hangt af van de omvang. Bel Lorenzo, hij bekijkt met u wat er moet gebeuren en wanneer we de ploeg en de wagens kunnen inzetten.'),
    ('Wat als er iets beschadigd raakt?', 'Daarom werken we met laadliften, ervaren mensen en een teamlead die opvolgt. Een opdracht is voor ons pas klaar als ze 100% correct is afgewerkt.'),
  ],
  fotosrc='/img/foto/ph-verhuizingen.jpg', alt='Twee medewerkers van Geert Vos dragen een kast bij een interne verhuizing',
  foto2='/img/werk/lichtmasten-op-vrachtwagen.webp|Lichtmasten geladen op de vrachtwagen voor transport')

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
  desc='Werkplekken opbouwen en aanpassen, kabels netjes en veilig wegwerken, elektrische bureaus en meubilair beheren. Voor bedrijven in de Kempen, dagelijks bij Nike.',
  lead='Werkplekken opbouwen, verplaatsen en aanpassen, met kabels die netjes en veilig zijn weggewerkt. Plus het beheer van elektrische bureaus, stoelen en meubilair.',
  intro=('Een werkplek die werkt, en er ook zo uitziet.', 'Werkplekaanpassingen komen bij Nike dagelijks binnen via het ticketsysteem: een nieuwe collega, een team dat verhuist, een bureau dat anders moet staan. Wij bouwen op, sluiten aan en werken de kabels weg.',
         'We beheren en onderhouden er ook de elektrische bureaus, de bureaustoelen en een groot deel van het meubilair in breakrooms en restaurants. Kapot? Wij herstellen het. Versleten? Wij vervangen het.',
         'Kabelmanagement is geen cosmetica. Losse en geplette kabels raken beschadigd en leiden tot uitgebrande stekkers. Netjes weggewerkt is dus ook veilig weggewerkt.'),
  werk=('Van kabelgoot tot bureaustoel.', 'Alles wat een werkplek nodig heeft om te werken, elke dag opnieuw.', [
        ('Werkplekken opbouwen en aanpassen', 'Nieuwe werkplekken opbouwen, bestaande verplaatsen of aanpassen. Bureau, stoel, scherm, stroom en data: klaar om te gebruiken.'),
        ('Kabelmanagement', 'Kabels leiden, bundelen en vastzetten in goten en onder bureaus. Netjes, veilig en makkelijk aan te passen als er iets verandert.'),
        ('Elektrische bureaus en stoelen', 'Beheer, onderhoud en herstelling van elektrische zit-stabureaus en bureaustoelen.'),
        ('Meubilair breakrooms en restaurants', 'Tafels, stoelen en ander meubilair in gemeenschappelijke ruimtes onderhouden, herstellen en vervangen.')]),
  punten=['Werkplek klaar om te gebruiken, inclusief stroom en data', 'Kabels weggewerkt volgens de regels van de kunst', 'Herstelling van elektrische bureaus en stoelen in eigen beheer', 'Dagelijks bereikbaar via ticketsysteem of telefoon', 'Werkplek proper en ordelijk achtergelaten'],
  faq=[
    ('Doen jullie ook kleine aanpassingen, zoals één bureau verplaatsen?', 'Ja. Bij Nike komen zulke tickets dagelijks binnen. Klein of groot, we plannen het in.'),
    ('Herstellen jullie elektrische bureaus?', 'Ja, beheer en onderhoud van elektrische bureaus en bureaustoelen hoort bij ons dagelijks werk.'),
    ('Waarom is kabelmanagement belangrijk?', 'Losse of geplette kabels raken beschadigd en kunnen uitbranden. Netjes weggewerkte kabels zijn veiliger, gaan langer mee en zijn makkelijker aan te passen.'),
    ('Kunnen jullie een hele afdeling inrichten?', 'Ja. Samen met onze verhuisploeg en onze elektriciens richten we complete afdelingen in, van meubilair tot bekabeling.'),
  ],
  fotosrc='/img/werk/kabelgoot-kabelmanagement.webp', alt='Kabelgoot met netjes weggewerkte kabels aan een reeks werkstations',
  foto2='/img/werk/werkstation-kabelmanagement-2.webp|Afgewerkt kabelmanagement aan een werkstation', galerij=GAL_KABEL)

# --- 3 Verlichting
GAL_LICHT = '''<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Werk in beeld</p><h2>Van magazijn tot straat.</h2></div>
    <div class="galerij galerij-4">
      ''' + fig('/img/werk/magazijn-verlichting-hoogwerker-1.webp', 'Verlichting vervangen tussen magazijnstellingen met de hoogwerker') + fig('/img/werk/magazijn-verlichting-hoogwerker-2.webp', 'Verlichting vervangen in een magazijn') + fig('/img/werk/straatverlichting-hoogwerker-1.webp', 'Straatverlichting vervangen met de hoogwerker') + fig('/img/werk/lichtmast-verplaatsen-heftruck.webp', 'Mobiele lichtmast verplaatsen met de heftruck') + '''
    </div>
  </div>
</section>
'''
pages['verlichting'] = dienst_pagina('verlichting', DIENSTEN[2][1], DIENSTEN[2][2], DIENSTEN[2][3],
  title='Verlichting vervangen en onderhouden | BV Geert Vos, Meerhout',
  desc='Lampen en armaturen vervangen in kantoren en magazijnen, straatverlichting met de hoogwerker, lichtmasten verplaatsen. Voor bedrijven in de Kempen.',
  lead='Lampen vervangen was in 1996 een van onze allereerste opdrachten. Vandaag onderhouden we verlichting van kantoor tot magazijn en van parking tot straat.',
  intro=('Alles blijft branden.', 'Een defecte lamp lijkt een detail, tot het er tien zijn in een magazijngang of op een parking. Wij vervangen en onderhouden verlichting zodat u er niet aan hoeft te denken.',
         'In kantoren, gangen en werkruimtes doen we dat vanop de ladder. In magazijnen met hoge stellingen en buiten aan straatverlichting werken we met de hoogwerker. Mobiele lichtmasten verplaatsen en verhuizen we met de heftruck en onze eigen wagens.',
         'Het werk gebeurt door onze eigen elektriciens, met de certificaten en de uitrusting die erbij horen. Gepland als onderhoud, of snel als er iets uitvalt.'),
  werk=('Binnen, buiten en in de hoogte.', 'Verlichting in al zijn vormen, uitgevoerd door onze eigen elektriciens.', [
        ('Kantoren en werkruimtes', 'Lampen en armaturen vervangen en onderhouden in kantoren, gangen, breakrooms en werkplaatsen.'),
        ('Magazijnen', 'Verlichting vervangen tussen en boven hoge stellingen, met de hoogwerker. Veilig en zonder het magazijn stil te leggen.'),
        ('Straat- en buitenverlichting', 'Straatverlichting en parkingverlichting vervangen met de hoogwerker.'),
        ('Lichtmasten', 'Mobiele lichtmasten verplaatsen, verhuizen en opstellen, met heftruck en eigen wagens.')]),
  punten=['Eigen elektriciens met de nodige certificaten', 'Hoogwerker voor magazijnen en buitenverlichting', 'Geplande onderhoudsrondes of snel bij uitval', 'Lichtmasten verplaatst met eigen materieel', 'Werkplek proper achtergelaten, oude lampen afgevoerd'],
  faq=[
    ('Vervangen jullie ook verlichting op grote hoogte?', 'Ja. Voor magazijnen met hoge stellingen en voor straatverlichting werken we met de hoogwerker.'),
    ('Kunnen jullie een onderhoudsronde inplannen?', 'Ja. Veel klanten laten ons de verlichting periodiek nakijken en vervangen, zodat er minder uitval is tussendoor.'),
    ('Wie voert het werk uit?', 'Onze eigen elektriciens, met de certificaten, het materiaal en de uitrusting die erbij horen.'),
    ('Verplaatsen jullie ook lichtmasten?', 'Ja. Mobiele lichtmasten verplaatsen en verhuizen we met de heftruck en onze eigen wagens.'),
  ],
  fotosrc='/img/werk/magazijn-verlichting-hoogwerker-2.webp', alt='Verlichting vervangen in een magazijn met de hoogwerker',
  foto2='/img/werk/straatverlichting-hoogwerker-2.webp|Straatverlichting vervangen met de hoogwerker', galerij=GAL_LICHT)

# --- 4 Fietsenbeheer
pages['fietsenbeheer'] = dienst_pagina('fietsenbeheer', DIENSTEN[3][1], DIENSTEN[3][2], DIENSTEN[3][3],
  title='Fietsenbeheer en fietsonderhoud voor bedrijven | BV Geert Vos',
  desc='Beheer en onderhoud van bedrijfsfietsen door een echte fietsenmaker in dienst. Herstellingen, nazicht en beheer van de vloot, voor bedrijven in de Kempen.',
  lead='Een bedrijf met veel fietsen heeft veel onderhoud. Wij hebben daarvoor een echte fietsenmaker in dienst.',
  intro=('Een fietsenmaker op uw site.', 'Bedrijfsfietsen, dienstfietsen, fietsen om over een grote site te rijden: ze worden intensief gebruikt en moeten het blijven doen. Daarom hebben we een echte fietsenmaker in dienst, geen collega die het er even bij doet.',
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
  fotosrc='/img/foto/ph-fietsen.jpg', alt='Rij bedrijfsfietsen in beheer bij Geert Vos',
  foto2='Foto volgt: onze fietsenmaker aan het werk')

# --- 5 Opslag
pages['opslag'] = dienst_pagina('opslag', DIENSTEN[4][1], DIENSTEN[4][2], DIENSTEN[4][3],
  title='Opslag en voorraadbeheer, 300 palletplaatsen | BV Geert Vos',
  desc='Opslagruimte met ongeveer 300 palletplaatsen en een digitale inventaris die dagelijks wordt bijgewerkt. Opslag en voorraadbeheer voor bedrijven in de Kempen.',
  lead='Ongeveer 300 palletplaatsen en een digitale inventaris die elke dag wordt bijgewerkt. U weet altijd wat er ligt en waar.',
  intro=('Wat u niet dagelijks nodig hebt, ligt bij ons klaar.', 'Meubilair dat tijdelijk weg moet, materiaal voor events, reserveonderdelen, seizoensmateriaal: het moet ergens naartoe, en het moet terug te vinden zijn als u het nodig hebt.',
         'Wij beschikken over een opslagruimte met ongeveer 300 palletplaatsen. Alles wat binnenkomt, wordt geregistreerd in een digitale inventaris die dagelijks wordt bijgewerkt. Geen zoekwerk, geen dubbele aankopen.',
         'Onze fietsenmaker staat mee in voor het beheer van het magazijn, en onze verhuiswagens met laadlift brengen en halen wat u nodig hebt.'),
  werk=('Opslaan, bijhouden, leveren.', 'Meer dan een loods: een voorraad die beheerd wordt.', [
        ('300 palletplaatsen', 'Droge, geordende opslag voor meubilair, materiaal en reserveonderdelen.'),
        ('Digitale inventaris', 'Elke pallet en elk stuk geregistreerd, dagelijks bijgewerkt. U weet wat er ligt zonder te gaan kijken.'),
        ('In- en uitslag', 'Materiaal ophalen, opslaan en terugbrengen met onze eigen verhuiswagens met laadlift.'),
        ('Beheer door een vast aanspreekpunt', 'Eén persoon die het magazijn kent en weet waar alles ligt.')]),
  punten=['Ongeveer 300 palletplaatsen', 'Digitale inventaris, dagelijks bijgewerkt', 'Transport met eigen verhuiswagens', 'Vast aanspreekpunt voor het magazijn', 'Combineerbaar met verhuizingen en werkplekinrichting'],
  faq=[
    ('Hoeveel opslagruimte hebben jullie?', 'Ongeveer 300 palletplaatsen.'),
    ('Hoe weet ik wat er van mij ligt?', 'Alles wordt bijgehouden in een digitale inventaris die dagelijks wordt bijgewerkt. Vraag het aan ons vast aanspreekpunt en u krijgt het overzicht.'),
    ('Halen en brengen jullie ook?', 'Ja, met onze eigen verhuiswagens met laadlift.'),
    ('Kunnen jullie tijdelijke opslag doen tijdens een verhuizing?', 'Ja. Dat combineren we vaak: meubilair tijdelijk bij ons, en terug op zijn plaats als de nieuwe ruimte klaar is.'),
  ],
  fotosrc='/img/werk/magazijn-verlichting-hoogwerker-1.webp', alt='Magazijnstellingen met pallets',
  foto2='Foto volgt: ons eigen magazijn met palletplaatsen')

# --- overzicht
FAQ_FAC = [
  ('Doen jullie ook kleine klussen?', 'Ja. Het begon in 1996 met een deurklink. Van een kleine herstelling tot een volledige interne verhuizing: we plannen het in.'),
  ('Hoe komen opdrachten bij jullie binnen?', 'Bij Nike via een online ticketsysteem waarin dagelijks opdrachten binnenkomen; onze medewerkers en teamleads plannen en voeren ze uit. Voor andere klanten spreken we af wat het beste werkt.'),
  ('Kunnen jullie meerdere diensten combineren?', 'Dat is net onze sterkte: één team dat verhuist, werkplekken inricht, verlichting vervangt, fietsen onderhoudt en het magazijn beheert. Eén aanspreekpunt, Lorenzo.'),
  ('Werken jullie ook buiten Nike?', 'Ja. Sinds 2024 zetten we onze ervaring ook in bij andere bedrijven in de Kempen en omstreken.'),
]
FAC_TEGELS = [
  ('verhuizingen', '/img/foto/ph-verhuizingen.jpg', 'Twee eigen verhuiswagens met laadlift, meetings en events.'),
  ('kabelmanagement', '/img/werk/kabelgoot-kabelmanagement.webp', 'Werkplekken opbouwen, kabels wegwerken, bureaus en stoelen beheren.'),
  ('verlichting', '/img/werk/magazijn-verlichting-hoogwerker-2.webp', 'Van kantoor tot magazijn en straat, met de hoogwerker.'),
  ('fietsenbeheer', '/img/foto/ph-fietsen.jpg', 'Met een echte fietsenmaker in dienst.'),
  ('opslag', '/img/werk/magazijn-verlichting-hoogwerker-1.webp', '300 palletplaatsen en een digitale inventaris.'),
]
pages['facility-diensten'] = dict(
  extra=schema('facility-diensten', 'Facility', ('Facility en logistiek', 'Interne verhuizingen, kabelmanagement en werkplekinrichting, verlichting, fietsenbeheer en opslag met 300 palletplaatsen.'), FAQ_FAC),
  title='Facility en logistiek in de Kempen | BV Geert Vos, Meerhout',
  desc='Interne verhuizingen, kabelmanagement en werkplekinrichting, verlichting, fietsenbeheer en opslag met 300 palletplaatsen. Al bijna 30 jaar elke dag bij Nike.',
  body=kop('Facility &amp; logistiek', 'Facility en logistiek', 'Vijf facility- en logistieke diensten die we bij Nike al bijna dertig jaar elke dag uitvoeren, via een online ticketsysteem waarin dagelijks opdrachten binnenkomen. Ook voor uw bedrijf in de Kempen.', 'Facility') + f'''
<main id="inhoud">
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Vijf takken, één team</p><h2>Alles wat een site elke dag nodig heeft.</h2><p class="lead">Elke dienst heeft een eigen pagina met wat we precies doen, foto's en veelgestelde vragen.</p></div>
    <ul class="takken">
      {''.join(f'<li><a href="/{sl}/"><div class="tegel"><img src="{src}" alt="" loading="lazy" width="440" height="550"></div><h3>{nm}</h3><p>{tx}</p></a></li>' for (sl, src, tx), (_, nm, _, _) in zip(FAC_TEGELS, DIENSTEN))}
    </ul>
  </div>
</section>
<section class="sec-paper">
  <div class="wrap twee">
    <div>
      <p class="label">Werking</p>
      <h2>Elke dag een ticket, elke dag geregeld.</h2>
      <p class="lead" style="margin-top:16px">Bij Nike werken we met een online ticketsysteem waarin dagelijks opdrachten binnenkomen. Onze medewerkers en teamleads zorgen voor de planning en de uitvoering.</p>
      <p style="margin-top:16px">Die opdrachten zijn zeer uiteenlopend: van werkplekaanpassingen, kabelmanagement en verlichting tot verhuizingen, meetingopstellingen, fietsenbeheer, meubilair en logistieke ondersteuning. Eén team dat alles kent, één aanspreekpunt voor u.</p>
      <p>Dat we hier na bijna dertig jaar nog steeds dagelijks met een volledig team actief zijn, zegt volgens ons veel over de samenwerking en het vertrouwen dat doorheen de jaren is opgebouwd.</p>
    </div>
    {foto('/img/foto/ph-verhuizingen.jpg', 'Medewerkers van Geert Vos aan het werk', 'foto-hoog')}
  </div>
</section>
''' + faq_blok(FAQ_FAC) + '</main>\n' + CTA)

# ---------------------------------------------------------------- DIENSTEN (overzicht)
pages['diensten'] = dict(
  extra=schema('diensten', 'Diensten'),
  title='Onze diensten: techniek en facility | BV Geert Vos, Meerhout',
  desc='Elektriciens en mechaniciens voor langere tijd bij uw bedrijf, plus verhuizingen, werkplekinrichting, verlichting, fietsenbeheer en opslag. Alle diensten van BV Geert Vos.',
  body=kop('Alles op een rij', 'Onze diensten', 'Twee technische pijlers en vijf facility-takken, met één aanspreekpunt.', 'Diensten') + f'''
<main id="inhoud">
<section>
  <div class="wrap">
    <div class="sec-kop"><p class="label">Techniek</p><h2>Techniekers die blijven.</h2><p class="lead">Sinds 2024 stellen we elektriciens en mechaniciens tewerk bij andere bedrijven in de Kempen. Zelfstandig, met certificaten, materiaal en uitrusting, en bij voorkeur voor lange tijd bij dezelfde klant.</p></div>
    <div class="pijlers">
      <a class="pijler" href="/elektriciens/">
        <img src="/img/werk/werkstation-kabelmanagement-1.webp" alt="" loading="lazy" width="440" height="591">
        <div class="in"><p class="label">Pijler 1</p><h3>Elektriciens</h3><p>Voor langdurige samenwerkingen op uw locatie, of voor een kortere elektrische opdracht.</p><span class="meer">Meer over onze elektriciens</span></div>
      </a>
      <a class="pijler" href="/mechaniciens/">
        <img src="/img/werk/lichtmast-verplaatsen-heftruck.webp" alt="" loading="lazy" width="347" height="557">
        <div class="in"><p class="label">Pijler 2</p><h3>Mechaniciens</h3><p>Mechanisch onderhoud, montage en herstellingen, 100% afgewerkt.</p><span class="meer">Meer over onze mechaniciens</span></div>
      </a>
    </div>
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Facility &amp; logistiek</p><h2>Wat we al bijna dertig jaar elke dag doen.</h2><p class="lead">Vijf takken, één team. <a href="/facility-diensten/">Lees hoe onze facility-werking in elkaar zit</a>, of ga meteen naar een dienst.</p></div>
    <ul class="takken">
      {''.join(f'<li><a href="/{sl}/"><div class="tegel"><img src="{src}" alt="" loading="lazy" width="440" height="550"></div><h3>{nm}</h3><p>{tx}</p></a></li>' for (sl, src, tx), (_, nm, _, _) in zip(FAC_TEGELS, DIENSTEN))}
    </ul>
  </div>
</section>
''' + faq_blok(FAQ_FAC) + '</main>\n' + CTA)

# ---------------------------------------------------------------- ONS VERHAAL
pages['ons-verhaal'] = dict(
  extra=schema('ons-verhaal', 'Ons verhaal'),
  title='Ons verhaal: sinds 1996 bij Nike | BV Geert Vos, Meerhout',
  desc='Begonnen in 1996 met een deur en een deurklink bij Nike. Vandaag elke dag een volledig team ter plaatse, sinds 2024 ook elektriciens en mechaniciens elders.',
  body=kop('Sinds 1996', 'Ons verhaal', 'Het begon ongeveer dertig jaar geleden met een kleine opdracht. Vandaag is het een samenwerking die nog altijd bestaat, en een tweede pijler die groeit.', 'Ons verhaal') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee">
    <div>
      <h2>1996: een deur en een deurklink.</h2>
      <p class="lead" style="margin-top:16px">Geert Vos begon in 1996 als contractor bij Nike. Wat begon met het herstellen van een deur en een deurklink, groeide stap voor stap uit tot een samenwerking die vandaag nog steeds bestaat.</p>
      <p style="margin-top:16px">In het begin ging het onder andere om het vervangen van lampen en het klaarzetten van meetings met tafels, stoelen, beamers en geluidsinstallaties. Doorheen de jaren kregen we steeds meer verantwoordelijkheden, en groeide zowel het takenpakket als ons team.</p>
      <p>Vandaag beheren en onderhouden we onder andere elektrische bureaus, bureaustoelen en een groot deel van het meubilair in breakrooms en restaurants. We ondersteunen nog steeds meetings en evenementen. De vroegere beamers hebben ondertussen plaatsgemaakt voor grote mobiele schermen.</p>
    </div>
    {foto('/img/foto/ph-verhuizingen.jpg', 'Medewerkers van Geert Vos aan het werk', 'foto-hoog')}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap twee">
    <ol class="tijd">
      <li><time>1996</time><p>Geert Vos start als contractor bij Nike. Eerste opdracht: een deur en een deurklink.</p></li>
      <li><time>De jaren erna</time><p>Lampen vervangen, meetings klaarzetten. Meer verantwoordelijkheden, een groter team.</p></li>
      <li><time>Vandaag</time><p>Elke dag een volledig team bij Nike: meubilair, verhuizingen, fietsen, opslag, events. Twee eigen verhuiswagens, 300 palletplaatsen, een fietsenmaker in dienst.</p></li>
      <li><time>2024</time><p>Elektriciens en mechaniciens worden ook bij andere klanten tewerkgesteld. De tweede pijler van BV Geert Vos.</p></li>
    </ol>
    <div>
      <p class="label">Werking bij Nike</p>
      <h2>Elke dag een ticket, elke dag geregeld.</h2>
      <p class="lead" style="margin-top:16px">Bij Nike werken we met een online ticketsysteem waarin dagelijks opdrachten binnenkomen. Onze medewerkers en teamleads zorgen voor de planning en de uitvoering.</p>
      <p style="margin-top:16px">Die opdrachten zijn zeer uiteenlopend: van werkplekaanpassingen, kabelmanagement en verlichting tot verhuizingen, meetingopstellingen, fietsenbeheer, meubilair en logistieke ondersteuning.</p>
      <p>Dat we hier na bijna dertig jaar nog steeds dagelijks met een volledig team actief zijn, zegt volgens ons veel over de samenwerking en het vertrouwen dat doorheen de jaren is opgebouwd.</p>
    </div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-kop">
      <p class="label">Wie wij zijn</p>
      <h2>Een jong en hecht team.</h2>
      <p class="lead">Veel collega's komen ook buiten het werk goed met elkaar overeen. Tegelijk werken we binnen een duidelijke organisatie, met ervaren teamleads die ervoor zorgen dat opdrachten correct worden opgevolgd.</p>
    </div>
    <div class="waarden">
      <div><h3>Orde, stiptheid, kwaliteit</h3><p>Onze belangrijkste waarden. Een opdracht is pas klaar wanneer ze 100% afgewerkt is.</p></div>
      <div><h3>Proper achterlaten</h3><p>Minstens even belangrijk: we laten onze werkplek na afloop proper en ordelijk achter.</p></div>
      <div><h3>Vriendelijk, flexibel, positief</h3><p>Onze manier van werken. Daardoor vertrouwen klanten ons, en groeien samenwerkingen uit tot vele jaren.</p></div>
    </div>
    <div class="drie" style="margin-top:56px">
      {ph('Foto volgt: het team')}
      {ph('Foto volgt: bestelwagens en verhuiswagens')}
      {ph('Foto volgt: het magazijn')}
    </div>
  </div>
</section>
</main>
''' + CTA)


# ---------------------------------------------------------------- WERKEN BIJ
pages['werken-bij'] = dict(
  extra=schema('werken-bij', 'Werken bij'),
  title='Werken bij Geert Vos: elektricien, mechanicien, facility | Meerhout',
  desc='Elektricien, mechanicien of facility-medewerker in de Kempen? BV Geert Vos zoekt techniekers voor langdurige opdrachten bij vaste klanten. Solliciteer spontaan.',
  body=kop('Werken bij', 'Werken bij Geert Vos', 'Een jong en hecht team, vaste klanten, en werk dat pas klaar is als het 100% af is. Elektricien, mechanicien of facility-medewerker in de Kempen? Laat van u horen.', 'Werken bij') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee">
    <div>
      <h2>Vast werk bij vaste klanten.</h2>
      <p class="lead" style="margin-top:16px">Onze techniekers werken gedurende langere periodes bij dezelfde klant. Geen andere werf elke week, wel een site die u leert kennen en collega's die u kent.</p>
      <p style="margin-top:16px">We zijn een jong en hecht team, waarin veel collega's ook buiten het werk goed met elkaar overeenkomen. Tegelijk werken we binnen een duidelijke organisatie, met ervaren teamleads die u niet in de steek laten. Orde, stiptheid en kwaliteit zijn belangrijk voor ons, en een vriendelijke, positieve ingesteldheid ook.</p>
      <p>Sinds 1996 zijn we dagelijks actief bij Nike, met een volledig team. Sinds 2024 groeit onze tweede pijler: elektriciens en mechaniciens bij andere bedrijven in de Kempen.</p>
    </div>
    {foto('/img/foto/ph-verhuizingen.jpg', 'Twee medewerkers van Geert Vos aan het werk', 'foto-hoog')}
  </div>
</section>
<section class="sec-paper">
  <div class="wrap">
    <div class="sec-kop"><p class="label">Wie we zoeken</p><h2>Profielen waar we altijd naar uitkijken.</h2></div>
    <div class="waarden">
      <div><h3>Elektricien</h3><p>Elektrieker of elektrotechnieker met de nodige certificaten, die zelfstandig kan werken en graag voor langere tijd op één site staat.</p></div>
      <div><h3>Mechanicien</h3><p>Onderhoudstechnieker of mecanicien die kan monteren, herstellen en onderhouden, en die pas stopt als het écht af is.</p></div>
      <div><h3>Facility-medewerker</h3><p>Handige alleskunner voor verhuizingen, werkplekinrichting, verlichting, fietsen en magazijn. Rijbewijs is een plus (eigen verhuiswagens).</p></div>
    </div>
  </div>
</section>
<section>
  <div class="wrap twee" style="align-items:start">
    <div>
      <p class="label">Solliciteren</p>
      <h2>Laat van u horen.</h2>
      <p class="lead" style="margin-top:16px">Geen vacature die past? Solliciteer spontaan. We antwoorden persoonlijk.</p>
      <p style="margin-top:16px">Liever bellen? Lorenzo: <a class="tel" href="tel:{TEL_LORENZO}">{TEL_LORENZO_TXT}</a></p>
    </div>
    <form data-gv action="https://formsubmit.co/{MAIL}" method="POST">
      <input type="hidden" name="_subject" value="Sollicitatie via geertvos.be">
      <input type="hidden" name="_template" value="table">
      <input type="hidden" name="_next" value="https://geertvos.be/bedankt/">
      <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off">
      <div class="veld-2">
        <div class="veld"><label for="s-naam">Naam</label><input id="s-naam" name="Naam" required autocomplete="name"></div>
        <div class="veld"><label for="s-tel">Telefoon</label><input id="s-tel" type="tel" name="Telefoon" required autocomplete="tel"></div>
      </div>
      <div class="veld"><label for="s-email">E-mail</label><input id="s-email" type="email" name="E-mail" required autocomplete="email"></div>
      <div class="veld"><label for="s-functie">Functie</label>
        <select id="s-functie" name="Functie"><option>Elektricien</option><option>Mechanicien</option><option>Facility-medewerker</option><option>Iets anders</option></select></div>
      <div class="veld"><label for="s-bericht">Vertel kort iets over uzelf</label><textarea id="s-bericht" name="Bericht" required placeholder="Ervaring, certificaten, vanaf wanneer u beschikbaar bent"></textarea></div>
      <div><button class="btn btn-geel" type="submit">Verstuur sollicitatie</button></div>
      <p class="form-noot">We gebruiken uw gegevens alleen voor deze sollicitatie. Zie ons <a href="/privacybeleid/">privacybeleid</a>.</p>
    </form>
  </div>
</section>
</main>
''' + CTA)

# ---------------------------------------------------------------- CONTACT
pages['contact'] = dict(
  extra=schema('contact', 'Contact'),
  title='Contact | BV Geert Vos, Meerhout',
  desc='Neem contact op met BV Geert Vos, Bevrijdingslaan 256 in Meerhout. Bel ons of stuur een bericht via het formulier. We antwoorden snel.',
  body=kop('Neem contact op', 'Contact', 'Bel ons, of stuur een bericht, dan nemen we contact met u op.', 'Contact') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee" style="align-items:start">
    <div>
      <div class="bel-kaart">
        <strong>Bel ons</strong>
        <p class="rol">We zijn bereikbaar op</p>
        <a class="tel" href="tel:{TEL_LORENZO}">{TEL_LORENZO_TXT}</a>
        <a class="tel" href="tel:{TEL_PJ}">{TEL_PJ_TXT}</a>
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
            <option>Elektriciens</option><option>Mechaniciens</option><option>Verhuizingen en interne logistiek</option><option>Kabelmanagement en werkplekinrichting</option><option>Verlichting</option><option>Fietsenbeheer</option><option>Opslag en voorraadbeheer</option><option>Iets anders</option>
          </select></div>
        <div class="veld"><label for="bericht">Bericht</label><textarea id="bericht" name="Bericht" required></textarea></div>
        <div><button class="btn btn-geel" type="submit">Verstuur bericht</button></div>
        <p class="form-noot">We gebruiken uw gegevens alleen om te antwoorden. Zie ons <a href="/privacybeleid/">privacybeleid</a>.</p>
      </form>
    </div>
  </div>
</section>
</main>
''')

pages['bedankt'] = dict(
  title='Bedankt voor uw bericht | BV Geert Vos',
  desc='Uw bericht is verstuurd. We nemen zo snel mogelijk contact met u op.',
  extra='<meta name="robots" content="noindex">',
  body=kop('Contact', 'Bedankt', 'Uw bericht is aangekomen. We nemen zo snel mogelijk contact met u op.', 'Contact') + f'''
<main id="inhoud"><section><div class="wrap"><p class="lead">Dringend? Bel ons op <a class="tel" href="tel:{TEL_LORENZO}">{TEL_LORENZO_TXT}</a> of <a class="tel" href="tel:{TEL_PJ}">{TEL_PJ_TXT}</a>.</p><p style="margin-top:24px"><a class="btn btn-ink" href="/">Terug naar de startpagina</a></p></div></section></main>
''')

pages['404'] = dict(
  title='Pagina niet gevonden | BV Geert Vos',
  desc='Deze pagina bestaat niet (meer).',
  extra='<meta name="robots" content="noindex">',
  body=kop('Fout 404', 'Niet gevonden', 'Deze pagina bestaat niet of is verhuisd. Misschien zoekt u een van onze diensten?', 'Niet gevonden') + f'''
<main id="inhoud"><section><div class="wrap"><p class="lead"><a href="/elektriciens/">Elektriciens</a> · <a href="/mechaniciens/">Mechaniciens</a> · <a href="/facility-diensten/">Facility en logistiek</a> · <a href="/contact/">Contact</a></p><p style="margin-top:24px"><a class="btn btn-ink" href="/">Naar de startpagina</a></p></div></section></main>
''')

# ---------------------------------------------------------------- PRIVACY
pages['privacybeleid'] = dict(
  title='Privacybeleid | BV Geert Vos',
  desc='Hoe BV Geert Vos omgaat met uw persoonsgegevens op geertvos.be.',
  body=kop('Juridisch', 'Privacybeleid', 'Kort en zonder kleine lettertjes: welke gegevens we verwerken, waarom, en hoelang.', 'Privacybeleid') + f'''
<main id="inhoud"><section><div class="wrap prose">
<p>BV Geert Vos, Bevrijdingslaan 256, 2450 Meerhout (BTW BE 0862.515.981) is verantwoordelijk voor de verwerking van persoonsgegevens op deze website. Vragen? Mail naar <a href="mailto:{MAIL}">{MAIL}</a>.</p>
<h2>Contact- en sollicitatieformulier</h2>
<p>Als u een formulier invult, verwerken we uw naam, e-mailadres, en wat u verder invult (bedrijf, telefoonnummer, bericht). We gebruiken die gegevens alleen om uw vraag te beantwoorden en bewaren ze zolang dat nodig is voor de opvolging. Het formulier wordt technisch verzonden via FormSubmit, die het bericht als e-mail aan ons bezorgt.</p>
<h2>Cookies</h2>
<p>Deze website gebruikt geen cookies, geen tracking en geen analysediensten van derden. De lettertypes worden vanaf onze eigen server geladen.</p>
<h2>Uw rechten</h2>
<p>U hebt het recht om uw gegevens in te kijken, te laten verbeteren of te laten verwijderen. Stuur daarvoor een mail naar <a href="mailto:{MAIL}">{MAIL}</a>. U kunt ook een klacht indienen bij de Gegevensbeschermingsautoriteit (gegevensbeschermingsautoriteit.be).</p>
<p class="grijs" style="margin-top:32px">Laatst bijgewerkt: september 2026.</p>
</div></section></main>
''')

# ---------------------------------------------------------------- schrijven
bulb = open(os.path.join(OUT, 'img', 'bulb.svg')).read()
for slug, p in pages.items():
    html = head(p['title'], p['desc'], slug, p.get('extra', '')) + header(slug) + p['body'].replace('BULBSVG', bulb) + FOOT
    open(os.path.join(OUT, f'{slug}.html'), 'w').write(html)
    print(slug, len(html))

urls = ['', 'diensten/', 'elektriciens/', 'mechaniciens/', 'facility-diensten/', 'verhuizingen/', 'kabelmanagement/', 'verlichting/', 'fietsenbeheer/', 'opslag/', 'ons-verhaal/', 'werken-bij/', 'contact/', 'privacybeleid/']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
