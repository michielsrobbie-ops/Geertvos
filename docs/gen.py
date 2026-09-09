# Genereert de statische pagina's van geertvos.be (header/footer één keer gedefinieerd).
# Draaien vanuit docs/: python3 gen.py  → schrijft de html-bestanden in de projectmap.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'site') if os.path.isdir(os.path.join(HERE, 'site')) else os.path.dirname(HERE)
DOMAIN = 'https://geertvos.be'
V = '20260909'          # versie voor css/js — ophogen bij elke wijziging
TEL_LORENZO = ''        # TODO: nummer Lorenzo (formaat +32470123456)
TEL_PJ = ''             # TODO: nummer Pieter-Jan
TEL_LORENZO_TXT = '[nummer Lorenzo]'
TEL_PJ_TXT = '[nummer Pieter-Jan]'
MAIL = 'info@geertvos.be'   # TODO: bevestigen bij klant

NAV = [('elektriciens', 'Elektriciens'), ('mechaniciens', 'Mechaniciens'),
       ('facility-diensten', 'Facility'), ('ons-verhaal', 'Ons verhaal'), ('werken-bij', 'Werken bij')]


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

def header(slug):
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="/{s}/"{cur if s == slug else ""}>{t}</a>' for s, t in NAV)
    return f'''<header class="site-head">
  <div class="wrap">
    <a class="brand" href="/" aria-label="BV Geert Vos, naar de startpagina"><img src="/img/logo-nav.svg" alt="BV Geert Vos" width="236" height="64"></a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="menu"><span></span>Menu</button>
    <nav class="nav" id="menu" aria-label="Hoofdmenu">{links}<a class="nav-cta" href="/contact/">Contact</a></nav>
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

ICO_FLEX = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>'
ICO_BETR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12l4-4h4l3 3-3 3-2-2"/><path d="M21 12l-4-4h-3"/><path d="M7 16l2 2h2l2-2"/><path d="M11 18l2 2h2l3-3"/></svg>'
ICO_OPL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="4"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3"/></svg>'

BALK = f'''<div class="balk">
  <div class="wrap">
    <ul>
      <li>{ICO_FLEX}Flexibel.</li>
      <li>{ICO_BETR}Betrouwbaar.</li>
      <li>{ICO_OPL}Oplossingsgericht.</li>
    </ul>
    <p class="hand">Wij regelen het, zodat u zich kunt focussen op wat <em>écht belangrijk</em> is.</p>
  </div>
</div>
'''

CTA = f'''<div class="cta-band">
  <div class="wrap">
    <div>
      <p class="label">Van kleine klussen tot complete projecten</p>
      <h2>Wij regelen het.</h2>
      <p>Bel Lorenzo. Hij bekijkt samen met u wat u nodig hebt en wanneer we kunnen starten.</p>
    </div>
    <div class="knoppen">
      <a class="btn btn-geel" href="tel:{TEL_LORENZO}">Bel Lorenzo</a>
      <a class="btn btn-licht" href="/contact/">Stuur een bericht</a>
    </div>
  </div>
</div>
'''

FOOT = f'''<footer class="site-foot">
  <div class="wrap">
    <div>
      <img src="/img/logo-nav.svg" alt="BV Geert Vos" width="258" height="70">
      <p>Uw partner in techniek en facility management. Sinds 1996 dagelijks aan het werk bij Nike, sinds 2024 ook bij andere bedrijven.</p>
    </div>
    <div>
      <p class="foot-kop">Diensten</p>
      <ul>
        <li><a href="/elektriciens/">Elektriciens</a></li>
        <li><a href="/mechaniciens/">Mechaniciens</a></li>
        <li><a href="/facility-diensten/#verhuizingen">Verhuizingen en logistiek</a></li>
        <li><a href="/facility-diensten/#kabelmanagement">Kabelmanagement en werkplekken</a></li>
        <li><a href="/facility-diensten/#verlichting">Verlichting</a></li>
        <li><a href="/facility-diensten/#fietsen">Fietsenbeheer</a></li>
        <li><a href="/facility-diensten/#opslag">Opslag en voorraad</a></li>
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
      <a href="tel:{TEL_LORENZO}">Lorenzo: {TEL_LORENZO_TXT}</a><br>
      <a href="tel:{TEL_PJ}">Pieter-Jan: {TEL_PJ_TXT}</a><br>
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

