#!/usr/bin/env python3
"""Generate entry.png for make.fun news-image-20261123.

Flat-illustration newspaper poster: 49 stories from Monday 23 November 2026
(4 features + 12 minis + 33 one-liners), UTC timeline strip, 12-pin world
map, DATE CHECK box, sources footer. Output is a 1024x1024 PNG.

Written from scratch from the research brief
(~/workspace/makefun/news-image-20261123-brief.md).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# --- palette (flat newspaper) ---
PAPER = (250, 246, 238)
INK = (26, 26, 26)
MUTED = (90, 86, 78)
RULE = (216, 210, 196)
NAVY = (31, 58, 95)
NAVY_DARK = (20, 38, 64)
RED = (179, 38, 30)
TEAL = (14, 124, 123)
GOLD = (200, 144, 26)
SEA = (220, 233, 242)
LAND = (200, 216, 176)
LAND_EDGE = (159, 177, 132)
YELLOW_BOX = (255, 243, 205)
WHITE = (255, 255, 255)


def font(size, bold=False, serif=False):
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, f, max_w):
    """Greedy word wrap to pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_line(draw, text, f, max_w):
    """Truncate with an ellipsis so the text fits one line of max_w px."""
    if draw.textlength(text, font=f) <= max_w:
        return text
    while text and draw.textlength(text + "\u2026", font=f) > max_w:
        text = text[:-1].rstrip()
    return text + "\u2026"


# --- content (from the brief) ---
KICKER_L = "ONE DAY OF WORLD NEWS, ONE PICTURE"
KICKER_R = "49 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE FROM THIS MONDAY"
MASTHEAD = "MONDAY 23 NOVEMBER 2026"

TIMELINE = [
    ("OVERNIGHT", "153 Russian drones; Ukraine hits 3 oil sites"),
    ("01:39 UTC", "KOSPI -3.79%; TAIEX steadies"),
    ("05:29 UTC", "Lowy Asia Power Index: India 3rd (40.5)"),
    ("05:46 UTC", "NZ\u2013India drawn; Australia in WTC top 2"),
    ("07:28 UTC", "134 of 153 drones downed overnight"),
    ("08:22 UTC", "Zelensky confirms Merkury sunk off Libya"),
    ("08:31 UTC", "Modi gives Nepal $1.62bn package"),
    ("11:30 UTC", "China: COP31 failure \u201cdisappointing\u201d"),
    ("12:30 UTC", "U-17 World Cup fixtures kick off"),
]

FEATURES = [
    {
        "num": "1",
        "tag": "EUROPE / AFRICA \u00b7 CONFLICT",
        "label": "CONFIRMED",
        "label_color": TEAL,
        "head": "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
        "body": "Zelensky confirmed Monday that Ukrainian naval drones sank "
                "the Russian corvette Merkury (1,800 tons) at Benghazi, "
                "destroying a helicopter on board; a second ship, MV Angara, "
                "was also hit. Russia has not commented; the UN urged a probe.",
        "src": "CNN \u00b7 France 24 \u00b7 AFP",
        "art": "ship",
    },
    {
        "num": "2",
        "tag": "EUROPE \u00b7 CONFLICT",
        "label": "CONFIRMED",
        "label_color": TEAL,
        "head": "RUSSIA\u2019S OVERNIGHT DRONE BARRAGE; UKRAINE HITS 3 OIL PLANTS",
        "body": "Russia launched 153 drones overnight; air defences downed "
                "134. A strike on a Vyshneve grocery store killed 3. Ukraine "
                "hit back, striking three Russian oil facilities in Rostov, "
                "Perm and Tatarstan.",
        "src": "h.ua \u00b7 Ukrinform \u00b7 France 24",
        "art": "drones",
    },
    {
        "num": "3",
        "tag": "ASIA-PACIFIC \u00b7 DISASTER",
        "label": "CONFIRMED",
        "label_color": TEAL,
        "head": "INDONESIA: MILKITA FIRE TOLL RISES TO 24",
        "body": "Officials confirmed 24 dead in Saturday\u2019s fire at the PT "
                "Fonusa Agung Mulia confectionery factory in Cikande, "
                "Banten; about 30 are still missing. The search continued "
                "Monday through unstable wreckage.",
        "src": "Reuters \u00b7 TBS News",
        "art": "fire",
    },
    {
        "num": "4",
        "tag": "GLOBAL \u00b7 MARKETS",
        "label": "CONFIRMED",
        "label_color": TEAL,
        "head": "AI SELL-OFF SPREADS ACROSS ASIA",
        "body": "South Korea\u2019s KOSPI fell 3.79% by 01:39 UTC as the AI "
                "rout deepened. Taiwan\u2019s short-selling ban took effect "
                "and the TAIEX steadied. Japan\u2019s market was closed for "
                "a holiday.",
        "src": "Yonhap \u00b7 HKET \u00b7 UDN Money",
        "art": "chart",
    },
]

