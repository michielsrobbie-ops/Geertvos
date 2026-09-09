# SEO-audit geertvos.be — september 2026 (site nog niet live)

Audit op de statische bestanden; live-checks (Search Console, PageSpeed, indexatie) volgen na livegang.

## Samenvatting
Technisch staat de basis goed: één H1 per pagina, unieke titels en omschrijvingen, canonicals met vaste trailing slash, sitemap + robots, lang="nl-BE", HTTPS/HSTS via Vercel, zelf gehoste fonts, geen cookies. De grootste kansen zitten in **inhoud en zoekwoorden** (regio, synoniemen, dunne en dubbele dienstpagina's) en in **lokale signalen** (telefoonnummer, Google Business Profile).

## Meteen gefixt in deze ronde
- Titels ingekort tot ≤ 62 tekens, meta-omschrijvingen naar 150–160 tekens, regio "Kempen" erin.
- Koppenstructuur: footer-koppen zijn geen `<h4>` meer (sprong h2→h4), contact `<h3>` → `<h2>`.
- Structured data: LocalBusiness uitgebreid (regio, areaServed, e-mail, image, knowsAbout); Service + BreadcrumbList op elektriciens, mechaniciens en facility; BreadcrumbList op verhaal en contact.
- Afbeeldingen: width/height op alle foto's (geen layout shift), og-afbeelding van 430 KB png naar 80 KB jpg.
- 404-pagina toegevoegd (Vercel serveert `404.html` automatisch).
- robots.txt: `Disallow: /bedankt/` weg — de pagina heeft `noindex`, en Google moet die kunnen lezen.

## Tweede ronde (zelfde dag) — inhoud
- Elektriciens en mechaniciens zijn nu echt verschillende pagina's (±700 en ±670 woorden): eigen intro, een blok "wat onze elektriciens/mechaniciens doen" (afgeleid van het werk dat ze al bijna 30 jaar bij Nike doen), eigen FAQ met FAQPage-schema. H1 = "Elektriciens in de Kempen" / "Mechaniciens in de Kempen".
- Vlaamse synoniemen verwerkt: elektrieker, elektrotechnieker, onderhoudstechnieker, mecanicien, technieker inhuren.
- Regio "Kempen en omstreken" in leads, home en meta's. **Navragen bij klant** hoe ver ze rijden (Limburg? Antwerpen-stad?).
- FAQ + FAQPage-schema ook op de facility-pagina.
- Nieuwe pagina **werken-bij** (in menu, footer, sitemap) met sollicitatieformulier via FormSubmit naar hetzelfde adres. Zonder concrete vacatures nog geen JobPosting-schema; zodra er een echte vacature is, toevoegen.
- De blokken "wat onze elektriciens/mechaniciens doen" zijn redactioneel ingevuld op basis van de briefing — **laten nalezen door de klant** (zie open-vragen-klant.md).

## Open punten, op prioriteit

### 1. Kritiek voor lokaal ranken
- **Telefoonnummer ontbreekt** in de LocalBusiness-schema en op de site. Zodra bekend: in `gen.py` invullen, dan komt het ook in de schema (`telephone`).
- **Google Business Profile** aanmaken/claimen op Bevrijdingslaan 256, Meerhout, met dezelfde naam/adres als de site (NAP-consistentie), categorieën "Elektricien" en "Facility management" en link naar geertvos.be. Dit weegt voor "elektricien Meerhout"-zoekopdrachten zwaarder dan de site zelf.
- **Regio**: nu overal "Kempen en omstreken". Navragen bij klant welke regio ze echt bedienen en dat concreet maken (gemeentes, provincies).

### 2. Inhoud (hoog)
- **Elektriciens en mechaniciens**: nu gesplitst en uitgebreid (zie tweede ronde). Nog nodig van de klant om het écht sterk te maken: certificaten (BA4/BA5, VCA?), sectoren, één of twee voorbeeldopdrachten met naam.
- **Facility op één pagina met ankers**: voor "interne verhuizingen Kempen" of "fietsenbeheer bedrijven" is een eigen pagina per tak sterker. Later splitsen zodra er per tak ≥ 300 woorden en foto's zijn.
- **Werken bij**: pagina staat er. Per echte vacature een eigen blok + JobPosting-schema toevoegen.
- **Nike als bewijs** is de sterkste E-E-A-T-troef ("30 jaar dagelijks bij Nike") — mag alleen blijven staan als de klant dat bevestigt.

### 3. Techniek (na livegang)
- Foto's: nu lage-resolutie jpg's uit de banner. Echte foto's als **WebP**, max ±1600 px breed, bestandsnamen met betekenis (`elektricien-schakelkast-geert-vos.webp`), beschrijvende alt-teksten.
- Search Console koppelen + sitemap indienen; Bing Webmaster Tools idem.
- PageSpeed/Core Web Vitals meten na livegang (verwachting: goed — statisch, geen JS-frameworks, fonts gepreload).
- Als geertvos.be nu al een oude site heeft: oude URL's inventariseren en 301's toevoegen in `vercel.json`.

### 4. Kleine dingen
- `bedankt` en `404` staan terecht op noindex.
- Meta-omschrijving privacybeleid is kort (63 tekens) — onbelangrijk.
- `<h1>` op de subpagina's is één woord ("Facility", "Contact"). Prima voor gebruikers; voor SEO draagt de kop op de dienstpagina's het zoekwoord al ("Elektriciens"). Alleen "Facility" mag sterker: bv. "Facility en logistiek".

## Zoekwoordkaart (voorstel)
| Pagina | Primair | Secundair |
|---|---|---|
| Home | facility management Kempen | techniekers inhuren, BV Geert Vos |
| Elektriciens | elektricien inhuren Kempen | elektrieker detachering, industrieel elektricien Meerhout |
| Mechaniciens | mechanicien inhuren | onderhoudstechnieker, mecanicien bedrijven Kempen |
| Facility | facility diensten Kempen | interne verhuizing bedrijf, kabelmanagement kantoor, fietsenbeheer bedrijven |
| Ons verhaal | Geert Vos Meerhout | contractor Nike Laakdal |
