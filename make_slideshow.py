#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# make_slideshow.py — génère PICS/slideshow.svg avec les 28 utilitaires chris1111
# Usage : pip3 install Pillow   puis   python3 make_slideshow.py

import base64, io, os, time
from PIL import Image
from xml.sax.saxutils import escape

# ══════════ LES 28 UTILITAIRES (image PICS + nom affiché) ══════════
SLIDES = [
    ("PICS/Background-Resizer.png",                      "Background-Resizer"),
    ("PICS/Workshop.png",                                "Workshop-Layered-Image-Studio"),
    ("PICS/Studio.png",                                  "Icon-Studio"),
    ("PICS/OCUSBMEDIA.png",                              "OC-USB-MEDIA"),
    ("PICS/Chameleon.png",                               "Chameleon"),
    ("PICS/OpenCoreCreator.png",                         "OpenCore-Creator"),
    ("PICS/InstallMediaOC.png",                          "Install-Media-OC"),
    ("PICS/Clover-Duet.png",                             "Clover-Duet"),
    ("PICS/HP-EliteBook-840-G4.png",                     "HP EliteBook 840 G4"),
    ("PICS/MacEFI-Mounter.png",                          "MacEFIMounter"),
    ("PICS/Optiplex-790.png",                            "Dell-Optiplex-790"),
    ("PICS/Snow-DVD-Creator.png",                        "Snow-Leopard-DVD-Creator"),
    ("PICS/Wireless-USB-Big-Sur-Adapter.png",            "Wireless USB BigSur Adapter"),
    ("PICS/OpenCanopy-Generator.png",                    "OpenCanopy Generator"),
    ("PICS/Themes-OpenCore.png",                         "Themes OpenCore"),
    ("PICS/Lion-DVD-Creator.png",                        "Lion-DVD-Creator"),
    ("PICS/Wifi-Mediatek-macOS.png",                     "WIFI Mediatek macOS"),
    ("PICS/HP-Probook-EliteBook-Package-Creator-OC.png", "HP ProBook EliteBook macOS OC"),
    ("PICS/IconSet-Tahoe-Style-Linux-Mac.png",           "IconSet Tahoe Style"),
    ("PICS/Create-Windows-USB.png",                      "Create-Windows-USB"),
    ("PICS/Garuda.png",                                  "Linux Tahoe Style Disk"),
    ("PICS/Disable-Gatekeeper.png",                      "Gatekeeper Tools"),
    ("PICS/Wimlib-imagex-Packager.png",                  "Wimlib imagex Packager"),
    ("PICS/Software-Update.png",                         "Softwareupdate Full Installer"),
    ("PICS/SF-Symbols-Composer-PNG.png",                 "SF Symbols Composer PNG"),
    ("PICS/CreateApp-Platypus.png",                      "CreateApp-Platypus"),
    ("PICS/Compress-PNG.png",                            "Compress-PNG"),
    ("PICS/Download.png",                                "Download-macOS"),
]

OUT        = "PICS/slideshow.svg"
W, H       = 760, 420        # zone image d'une slide
PAD        = 14              # marge interne autour de la capture
DURATION   = 4.0             # secondes par slide (28 slides ≈ 1 min 52 par boucle)
FADE       = 0.8             # durée du fondu enchaîné
MAX_SIZE   = 2.8 * 1024**2   # le script baisse la qualité JPEG tout seul si > 2.8 Mo

BG, BORDER      = "#0d1117", "#30363d"
ACCENT, ACCENT2 = "#FF8C00", "#F97316"
TEXT, MUTED     = "#e6edf3", "#8b949e"
TITLE           = "chris1111 — macOS Utilities"
# ════════════════════════════════════════════════════════════════════

CARD_W, CARD_H = 800, 558
IMG_X, IMG_Y   = 20, 70
CAP_Y, DOT_Y   = 522, 544
DOT_R, DOT_GAP = 4.5, 24


def load_slides():
    slides = []
    for path, name in SLIDES:
        if not os.path.exists(path):
            print(f"⚠  Introuvable, ignoré : {path}")
            continue
        slides.append((Image.open(path).convert("RGBA"), name))
    if not slides:
        raise SystemExit("✖ Aucune image trouvée — vérifie les chemins PICS/")
    return slides


