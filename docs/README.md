# geertvos.be — statische website

Statisch HTML/CSS/JS, zelfde opzet als vandis-website (GitHub → Vercel, `cleanUrls` in vercel.json).

- `index.html` — home: donkere hero waarin de logo-lamp aanflikkert (één keer per sessie, `sessionStorage`), het licht volgt de cursor, de lamp knipoogt bij hover/tik, cijfer '30 jaar elke dag aanwezig bij Nike' (de dagenteller is vervangen; de teller-code in main.js staat er nog maar wordt niet gebruikt). Alles respecteert `prefers-reduced-motion`.
- Stroomlijn (`.stroom`, de drie gele lijnen): onder de hero, onder elke paginakop en boven de CTA-band; er loopt een lichtpuls doorheen als hij in beeld komt (main.js).
- Voor/na-slider (`voor_na()` in gen.py, `[data-vergelijk]` in main.js) op kabelmanagement.html.
- Geen elementen van de Facebook-banner meer (schuine tegels, zwarte balk, slogan) — eigen stijl.
- Structuur sinds feedback ronde 2 (25 sept): twee pijlers, allebei enkel voor langdurige projecten. `servicetechniekers.html` (hub) → `elektriciens.html`, `mechaniciens.html`. `facilityprojecten.html` (hub) → `verhuizingen.html`, `kabelmanagement.html`, `verlichting.html`.
- `diensten.html` — overzicht van de twee pijlers (menu-item Diensten, dropdown gegroepeerd per pijler)
- Alle dienstpagina's gebruiken dezelfde template `dienst_pagina()` in gen.py: intro, wat we doen, foto's, wat je mag verwachten, stappen, FAQ met schema, andere diensten. `fietsenbeheer.html` en `opslag.html` zijn **extra diensten** (parameter `extra=True`, menu-kop 'Extra diensten', sectie op diensten.html) en horen niet bij Nike. De oude URL's `/facility-diensten/` en `/werken-bij/` redirecten via vercel.json.
- Aanspreekvorm is 'je' (Lorenzo, 25 sept). Alle formulieren gaan naar `MAIL` bovenaan gen.py (lorenzo.sterckx@electro-geertvos.be).
- `vacatures.html` — één vacature (Service Technieker) met kerngegevens, taken, eisen en aanbod, plus sollicitatieformulier met cv-upload (FormSubmit, `enctype=multipart/form-data`, veldnaam `attachment`) en JobPosting-schema. Nieuwe vacature: `VACATURE_JSON` en het blok in gen.py aanpassen.
- `ons-verhaal.html`, `contact.html`, `bedankt.html` (na formulier), `privacybeleid.html`
- `css/style.css`, `js/main.js` — bij wijziging de `?v=` versiedatum in alle html-bestanden ophogen
- `fonts/` — Bricolage Grotesque, zelf gehost, OFL (caveat-*.woff2 is niet meer in gebruik en mag weg). Geen Google Fonts, dus geen cookiebanner nodig.
- `img/logo*.svg`, `bulb*.svg`, `favicon.svg` — nagetekend uit de jpg; `logo-nav.svg` (wit, uitlopende lijnen) in header en footer, `bulb.svg` inline in de hero
- Foto's: `img/werk/*.webp` (techniek: kabels, verlichting, hoogwerkers; `-hd`-bestanden zijn de scherpe versies) en `img/team/*.webp` (team, verhuiswagen, fietsen, magazijn). Beide komen uit de foto's van de klant (WhatsApp-export in `img/foto/fotos/`, staat in .gitignore en wordt niet gepubliceerd). Nieuwe foto's toevoegen: in die map zetten, `docs/optimize_photos.py` uitbreiden en draaien, daarna de paden in `docs/gen.py` aanpassen. Bestandsnamen in `img/` krijgen een jaar cache: bij een nieuwe versie van dezelfde foto een nieuwe bestandsnaam gebruiken. `img/og-team.jpg` is de afbeelding bij delen op social media.
- `docs/briefing-klant.md` — letterlijke briefing; `docs/open-vragen-klant.md` — wat nog ontbreekt

Alle html wordt gegenereerd door `docs/gen.py` (header, footer, teksten, telefoonnummers staan daar één keer). Wijzigen → `python3 docs/gen.py` draaien vanuit de projectmap. Rechtstreeks in de html editen kan ook, maar wordt overschreven bij de volgende generatie.
