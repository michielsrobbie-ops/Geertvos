# Open vragen en aan te leveren — BV Geert Vos

Zaken die de site nog nodig heeft of die de klant moet bevestigen. Tijdelijke waarden in de code: `+32 400 00 00 00` (Lorenzo), `+32 400 00 00 01` (Pieter-Jan) en `info@geertvos.be`.

## Aan te leveren
- Telefoonnummer Lorenzo en Pieter-Jan → `docs/gen.py` (TEL_LORENZO / TEL_PJ + de _TXT-varianten), daarna `python3 docs/gen.py`. Nu staan er tijdelijke +32 400-nummers in.
- Definitief e-mailadres (klant regelt zelf) → vervang `info@geertvos.be` overal, ook in het formulier (`formsubmit.co/...`). Na livegang: eerste inzending activeert FormSubmit via een bevestigingsmail.
- Foto's: de 16 werkfoto's uit "Werkzaamheden Vos.pages" staan in `img/werk/` (webp, ±450×600 px — lage resolutie, prima voor tegels, aan de krappe kant voor grote vlakken) en zijn verwerkt op home, elektriciens, mechaniciens en facility. Nog gewenst, liefst in hoge resolutie: team, bestelwagens en verhuiswagens met laadlift, eigen magazijn/opslag (nu staat er een magazijnfoto van een klant bij 'Opslag'), fietsenmaker aan het werk, ingerichte kantoorwerkplek. De drie bannerfoto's (verhuizing, werkplek, fietsen) staan nog als lage-resolutie uitsnede in `img/foto/`.
- Logo in hoge resolutie of vector, als dat bestaat. De SVG's in `img/` zijn nagetekend van de lage-resolutie jpg (potrace) en zien er scherp uit, maar een origineel bestand is altijd beter.

## Te bevestigen
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
- "Werken bij"-pagina met sollicitatieformulier gewenst?
- Domein geertvos.be: al geregistreerd? Waar staat de DNS? (Nodig om te koppelen aan Vercel.)
- OG-afbeelding (`img/og.png`) is nu een screenshot van de hero; vervangen door een echte foto zodra die er is.
