# Open vragen en aan te leveren — BV Geert Vos

Zaken die de site nog nodig heeft of die de klant moet bevestigen. Tijdelijke waarden in de code: `+32 400 00 00 00` en `+32 400 00 00 01` (`TEL_LORENZO`/`TEL_PJ` in `gen.py`).

## Aan te leveren
- Telefoonnummer Lorenzo en Pieter-Jan → `docs/gen.py` (TEL_LORENZO / TEL_PJ + de _TXT-varianten), daarna `python3 docs/gen.py`. Nu staan er tijdelijke +32 400-nummers in.
- ~~Definitief e-mailadres~~ — bevestigd: lorenzo.sterckx@electro-geertvos.be (staat in `MAIL` in gen.py).
- Foto's: de 16 werkfoto's uit "Werkzaamheden Vos.pages" staan in `img/werk/` (webp, ±450×600 px — lage resolutie, prima voor tegels, aan de krappe kant voor grote vlakken) en zijn verwerkt op home, elektriciens, mechaniciens en facility. Nog gewenst, liefst in hoge resolutie: team, bestelwagens en verhuiswagens met laadlift, eigen magazijn/opslag (nu staat er een magazijnfoto van een klant bij 'Opslag'), fietsenmaker aan het werk, ingerichte kantoorwerkplek. De drie bannerfoto's (verhuizing, werkplek, fietsen) staan nog als lage-resolutie uitsnede in `img/foto/`.
- Logo in hoge resolutie of vector, als dat bestaat. De SVG's in `img/` zijn nagetekend van de lage-resolutie jpg (potrace) en zien er scherp uit, maar een origineel bestand is altijd beter.

## Te bevestigen
- Teller op de home rekent dagen sinds 1 januari 1996. Wat was de echte startdatum bij Nike (maand)? Dan zet ik die in `data-sinds`.
- De vijf facility-pagina's (verhuizingen, kabelmanagement, verlichting, fietsenbeheer, opslag) zijn uitgeschreven op basis van de briefing plus redactionele invulling (bv. 'ook buiten de kantooruren', 'onderdelen op voorraad', 'periodieke onderhoudsrondes', 'tijdelijke opslag tijdens verhuizing'). Laten nalezen; wat niet klopt, halen we eruit.
- Eén functie moet echt gehighlight worden — Robbie geeft die nog door.
- Regio: overal staat nu "Kempen en omstreken". Klopt dat? Welke gemeentes/provincies bedienen ze echt?
- Elektriciens-pagina, blok "Elektrisch werk op uw site": verlichting, werkplekken/kabelmanagement, onderhoud en storingen, meetings/events — afgeleid van het Nike-werk uit de briefing. Nalezen: doen de elektriciens bij andere klanten ook dit soort werk, of iets anders (industriële installaties, kastenbouw)?
- Mechaniciens-pagina, blok "Onderhouden, monteren, herstellen": mechanisch onderhoud, montage/demontage, storingen, fietsen en materieel. Zelfde vraag.
- FAQ's op elektriciens, mechaniciens en facility: antwoorden komen uit de briefing, maar laten nalezen.
- Werken-bij-pagina: sollicitaties komen op hetzelfde e-mailadres als het contactformulier. Apart adres gewenst? Concrete vacatures om te vermelden?
- Mag Nike bij naam worden genoemd op de site? Staat nu prominent (hero, verhaal, footer, meta-omschrijvingen). Zo niet: vervangen door "een grote internationale site in de Kempen" of iets dergelijks.
- Aanspreekvorm: nu "u". Wil de klant "je"?
- Elektriciens/mechaniciens: welke certificaten precies (BA4/BA5, VCA, ...), welke sectoren, welke regio? Nu bewust algemeen gehouden ("de nodige certificaten"), want de briefing zegt niet meer.
- Werkwijze in 3 stappen (bel Lorenzo → inzet → opvolging teamleads) is een redactionele invulling van de briefing; laten nalezen.
- Contactpagina en footer noemen Lorenzo/Pieter-Jan niet meer bij naam (gewoon twee telefoonnummers), in afwachting van de afspraak hierover. Op de rest van de site (CTA-blok "Lorenzo bekijkt samen met u...", FAQ's, "U belt Lorenzo"-stap, werken-bij-pagina) staat de naam Lorenzo nog overal. Zodra bekend is hoe dat definitief geregeld wordt, pas ik dat in één keer overal aan.
- "Werken bij"-pagina met sollicitatieformulier gewenst?
- Domein geertvos.be: al geregistreerd? Waar staat de DNS? (Nodig om te koppelen aan Vercel.)
- OG-afbeelding (`img/og.png`) is nu een screenshot van de hero; vervangen door een echte foto zodra die er is.


## Na feedback ronde 2 (25 september 2026)
Verwerkt: nieuwe hero-titel en -tekst, twee pijlers (servicetechniekers en facilityprojecten), Vacatures-knop en -pagina, "30 jaar" in plaats van de dagenteller, contactblok met servicecoördinator en 24 uur, nadruk op hecht en bereikbaar team, en overal "enkel voor langdurige projecten". Daarmee zijn ook de vragen over regio ("Limburg en de Kempen") en de naam Lorenzo in de teksten beantwoord: overal staat nu "onze servicecoördinator".

Nog te bevestigen of aan te leveren:
- **Foto's**: Lorenzo bezorgt volgende week enkele foto's. Zelfde bestandsnamen houden, of paden aanpassen in gen.py.
- **Vacatures**: de drie kaarten (elektricien, mechanicien, facility-medewerker) zijn algemene profielen. Echte vacatureteksten uit de campagnes van Robbie/Max invullen (lijst `FUNCTIES` in gen.py).
- **Sollicitatievragen**: de vragen in het formulier (woonplaats, ervaring, certificaten, rijbewijs, beschikbaar vanaf) zijn een voorstel. Afstemmen met de vragen uit de campagnes.
- **Cv-upload** via FormSubmit na livegang testen (bijlage en groottelimiet).
- **Nike** wordt bij naam genoemd (hero-cijfer, verhaal). Lorenzo schreef zelf "Nike of dergelijke", dus bevestigen dat de naam op de site mag.
- Eerder open en nog steeds: telefoonnummers, e-mailadres, domein/DNS, nalezen van alle teksten.

## Na antwoord van Lorenzo (25 september 2026, later)
- E-mailadres bevestigd: `lorenzo.sterckx@electro-geertvos.be`. Staat overal (formulieren, privacybeleid, footer, schema). **Na livegang eerste inzending doen**: FormSubmit stuurt eerst een bevestigingsmail naar dit adres, die Lorenzo moet activeren.
- Fietsenbeheer en opslag zijn een **extra dienst en horen niet bij Nike**. Pagina's staan terug (`/fietsenbeheer/`, `/opslag/`), in het menu onder "Extra diensten" en op de pagina Diensten. Alle verwijzingen naar fietsen/opslag in de Nike-teksten zijn eruit. Let op: de mechaniciens-pagina noemt nog "fietsen nakijken met een eigen fietsenmaker" en "beheer van magazijn en voorraad" in de opsomming van onderhoudswerk; nalezen of dat zo blijft.
- Aanspreekvorm is nu overal **je** in plaats van u.