def ph(tekst, cls=''):
    return f'<div class="foto foto-ph {cls}"><span>{tekst}</span></div>'

def foto(src, alt, cls=''):
    return f'<div class="foto {cls}"><img src="{src}" alt="{alt}" loading="lazy" width="460" height="520"></div>'

# Tegels in de hero: (href, label, foto, alt) — foto's zijn nu lage-resolutie uitsneden uit de banner
TEGELS = [
  ('/elektriciens/', 'Elektriciens', '/img/foto/ph-elektricien.jpg', 'Elektricien aan een schakelkast'),
  ('/mechaniciens/', 'Mechaniciens', '', 'Mechanicien aan het werk'),
  ('/facility-diensten/#verhuizingen', 'Verhuizingen &amp; logistiek', '/img/foto/ph-verhuizingen.jpg', 'Twee medewerkers van Geert Vos bij een interne verhuizing'),
  ('/facility-diensten/#kabelmanagement', 'Kabelmanagement &amp; werkplekken', '/img/foto/ph-werkplek.jpg', 'Ingerichte kantoorwerkplekken'),
  ('/facility-diensten/#verlichting', 'Verlichting', '/img/foto/ph-verlichting.jpg', 'Technieker vervangt een inbouwspot'),
  ('/facility-diensten/#fietsen', 'Fietsen beheren &amp; onderhouden', '/img/foto/ph-fietsen.jpg', 'Rij bedrijfsfietsen'),
  ('/facility-diensten/#opslag', 'Opslag &amp; voorraad', '', 'Magazijn met palletplaatsen'),
]
def tegel_img(src, alt):
    if src:
        return f'<img src="{src}" alt="{alt}" loading="lazy" width="300" height="400">'
    return '<div class="foto-ph" style="position:absolute;inset:0;clip-path:none"><span>Foto volgt</span></div>'

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
      <p class="label label-licht">Van kleine klussen tot complete projecten</p>
      <h1>Uw partner in techniek &amp; facility.</h1>
      <p class="lead">Elektriciens en mechaniciens die voor langere tijd bij uw bedrijf aan de slag gaan, en alle facility-werk eromheen. Vanuit Meerhout, al bijna dertig jaar elke dag bij Nike. <strong class="geel">Wij regelen het.</strong></p>
      <div class="hero-cta">
        <a class="btn btn-geel" href="tel:{TEL_LORENZO}">Bel Lorenzo</a>
        <a class="btn btn-licht" href="#diensten">Onze diensten</a>
      </div>
      <div class="hero-feit">
        <div><strong>Sinds 1996</strong>dagelijks aan het werk bij Nike</div>
        <div><strong>±11 medewerkers</strong>elke dag op één site</div>
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

<section class="sec-strook" id="diensten">
  <div class="wrap">
    <ul class="strook" aria-label="Onze diensten">
      {''.join(f'<li><a href="{h}"><p class="label">{l}</p><div class="tegel">{tegel_img(s,a)}</div></a></li>' for h,l,s,a in TEGELS)}
    </ul>
  </div>
</section>
{BALK}

