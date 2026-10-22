# Michigan sources (checked 2026-10-22)

Every host was checked with `pipeline/check_sources.py` (RFC 9309 robots matcher, honest UA `MichiganEatsSourceCheck/1.0`)
before its first data request. Raw files: `data/raw/official/` (git-ignored).

## Used

| Source | What | Terms | Cadence | Coverage | Fields used |
|---|---|---|---|---|---|
| **MDARD "Michigan Restaurants and Commissaries"** — `gisagomdard.state.mi.us/arcgis/rest/services/MDARD/RestaurantsCommissariesOpenData/FeatureServer/0` (ArcGIS item f6232e1305d444f7a649b5defaa5f861; robots: no robots.txt, usable) | Every food service establishment (fixed + mobile commissary) licensed by Michigan's 45 local health departments | Item license text: "provided as a public service, and there are no restrictions on the use, reproduction, or distribution of the Information"; AS IS, no warranty | Item modified 2026-04-09; read 2026-10-22 | **34,310 active licenses, statewide, 83 counties, all with a point** (34,158 fixed establishments) | Licensekey, LicensetypeName, LocationName (shown as the name), AddressLine1, City, Zip, County, RegionName (health department), lat/lon. **OrganizationName = license holder: never shown** (can be a person). |
| **Detroit Health Department "Restaurant Inspections"** — data.detroitmi.gov item ffd4ed9aa12a4df5ad13d81175da4e49, CSV via the portal's own download (`/api/download/v1/items/<id>/csv?layers=0,1,2`); robots allows (Crawl-delay 60 respected) | Layer 0 establishments (7,994: id, name, address, license, type, status, point); layer 1 inspections (16,421, **2021-10-22 → 2026-10-05**: type, `is_in_compliance`, counts of Priority / Priority Foundation / Core violations); layer 2 violations (30,880 cited items) | City open data portal; no license field on the item; page copyright says City material needs permission → **ask Nick / check Detroit's open data terms before the app ships Detroit data** (other cities' portals are public domain; Detroit's terms page is a JS app we couldn't read) | "Updated monthly"; records within ~30 days of an update are missing | City of Detroit only (~3,200 food service establishments open) | Shown: the City's own result of the latest **routine** inspection ("In compliance" / "Not in compliance") and the P / Pf / Core counts, with history. Attempted visits, closures, complaints and plan reviews carry no result (they all read True) and are not shown. |
| **Detroit "Liquor Licenses"** — data.detroitmi.gov item 990a559e64754eb4a2e3cf34fce6516f | The City's copy of the MLCC list for Detroit (2,014 licenses: Class C, Tavern, SDM, SDD, Club, B-Hotel, Brew Pub, makers) | as above | City refreshes from the State list on the 1st of each month | Detroit only | DBA (Account Name = holder, never shown), type, status, point → "serves alcohol" in Detroit |
| **Ottawa County "Food Inspection Location"** — services2.arcgis.com/ixRLoNIl4gmM9jgg/.../Food_Inspection_Location_View/FeatureServer/1 (the county's public ArcGIS Experience "Food Inspection Reports") | 816 locations, each with a link to its inspection-report PDF viewer (onbaseweb.miottawa.org, robots usable, page returns 200) | county public app | — | Ottawa County | **Not wired in yet.** Candidate per-place "official records" link; no results in bulk. Check that a link renders in a browser before shipping. |
| Overture Maps places 2026-09-23.1 | statewide base, 40,082 eating/drinking listings in MI | CDLA-Permissive-2.0 / Apache-2.0 (+ Foursquare NOTICE) | monthly releases | statewide | as in other states |
| Overture divisions (state + 83 counties, land areas) | outlines, county assignment | ODbL (OSM-derived): leaderboard only; attribute or don't ship in the app | | | |
| UCSD Google Local 2021 (`meta-Michigan.json.gz`) | ratings, reviews, price — **web leaderboard only, never the app** | research dataset | frozen 2021 | 27,077 food listings | |

## Checked, not usable (no bulk data, or blocked)

| Source | Verdict |
|---|---|
| Michigan Liquor Control Commission statewide list (michigan.gov/lara/bureau-list/lcc/licensing-list, weekly Excel) | michigan.gov answers robots.txt with **403 (bot check)**. **Nick can download the Excel by hand** into `data/raw/official/manual/` if he wants "serves alcohol" statewide. |
| MDARD MiSafe inspections | grocery / retail food, not restaurants: never presented as restaurant inspections. |
| Washtenaw County (washtenaw.org/1613/Restaurant-Inspection-Reports) | page has no data or search link we can read; no bulk data. |
| Oakland County (oakgov.com → oaklandcountymi.gov, "OCinspections" Sword Solutions portal) | search portal only, no bulk download. |
| Wayne County outside Detroit (waynecounty.com) | robots usable; no inspection data published. |
| Kent County (accesskent.com) | bot check (403). |
| Ingham County (hd.ingham.org) | robots.txt disallows ClaudeBot, Claude-User, anthropic-ai. |
| Kalamazoo County (kalcounty.com) | bot check. |
| Macomb County (macombgov.org) | robots.txt disallows ClaudeBot, anthropic-ai. |
| inspections.myhealthdepartment.com (used by several LHDs nationally) | bot check. |
| Property values | Detroit publishes parcels / assessment rolls (data.detroitmi.gov), but only for Detroit; no statewide open values → **no building-value board**. |
| MICHELIN | no Michigan guide; nothing implied. |

## Press hosts (for hand-checked guides)

usable: wxyz.com, fox2detroit.com, hourdetroit.com, bridgedetroit.com, metrotimes.com, secondwavemedia.com, wzzm13.com, miningjournal.net, pasty.com, jamesbeard.org, detroitmi.gov.
**blocked** (robots): freep.com, mlive.com, detroitnews.com, eater.com/detroit.eater.com, lansingstatejournal.com, record-eagle.com, outliermedia.org; crainsdetroit.com (bot check); michiganradio.org unreachable.

## Calibration (2026-10-22, `data/mi/calibration.json`)

Michigan is the first state with **one statewide list of every licensed food service establishment**, so the listing test is statewide
(county by county), not three cities. Share of cleaned listings matched to an active MDARD license:

| Listing group | n | matched |
|---|---|---|
| Meta + open in Google 2021 | 14,704 | **77.4%** |
| Meta only | 11,006 | 41.7% |
| Meta ≥0.95 (app grouping) | 16,025 | 76.4% |
| Meta 0.90–0.95 (app) | 5,253 | 53.9% |
| Meta <0.90 (app) | 4,575 | 20.3% |
| Chain store lists only | 495 | 47.7% |
| Foursquare / BrightQuery / Microsoft + Google 2021 | 4,192 | 22.6% |
| Microsoft only | 1,400 | 27.9% |
| BrightQuery only | 2,850 | 15.1% |
| Foursquare only | 3,333 | **6.6%** |
| Google 2021 says closed | 1,358 | 3.8% |

Lower bounds: a bar that serves no food needs no food license, and a renamed place misses. The rates match Chicago's (Meta + Google
open 74%, Foursquare-only 5–14%), so the playbook's keep rules stand (web: Meta and chain feeds, minus Google-closed; app: Meta ≥0.95,
Meta 0.90–0.95 with a website, chain feeds, licensed, hand-checked).

Coverage the other way: open map listings hold **59.5% of the 29,050 licensed fixed food service establishments** (Detroit 40.6% of
3,099). That gap is why licensed places with a food word in their name are added from the list (3,118 rows on the web build).

## First build (web, 2026-10-22)

30,189 places, 28,392 restaurants, 1,055 towns; 19,667 matched to an official record; 1,268 Detroit places with the City's latest
routine result (991 in compliance, 277 not); 11 adult clubs removed (8 via Overture's adult category: review "Chapeau Vert Lounge",
"Bev's Backstreet Lounge", "BTS Lounge" by hand, possible false positives).
