#!/usr/bin/env python3
"""Writes the App Store listing and the App Review reply from the build's own counts (playbook/site-numbers.json, which
scripts/make-site.py rewrites on every run), so the copy never drifts from the data. Modeled on wa-eats/playbook/06 and 13.

Usage (from mi-eats/): .venv/bin/python scripts/make-listing.py   (after make-site.py)
Writes playbook/06-app-store-listing.md, playbook/13-app-review-reply.md and playbook/app-store/listing.json (what
../scripts/asc_listing.py uploads once Nick creates the App Store Connect record and its FOLDERS line is added).
Checks before writing anything: Apple's length limits, no keyword repeating a name/subtitle word, no "best"/"top"/"#1", no price
claim outside the description's plain "free guide", the reply under 4,000 characters.
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(__file__), "..")
N = json.load(open(os.path.join(ROOT, "playbook", "site-numbers.json")))
R, T, INS, LIC, HON = N["restaurants"], N["towns"], N["inspection_results"], N["on_an_official_list"], N["honors"]
G = {k[6:]: v for k, v in N.items() if k.startswith("guide_") and isinstance(v, int)}
FLOOR = R // 1000 * 1000   # "24,000+": promo text and What's New outlive small data changes
SITE = "https://michigan.eatsranked.com/"   # until the CNAME resolves: https://nickstrom5.github.io/michigan-eats/

NAME = "Michigan Eats: Restaurants"
SUB = "Coneys, Pasties & Square Pizza"
# no word from the name or subtitle; towns are the biggest search win (rotate after a month of App Store Connect search-term data)
KW = "detroit,grand rapids,ann arbor,dearborn,paczki,traverse city,lansing,flint,food guide,mitten,novi"
PROMO = (f"{G['coney']} coney islands, {G['paczki']} pączki bakeries, Detroit-style pizza and pasties, each checked by hand. "
         f"Plus {FLOOR:,}+ Michigan restaurants near you.")
WHATS_NEW = f"First release: coney islands, Detroit-style pizza, pasties, pączki and {FLOOR:,}+ Michigan restaurants."

DESC = f"""Michigan's restaurants, from a coney with everything to a pasty north of the Bridge.

Michigan Eats is a free guide to eating in Michigan: {G['coney']} coney islands, {G['dpizza']} Detroit-style pizzerias, {G['pasty']} pasty shops, {G['paczki']} pączki bakeries and {G['mideast']} Middle Eastern places in Dearborn we checked by hand, plus {R:,} restaurants, cafés, bars and bakeries in {T} towns, from Detroit, Grand Rapids and Ann Arbor to Lansing, Traverse City and the U.P. {LIC:,} of them are on the state's list of licensed food-service establishments. No account, no ads.

MICHIGAN GUIDES
• Coney Islands: Detroit coneys with chili, mustard and onions, starting with downtown's side-by-side rivals.
• Detroit-Style Pizza: square, pan-baked pizza with the crisp cheese edge.
• Pasties: Upper Peninsula pasty shops.
• Pączki Bakeries: where Metro Detroit lines up on Fat Tuesday.
• Middle Eastern: Dearborn's Lebanese and Yemeni kitchens, bakeries and coffee houses.
• Award winners: {HON} James Beard semifinalists, finalists and America's Classics.
• Detroit Inspections: the Detroit Health Department's own result for {INS:,} places (in compliance or not, with the violations cited), shown as the City publishes it.

FIND IT FAST
• Sort by distance, or browse the map by guide.
• Search by name, town, street or dish: "coney dearborn", "paczki hamtramck".
• Filter by town or cuisine, or hide chains.
• Save places, and find hand-checked places from iPhone search (Spotlight).

LIVE DETAILS FROM APPLE MAPS
Tap "Ratings, hours & photos" on any place to open Apple Maps' own place card, with current hours, photos, ratings and directions.

HOW THE LISTS ARE BUILT
Every guide place was checked by hand in October 2026 against a 2025 or 2026 source: dated local news, an official tourism listing or the place's own site, plus an active food-service license or a recent Detroit inspection where the page had no date. The rest come from Overture Maps open data, checked against Michigan's list of licensed food-service establishments. Website links are checked too. Nothing is ranked by star ratings, and the app computes no grades.

PRIVATE BY DESIGN
No account, no tracking, no ads. Your location, if you share it, only sorts lists on your device. Saved places stay on your device.

Places open and close, so check before you go. Spot a mistake? Email nick@eatsranked.com.

An independent app, not affiliated with any restaurant, chain or government agency (including the State of Michigan, MDARD, the City of Detroit and the Detroit Health Department), or with the James Beard Foundation. James Beard Foundation and James Beard Award are trademarks of the James Beard Foundation. Place data from Overture Maps Foundation (CDLA Permissive 2.0) and others; sources and licenses are on the About tab."""

REPLY = f"""Thank you. Here is the information requested. A screen recording from an iPhone running the latest iOS is attached. It starts at launch and shows the full flow.