<section>
  <div class="wrap">
    <div class="sec-kop">
      <p class="label">Onze twee pijlers</p>
      <h2>Techniekers die blijven.</h2>
      <p class="lead">Sinds 2024 stellen we elektriciens en mechaniciens tewerk bij andere bedrijven in de Kempen en omstreken. Ze werken er zelfstandig, met de certificaten, het materiaal en de uitrusting die de opdracht vraagt, en bij voorkeur voor lange tijd bij dezelfde klant. Elektrieker, onderhoudstechnieker, mecanicien: zeg wat u nodig hebt, wij zoeken het profiel.</p>
    </div>
    <div class="pijlers">
      <a class="pijler" href="/elektriciens/">
        <img src="/img/foto/ph-elektricien.jpg" alt="" loading="lazy" width="460" height="520">
        <div class="in"><p class="label">Pijler 1</p><h3>Elektriciens</h3><p>Voor langdurige samenwerkingen op uw locatie, of voor een kortere technische opdracht.</p><span class="meer">Meer over onze elektriciens</span></div>
      </a>
      <a class="pijler" href="/mechaniciens/">
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
      <li><a href="/facility-diensten/#verhuizingen"><div class="tegel"><img src="/img/foto/ph-verhuizingen.jpg" alt="" loading="lazy" width="460" height="520"></div><h3>Verhuizingen &amp; interne logistiek</h3><p>Twee eigen verhuiswagens met laadlift.</p></a></li>
      <li><a href="/facility-diensten/#kabelmanagement"><div class="tegel"><img src="/img/foto/ph-werkplek.jpg" alt="" loading="lazy" width="460" height="520"></div><h3>Kabelmanagement &amp; werkplekinrichting</h3><p>Elektrische bureaus, stoelen, meubilair, netjes aangesloten.</p></a></li>
      <li><a href="/facility-diensten/#verlichting"><div class="tegel"><img src="/img/foto/ph-verlichting.jpg" alt="" loading="lazy" width="460" height="520"></div><h3>Verlichting vervangen &amp; onderhouden</h3><p>Waar het in 1996 mee begon.</p></a></li>
      <li><a href="/facility-diensten/#fietsen"><div class="tegel"><img src="/img/foto/ph-fietsen.jpg" alt="" loading="lazy" width="460" height="520"></div><h3>Fietsenbeheer &amp; -onderhoud</h3><p>Met een echte fietsenmaker in dienst.</p></a></li>
      <li><a href="/facility-diensten/#opslag"><div class="tegel"><div class="foto-ph" style="height:100%;clip-path:none"><span>Foto volgt</span></div></div><h3>Opslag &amp; voorraadbeheer</h3><p>300 palletplaatsen, digitale inventaris.</p></a></li>
    </ul>
  </div>
</section>

<section>
  <div class="wrap twee">
    <div>
      <p class="label">Ons verhaal</p>
      <h2>Begonnen met een deurklink.</h2>
      <p class="lead" style="margin-top:16px">In 1996 herstelde Geert Vos als contractor een deur en een deurklink bij Nike. Vandaag zijn we daar nog altijd elke dag, met een volledig team van ongeveer elf medewerkers.</p>
      <p style="margin-top:16px"><a class="btn btn-lijn" href="/ons-verhaal/">Lees ons verhaal</a> <a class="btn btn-lijn" href="/werken-bij/" style="margin-left:8px">Werken bij Geert Vos</a></p>
      <div class="feiten">
        <div><strong>1996</strong>gestart bij Nike</div>
        <div><strong>±11</strong>medewerkers per dag</div>
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
      <div><h3>Flexibel</h3><p>Vriendelijk, flexibel en met een positieve ingesteldheid. Onze mensen komen graag, en dat merkt u op de werkvloer.</p></div>
      <div><h3>Betrouwbaar</h3><p>Een jong en hecht team binnen een duidelijke organisatie. Ervaren teamleads zorgen dat elke opdracht correct wordt opgevolgd.</p></div>
      <div><h3>Oplossingsgericht</h3><p>Elke technieker heeft de certificaten, het materiaal en de uitrusting om zelfstandig te werken en af te werken.</p></div>
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
<section class="sec-paper">
  <div class="wrap twee">
    {ph(foto2, 'foto-hoog')}
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
        ('Meetings en events', 'Technische opstellingen klaarzetten: van geluid en grote mobiele schermen tot de stroomvoorziening erachter.')]),
  punten=['De nodige certificaten voor het werk dat u vraagt', 'Eigen materiaal en uitrusting, klaar om te starten', 'Zelfstandig werken, met opvolging door een ervaren teamlead', 'Een werkplek die proper en ordelijk achterblijft', 'Vriendelijk, flexibel en met een positieve ingesteldheid'],
  faq=FAQ_ELEK,
  fotosrc='/img/foto/ph-elektricien.jpg', foto1='Elektricien van Geert Vos aan een schakelkast', foto2='Foto volgt: elektricien aan het werk')

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
  fotosrc='', foto1='Foto volgt: mechanicien aan het werk', foto2='Foto volgt: technieker met gereedschap')