MINIS = [
    ("5", "INDIA GIVES NEPAL $1.62BN PACKAGE",
     "Modi announced a 240bn-rupee package after talks with Nepali PM Balen Shah."),
    ("6", "49ERS ROUT VIKINGS 35-10 IN MEXICO CITY",
     "Purdy threw 3 TD passes in the first Sunday Night Football game outside the US."),
    ("7", "BELGIUM STRIKE GROUNDS ALL FLIGHTS",
     "Unions shut Belgian airspace in a national day of action; most Brussels flights off."),
    ("8", "NZ\u2013INDIA TEST DRAWN; AUSTRALIA BACK IN WTC TOP TWO",
     "NZ batted out the final day in Wellington; the draw lifts Australia, drops NZ."),
    ("9", "HORMUZ: IRAN CLAIMS MQ-9A DOWNED; TWO SUPERTANKERS HIT MINES",
     "Iran claims it shot down a US Reaper drone \u2014 CLAIM, no US confirmation."),
    ("10", "OPENAI CHIEF SCIENTIST PROPOSES AI \u201cCEILING\u201d",
     "Jakub Pachocki\u2019s \u201cPerplexity and Intelligence\u201d urges labs to adopt joint limits."),
    ("11", "CPHIA 2026 OPENS IN ADDIS ABABA",
     "Africa\u2019s biggest public-health conference opened Monday, drawing 40,000+."),
    ("12", "US ARMY RESCHEDULES IOWA DETONATION TO WEDNESDAY",
     "The controlled blast of ~5 tons of unstable lead azide moves to 25 Nov."),
    ("13", "CHINA: COP31 FAILURE \u201cDISAPPOINTING\u201d",
     "Beijing\u2019s first reaction to Sunday\u2019s collapse: green transition \u201cirreversible\u201d."),
    ("14", "MANIPUR ORDERS INQUIRY INTO HOOCH TRAGEDY",
     "A high-level committee will probe the Chandel spurious-liquor deaths; toll 17\u201318."),
    ("15", "LOWY ASIA POWER INDEX 2026: INDIA 3RD",
     "India holds 3rd in Asia with 40.5 points; US 78.9, China 73.6."),
    ("16", "ALICE HUANG KEPT CONTACT WITH CHINESE SPY OFFICIAL",
     "ABC sources say the Nvidia scandal figure stayed in touch with an MSS official."),
]

ONELINERS = [
    "Zelensky presses US over delayed Patriots; ~2,700 drones hit Ukraine in a week",
    "Russia says it hit energy and port infrastructure in Izmail overnight \u2014 CLAIM",
    "Ukraine: 149 combat engagements in 24h; 2,471 Russian losses claimed \u2014 CLAIM",
    "Dymer: drone strike on a five-storey block kills 11; rescuers save a 7-year-old",
    "Kyiv: drone debris falls on a Podil warehouse and two school grounds in Sviatoshyn",
    "Ukraine drones hit 3 Russian oil sites: Novoshakhtinsk, Lukoil-Perm, Kaleikino",
    "Odesa schools go remote 23\u201327 Nov as strikes disrupt energy infrastructure",
    "UN urges a probe after the Russian ship was attacked off Libya (AFP Tripoli)",
    "KOSPI: Samsung -3.39%, SK hynix -2.34%, Hyundai Motor -3.73% at the open",
    "TAIEX +0.35% as Taiwan\u2019s short-selling ban takes effect; TSMC back above NT$2,000",
    "Brent crude ~$92.57 in Asian trading, little changed despite Gulf shipping attacks",
    "Seoul convenes 24 AI chip firms (AMD, Nvidia, Intel) over HBM supply concerns",
    "Oracle tells investors its ~$300bn five-year OpenAI contract is fully funded",
    "METR: AI capability growth outpacing safety evaluation; task length doubles ~3.6 mo",
    "AI coding agents solve fewer than 1 in 10 real-world tasks in simulated workplace",
    "DNI Clayton expects China has found ways to obtain Nvidia\u2019s advanced AI chips",
    "UK digging new reservoirs to fight persistent droughts (AFP Havant)",
    "Kuala Lumpur otters raise river revival hopes (AFP)",
    "UK PM Burnham puts EU deal to MPs: \u201ca choice between a broken status quo\u201d",
    "EU\u2013Indonesia CEPA due before the European Parliament as ratification begins",
    "Delta on manual workarounds after an outage delayed 1,600+ flights",
    "Pochettino: Man Utd must \u201cturn anger into energy\u201d after the 4-0 Liverpool defeat",
    "Labuschagne axed from Australia\u2019s Test squad for NZ; Smith tipped to No. 3",
    "Australia beat France in their Billie Jean King Cup tie; Maya Joint won two rubbers",
    "Giddey\u2019s triple-double rewrites a 60-year Chicago Bulls record in OT loss",
    "Australian shares set to slide at Monday open; NZX 50 -1% in early trade",
    "Screen time to be restricted in South Australia\u2019s public primary schools from 2027",
    "South Sudan raises its Ebola readiness score to 72.5% before its first case",
    "Mvolo referee James Sabah Tiara dies in Juba, weeks after being shot while officiating",
    "Seven oil tankers hit in the Strait of Hormuz since 16 Nov, maritime centre tally",
    "Meta\u2019s chief AI officer posts an AI deepfake of Sam Altman to promote Muse",
    "Signal blocks OS-level AI assistants (Siri AI, Gemini) from reading message content",
    "Bolsonaro remains in intensive care in Bras\u00edlia; hospital says clinically stable",
]

