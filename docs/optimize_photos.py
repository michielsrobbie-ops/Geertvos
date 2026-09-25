# Zet de ruwe klantfoto's (img/foto/fotos, WhatsApp-exports) om naar webp voor de site.
# Draaien vanuit de projectmap: python3 docs/optimize_photos.py
# De ruwe map staat in .gitignore. Nummering = volgorde op tijdstip in de bestandsnaam.
# Niet gebruikt (privacy / niet relevant): 16 en 27-29 (nummerplaten), 21-22 (schermafbeeldingen), 26, 30, 31 (privé).
import glob, os, re
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'img', 'foto', 'fotos')

def sleutel(f):
    m = re.search(r'14\.15\.(\d+)(?: \((\d+)\))?', os.path.basename(f))
    return (int(m.group(1)), int(m.group(2)) if m.group(2) else 0)

fotos = sorted(glob.glob(os.path.join(RAW, '*.jpeg')), key=sleutel)

# nummer -> (map, bestandsnaam)
UIT = {
    1: ('werk', 'kabelgoot-magazijn-hd'),
    2: ('werk', 'kabelgoot-hd'),
    3: ('werk', 'werkstation-kabelmanagement-1-hd'),
    4: ('werk', 'werkstation-kabelmanagement-2-hd'),
    5: ('werk', 'magazijn-verlichting-hoogwerker-1-hd'),
    6: ('werk', 'magazijn-verlichting-hoogwerker-2-hd'),
    7: ('werk', 'straatverlichting-hoogwerker-3-hd'),
    8: ('werk', 'straatverlichting-hoogwerker-4-hd'),
    9: ('werk', 'straatverlichting-hoogwerker-1-hd'),
    10: ('werk', 'straatverlichting-hoogwerker-2-hd'),
    11: ('werk', 'straatverlichting-hoogwerker-5-hd'),
    12: ('werk', 'lichtmast-heftruck-hd'),
    13: ('team', 'team-keuken-1'),
    14: ('team', 'team-keuken-2'),
    15: ('team', 'team-gang'),
    17: ('team', 'luidspreker-meeting'),
    18: ('team', 'fietsen-aanhanger'),
    19: ('team', 'team-lunch'),
    20: ('team', 'team-kerst'),
    23: ('team', 'opslag-rekken'),
    24: ('team', 'fietsen-opslag'),
    25: ('team', 'verhuiswagen-laadlift'),
}
for nr, (map_, naam) in UIT.items():
    im = ImageOps.exif_transpose(Image.open(fotos[nr - 1])).convert('RGB')
    maxb = 1400 if im.width > im.height else 900
    if im.width > maxb:
        im = im.resize((maxb, round(im.height * maxb / im.width)), Image.LANCZOS)
    os.makedirs(os.path.join(ROOT, 'img', map_), exist_ok=True)
    pad = os.path.join(ROOT, 'img', map_, naam + '.webp')
    im.save(pad, 'WEBP', quality=70 if im.height > 1400 else 80, method=6)
    print(nr, pad.replace(ROOT + '/', ''), im.size, os.path.getsize(pad) // 1024, 'kB')

# OG-afbeelding voor delen (WhatsApp, LinkedIn): teamfoto 1200x630
lunch = ImageOps.exif_transpose(Image.open(fotos[19 - 1])).convert('RGB')
b = 1200; h = round(lunch.height * b / lunch.width)
lunch = lunch.resize((b, h), Image.LANCZOS)
top = max(0, round((h - 630) * 0.55))
lunch.crop((0, top, b, top + 630)).save(os.path.join(ROOT, 'img', 'og-team.jpg'), quality=82)
print('og-team.jpg')