def encode(img, quality):
    im = img.copy()
    im.thumbnail((W - 2 * PAD, H - 2 * PAD), Image.LANCZOS)
    canvas = Image.new("RGB", (W, H), (13, 17, 23))
    canvas.paste(im, ((W - im.width) // 2, (H - im.height) // 2), im)
    buf = io.BytesIO()
    canvas.save(buf, "JPEG", quality=quality, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def build(slides, quality):
    n    = len(slides)
    dur  = f"{DURATION * n:.2f}s"
    step = 1.0 / n
    f    = FADE / (DURATION * n)

    s = [f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
     width="{CARD_W}" height="{CARD_H}" viewBox="0 0 {CARD_W} {CARD_H}" role="img">
  <title>macOS Utilities slideshow</title>
  <defs>
    <linearGradient id="grad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{ACCENT}"/><stop offset="1" stop-color="{ACCENT2}"/>
    </linearGradient>
    <clipPath id="clip"><rect x="{IMG_X}" y="{IMG_Y}" width="{W}" height="{H}" rx="14"/></clipPath>
  </defs>
  <rect x="1.5" y="1.5" width="{CARD_W-3}" height="{CARD_H-3}" rx="18"
        fill="{BG}" stroke="url(#grad)" stroke-opacity="0.6" stroke-width="1.5"/>
  <circle cx="30" cy="25" r="7" fill="#ff5f57"/>
  <circle cx="52" cy="25" r="7" fill="#febc2e"/>
  <circle cx="74" cy="25" r="7" fill="#28c840"/>
  <text x="{CARD_W//2}" y="30" text-anchor="middle"
        font-family="ui-monospace,SFMono-Regular,Menlo,monospace"
        font-size="15" font-weight="600" fill="{TEXT}">{escape(TITLE)}</text>
  <line x1="1.5" y1="50" x2="{CARD_W-1.5}" y2="50" stroke="#21262d"/>
  <rect x="0" y="48.5" width="0" height="1.5" fill="url(#grad)" opacity="0.9">
    <animate attributeName="width" values="0;{CARD_W}" dur="{DURATION}s" repeatCount="indefinite"/>
  </rect>''']

    for i, (img, name) in enumerate(slides):
        href = f"data:image/jpeg;base64,{encode(img, quality)}"
        if i == 0:
            values, keys = "1;1;0;0;1", f"0;{step-f:.5f};{step:.5f};{1-f:.5f};1"
        elif i == n - 1:
            values, keys = "0;0;1;1;0", f"0;{i*step-f:.5f};{i*step:.5f};{1-f:.5f};1"
        else:
            values = "0;0;1;1;0;0"
            keys = f"0;{i*step-f:.5f};{i*step:.5f};{(i+1)*step-f:.5f};{(i+1)*step:.5f};1"
        s.append(f'''
  <g>
    <image x="{IMG_X}" y="{IMG_Y}" width="{W}" height="{H}" clip-path="url(#clip)" href="{href}" xlink:href="{href}"/>
    <text x="{CARD_W//2}" y="{CAP_Y}" text-anchor="middle"
          font-family="-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
          font-size="16" font-weight="600" fill="{TEXT}">{escape(name)}<tspan fill="{MUTED}" font-weight="400">&#160;&#160;·&#160;&#160;{i+1:02d}/{n:02d}</tspan></text>
    <animate attributeName="opacity" values="{values}" keyTimes="{keys}" dur="{dur}" repeatCount="indefinite"/>
  </g>''')

    x0 = (CARD_W - (n - 1) * DOT_GAP) / 2
    for i in range(n):
        if i == 0:
            vals, keys = f"{ACCENT};{ACCENT};{BORDER};{BORDER};{ACCENT}", f"0;{step-f:.5f};{step:.5f};{1-f:.5f};1"
        elif i == n - 1:
            vals, keys = f"{BORDER};{BORDER};{ACCENT};{ACCENT};{BORDER}", f"0;{i*step-f:.5f};{i*step:.5f};{1-f:.5f};1"
        else:
            vals = f"{BORDER};{BORDER};{ACCENT};{ACCENT};{BORDER};{BORDER}"
            keys = f"0;{i*step-f:.5f};{i*step:.5f};{(i+1)*step-f:.5f};{(i+1)*step:.5f};1"
        s.append(f'''
  <circle cx="{x0 + i*DOT_GAP:.1f}" cy="{DOT_Y}" r="{DOT_R}" fill="{BORDER}">
    <animate attributeName="fill" values="{vals}" keyTimes="{keys}" dur="{dur}" repeatCount="indefinite"/>
  </circle>''')

    s.append("\n</svg>\n")
    return "".join(s)


def main():
    slides = load_slides()
    for quality in (85, 80, 75, 70, 65, 60):
        svg = build(slides, quality)
        if len(svg.encode()) <= MAX_SIZE:
            break
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"✔ {OUT} — {len(slides)} slides, {os.path.getsize(OUT)/1024/1024:.2f} Mo (qualité JPEG {quality})")
    if os.path.getsize(OUT) > MAX_SIZE:
        print("⚠  Fichier lourd — réduis W,H (ex: 640, 360) ou retire quelques slides")
    version = time.strftime("%Y%m%d")
    print(f'''
📌 Colle ceci dans ton README :

<div align="center">
  <a href="https://github.com/chris1111?tab=repositories">
    <img src="PICS/slideshow.svg?v={version}" width="820" alt="Slideshow macOS Utilities"/>
  </a>
</div>''')


if __name__ == "__main__":
    main()