# (number, name, short legend, lat, lon)
PINS = [
    (1, "Benghazi", "Merkury sunk", 32.1, 20.1),
    (2, "Kyiv / Dymer", "drone barrage", 50.5, 30.5),
    (3, "Perm / Rostov", "oil sites hit", 55.0, 50.0),
    (4, "Cikande", "fire toll 24", -6.2, 106.2),
    (5, "Seoul", "KOSPI slides", 37.5, 127.0),
    (6, "Taipei", "short-sale ban", 25.0, 121.6),
    (7, "New Delhi", "$1.62bn for Nepal", 28.6, 77.2),
    (8, "Brussels", "strike grounds flights", 50.8, 4.4),
    (9, "Mexico City", "49ers 35-10", 19.4, -99.1),
    (10, "Wellington", "Test drawn", -41.3, 174.8),
    (11, "Addis Ababa", "CPHIA opens", 9.0, 38.7),
    (12, "Hormuz", "MQ-9A claim; mines", 26.5, 56.3),
]

DATECHECK = (
    "LEFT OUT \u2014 NOT 23 NOVEMBER: COP31 collapse (Sun 22 Nov) \u00b7 Democrats\u2019 "
    "258 House seats (Sun) \u00b7 Riemann Hypothesis proof (Fri 20) \u00b7 Trump\u2013Putin "
    "Anchorage summit (no verified new summit; the Alaska meeting was 15 Aug 2025) "
    "\u00b7 Nikkei -5.06% (Fri 20; Tokyo closed Mon) \u00b7 M\u00e1rquez 8th MotoGP title, "
    "Alcaraz ATP Finals, Boca Sudamericana (Sun) \u00b7 El Chapo Isidro capture (Fri 20) "
    "\u00b7 US measles-elimination revoked (Fri 20) \u00b7 Amazon\u2013Decart $7.5B (Sat 21) "
    "\u00b7 U-17 World Cup Sunday results (Sun)."
)

SOURCES = (
    "Sources: Reuters, AP, AFP, CNN, France 24, BBC, WSJ, h.ua, Kyiv Post, "
    "EuropeSays, EMPR, Inshorts, The Times, UBStandard, OneTurn, EventGraph, "
    "The Decoder, AI Times, ABC News (Australia), cricket.com.au, Sportradar, "
    "USA Today, Fox Sports, Vikings.com, NAMPA, BusinessWorld, IANS, The Hindu "
    "BusinessLine, NewsPoint, Firstpost, TBS News, jawawa.id, CNBC Indonesia, "
    "Dubai Standard, Shipping Tribune, JMIC/UKMTO, Today News Africa, Nile "
    "Intel, Al Jazeera, The S Bharat, PTI, Nation Path India, Onmanorama, "
    "WION, Yonhap, HKET, UDN Money, BigGo Finance, PESTLE Analysis, "
    "frequentbusinesstraveler, Particle News, Intelligence Synthesis, Horizon "
    "AI Digest, NeuralWired, CBS Evening News, Des Moines Register, Inside "
    "Climate News, US Army, RTBF, Travel+Leisure Asia, Alicante Airport News, "
    "A-Sports, Morningstar, ABC News (US), Shafaq News, malaysiajournal, "
    "theworldopinion, Bridge Note, livefromeurope."
)

