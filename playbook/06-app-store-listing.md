# App Store listing (ASO)

Written by `scripts/make-listing.py` from `site-numbers.json` (2026-10-22); re-run it after every data refresh, never hand-edit.
The machine copy is `app-store/listing.json` (read by `../scripts/asc_listing.py` once Nick creates the App Store Connect record and
adds `"com.michiganeats.ios": "mi-eats"` to its FOLDERS). The URLs assume michigan.eatsranked.com is live; until Nick's CNAME
resolves, use https://nickstrom5.github.io/michigan-eats/.

## Name (30 max)
`Michigan Eats: Restaurants` (26)

## Subtitle (30 max)
`Coneys, Pasties & Square Pizza` (30)

Together they index: michigan, eats, restaurants, coneys, pasties, square, pizza. Home Screen name: MI Eats.

## Keywords (100 max)
`detroit,grand rapids,ann arbor,dearborn,paczki,traverse city,lansing,flint,food guide,mitten,novi` (97)

- No word repeats the name or subtitle; no trademarks (no Buddy's, Lafayette, Zingerman's, Lions), no "best", "top" or "#1".
- Towns are the biggest win; Kalamazoo, Marquette, Hamtramck and Royal Oak didn't fit. Rotate them in after a month of App Store Connect
  search-term data. Apple's public search can't be used for this research (itunes.apple.com's robots.txt blocks Claude).

## Promotional text (170 max, editable any time without review)
`8 coney islands, 13 pączki bakeries, Detroit-style pizza and pasties, each checked by hand. Plus 24,000+ Michigan restaurants near you.` (135)

## Description (2741 of 4,000)
```
Michigan's restaurants, from a coney with everything to a pasty north of the Bridge.

Michigan Eats is a free guide to eating in Michigan: 8 coney islands, 6 Detroit-style pizzerias, 4 pasty shops, 13 pączki bakeries and 7 Middle Eastern places in Dearborn we checked by hand, plus 24,830 restaurants, cafés, bars and bakeries in 988 towns, from Detroit, Grand Rapids and Ann Arbor to Lansing, Traverse City and the U.P. 19,643 of them are on the state's list of licensed food-service establishments. No account, no ads.

MICHIGAN GUIDES
• Coney Islands: Detroit coneys with chili, mustard and onions, starting with downtown's side-by-side rivals.
• Detroit-Style Pizza: square, pan-baked pizza with the crisp cheese edge.
• Pasties: Upper Peninsula pasty shops.
• Pączki Bakeries: where Metro Detroit lines up on Fat Tuesday.
• Middle Eastern: Dearborn's Lebanese and Yemeni kitchens, bakeries and coffee houses.
• Award winners: 13 James Beard semifinalists, finalists and America's Classics.
• Detroit Inspections: the Detroit Health Department's own result for 1,134 places (in compliance or not, with the violations cited), shown as the City publishes it.

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

An independent app, not affiliated with any restaurant, chain or government agency (including the State of Michigan, MDARD, the City of Detroit and the Detroit Health Department), or with the James Beard Foundation. James Beard Foundation and James Beard Award are trademarks of the James Beard Foundation. Place data from Overture Maps Foundation (CDLA Permissive 2.0) and others; sources and licenses are on the About tab.
```

## What's New (1.0)
`First release: coney islands, Detroit-style pizza, pasties, pączki and 24,000+ Michigan restaurants.`

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