1. Screen recording: attached. There is no account, login, user-generated content or paid content.

2. Purpose and audience: Michigan Eats is a free guide to restaurants in Michigan. Its focus is the state's food traditions: {G['coney']} coney islands, {G['dpizza']} Detroit-style pizzerias, {G['pasty']} pasty shops, {G['paczki']} pączki bakeries and {G['mideast']} Middle Eastern places in Dearborn, each checked by hand in October 2026 against a 2025 or 2026 source. It also lists {R:,} restaurants, cafés and bars statewide, checked against the State of Michigan's list of licensed food-service establishments. It is for Michigan residents and visitors deciding where to eat, with no ads, account or tracking.

3. How to use it (no login, no setup, no sample files needed):
- Home → Coney Islands (or Detroit-Style Pizza, Pasties, Pączki Bakeries, Middle Eastern, James Beard Honors, Detroit Inspections, Near Me) → tap any place.
- On a place, tap "Ratings, hours & photos" to open Apple Maps' own place card through MapKit. Directions, Call and Website are below it.
- Search from the Home search box by name, town, street or dish ("coney dearborn", "paczki hamtramck").
- The Map tab shows each guide as pins. "My location" and the Nearest sort use location only if allowed, on the device.
- The heart saves a place on the device, under the Saved tab. The About tab lists the data sources, licenses and the independence statement.
- On iPad, a sidebar replaces the tabs; a place opens in the right-hand column.
- Location: if you're outside Michigan (as App Review usually is), the map says so and stays on Michigan, and distance sorting still works from where you are.
- "MI Eats" is the short Home Screen name of "Michigan Eats: Restaurants".

4. External services and data:
- Apple MapKit: maps, local search to find a place's Apple Maps listing, and Apple's place card for live hours, photos and ratings.
- Core Location: optional, on-device only, for distance sorting.
- Core Spotlight: on-device indexing so places appear in iPhone search.
- No backend, accounts, analytics, advertising, payments or AI services. The restaurant data is bundled in the app.
- Bundled data sources: Overture Maps Foundation open place data (CDLA Permissive 2.0, with Foursquare-sourced records under Apache 2.0 and AllThePlaces under CC0; license texts are in the app); the Michigan Department of Agriculture and Rural Development's open list of licensed food service establishments (no reuse restrictions); the Detroit Health Department's restaurant inspection data and the City of Detroit's liquor license list (data.detroitmi.gov); James Beard Foundation award records (facts only); and our own research of public websites and local news.
- The website with the privacy policy and support page is static and hosted on GitHub Pages: {SITE}

5. Regional differences: none. The content covers Michigan; the app is offered in the United States and works the same everywhere.

6. Regulated or protected material: the app is not in a regulated industry and includes no protected third-party material. The data is open-licensed or public record, with attribution and licenses on the About tab. Ratings, hours and photos are shown only inside Apple's own place card through MapKit; the app stores no ratings or reviews. Detroit inspection results are the City's own, labeled and dated; the app never computes grades. Every website link was checked before release, and adult venues are excluded. The app is independent and not affiliated with any restaurant, agency or the James Beard Foundation.

Support: nick@eatsranked.com"""

# ---------------- checks (nothing is written unless all pass)
problems = []
for label, text, limit in (("name", NAME, 30), ("subtitle", SUB, 30), ("keywords", KW, 100), ("promotional text", PROMO, 170),
                           ("What's New", WHATS_NEW, 4000), ("description", DESC, 4000), ("review notes", REPLY, 4000)):
    if len(text) > limit:
        problems.append(f"{label}: {len(text)} characters, limit {limit}")
title_words = set(re.findall(r"[a-z]+", (NAME + " " + SUB).lower()))
for kw in KW.split(","):
    if kw != kw.strip() or not kw:
        problems.append(f"keyword {kw!r}: no spaces around commas, no empty entries")
    if set(kw.split()) & title_words:
        problems.append(f"keyword {kw!r} repeats a word from the name or subtitle")
for text, label in ((KW, "keywords"), (PROMO, "promotional text"), (SUB, "subtitle"), (WHATS_NEW, "What's New")):
    for bad in (r"\bbest\b", r"\btop\b", r"#1", r"\bfree\b", r"\bevery\b"):
        if re.search(bad, text, re.I):
            problems.append(f"{label}: contains {bad!r}")
if re.search(r"\bevery (?:restaurant|place)\b|\ball [\d,]+ ", DESC + REPLY, re.I):
    problems.append("description/reply: an 'every restaurant' or 'all N' claim the data can't back")
if problems:
    sys.exit("not written:\n  " + "\n  ".join(problems))

listing = {"bundleId": "com.michiganeats.ios", "name": NAME, "subtitle": SUB, "privacyPolicyUrl": SITE + "privacy.html",
           "primaryCategory": "FOOD_AND_DRINK", "secondaryCategory": "TRAVEL", "description": DESC, "keywords": KW,
           "promotionalText": PROMO, "supportUrl": SITE, "marketingUrl": SITE, "reviewNotes": REPLY}
os.makedirs(os.path.join(ROOT, "playbook", "app-store"), exist_ok=True)
json.dump(listing, open(os.path.join(ROOT, "playbook", "app-store", "listing.json"), "w"), indent=1, ensure_ascii=False)

open(os.path.join(ROOT, "playbook", "06-app-store-listing.md"), "w").write(f"""# App Store listing (ASO)