# ---------------------------------------------------------------- FACILITY
def blok(id, label, h2, tekst, punten, fotosrc, alt):
    f = foto(fotosrc, alt) if fotosrc else ph(alt)
    return f'''<div class="dienst-blok" id="{id}">
  <div>
    <p class="label">{label}</p>
    <h2>{h2}</h2>
    <p>{tekst}</p>
    <ul class="punten">{''.join(f'<li>{p}</li>' for p in punten)}</ul>
  </div>
  {f}
</div>'''

FAQ_FAC = [
  ('Doen jullie ook kleine klussen?', 'Ja. Van een deurklink herstellen tot een volledige interne verhuizing: van kleine klussen tot complete projecten. Wij regelen het.'),
  ('Hoe komen opdrachten bij jullie binnen?', 'Bij Nike via een online ticketsysteem waarin dagelijks opdrachten binnenkomen; onze medewerkers en teamleads plannen en voeren ze uit. Voor andere klanten spreken we af wat het beste werkt.'),
  ('Hebben jullie eigen verhuiswagens?', 'Ja, twee eigen verhuiswagens met laadlift, zodat materiaal veilig en ergonomisch geladen en gelost wordt.'),
  ('Kunnen jullie ook materiaal voor ons opslaan?', 'We beschikken over ongeveer 300 palletplaatsen en beheren de voorraad via een digitale inventaris die dagelijks wordt bijgewerkt.'),
  ('Wie onderhoudt de fietsen?', 'Een echte fietsenmaker in dienst van BV Geert Vos. Hij staat ook mee in voor het beheer van onze opslagruimte.'),
]

pages['facility-diensten'] = dict(
  extra=schema('facility-diensten', 'Facility', ('Facility en logistiek', 'Interne verhuizingen, kabelmanagement en werkplekinrichting, verlichting, fietsenbeheer en opslag met 300 palletplaatsen.'), FAQ_FAC),
  title='Facility en logistiek in de Kempen | BV Geert Vos, Meerhout',
  desc='Interne verhuizingen, kabelmanagement en werkplekinrichting, verlichting, fietsenbeheer en opslag met 300 palletplaatsen. Al bijna 30 jaar elke dag bij Nike.',
  body=kop('Facility &amp; logistiek', 'Facility en logistiek', 'Vijf facility- en logistieke diensten die we bij Nike al bijna dertig jaar elke dag uitvoeren, via een online ticketsysteem waarin dagelijks opdrachten binnenkomen. Ook voor uw bedrijf in de Kempen.', 'Facility') + f'''
<main id="inhoud">
<section>
  <div class="wrap">
    {blok('verhuizingen', 'Tak 1', 'Verhuizingen &amp; interne logistiek', 'Interne verhuizingen en logistieke opdrachten zijn een groot deel van ons dagelijks werk. Daarvoor beschikken we over twee eigen verhuiswagens met laadlift, zodat materiaal veilig en ergonomisch geladen en gelost wordt.', ['Interne verhuizingen van werkplekken, afdelingen en meubilair', 'Twee eigen verhuiswagens met laadlift', 'Meetings en evenementen klaarzetten, vandaag met grote mobiele schermen'], '/img/foto/ph-verhuizingen.jpg', 'Twee medewerkers van Geert Vos bij een interne verhuizing')}
    {blok('kabelmanagement', 'Tak 2', 'Kabelmanagement &amp; werkplekinrichting', 'We beheren en onderhouden elektrische bureaus, bureaustoelen en een groot deel van het meubilair in breakrooms en restaurants. Werkplekaanpassingen komen dagelijks binnen via het ticketsysteem.', ['Werkplekken opbouwen, verplaatsen en aanpassen', 'Kabelmanagement, netjes en veilig weggewerkt', 'Beheer en onderhoud van elektrische bureaus, stoelen en meubilair'], '/img/foto/ph-werkplek.jpg', 'Ingerichte kantoorwerkplekken')}
    {blok('verlichting', 'Tak 3', 'Verlichting vervangen &amp; onderhouden', 'Lampen vervangen was een van de allereerste opdrachten in 1996. Het zit nog altijd in ons takenpakket: verlichting vervangen en onderhouden, zodat alles blijft branden.', ['Lampen en armaturen vervangen', 'Onderhoud van verlichting in kantoren, gangen en werkruimtes'], '/img/foto/ph-verlichting.jpg', 'Technieker vervangt een inbouwspot')}
    {blok('fietsen', 'Tak 4', 'Fietsenbeheer &amp; -onderhoud', 'Voor het beheer en onderhoud van fietsen hebben we een echte fietsenmaker in dienst. Hij staat daarnaast mee in voor het beheer van onze opslagruimte.', ['Beheer van een fietsenvloot', 'Onderhoud en herstellingen door een fietsenmaker'], '/img/foto/ph-fietsen.jpg', 'Rij bedrijfsfietsen')}
    {blok('opslag', 'Tak 5', 'Opslag &amp; voorraadbeheer', 'We beschikken over ongeveer 300 palletplaatsen en beheren onze voorraad via een digitale inventaris die dagelijks wordt bijgewerkt. Zo weet u altijd wat waar ligt.', ['Ongeveer 300 palletplaatsen', 'Digitale inventaris, dagelijks bijgewerkt', 'Beheer door een vast aanspreekpunt'], '', 'Foto volgt: magazijn met palletplaatsen')}
  </div>
</section>
''' + faq_blok(FAQ_FAC) + '</main>\n' + CTA)