CLAIM_LINE = (
    "Every story here happened or was first reported on Monday 23 November "
    "2026, in any time zone. CLAIM = one side\u2019s account, not independently confirmed."
)

# Simplified continent outlines (lon, lat) for a flat stylised world map.
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 70),
     (-80, 62), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
     (-80, 32), (-81, 25), (-90, 21), (-97, 16), (-95, 15), (-105, 20),
     (-110, 23), (-115, 30), (-120, 34), (-125, 40), (-130, 48), (-135, 58),
     (-150, 60), (-165, 60)],
    # South America
    [(-80, 8), (-75, 11), (-70, 12), (-60, 8), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-38, -15), (-40, -22), (-48, -28), (-52, -33), (-58, -38),
     (-62, -41), (-65, -45), (-68, -50), (-70, -54), (-73, -50), (-73, -37),
     (-70, -30), (-70, -20), (-75, -15), (-80, -8), (-81, 0), (-80, 6)],
    # Africa
    [(-17, 15), (-15, 11), (-13, 8), (-8, 4), (0, 6), (6, 4), (9, -1),
     (12, -6), (13, -12), (15, -22), (18, -32), (20, -35), (26, -34),
     (32, -28), (35, -22), (40, -15), (41, -10), (40, -5), (42, 0), (48, 2),
     (51, 11), (44, 11), (40, 15), (38, 18), (35, 20), (32, 28), (32, 31),
     (20, 32), (11, 34), (10, 37), (0, 36), (-6, 35), (-10, 31), (-15, 25),
     (-17, 20)],
    # Europe (mainland)
    [(-10, 36), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (0, 50), (2, 51),
     (5, 53), (8, 55), (8, 57), (10, 59), (5, 60), (5, 62), (10, 64),
     (14, 67), (18, 69), (25, 71), (30, 70), (32, 66), (28, 60), (25, 58),
     (21, 55), (24, 54), (19, 54), (14, 54), (12, 54), (8, 54), (3, 51),
     (0, 50), (-2, 47), (-1, 44), (-2, 43), (-9, 38), (-10, 37)],
    # UK
    [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51)],
    # Asia
    [(30, 70), (40, 68), (50, 69), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 74), (120, 73), (130, 71), (140, 72), (150, 70),
     (160, 70), (170, 67), (178, 65), (170, 60), (162, 58), (158, 52),
     (150, 50), (142, 50), (140, 40), (135, 35), (130, 33), (127, 35),
     (122, 30), (120, 25), (115, 22), (110, 20), (108, 15), (105, 10),
     (104, 8), (100, 7), (98, 10), (95, 16), (92, 21), (88, 22), (85, 20),
     (80, 15), (78, 8), (76, 10), (73, 20), (68, 23), (66, 25), (61, 25),
     (57, 27), (52, 26), (50, 29), (48, 30), (44, 29), (40, 32), (36, 36),
     (30, 36), (28, 41), (33, 42), (39, 41), (41, 45), (44, 47), (47, 47),
     (48, 51), (50, 54), (45, 55), (40, 58), (35, 60), (32, 65)],
    # Australia
    [(113, -22), (114, -30), (115, -33), (118, -35), (124, -33), (129, -32),
     (132, -32), (135, -35), (138, -35), (140, -38), (145, -38), (147, -39),
     (150, -37), (153, -32), (153, -27), (151, -24), (149, -20), (146, -19),
     (142, -15), (142, -11), (141, -13), (140, -17), (139, -20), (136, -15),
     (135, -12), (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)],
    # Sumatra
    [(95, 5), (98, 2), (101, -1), (104, -3), (106, -6), (104, -5), (100, -2),
     (96, 4)],
    # Java
    [(105, -6), (108, -7), (112, -7), (114, -8), (111, -8), (107, -7)],
    # Borneo
    [(109, 1), (111, 2), (114, 4), (117, 6), (118, 2), (117, -2), (115, -4),
     (111, -3), (109, 0)],
    # New Guinea
    [(131, -1), (136, -2), (141, -3), (146, -6), (150, -10), (147, -9),
     (142, -8), (137, -6), (132, -4)],
]


# --- flat feature illustrations (drawn with primitives, no photos) ---