Written by `scripts/make-listing.py` from `site-numbers.json` ({N['generated']}); re-run it after every data refresh, never hand-edit.
The machine copy is `app-store/listing.json` (read by `../scripts/asc_listing.py` once Nick creates the App Store Connect record and
adds `"com.michiganeats.ios": "mi-eats"` to its FOLDERS). The URLs assume michigan.eatsranked.com is live; until Nick's CNAME
resolves, use https://nickstrom5.github.io/michigan-eats/.

## Name (30 max)
`{NAME}` ({len(NAME)})

## Subtitle (30 max)
`{SUB}` ({len(SUB)})

Together they index: michigan, eats, restaurants, coneys, pasties, square, pizza. Home Screen name: MI Eats.

## Keywords (100 max)
`{KW}` ({len(KW)})

- No word repeats the name or subtitle; no trademarks (no Buddy's, Lafayette, Zingerman's, Lions), no "best", "top" or "#1".
- Towns are the biggest win; Kalamazoo, Marquette, Hamtramck and Royal Oak didn't fit. Rotate them in after a month of App Store Connect
  search-term data. Apple's public search can't be used for this research (itunes.apple.com's robots.txt blocks Claude).

## Promotional text (170 max, editable any time without review)
`{PROMO}` ({len(PROMO)})

## Description ({len(DESC)} of 4,000)
```
{DESC}
```

## What's New (1.0)
`{WHATS_NEW}`

## Screenshots
Framed by `scripts/appstore-screenshots.py`: `app-store/iphone/` (8, 1320x2868, the 6.9" slot) and `app-store/ipad/` (6, 2064x2752, the
13" slot). Upload one file at a time in file order and check the order after a reload. No negative board and no place whose latest
Detroit result is "Not in compliance" appears in any image.

## Category and age rating
Primary Food & Drink, secondary Travel. Age rating: alcohol references "Infrequent" (bars, taverns) → 13+; everything else None/No.
Pricing $0.00, available in the United States. Content rights: yes, third-party content, with the rights (open data, public records,
Apple's place card). Untick "Sign-in required".

## App Review
Reply and recording script: `13-app-review-reply.md`. Put the reply in App Review Information → Notes from the start.
""")

open(os.path.join(ROOT, "playbook", "13-app-review-reply.md"), "w").write(f"""# App Review: prepared before submitting (Guideline 2.1 "Information Needed")

Written by `scripts/make-listing.py` ({N['generated']}). Wisconsin's new-developer review asked for a screen recording from a physical
device, starting at launch, plus answers to six questions; Michigan Eats should expect the same. Put the reply below in **App Review
Information → Notes** from the start ({len(REPLY):,} of 4,000 characters), and record the video before submitting. If Apple raises
Guideline 4.3(a), answer with Michigan's own guides and sources (coneys, square pizza, pasties, pączki, Dearborn, Detroit's inspections,
the state license list); never compare with the other state apps in the Notes.

## Screen recording (Nick, on his iPhone, latest iOS, 60–120 seconds, no sound)

Install from TestFlight first (the internal tester's email must be the Apple ID under Settings › your name › Media & Purchases on the
phone, or TestFlight says "not available"). Record with Control Center → Screen Recording:

1. Start on the Home Screen and tap **MI Eats**. The recording must begin with the launch.
2. Home: scroll the cards a little.
3. Tap **Coney Islands**, then **American Coney Island**.
4. Tap **Ratings, hours & photos**; Apple's place card opens. Close it, then scroll to the Detroit Health Department inspection section.
5. Tap the **heart** (Save), then go back to Home.
6. Tap the search box and type `paczki hamtramck`. Open one result.
7. Tap the **Map** tab, then **Coneys**, then a pin and its name.
8. Tap the **Saved** tab, where the saved place shows. Then tap **About** and scroll to the sources.

## Reply text

```
{REPLY}
```
""")
print(f"wrote listing.json, 06-app-store-listing.md, 13-app-review-reply.md | keywords {len(KW)}/100, promo {len(PROMO)}/170, "
      f"description {len(DESC):,}/4,000, reply {len(REPLY):,}/4,000")