# ---------------------------------------------------------------- ONS VERHAAL
pages['ons-verhaal'] = dict(
  extra=schema('ons-verhaal', 'Ons verhaal'),
  title='Ons verhaal: sinds 1996 bij Nike | BV Geert Vos, Meerhout',
  desc='Begonnen in 1996 met een deur en een deurklink bij Nike. Vandaag elke dag elf medewerkers ter plaatse, sinds 2024 ook elektriciens en mechaniciens elders.',
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
      <li><time>Vandaag</time><p>Ongeveer elf medewerkers dagelijks bij Nike: meubilair, verhuizingen, fietsen, opslag, events. Twee eigen verhuiswagens, 300 palletplaatsen, een fietsenmaker in dienst.</p></li>
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
      <p>Sinds 1996 zijn we dagelijks actief bij Nike, met ongeveer elf medewerkers. Sinds 2024 groeit onze tweede pijler: elektriciens en mechaniciens bij andere bedrijven in de Kempen.</p>
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
  desc='Neem contact op met BV Geert Vos, Bevrijdingslaan 256 in Meerhout. Bel Lorenzo of Pieter-Jan, of stuur een bericht via het formulier. We antwoorden snel.',
  body=kop('Wij regelen het', 'Contact', 'Bel Lorenzo, hij is uw eerste aanspreekpunt. Of stuur een bericht, dan nemen we contact met u op.', 'Contact') + f'''
<main id="inhoud">
<section>
  <div class="wrap twee" style="align-items:start">
    <div>
      <div class="personen">
        <div class="persoon eerst">
          <div class="init" aria-hidden="true">L</div>
          <div><strong>Lorenzo</strong><div class="rol">Eerste aanspreekpunt</div><a class="tel" href="tel:{TEL_LORENZO}">{TEL_LORENZO_TXT}</a></div>
        </div>
        <div class="persoon">
          <div class="init" aria-hidden="true">PJ</div>
          <div><strong>Pieter-Jan</strong><div class="rol">Aanspreekpunt</div><a class="tel" href="tel:{TEL_PJ}">{TEL_PJ_TXT}</a></div>
        </div>
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
            <option>Elektriciens</option><option>Mechaniciens</option><option>Verhuizingen en logistiek</option><option>Kabelmanagement en werkplekinrichting</option><option>Verlichting</option><option>Fietsenbeheer</option><option>Opslag en voorraadbeheer</option><option>Iets anders</option>
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
  body=kop('Contact', 'Bedankt', 'Uw bericht is aangekomen. Lorenzo of Pieter-Jan neemt zo snel mogelijk contact met u op.', 'Contact') + f'''
<main id="inhoud"><section><div class="wrap"><p class="lead">Dringend? Bel Lorenzo op <a class="tel" href="tel:{TEL_LORENZO}">{TEL_LORENZO_TXT}</a>.</p><p style="margin-top:24px"><a class="btn btn-ink" href="/">Terug naar de startpagina</a></p></div></section></main>
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

urls = ['', 'elektriciens/', 'mechaniciens/', 'facility-diensten/', 'ons-verhaal/', 'werken-bij/', 'contact/', 'privacybeleid/']
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{DOMAIN}/{u}</loc></url>\n' for u in urls) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