def _drone(draw, cx, cy, s, color):
    """Tiny quadcopter silhouette."""
    draw.ellipse([cx - s, cy - s // 2, cx + s, cy + s // 2], fill=color)
    draw.line([cx - s * 2, cy - s, cx - s, cy], fill=color, width=1)
    draw.line([cx + s, cy, cx + s * 2, cy - s], fill=color, width=1)
    draw.line([cx - s * 2 - 2, cy - s - 1, cx - s * 2 + 2, cy - s - 1],
              fill=color, width=1)
    draw.line([cx + s * 2 - 2, cy - s - 1, cx + s * 2 + 2, cy - s - 1],
              fill=color, width=1)


def _starburst(draw, cx, cy, r, color):
    pts = []
    for i in range(16):
        ang = 3.14159 * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * _cos(ang), cy + rr * _sin(ang)))
    draw.polygon(pts, fill=color)


def _cos(a):
    import math
    return math.cos(a)


def _sin(a):
    import math
    return math.sin(a)


def art_ship(draw, x, y, w, h):
    """Warship at sea under drone attack."""
    draw.rectangle([x, y, x + w, y + h], fill=(198, 220, 236))
    draw.rectangle([x, y + h * 0.62, x + w, y + h], fill=(58, 102, 150))
    # waves
    for i in range(5):
        wx = x + 6 + i * 22
        draw.arc([wx, y + h * 0.66, wx + 18, y + h * 0.66 + 8],
                 180, 360, fill=(140, 180, 215), width=2)
    # hull
    draw.polygon([(x + 12, y + h * 0.58), (x + w - 14, y + h * 0.58),
                  (x + w - 26, y + h * 0.74), (x + 22, y + h * 0.74)],
                 fill=(52, 64, 78))
    draw.rectangle([x + 30, y + h * 0.46, x + 62, y + h * 0.58],
                   fill=(52, 64, 78))
    draw.line([x + 46, y + h * 0.30, x + 46, y + h * 0.46],
              fill=(52, 64, 78), width=2)
    draw.rectangle([x + 68, y + h * 0.50, x + 78, y + h * 0.58],
                   fill=(120, 34, 28))
    # drones + explosion
    _drone(draw, x + 22, y + 14, 4, INK)
    _drone(draw, x + 92, y + 10, 3, INK)
    _starburst(draw, x + 78, y + h * 0.44, 13, (240, 150, 40))
    _starburst(draw, x + 78, y + h * 0.44, 7, (250, 210, 90))


