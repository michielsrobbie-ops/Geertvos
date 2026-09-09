# geertvos.be — statische website

Statisch HTML/CSS/JS, zelfde opzet als vandis-website (GitHub → Vercel, `cleanUrls` in vercel.json).

- `index.html` — home: donkere hero waarin de logo-lamp aanflikkert (één keer per sessie, `sessionStorage`, respecteert `prefers-reduced-motion`), daaronder de strook met zeven schuine fototegels en de zwarte balk Flexibel/Betrouwbaar/Oplossingsgericht (opbouw van de bedrijfsbanner)
- `elektriciens.html`, `mechaniciens.html` — de twee hoofdpijlers
- `facility-diensten.html` — overzicht van de vijf takken; elke tak heeft een eigen pagina: `verhuizingen.html`, `kabelmanagement.html`, `verlichting.html`, `fietsenbeheer.html`, `opslag.html` (zelfde template `dienst_pagina()` in gen.py: intro, wat we doen, foto's, wat u mag verwachten, stappen, FAQ met schema, andere diensten)
- `werken-bij.html` — spontaan solliciteren (FormSubmit)
- `ons-verhaal.html`, `contact.html`, `bedankt.html` (na formulier), `privacybeleid.html`
- `css/style.css`, `js/main.js` — bij wijziging de `?v=` versiedatum in alle html-bestanden ophogen
- `fonts/` — Bricolage Grotesque (alles) + Caveat (alleen de handgeschreven slogan in de zwarte balk); zelf gehost, OFL. Geen Google Fonts, dus geen cookiebanner nodig.
- `img/logo*.svg`, `bulb*.svg`, `favicon.svg` — nagetekend uit de jpg; `logo-nav.svg` (wit, uitlopende lijnen) in header en footer, `bulb.svg` inline in de hero
- `img/werk/*.webp` — 16 werkfoto's van de klant (uit Werkzaamheden Vos.pages): lichtmasten, kabelmanagement voor/na, uitgebrande kabels, verlichting, straatverlichting. Galerij op elektriciens.html.
- `img/foto/ph-*.jpg` — TIJDELIJK: lage-resolutie uitsneden uit de banner (nog gebruikt voor verhuizing, fietsen, team). Vervangen door de echte foto's zodra Robbie die heeft (zelfde bestandsnamen houden, of paden aanpassen in docs/gen.py en opnieuw genereren)
- `docs/briefing-klant.md` — letterlijke briefing; `docs/open-vragen-klant.md` — wat nog ontbreekt

Alle html wordt gegenereerd door `docs/gen.py` (header, footer, teksten, telefoonnummers staan daar één keer). Wijzigen → `python3 docs/gen.py` draaien vanuit de projectmap. Rechtstreeks in de html editen kan ook, maar wordt overschreven bij de volgende generatie.