def art_drones(draw, x, y, w, h):
    """Night drone barrage over a burning refinery."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY_DARK)
    for sx, sy in [(10, 12), (34, 8), (58, 16), (84, 9), (102, 20),
                   (22, 26), (70, 28), (96, 34)]:
        draw.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=WHITE)
    # searchlight beams
    draw.polygon([(x + 14, y + h), (x + 20, y + h), (x + 60, y + 6)],
                 fill=(90, 120, 170))
    draw.polygon([(x + w - 16, y + h), (x + w - 22, y + h), (x + 66, y + 8)],
                 fill=(90, 120, 170))
    _drone(draw, x + 30, y + 22, 4, (200, 210, 225))
    _drone(draw, x + 62, y + 14, 3, (200, 210, 225))
    _drone(draw, x + 88, y + 26, 4, (200, 210, 225))
    _drone(draw, x + 46, y + 36, 3, (200, 210, 225))
    # refinery ground
    draw.rectangle([x, y + h * 0.78, x + w, y + h], fill=(30, 30, 34))
    draw.rectangle([x + 12, y + h * 0.62, x + 26, y + h * 0.78],
                   fill=(70, 70, 78))
    draw.rectangle([x + 34, y + h * 0.56, x + 52, y + h * 0.78],
                   fill=(70, 70, 78))
    draw.rectangle([x + 66, y + h * 0.66, x + 88, y + h * 0.78],
                   fill=(70, 70, 78))
    # flames
    for fx, fh in [(19, 16), (43, 22), (77, 14)]:
        draw.polygon([(x + fx - 6, y + h * 0.62), (x + fx, y + h * 0.62 - fh),
                      (x + fx + 6, y + h * 0.62)], fill=(240, 120, 30))
        draw.polygon([(x + fx - 3, y + h * 0.62), (x + fx, y + h * 0.62 - fh * 0.6),
                      (x + fx + 3, y + h * 0.62)], fill=(250, 210, 90))


def art_fire(draw, x, y, w, h):
    """Factory fire with smoke."""
    draw.rectangle([x, y, x + w, y + h], fill=(250, 226, 196))
    # smoke
    for sx, sy, sr in [(30, 18, 12), (52, 12, 14), (78, 18, 11), (100, 26, 9)]:
        draw.ellipse([x + sx - sr, y + sy - sr, x + sx + sr, y + sy + sr],
                     fill=(150, 145, 138))
    # factory building
    draw.rectangle([x + 10, y + h * 0.55, x + w - 10, y + h * 0.92],
                   fill=(96, 96, 100))
    # sawtooth roof
    draw.polygon([(x + 10, y + h * 0.55), (x + 32, y + h * 0.42),
                  (x + 54, y + h * 0.55), (x + 76, y + h * 0.42),
                  (x + 98, y + h * 0.55)], fill=(70, 70, 76))
    draw.rectangle([x + 86, y + h * 0.30, x + 96, y + h * 0.55],
                   fill=(70, 70, 76))
    # windows
    for wx in (20, 40, 60):
        draw.rectangle([x + wx, y + h * 0.66, x + wx + 10, y + h * 0.80],
                       fill=(250, 210, 120))
    # flames
    for fx, fh in [(24, 24), (48, 34), (72, 26)]:
        draw.polygon([(x + fx - 9, y + h * 0.55), (x + fx, y + h * 0.55 - fh),
                      (x + fx + 9, y + h * 0.55)], fill=(230, 90, 30))
        draw.polygon([(x + fx - 5, y + h * 0.55), (x + fx, y + h * 0.55 - fh * 0.65),
                      (x + fx + 5, y + h * 0.55)], fill=(250, 200, 60))
    draw.rectangle([x, y + h * 0.92, x + w, y + h], fill=(60, 58, 54))


def art_chart(draw, x, y, w, h):
    """Falling stock chart."""
    draw.rectangle([x, y, x + w, y + h], fill=WHITE)
    # grid
    for gy in range(1, 4):
        gypos = y + h * gy / 4
        draw.line([x + 6, gypos, x + w - 6, gypos], fill=(230, 230, 230))
    # candlesticks
    candles = [(14, 30, 44, True), (30, 36, 54, True), (46, 48, 62, False),
               (62, 58, 74, False), (78, 66, 84, False), (94, 76, 92, False)]
    for cx, top, bot, up in candles:
        col = (46, 160, 90) if up else (200, 40, 32)
        draw.line([x + cx + 4, y + top - 6, x + cx + 4, y + bot + 4],
                  fill=col, width=1)
        draw.rectangle([x + cx, y + top, x + cx + 8, y + bot], fill=col)
    # falling line
    pts = [(x + 8, y + 24), (x + 28, y + 34), (x + 48, y + 30),
           (x + 68, y + 52), (x + 88, y + 62), (x + w - 8, y + 82)]
    draw.line(pts, fill=RED, width=3, joint="curve")
    # down arrow + label
    draw.polygon([(x + w - 30, y + 8), (x + w - 14, y + 8), (x + w - 22, y + 20)],
                 fill=RED)
    draw.rectangle([x + w - 26, y + 4, x + w - 18, y + 10], fill=RED)
    f = font(13, bold=True)
    draw.text((x + 8, y + h - 20), "KOSPI -3.79%", font=f, fill=RED)


ARTS = {"ship": art_ship, "drones": art_drones, "fire": art_fire,
        "chart": art_chart}


# --- world map ---

def project(lon, lat, x0, y0, x1, y1):
    """Equirectangular projection into the map box."""
    px = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    py = y0 + (72.0 - lat) / (72.0 + 55.0) * (y1 - y0)
    return (px, py)


def draw_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SEA, outline=RULE)
    # faint graticule
    for lon in range(-150, 181, 30):
        gx, _ = project(lon, 0, x0, y0, x1, y1)
        draw.line([gx, y0, gx, y1], fill=(205, 220, 232))
    for lat in (-30, 0, 30, 60):
        _, gy = project(0, lat, x0, y0, x1, y1)
        draw.line([x0, gy, x1, gy], fill=(205, 220, 232))
    for poly in CONTINENTS:
        pts = [project(lon, lat, x0, y0, x1, y1) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    # pins
    fnum = font(9, bold=True)
    for num, _name, _leg, lat, lon in PINS:
        px, py = project(lon, lat, x0, y0, x1, y1)
        r = 7
        draw.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                     outline=WHITE, width=1)
        t = str(num)
        tw = draw.textlength(t, font=fnum)
        draw.text((px - tw / 2, py - 5), t, font=fnum, fill=WHITE)


# --- layout ---

MARGIN = 16
CW = W - 2 * MARGIN  # content width: 992


def section_header(draw, y, text, right_text=None):
    f = font(13, bold=True)
    draw.text((MARGIN, y), text, font=f, fill=NAVY)
    if right_text:
        fr = font(10, bold=True)
        tw = draw.textlength(right_text, font=fr)
        draw.text((W - MARGIN - tw, y + 2), right_text, font=fr, fill=MUTED)
    draw.line([MARGIN, y + 18, W - MARGIN, y + 18], fill=NAVY, width=2)
    return y + 22


def draw_feature(draw, x, y, w, h, feat):
    art_w = 118
    ARTS[feat["art"]](draw, x, y + 2, art_w, h - 4)
    tx = x + art_w + 8
    tw = w - art_w - 8
    # number badge + tag + label
    fnum = font(11, bold=True)
    draw.text((tx, y + 2), feat["num"], font=fnum, fill=RED)
    nw = draw.textlength(feat["num"] + " ", font=fnum)
    ftag = font(9, bold=True)
    draw.text((tx + nw, y + 3), feat["tag"], font=ftag, fill=MUTED)
    flab = font(9, bold=True)
    lab = feat["label"]
    lw = draw.textlength(lab, font=flab)
    draw.text((x + w - lw, y + 3), lab, font=flab, fill=feat["label_color"])
    # headline, max 2 lines
    fh = font(13, bold=True)
    lines = wrap(draw, feat["head"], fh, tw)[:2]
    hy = y + 17
    for ln in lines:
        draw.text((tx, hy), ln, font=fh, fill=INK)
        hy += 16
    # body, max 4 lines
    fb = font(10)
    blines = wrap(draw, feat["body"], fb, tw)
    if len(blines) > 4:
        blines = blines[:4]
        blines[3] = fit_line(draw, blines[3], fb, tw)
    by = hy + 1
    for ln in blines:
        draw.text((tx, by), ln, font=fb, fill=INK)
        by += 12.5
    # source line
    fs = font(9)
    draw.text((tx, y + h - 13), feat["src"], font=fs, fill=MUTED)


def draw_mini(draw, x, y, w, num, head, body):
    fnum = font(11, bold=True)
    draw.text((x, y), num, font=fnum, fill=RED)
    nw = draw.textlength(num + " ", font=fnum)
    fh = font(11, bold=True)
    head = fit_line(draw, head, fh, w - nw)
    draw.text((x + nw, y), head, font=fh, fill=INK)
    fb = font(10)
    body = fit_line(draw, body, fb, w - nw)
    draw.text((x + nw, y + 13.5), body, font=fb, fill=MUTED)


def fit_sources(draw, f, max_w, max_lines):
    """Trim the outlet list so it wraps to at most max_lines lines."""
    outlets = SOURCES[len("Sources: "):].split(", ")
    lo, hi = 1, len(outlets)
    best = outlets
    while lo <= hi:
        mid = (lo + hi) // 2
        txt = "Sources: " + ", ".join(outlets[:mid]) + "."
        if len(wrap(draw, txt, f, max_w)) <= max_lines:
            best = outlets[:mid]
            lo = mid + 1
        else:
            hi = mid - 1
    return "Sources: " + ", ".join(best) + " & more."


def build():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- kicker bar ---
    draw.rectangle([0, 0, W, 26], fill=NAVY_DARK)
    fk = font(11, bold=True)
    draw.text((MARGIN, 6), KICKER_L, font=fk, fill=WHITE)
    rw = draw.textlength(KICKER_R, font=fk)
    draw.text((W - MARGIN - rw, 6), KICKER_R, font=fk, fill=(200, 210, 225))

    # --- masthead ---
    draw.line([MARGIN, 32, W - MARGIN, 32], fill=RED, width=2)
    fm = font(40, bold=True, serif=True)
    mw = draw.textlength(MASTHEAD, font=fm)
    draw.text(((W - mw) / 2, 36), MASTHEAD, font=fm, fill=INK)
    draw.line([MARGIN, 84, W - MARGIN, 84], fill=RED, width=2)

    # --- UTC timeline strip ---
    y0 = 88
    ftime = font(9, bold=True)
    ftext = font(9)
    col_w = CW / len(TIMELINE)
    for i, (t, txt) in enumerate(TIMELINE):
        cx = MARGIN + i * col_w
        draw.text((cx + 2, y0 + 2), t, font=ftime, fill=RED)
        lines = wrap(draw, txt, ftext, col_w - 6)[:2]
        ty = y0 + 14
        for ln in lines:
            draw.text((cx + 2, ty), ln, font=ftext, fill=INK)
            ty += 11
        if i:
            draw.line([cx, y0 + 2, cx, y0 + 36], fill=RULE)
    draw.line([MARGIN, 128, W - MARGIN, 128], fill=RULE)

    # --- features 2x2 ---
    feat_w = (CW - 8) // 2
    feat_h = 106
    for i, feat in enumerate(FEATURES):
        fx = MARGIN + (i % 2) * (feat_w + 8)
        fy = 132 + (i // 2) * feat_h
        draw_feature(draw, fx, fy, feat_w, feat_h, feat)
        if i % 2 == 0:
            draw.line([fx + feat_w + 4, fy + 4, fx + feat_w + 4,
                       fy + feat_h - 4], fill=RULE)
    draw.line([MARGIN, 340, W - MARGIN, 340], fill=RULE)

    # --- minis ---
    y = section_header(draw, 344, "MORE FROM MONDAY", "STORIES 5\u201316")
    mini_w = (CW - 8) // 2
    for i, (num, head, body) in enumerate(MINIS):
        mx = MARGIN + (i % 2) * (mini_w + 8)
        my = y + (i // 2) * 27
        draw_mini(draw, mx, my, mini_w, num, head, body)
    draw.line([MARGIN, 522, W - MARGIN, 522], fill=RULE)

    # --- map + pin legend ---
    y = section_header(draw, 526, "WHERE IT HAPPENED", "12 PINS")
    draw_map(draw, MARGIN, y, 640, 642)
    # legend, two columns of six
    fleg = font(10)
    flegn = font(10, bold=True)
    for i, (num, name, leg, _lat, _lon) in enumerate(PINS):
        lx = 652 + (i // 6) * 180
        ly = y + (i % 6) * 17
        draw.text((lx, ly), str(num), font=flegn, fill=RED)
        nw = draw.textlength(str(num) + " ", font=flegn)
        txt = "%s \u2014 %s" % (name, leg)
        txt = fit_line(draw, txt, fleg, 176 - nw)
        draw.text((lx + nw, ly), txt, font=fleg, fill=INK)

    # --- one-liners ---
    y = section_header(draw, 646, "ALSO ON 23 NOVEMBER", "STORIES 17\u201349")
    col_w = (CW - 8) // 2
    row_h = (872 - y) / 17.0
    fon = font(11)
    fonn = font(11, bold=True)
    for i, txt in enumerate(ONELINERS):
        col = 0 if i < 17 else 1
        row = i if i < 17 else i - 17
        ox = MARGIN + col * (col_w + 8)
        oy = y + row * row_h
        num = str(17 + i)
        draw.text((ox, oy), num, font=fonn, fill=RED)
        nw = draw.textlength(num + " ", font=fonn)
        txt = fit_line(draw, txt, fon, col_w - nw)
        draw.text((ox + nw, oy), txt, font=fon, fill=INK)

    # --- date check box ---
    draw.rectangle([MARGIN, 874, W - MARGIN, 938], fill=YELLOW_BOX,
                   outline=GOLD, width=1)
    fdh = font(11, bold=True)
    draw.text((MARGIN + 8, 878), "DATE CHECK \u2014 WHAT WE LEFT OUT",
              font=fdh, fill=(120, 80, 10))
    fdc = font(10)
    lines = wrap(draw, DATECHECK, fdc, CW - 16)
    dy = 894
    for ln in lines[:4]:
        draw.text((MARGIN + 8, dy), ln, font=fdc, fill=INK)
        dy += 12

    # --- footer ---
    draw.line([MARGIN, 944, W - MARGIN, 944], fill=NAVY, width=2)
    fc = font(10, bold=True)
    clines = wrap(draw, CLAIM_LINE, fc, CW)
    cy = 949
    for ln in clines:
        draw.text((MARGIN, cy), ln, font=fc, fill=INK)
        cy += 13
    fs = font(8)
    src_txt = fit_sources(draw, fs, CW, 4)
    slines = wrap(draw, src_txt, fs, CW)
    sy = cy + 3
    for ln in slines:
        draw.text((MARGIN, sy), ln, font=fs, fill=MUTED)
        sy += 10.5
    fbot = font(9, bold=True)
    bot = "make.fun \u00b7 news-image-20261123 \u00b7 Poster built from the 23 Nov 2026 research brief"
    bw = draw.textlength(bot, font=fbot)
    draw.text((W - MARGIN - bw, H - 16), bot, font=fbot, fill=MUTED)

    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    img = build()
    out = os.path.join(here, "entry.png")
    img.save(out, "PNG", optimize=True)
    size = os.path.getsize(out)
    print("wrote %s (%d bytes, %dx%d)" % (out, size, img.width, img.height))


if __name__ == "__main__":
    main()
