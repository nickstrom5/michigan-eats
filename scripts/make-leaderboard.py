"""Builds site/index.html (the private web leaderboard) from wi-eats/site/index.html, with Michigan's boards, sources and palette.
Ported from tx-eats/scripts/make-leaderboard.py (itself from co-eats).
Every replacement is asserted, so a change in the Wisconsin page fails loudly instead of leaving Wisconsin text behind.
Usage: .venv/bin/python scripts/make-leaderboard.py"""
import os, re, sys
ROOT = os.path.join(os.path.dirname(__file__), "..")
src = open(os.path.join(ROOT, "..", "wi-eats", "site", "index.html")).read()
s = src
def R(a, b, n=1):
    global s
    c = s.count(a)
    if c != n:
        sys.exit(f"expected {n} of {a[:90]!r}, found {c}")
    s = s.replace(a, b)

# ---------------- head, palette, type
R('<title>Wisconsin Restaurant Leaderboard</title>', '<meta charset="utf-8">\n<title>Michigan Restaurant Leaderboard</title>')
R('<meta name="description" content="Every restaurant in Wisconsin, ranked on ratings, popularity, fish fry, supper clubs, custard, value and estimated sales.">',
  '<meta name="description" content="Every restaurant in Michigan, ranked on ratings, popularity, honors, value and sales, with the state\'s food-service licenses and Detroit\'s official inspection results.">')
R('family=Saira+Extra+Condensed:wght@600;700;800;900&family=Source+Sans+3:ital,wght@0,400;0,500;0,600;0,700;1,400', 'family=Oswald:wght@500;600;700&family=Public+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400')
R('''  /* Packers: green #203731, gold #FFB612, white. Light-only by design; gold is a fill with green text on it, never text on white. */
  color-scheme:light;
  --bg:#FFFFFF; --surface:#FFFFFF; --surface-2:#F1F5F2; --surface-3:#E1EAE4;
  --ink:#14241D; --ink-2:#2E4238; --muted:#53665B; --rule:#DAE3DD; --rule-2:#B6C6BC;
  --green:#203731; --green-2:#2D5242; --gold:#FFB612; --gold-soft:#FFE7A8; --on-gold:#203731;
  --map-fill:#EEF3EF; --map-line:#C2D1C7; --dot-edge:rgba(20,36,29,.35);
  --seq1:#CFE2D5; --seq2:#9CC4A9; --seq3:#5F9A74; --seq4:#326B4B; --seq5:#203731;
  --scrim:rgba(20,36,29,.38);
  --shadow:0 1px 2px rgba(20,36,29,.06),0 8px 28px rgba(20,36,29,.10);
  --display:"Saira Extra Condensed","Arial Narrow","Roboto Condensed",sans-serif;
  --body:"Source Sans 3",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;''',
'''  /* Layout: sticky leaderboard tabs over a filter rail + ranked list; one Michigan element, a Great Lakes shoreline band under the
     header. Nick's palette (2026-10-22): Great Lakes blue #1B6EA8 and Northwoods pine #2E5E47 on white, deep lake #0D3F63 for
     headings and the icon ground. "gold" here is the pine used as a fill under white text (7.3:1); its soft tint is a fill under pine
     text. Light-only by design, like the other leaderboards: every color is set explicitly below. */
  color-scheme:light;
  --bg:#FFFFFF; --surface:#FFFFFF; --surface-2:#F2F6F8; --surface-3:#E1EAEF;
  --ink:#0C1D2A; --ink-2:#24384A; --muted:#536575; --rule:#DAE3EA; --rule-2:#B3C4D0;
  --green:#0D3F63; --green-2:#1B6EA8; --gold:#2E5E47; --gold-soft:#E1EEE7; --on-gold:#FFFFFF; --red:#1B6EA8;
  --map-fill:#F0F5F7; --map-line:#C2D0DA; --dot-edge:rgba(12,29,42,.35);
  --seq1:#D2E4F1; --seq2:#99C1DF; --seq3:#4F8FC2; --seq4:#1B6EA8; --seq5:#0D3F63;
  --scrim:rgba(12,29,42,.38);
  --shadow:0 1px 2px rgba(12,29,42,.06),0 8px 28px rgba(12,29,42,.10);
  --display:"Oswald","Arial Narrow","Roboto Condensed",sans-serif;
  --body:"Public Sans",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;''')
R('body{margin:0;background:var(--bg);', 'html,body{background:var(--bg)}\nbody{margin:0;background:var(--bg);')
R('.hmid{padding:22px 16px 18px;border-bottom:4px solid var(--gold)}', '.hmid{padding:22px 16px 10px}\n.ridge{display:block;width:100%;height:22px;margin-top:-1px}\n.ridge .r1{fill:var(--green)} .ridge .r2{fill:#E3D5AE} .ridge .r3{fill:#1B6EA8}')
R('.tab.wi{border-color:#D9A21A;background:#FFF9EA}', '.tab.wi{border-color:#2E5E47;background:#EEF5F1}')
R('.chips.wi .chip[aria-pressed="false"]{background:#FFF9EA;border-color:#D9A21A}', '.chips.wi .chip[aria-pressed="false"]{background:#EEF5F1;border-color:#2E5E47}')
R('.badge.sc{background:var(--gold-soft);color:var(--on-gold)}', '.badge.sc{background:var(--gold-soft);color:#2E5E47}\n.badge.mi{background:var(--red);color:#fff}\n.res{display:inline-block;font:700 11.5px/1.5 var(--body);letter-spacing:.04em;text-transform:uppercase;padding:1px 7px;border-radius:5px;white-space:nowrap}\n.res-0{background:#DDEFE3;color:#0E5A2B} .res-1{background:#FFE9C2;color:#6B3A00} .res-2{background:#F9D5DB;color:#7A0019}\n.res-3{background:#DDEFE3;color:#0E5A2B} .res-4{background:#F9D5DB;color:#7A0019} .res-5{background:#DDEFE3;color:#0E5A2B} .res-6{background:#E3ECF8;color:#1C3F86} .res-7{background:#FFE9C2;color:#6B3A00} .res-8{background:#F9D5DB;color:#7A0019}')
R('.fhint{font-size:12.5px;color:#8A4B00;margin:0}', '.fhint{font-size:12.5px;color:#8A4B00;margin:0}')
R('#map{display:block;width:100%;max-width:min(760px,max(240px,calc((100dvh - var(--stickyH) - 120px) * 0.95)));margin:0 auto;aspect-ratio:0.95;touch-action:manipulation}',
  '#map{display:block;width:100%;max-width:min(760px,max(240px,calc((100dvh - var(--stickyH) - 120px) * 0.9)));margin:0 auto;aspect-ratio:0.9;touch-action:manipulation}')
R('@media (max-height:500px){#map{max-width:max(160px,calc((100dvh - var(--stickyH) - 70px) * 0.95))}}', '@media (max-height:500px){#map{max-width:max(160px,calc((100dvh - var(--stickyH) - 70px) * 0.9))}}')

# ---------------- header and filters
# a Great Lakes shoreline band (Nick, 2026-10-22): deep lake, a sand beach line, lake-blue water (laid flat, no map or team marks)
RIDGE = ('<svg class="ridge" viewBox="0 0 1200 22" preserveAspectRatio="none" aria-hidden="true">'
         '<rect class="r1" x="0" y="0" width="1200" height="8"/><rect class="r2" x="0" y="8" width="1200" height="5"/>'
         '<path class="r3" d="M0 13 Q150 10 300 13 T600 13 T900 13 T1200 13 V22 H0Z"/></svg>')
R('''    <p class="kicker" id="kicker">Wisconsin · map listings as of Sep 2026</p>
    <h1 id="h1">Every Wisconsin restaurant, <span class="count">ranked</span></h1>
    <p class="lede" id="lede">Supper clubs, taverns, custard stands, Friday fish fries and the places in between, from Superior to Kenosha. Each one is ranked on ratings, popularity, value and estimated sales, with Wisconsin's own boards for fish fry, supper clubs, custard and cheese curds. Flip any leaderboard to see the bottom.</p>
  </div></div>''',
'''    <p class="kicker" id="kicker">Michigan · map listings as of Sep 2026</p>
    <h1 id="h1">Every Michigan restaurant, <span class="count">ranked</span></h1>
    <p class="lede" id="lede">Coney islands, square pizza, pasty shops, Dearborn bakeries, lakeshore fish fries and the places in between, from Monroe to Copper Harbor. Each one is ranked on ratings, popularity, value and sales, checked against the state's list of licensed food-service establishments, with the Detroit Health Department's own inspection results. Flip any leaderboard to see the bottom.</p>
  </div></div>''' + RIDGE)
R('<select id="city"><option value="">All of Wisconsin</option></select>', '<select id="city"><option value="">All of Michigan</option></select>')
R('<span class="flabel" id="l-tags">Wisconsin classics</span>', '<span class="flabel" id="l-tags">Michigan guides</span>')
R('<label class="toggle"><input type="checkbox" id="confirmed"> Only confirmed places (on a Milwaukee or Dane County license list, or in two sources)</label>',
  '<label class="toggle"><input type="checkbox" id="confirmed"> Only confirmed places (on the state\'s food-service license list or a Detroit record, or in two sources)</label>')
R('<p class="wnote">Each ingredient is a 0–100 percentile across Wisconsin.', '<p class="wnote">Each ingredient is a 0–100 percentile across Michigan.')
R('WI Score recipe: <span id="wname">', 'MI Score recipe: <span id="wname">')
R('placeholder="Search name, town, street, zip, “fish fry”…"', 'placeholder="Search name, town, street, zip, “coney”…"')

# ---------------- constants
R('const TAGS = [["supper","Supper clubs",1],["fishfry","Fish fry",2],["custard","Frozen custard",8],["curds","Cheese curds",4]];',
  'let HAVE_TAGS = 0;\nconst TAGS_ALL = [["coney","Coney islands",1],["dpizza","Detroit-style pizza",2],["pasty","Pasties",4],["paczki","Pączki bakeries",8],["mideast","Middle Eastern",16],["fishfry","Fish fry & supper clubs",32],["oldest","Oldest places",64]];\nlet TAGS = [];')
R('const JUR = ["", "City of Milwaukee", "Public Health Madison & Dane County"];', 'const JUR = ["", "food-service license (MDARD list)", "Detroit Health Department establishment record", "Detroit liquor license (MLCC)"];')
R('research:"our verified list, placed with its Google listing"', 'research:"our hand-checked list, placed on its street address"')
R('try { S = sanitize(JSON.parse(localStorage.getItem("wi-eats") || "null")); }', 'try { S = sanitize(JSON.parse(localStorage.getItem("mi-eats") || "null")); }')
R('localStorage.setItem("wi-eats", JSON.stringify(rest));', 'localStorage.setItem("mi-eats", JSON.stringify(rest));')
R('let D = [], META = {}, SHAPES = null, WI_BOUNDS = null,', 'let D = [], META = {}, SHAPES = null, WI_BOUNDS = null, RESN = ["In compliance", "Not in compliance"], INSJ = ["Detroit"],')

# ---------------- boards
a = s.index('const sigShow = '); b = s.index('const board = () =>')
BOARDS = r'''const ratedShow = r => [stars(r.rating), revs(r)+(r.reviews === 1 ? " review" : " reviews")+" ('21)"];
const resPill = r => `<span class="res res-${r.in_r === 0 ? 0 : 1}">${esc(INSJ[r.in_j])} · ${esc(RESN[r.in_r])}</span>`;
const MI_TXT = ["", "MICHELIN Recommended", "Bib Gourmand", "1 MICHELIN Star", "2 MICHELIN Stars", "3 MICHELIN Stars"];
const B = [
  {id:"overall", tab:"MI Score", top:"Top MI Score", bottom:"Lowest MI Score", metric:"MI Score", val:r=>r.score,
   sub:()=>"A blend of rating, popularity, value and estimated profit, weighted by the MI Score recipe in the filters. Places missing some data are pulled toward 40, a little below the middle. A James Beard honor sets a floor: 85 for an America's Classic or a win, 80 for a finalist, 72 for a semifinalist. (Michigan has no MICHELIN Guide.)",
   show:r=>[Math.round(r.score), "MI Score"]},
  {id:"rating", tab:"Rating", top:"Highest rated", bottom:"Lowest rated", metric:"rating", val:r=>r.bayes, need:(r,d)=>r.reviews >= (d==="top"?15:40),
   sub:"Google star rating as of the Sep 2021 snapshot, adjusted for review count so a 5.0 from three friends doesn't beat a 4.8 from 3,000 strangers.",
   show:ratedShow, dup:"rating"},
  {id:"popular", tab:"Popularity", top:"Most popular", bottom:"Least popular", metric:"reviews", val:r=>r.reviews, need:r=>r.reviews!=null,
   sub:"Total Google reviews as of Sep 2021: the best public stand-in for how many people walk through the door. Places opened since aren't in the snapshot, and the snapshot caps counts at 9,998 (shown as 9,998+).",
   show:r=>[revs(r), (r.reviews === 1 ? "review" : "reviews")+" ('21) · "+stars(r.rating)], dup:"rating"},
  {id:"gems", tab:"Hidden gems", top:"Hidden gems", bottom:"Popular but panned", metric:"rating", val:r=>r.gem, need:(r,d)=> d==="top" ? (r.reviews>=20 && r.reviews<=250 && r.chain_n<5) : r.reviews>=600,
   sub:"Top: independents with 20–250 reviews and great ratings. Bottom: places with 600+ reviews and the lowest ratings. Both from the Sep 2021 snapshot.",
   show:ratedShow, dup:"rating"},
  {id:"coney", wi:true, tagbit:1, tab:"Coney islands", top:"Coney islands, highest rated", bottom:"Coney islands, lowest rated", metric:"rating", val:r=>r.bayes, need:(r,d)=>(r.tags & 1) && r.reviews >= (d==="top"?15:30),
   sub:"Detroit- and Flint-style coney islands: a natural-casing hot dog, beanless chili, mustard and onions. Hand-checked: each place confirmed open with a 2025–26 source. Ranked by Google rating (Sep 2021), adjusted for review count.",
   show:ratedShow, dup:"rating"},
  {id:"dpizza", wi:true, tagbit:2, tab:"Detroit-style pizza", top:"Detroit-style pizza, highest rated", bottom:"Detroit-style pizza, lowest rated", metric:"rating", val:r=>r.bayes, need:(r,d)=>(r.tags & 2) && r.reviews >= (d==="top"?15:30),
   sub:"Square, pan-baked pizza with the caramelized cheese edge. Hand-checked: each place confirmed open with a 2025–26 source. Ranked by Google rating (Sep 2021), adjusted for review count.",
   show:ratedShow, dup:"rating"},
  {id:"pasty", wi:true, tagbit:4, tab:"Pasties", top:"Pasties, highest rated", bottom:"Pasties, lowest rated", metric:"rating", val:r=>r.bayes, need:(r,d)=>(r.tags & 4) && r.reviews >= (d==="top"?10:30),
   sub:"Pasty shops, most of them in the Upper Peninsula. Hand-checked: each place confirmed open with a 2025–26 source. Ranked by Google rating (Sep 2021), adjusted for review count.",
   show:ratedShow, dup:"rating"},
  {id:"iconic", tab:"Iconic", top:"Most iconic", bottom:"Least iconic", metric:"iconic points", val:r=>r.s_icon, need:r=>r.s_icon!=null,
   sub:"Only places with an honor or a long, verified history: James Beard awards and nominations 2025–26, America's Classics, and places we verified open at the same address since 1960 or earlier. Points for honors, years open and how many people know it.",
   show:r=>[Math.round(r.s_icon), "iconic pts" + (r.founded ? " · since " + r.founded : "")]},
  {id:"value", tab:"Value", top:"Best bang for buck", bottom:"Worst value", metric:"value score", val:r=>r.value_raw, need:r=>r.rating!=null,
   sub:"Rating (2021) relative to price level: a 4.7 at $ beats a 4.7 at $$$.",
   show:r=>[stars(r.rating)+" "+dollars(r.price)+(r.price_est?ESTTAG:""), "value "+Math.round(r.i_value)+" · rating '21"], dup:"rating"},
  {id:"price", tab:"Price", top:"Priciest", bottom:"Cheapest", metric:"price", val:r=>r.spend,
   sub:"Google price level (filled in from the chain or cuisine when missing, and marked est.) with typical spend per person. Within a price level, ties are ordered by MI Score.",
   show:r=>[dollars(r.price)+(r.price_est?ESTTAG:""), "~$"+r.spend+"/person "+ESTTAG]},
  {id:"sales", tab:"Sales", top:"Highest sales", bottom:"Lowest sales", metric:"sales", val:r=>r.rev, need:(r,d)=>r.rev!=null && (d==="top" || r.rev_src!=="model-low"), est:true,
   sub:d=>`Estimated yearly sales. Locations of chains with a published average (${META.model?.n_chains ?? "80+"} brands) use that average scaled by how busy the location is; independents use a model.` + (d==="bottom" ? " This end leaves out places with no review data (their figures are rough placeholders). The model never goes below $100K a year, so the very bottom is a tie, ordered by MI Score." : ""),
   show:r=>[money(r.rev), "sales/yr · " + src(r)], dup:"sales"},
  {id:"profit", tab:"Profit", top:"Most profitable", bottom:"Least profitable", metric:"profit", val:r=>r.profit, need:(r,d)=>r.profit!=null && (d==="top" || r.rev_src!=="model-low"), est:true,
   sub:d=>"Estimated yearly pre-tax profit: estimated sales × a typical margin for the segment, nudged by how well-loved the place is." + (d==="bottom" ? " This end leaves out places with no review data (their figures are rough placeholders). The sales model never goes below $100K a year, so the very bottom is mostly places at that floor, ordered by margin and then MI Score." : ""),
   show:r=>[money(r.profit), "profit/yr "+ESTTAG]},
  {id:"clean", tab:"Detroit inspections", top:"In compliance, fewest priority violations", bottom:"Not in compliance at latest inspection", metric:"inspection result", val:r=>r.in_r == null ? null : (r.in_r === 0 ? 100 : 0) - r.in_p, need:r=>r.in_r!=null,
   sub:d=>`Detroit only: the Detroit Health Department is the one Michigan health department that publishes inspection results in bulk (the others offer search pages, or nothing online). Each place shows the result of its latest routine inspection as the City published it, "in compliance" or "not in compliance", and the number of Priority and Priority Foundation violations cited (the serious kinds). Routine inspections through ${esc((META.inspections_through||{}).det || "")}; the City publishes about a month late. We compute no grade, and the placard on the door can differ: it also reflects enforcement and license status.` + (d==="bottom" ? " One inspection is a snapshot of one day, and a violation corrected on the spot still counts." : ""),
   show:r=>[`${resPill(r)}`, `${r.in_p} priority · ${esc(r.in_d)}`], dup:"grade"},
];'''
s = s[:a] + BOARDS + "\n" + s[b:]

# ---------------- honors lift the MI Score: a James Beard place that opened after the 2021 snapshot has no rating data, so the blend
# alone would pull it to 40 (Nick on Texas, 2026-10-20: "the score would be higher"). Michigan has no MICHELIN Guide, so mi is always 0.
R("""    r.score = have ? (sum/have)*(have/weightTotal) + 40*(1 - have/weightTotal) : 40;
  }""", """    r.score = have ? (sum/have)*(have/weightTotal) + 40*(1 - have/weightTotal) : 40;
    // an honor sets a floor: 1+ MICHELIN Star 92, Bib Gourmand or America's Classic or a James Beard win 85, a finalist 80,
    // MICHELIN Recommended 78, a semifinalist 72
    const h = r.hon || 0, mi = r.mi || 0;
    const floor = Math.max(mi >= 3 ? 92 : mi === 2 ? 85 : mi === 1 ? 78 : 0, (h & 3) ? 85 : (h & 4) ? 80 : (h & 8) ? 72 : 0);
    if (floor > r.score) r.score = floor;
  }""")
# ---------------- rows, badges, stats
R('''  if (r.hon & 1) h += `<span class="badge jbf">America's Classic</span>`;''',
  '''  if (r.mi) h += `<span class="badge mi">${MI_TXT[r.mi]}</span>`;
  if (r.hon & 1) h += `<span class="badge jbf">America's Classic</span>`;''')
R('''  if ((r.hon & 16) && !(r.hon & 7)) h += `<span class="badge icon">Icon</span>`;
  if ((r.tags & 1) && !/supper ?club/i.test(r.name)) h += `<span class="badge sc">Supper club</span>`;''',
  '''  if ((r.hon & 16) && r.founded) h += `<span class="badge icon">Since ${esc(r.founded)}</span>`;
  if (r.tags & 1) h += `<span class="badge sc">Coney island</span>`;
  if (r.tags & 2) h += `<span class="badge sc">Detroit-style pizza</span>`;
  if (r.tags & 4) h += `<span class="badge sc">Pasties</span>`;
  if (r.tags & 8) h += `<span class="badge sc">Pączki</span>`;
  if (r.tags & 16) h += `<span class="badge sc">Middle Eastern</span>`;
  if (r.tags & 32) h += `<span class="badge sc">Fish fry</span>`;''')
R('''  if (r.ff_n >= 3 && b.id !== "fishfry") bits.push(`<span>${r.ff_n} <i>fish fry mentions</i></span>`);
  if (r.grade) bits.push(`<span class="${dup("grade")}" title="Our grade from Dane County inspection results, not an official grade"><span class="grade sm g-${r.grade}">${r.grade}</span> <i>our inspection grade</i></span>`);''',
  '''  if (r.in_r != null) bits.push(`<span class="${dup("grade")}" title="Latest routine inspection, as the Detroit Health Department published it">${resPill(r)} <i>${r.in_p} priority violations · ${esc(r.addr || "")} · inspected ${esc(r.in_d)}</i></span>`);''')
R('''  if (S.board !== "overall" && r.score != null) bits.push(`<span>${Math.round(r.score)} <i>WI Score</i></span>`);''',
  '''  if (S.board !== "overall" && r.score != null) bits.push(`<span>${Math.round(r.score)} <i>MI Score</i></span>`);''')
R('''const TAG_PH = [["friday fish fry","fishfry"],["fish fries","fishfry"],["fish fry","fishfry"],["fishfry","fishfry"],["supper clubs","supper"],["supper club","supper"],
  ["supperclub","supper"],["frozen custard","custard"],["custard","custard"],["cheese curds","curds"],["cheese curd","curds"],["curds","curds"]].map(([p, t]) => [norm(p), t]);''',
  '''const TAG_PH_ALL = [["coney islands","coney"],["coney island","coney"],["coneys","coney"],["detroit style pizza","dpizza"],["detroit style","dpizza"],
  ["pasties","pasty"],["pasty","pasty"],["paczki","paczki"],["fish fry","fishfry"],["fish fries","fishfry"],["supper club","fishfry"]]
  .map(([p, t]) => [norm(p), t]);
let TAG_PH = [];''')
R('''  // "fish fry", "supper club", "custard", "cheese curds" mean the Wisconsin tags, not words in a name''', '''  // "coney", "pasty", "paczki" mean the Michigan guides, not words in a name''')
R('''  // "fond du lac fish fry" means the town; "green bay rd" or "madison st" is a street, not the town''', '''  // "hamtramck paczki" means the town; "michigan ave" or "grand river ave" is a street, not the town''')
R('''  // a town named in the search ("fond du lac fish fry") narrows to it; a place NAMED that way still counts''', '''  // a town named in the search ("hamtramck paczki") narrows to it; a place NAMED that way still counts''')
R('''    return `No places match “${esc(S.q.trim())}” in Wisconsin.''', '''    return `No places match “${esc(S.q.trim())}” in Michigan.''')
R('''  const setPh = () => { $("#q").placeholder = innerWidth < 400 ? "Search name, town, street…" : "Search name, town, street, zip, “fish fry”…"; };''', '''  const setPh = () => { $("#q").placeholder = innerWidth < 400 ? "Search name, town, street…" : "Search name, town, street, zip, “coney”…"; };''')
R('''  if (S.board === "overall" && !weightTotal) return `The WI Score recipe is empty.''', '''  if (S.board === "overall" && !weightTotal) return `The MI Score recipe is empty.''')
R('''  if (pool.length && board().id === "clean") return `${plural(pool.length, "place matches", "places match")} ${what}, but inspection results are only published for Dane County (Madison and its suburbs). ${f.length ? undo + " to see them." : ""}`;''',
  '''  if (pool.length && board().id === "clean") return `${plural(pool.length, "place matches", "places match")} ${what}, but inspection results are only published in bulk for Detroit. ${f.length ? undo + " to see them." : ""}`;''')
R('''"All of Wisconsin"}</option>`''', '''"All of Michigan"}</option>`''')
R('''$("#cityhint").textContent = `No Wisconsin town matches''', '''$("#cityhint").textContent = `No Michigan town matches''')
R('''    else if (cityFromBox && S.city) { S.city = ""; cityFromBox = false; rerender(); }   // "Wausauk" is no longer Wausau''', '''    else if (cityFromBox && S.city) { S.city = ""; cityFromBox = false; rerender(); }   // "Novii" is no longer Novi''')
R('''    const hit = CITY_N.get(v) || (CITIES.find(([c]) => (" " + norm(c)).includes(" " + v)) || [])[0];   // CITIES is biggest first: "bay" -> Green Bay''',
  '''    const hit = CITY_N.get(v) || (CITIES.find(([c]) => (" " + norm(c)).includes(" " + v)) || [])[0];   // CITIES is biggest first: "rapids" -> Grand Rapids''')
R('''const cols = [["name","City or town"],["n","Places","r"],["score","Avg WI Score","r"]''', '''const cols = [["name","City or town"],["n","Places","r"],["score","Avg MI Score","r"]''')

# ---------------- map
R('shapesPending = fetchJSON("wi_shapes.json").then(j => {', 'shapesPending = fetchJSON("mi_shapes.json").then(j => {')
R("WI_BOUNDS = a[0] < a[1] ? a : [-92.9, -86.8, 42.49, 47.08];", "WI_BOUNDS = a[0] < a[1] ? a : [-90.42, -82.41, 41.69, 48.31];")
R("const w = c.clientWidth || 600, h = Math.round(w / 0.95);", "const w = c.clientWidth || 600, h = Math.round(w / 0.9);")
R("  ctx.save(); land(); ctx.clip(\"evenodd\");   // county lines stop at the shore", "  ctx.save(); land(); ctx.clip(\"evenodd\");   // county lines stop at the shore")
R('''  $("#live").textContent = pool.length === 1 ? `Only one place matches your filters: ${r.name}.` : `Random pick: ${r.name}, ${r.city || "Wisconsin"}.`;''',
  '''  $("#live").textContent = pool.length === 1 ? `Only one place matches your filters: ${r.name}.` : `Random pick: ${r.name}, ${r.city || "Michigan"}.`;''')

# ---------------- drawer
a = s.index('function calibNote(r) {'); b = s.index('function sigCard(n, rt, what)')
s = s[:a] + r'''function calibNote(r) {
  const c = (META.calibration || {}).areas || {}, g = k => [c["Michigan (statewide)"]?.groups?.[k]].filter(Boolean);
  const range = k => { const v = g(k).map(x => x.official); if (!v.length) return null; const lo = Math.min(...v), hi = Math.max(...v); return lo === hi ? pctTxt(lo) : `${pctTxt(lo)}–${pctTxt(hi)}`; };
  const feed = r.src === "AllThePlaces" || r.src === "DAC", checked = r.hc ? " It's also on our hand-checked list." : "";
  if (r.src === "research") return "This place isn't in the map listings as a place to eat. It's on our hand-checked list and placed on its street address.";
  if (r.tier === 2) return (r.src === "official" ? `This place comes straight from the ${esc(JUR[r.jur])} list. The map listings we use didn't have it, so its location comes from the record.` : `Matched to a ${esc(JUR[r.jur])}, so it's confirmed as a licensed business.`) + checked;
  const via = feed ? (r.tier === 1 ? "brand feed + Google 2021" : "brand feed only") : r.src === "meta" ? (r.tier === 1 ? "Meta + open in Google 2021" : "Meta only") : null;
  const rate = via ? range(via) : null, kind = feed ? "chain store-list listings" : "listings";
  if (!via) return "Kept because it's on our hand-checked list, even though its only map listing comes from a source that's usually unreliable.";
  if (r.tier === 1) return `Found in two independent sources: a map listing and Google's 2021 data, but not matched to a license. Checked against the state's list of licensed food-service establishments, ${kind} like this matched a license ${rate || "most"} of the time; a bar that serves no food needs no food license.` + checked;
  return `Found in one map source only, and not matched to a license. Checked against the state's list of licensed food-service establishments, single-source ${kind} like this matched a license ${rate || "less than half"} of the time, so this one may be closed or misfiled.` + checked;
}
''' + s[b:]
R('''  const gq = encodeURIComponent(`${r.name} ${r.addr || ""} ${r.city || ""} WI`);''', '''  const gq = encodeURIComponent(`${r.name} ${r.addr || ""} ${r.city || ""} MI`);''')
R('''  const heroLbl = r.score == null ? (weightTotal ? "No WI Score: not enough data" : "WI Score recipe is empty")
    : ri >= 0 ? `WI Score · #${fmtN(ri+1)} of ${fmtN(L.length)} with your filters (ignoring search)` : "WI Score · outside your current filters";''',
  '''  const heroLbl = r.score == null ? (weightTotal ? "No MI Score: not enough data" : "MI Score recipe is empty")
    : ri >= 0 ? `MI Score · #${fmtN(ri+1)} of ${fmtN(L.length)} with your filters (ignoring search)` : "MI Score · outside your current filters";''')
R('''  const cats = `<div class="dsec"><h3>Category scores (percentile vs. all Wisconsin places)</h3>''', '''  const cats = `<div class="dsec"><h3>Category scores (percentile vs. all Michigan places)</h3>''')
a = s.index('  const sig = [sigCard('); b = s.index('  const moneyNote = {')
s = s[:a] + s[b:]
R('''This location isn't in the 2021 review snapshot, so this uses 85% of the chain's published U.S. average sales per location." : "Based on the chain's published U.S. average sales per location, scaled up or down by how busy this location was (2021 reviews) compared with the chain's other Wisconsin locations.",''',
  '''This location isn't in the 2021 review snapshot, so this uses 85% of the chain's published U.S. average sales per location." : "Based on the chain's published U.S. average sales per location, scaled up or down by how busy this location was (2021 reviews) compared with the chain's other Michigan locations.",''')
R('''scaled by 2021 review volume relative to similar Wisconsin places''', '''scaled by 2021 review volume relative to similar Michigan places''')
a = s.index('  const honorsList = ['); b = s.index('  $("#drawer").innerHTML = `${dhead(')
s = s[:a] + r'''  const honorsList = [...(x.jbf ? x.jbf.split(/;\s(?![^()]*\))/).map(v => "James Beard: " + v) : [])];
  const tagsTxt = TAGS.filter(([, , bit]) => r.tags & bit).map(([, l]) => l);
  const facts = (x.note || x.dishes || x.founded_note || x.seasonal) ? `<div class="dsec"><h3>Hand-checked facts</h3>${x.note ? `<p style="margin:0 0 8px;color:var(--ink-2);font-size:14px">${esc(x.note)}</p>` : ""}
      ${kv([x.dishes ? ["On the menu", esc(x.dishes.split("; ").join(", "))] : null, x.founded ? ["Open here since", esc(x.founded)] : null, x.seasonal ? ["Season", esc(x.seasonal)] : null])}
      ${x.founded_note ? `<p class="note">${esc(x.founded_note)}</p>` : ""}${x.web ? `<p class="note">Source: <a href="${esc(x.web)}" target="_blank" rel="noopener">${esc(x.web.replace(/^https?:\/\/(www\.)?/, "").replace(/\/$/, ""))}</a>.</p>` : ""}</div>` : "";
  const lic = (x.lic || []).map(l => [esc(l.src), esc(l.type || "") + (l.id ? " · " + esc(l.id) : "")]);
  const insp = r.in_r != null ? `<div class="dsec"><h3>Health inspections · Detroit Health Department</h3>
      <div class="hero" style="margin:0 0 10px">${resPill(r)}<span class="lbl">Latest routine inspection, ${esc(r.in_d)} · ${r.in_p} priority violations</span></div>
      ${x.insp ? `<ul class="lines">${x.insp.map(([d, res, pp, t, p, pf, c]) => `<li>${esc(d)} · ${esc(t)} · ${esc(res)} · Priority ${p} · Priority Foundation ${pf} · Core ${c}</li>`).join("")}</ul>` : (DETAIL ? "" : `<p class="note">${detailFailed ? "Couldn't load the inspection list. Check your connection and reopen this place." : "Loading the inspection list…"}</p>`)}
      <p class="note">"In compliance" or "not in compliance" is the City's own result for each routine inspection, with the counts of Priority (most serious), Priority Foundation and Core violations it cited, corrected on the spot or not. We compute no grade, and the placard posted at the door also reflects enforcement and license status. Source: Detroit Health Department, Restaurant Inspections (data.detroitmi.gov), routine inspections through ${esc((META.inspections_through || {}).det || "")}.</p></div>` : "";
  const alcSec = "";
''' + s[b:]
R('''  $("#drawer").innerHTML = `${dhead(esc(r.city || "Wisconsin"), random)}''', '''  $("#drawer").innerHTML = `${dhead(esc(r.city || "Michigan"), random)}''')
R('''    <div class="addr">${r.addr ? esc(r.addr) + ", " : ""}${esc(r.city || "Wisconsin")}''', '''    <div class="addr">${r.addr ? esc(r.addr) + ", " : ""}${esc(r.city || "Michigan")}''')
R('''    ${sig ? `<div class="dsec"><h3>Wisconsin classics · from Google reviews through Sep 2021</h3><div class="wisig">${sig}</div><p class="note">Average star rating of just the reviews that mention it. Reviews rate the whole visit, so read these as a lean, not a verdict.</p></div>` : ""}
    ${(honorsList.length || x.icon || x.founded) ? `<div class="dsec"><h3>Honors &amp; history</h3>${x.icon?`<p style="margin:0 0 8px;color:var(--ink-2);font-size:14px">${esc(x.icon)}</p>`:""}${honorsList.length?`<ul class="lines">${honorsList.map(v=>`<li>${esc(v)}</li>`).join("")}</ul>`:""}${x.founded ? `<p class="note">Open since ${esc(x.founded)} (verified).</p>` : ""}</div>`
      : (r.hon && !DETAIL ? `<div class="dsec"><h3>Honors &amp; history</h3><p class="note">${detailFailed ? "Couldn't load the honors. Check your connection and reopen this place." : "Loading…"}</p></div>` : "")}
    ${insp}''',
  '''    ${honorsList.length ? `<div class="dsec"><h3>Honors</h3><ul class="lines">${honorsList.map(v=>`<li>${esc(v)}</li>`).join("")}</ul><p class="note">MICHELIN and the MICHELIN Guide are trademarks of Michelin. James Beard Foundation awards are the Foundation's. Honors are facts, not ratings.</p></div>`
      : ((r.hon & 15) && !DETAIL ? `<div class="dsec"><h3>Honors</h3><p class="note">${detailFailed ? "Couldn't load the honors. Check your connection and reopen this place." : "Loading…"}</p></div>` : "")}
    ${facts}
    ${alcSec}
    ${insp}''')
R('''      x.lic ? ["License number", esc(x.lic.replace(/^(MKE|PHMDC)-/, ""))] : null,
      tagsTxt.length ? ["Wisconsin tags", esc(tagsTxt.join(", "))] : null,
      ["Listed as a bar or tavern", r.bar ? "Yes" : "No"], ["Locations in Wisconsin", r.chain_n >= 2 ? fmtN(r.chain_n) : "This one only"],''',
  '''      ...lic, r.liq ? ["Serves alcohol", "Yes · " + esc(META.liqt[r.liq])] : ["Serves alcohol", r.city === "Detroit" ? "— (no on-premises liquor license matched)" : "— (unknown: only Detroit's copy of the state liquor list is open)"],
      tagsTxt.length ? ["Michigan guides", esc(tagsTxt.join(", "))] : null,
      r.county ? ["County", esc(r.county)] : null,
      ["Listed as a bar or tavern", r.bar ? "Yes" : "No"], ["Locations in Michigan", r.chain_n >= 2 ? fmtN(r.chain_n) : "This one only"],''')
R('''  detailPending = fetchJSON("wi_detail.json").then(j => {''', '''  detailPending = fetchJSON("mi_detail.json").then(j => {''')

# ---------------- method cards
a = s.index('function methodCards() {'); b = s.index('// ---------------- boot ----------------')
s = s[:a] + r'''function methodCards() {
  const m = META, c = (m.calibration || {}).areas || {}, S0 = c["Michigan (statewide)"] || {};
  const dv = ["Foursquare only", "BrightQuery only", "Microsoft only", "Foursquare/BrightQuery/Microsoft + Google 2021"].map(k => S0.groups?.[k]).filter(Boolean).map(g => g.official);
  const dropRange = dv.length ? `${Math.round(Math.min(...dv) * 100)}–${Math.round(Math.max(...dv) * 100)}%` : "a small share";
  const it = m.inspections_through || {};
  const cols = [
    ["m", "Official records", [
      ["Food-service licenses (statewide)", `MDARD's open list of the food service establishments Michigan's 45 local health departments license ("Michigan Restaurants and Commissaries", gisagomdard.state.mi.us; ${fmtN(m.mdard_active_licenses || 0)} active licenses, read ${esc(m.licenses_updated || "")}). It covers restaurants, cafés, bars that serve food and caterers, and also school, church and office kitchens, so a listing matched to a license is confirmed, and a licensed place the map listings lack is added only when its name says it's a place to eat. The State's terms put no restriction on reuse. A bar that serves no food needs no food license.`],
      ["Detroit inspections", `The Detroit Health Department's Restaurant Inspections dataset (data.detroitmi.gov): every inspection since late 2021 with the City's own "in compliance" result and its counts of Priority, Priority Foundation and Core violations. We show the latest routine inspection as published, through ${esc(it.det || "")}. Detroit is the only Michigan health department that publishes results in bulk; Oakland, Washtenaw, Wayne, Kent, Ingham, Kalamazoo and Macomb counties offer search pages or reports only (several block automated access), so they aren't here.`],
      ["Liquor licenses", `Detroit only: the City's copy of the Michigan Liquor Control Commission list (refreshed on the 1st of each month; read ${esc(m.liquor_updated || "")}). On-premises licenses (Class C, Tavern, Club, hotels, brewpubs, makers' tasting rooms) say a place serves alcohol. The MLCC's own statewide list is on michigan.gov, which blocks automated access, so outside Detroit "serves alcohol" is unknown, not "no".`],
      ["Not used", "MDARD's own inspections (MiSafe) cover grocery and retail food, not restaurants. No county publishes open property values we could use, so there's no building-value board."]]],
    ["s", "Map listings & 2021 snapshot", [
      ["Places statewide", `Overture Maps' open map listings (${esc(m.overture_release || "Sep 2026")} release, which merges Meta, Foursquare, chain store lists and other sources). We keep listings from Meta and from chains' own store lists, and drop Foursquare, BrightQuery and Microsoft listings: statewide only ${dropRange} of those matched a licensed food business. Anything Google already showed as closed in 2021 is dropped, unless an official record or our research confirms it.`],
      ["Ratings, reviews & price level", "Google Maps ratings from the UCSD Google Local research dataset, frozen in September 2021. Each Google listing is matched to one place at most, on a shared distinctive name word nearby. Places that opened later aren't in it, and the rating boards leave them out rather than guess."],
      ["Honors & guides", "Michigan has no MICHELIN Guide. James Beard honors and the hand-checked Michigan guides (coney islands, Detroit-style pizza, pasties, pączki, Dearborn's Middle Eastern places, fish fries and supper clubs, the oldest places), each with a 2025–26 source, are added in the next pass."]]],
    ["e", "Estimated", [
      ["Sales & profit", `Chains use their published U.S. average sales per store (QSR 50, Technomic, company filings and franchise disclosures; ${m.model?.n_chains ?? "80+"} brands found here), scaled by how busy the location is. Independents start from a typical figure for their price level ($600K for $ up to $3.5M for $$$$) and scale with 2021 review volume relative to similar Michigan places, with an exponent of ${m.model?.b ?? 0.76} fit on published Chicago sales. Places without reviews get a rough placeholder. Profit = sales × a typical segment margin.`],
      ["Price, cuisine & food cost", "Missing price levels are filled in from the chain's or cuisine's usual Michigan level and marked est. Cuisine comes from the listing's category, the business name and Google categories, so a few will be off."]]],
  ];
  $("#srcgrid").innerHTML = cols.map(([t, h, cards]) => `<div class="srccol"><span class="tag ${t}">${h}</span>${cards.map(([h,p]) => `<div class="src"><h3>${h}</h3><p>${p}</p></div>`).join("")}</div>`).join("");
  const G = [["Meta + open in Google 2021","Meta listing, open in Google's 2021 data","kept · two sources"],["Meta only","Meta listing only","kept · listing only"],
    ["brand feed + Google 2021","Chain store list + Google 2021","kept · two sources"],["brand feed only","Chain store list only","kept · listing only"],
    ["Foursquare/BrightQuery/Microsoft + Google 2021","Foursquare / BrightQuery / Microsoft + Google 2021","dropped"],["Foursquare only","Foursquare only","dropped"],
    ["BrightQuery only","BrightQuery only","dropped"],["Microsoft only","Microsoft only","dropped"],["Google 2021 says closed","Google showed it closed in 2021","dropped"]];
  const cell = (j, k) => { const g = c[j]?.groups?.[k]; return g ? `${Math.round(g.official * 100)}% <span style="color:var(--muted)">of ${fmtN(g.n)}</span>` : "—"; };
  const pc = (m.calibration || {}).per_county || {};
  const ctyRows = Object.entries(pc).sort((a, b) => b[1].listings - a[1].listings);
  const SEARCH = new Set(["Oakland County","Washtenaw County","Kent County","Ingham County","Kalamazoo County","Macomb County","Ottawa County","Genesee County"]);
  $("#calib").innerHTML = S0.groups ? `<div class="src" style="display:grid;gap:10px"><h3>How the map listings were checked</h3>
    <p>Every map listing was checked against the state's list of licensed food-service establishments, county by county: same business name nearby, or the same street address with a distinctive name word in common. The share that matched decides what's kept. Coverage runs the other way too: the open map listings held ${Math.round((S0.coverage||0)*100)}% of the ${fmtN(S0.official_food || 0)} licensed establishments statewide and ${Math.round((c["Detroit"]?.coverage||0)*100)}% of Detroit's; plainly named restaurants among the rest were added from the list.</p>
    <div class="calib"><table><thead><tr><th scope="col">Kind of listing</th><th scope="col" class="r">Michigan</th><th scope="col" class="r">Detroit</th><th scope="col">Here</th></tr></thead><tbody>
    ${G.map(([k, l, what]) => `<tr><td>${esc(l)}</td><td class="r num">${cell("Michigan (statewide)", k)}</td><td class="r num">${cell("Detroit", k)}</td><td>${what}</td></tr>`).join("")}</tbody></table></div>
    <p class="note">Matched = on the food-service license list (and, in Detroit, the City's establishment list). These are lower bounds: a real place under a different name on its license counts as a miss, and bars that serve no food hold no food license. Hand-checked places are kept whatever their source.</p></div>
    <div class="src" style="display:grid;gap:10px"><h3>Coverage by county</h3>
    <p>Every county is on the statewide license list; only Detroit publishes inspection results in bulk. “Licenses found” is the share of each county's licensed food-service establishments that the open map listings already held (plainly named restaurants among the rest were added).</p>
    <div class="calib" style="max-height:420px;overflow:auto"><table><thead><tr><th scope="col">County</th><th scope="col" class="r">Map listings</th><th scope="col" class="r">Food-service licenses</th><th scope="col" class="r">Licenses found</th><th scope="col">Inspection results</th></tr></thead><tbody>
    ${ctyRows.map(([n, v]) => `<tr><td>${esc(n)}</td><td class="r num">${fmtN(v.listings)}</td><td class="r num">${fmtN(v.lhd_records || 0)}</td><td class="r num">${v.lhd_found == null ? "—" : Math.round(v.lhd_found * 100) + "%"}</td><td>${n === "Wayne County" ? "Detroit: bulk (data.detroitmi.gov)" : (SEARCH.has(n) ? "Search or report pages only" : "None found online")}</td></tr>`).join("")}</tbody></table></div></div>` : "";
}

''' + s[b:]

# ---------------- build
R('''  // Wisconsin signals: Bayes-shrink each place's average toward the statewide average for that dish (5 reviews' worth)
  for (const [key, n, r, out] of [["ff","ff_n","ff_r","ff"],["cc","cc_n","cc_r","cc"],["cs","cs_n","cs_r","cs"]]) {
    let sw = 0, sn = 0; for (const [i, nn, rr] of sp[key] || []) if (rr != null) { sw += nn * rr / 100; sn += nn; }
    const mu = sn ? sw / sn : 4.2;
    for (const [i, nn, rr] of sp[key] || []) { const o = rows[i]; if (!o) continue; o[n] = nn; o[r] = rr == null ? null : rr / 100; o[out] = rr == null ? null : (nn * rr / 100 + 5 * mu) / (nn + 5); }
  }
  for (const [i, nn] of sp.sc || []) if (rows[i]) rows[i].sc_n = nn;
  for (const [i, s, f] of sp.hon || []) if (rows[i]) { rows[i].s_icon = s / 10; rows[i].hon = f; }
  for (const [i, cl, g, ni, nr] of sp.insp || []) if (rows[i]) Object.assign(rows[i], {clean: cl, grade: g, n_insp: ni, n_reinsp: nr});''',
  '''  for (const [i, s, f, mi, gs] of sp.hon || []) if (rows[i]) { rows[i].s_icon = s / 10; rows[i].hon = f; rows[i].mi = mi; rows[i].gs = gs; }
  HAVE_TAGS = 0; for (let i = 0; i < C.tags.length; i++) HAVE_TAGS |= C.tags[i] || 0;
  TAGS = TAGS_ALL.filter(([, , b]) => HAVE_TAGS & b); TAG_PH = TAG_PH_ALL.filter(([, t]) => TAGS.some(([k]) => k === t));
  for (let i = B.length - 1; i >= 0; i--) if (B[i].tagbit && !(HAVE_TAGS & B[i].tagbit)) B.splice(i, 1);   // a guide shows once its research lands
  for (const [i, res, p, d, n, rr, cl, j] of sp.insp || []) if (rows[i]) Object.assign(rows[i], {in_r: res, in_p: p, in_d: d, in_n: n, in_rr: rr, in_cl: cl, in_j: j});''')
R('''    o.src = (m.srcs || [])[C.src[i]] || null;''', '''    o.src = (m.srcs || [])[C.src[i]] || null; o.liq = C.liq[i] || 0; o.hc = C.hc[i] || 0; o.county = C.county[i] == null ? null : m.counties[C.county[i]];
    o.alc_k = null; o.alc_n = 0;''')
R('''    o._s = " " + normRaw([o.name, o.city, o.zip, o.cuisine, o.brand].join(" ")) + " " + norm(o.addr) + " ";''', '''    o._s = " " + normRaw([o.name, o.city, o.zip, o.cuisine, o.brand, o.county].join(" ")) + " " + norm(o.addr) + " ";''')
R('''  CITY_N = new Map();   // "st germain", "saint germain" and "St. Germain" are one town''', '''  CITY_N = new Map();   // "sault ste marie", "sault sainte marie" and "Sault Ste. Marie" are one town''')
R('''             "fish", "fry", "custard", "curds", "cheese", "supper", "club", "brats", "tavern", "tap", "brewery", "kringle"]));''',
  '''             "coney", "coneys", "pizza", "pasty", "pasties", "paczki", "shawarma", "fish", "fry", "supper", "club", "tavern", "tap", "brewery", "whitefish", "perch"]));''')
R('''  $("#h1").innerHTML = `<span class="count num">${fmtN(n)}</span> Wisconsin restaurants, ranked`;''', '''  $("#h1").innerHTML = `<span class="count num">${fmtN(n)}</span> Michigan restaurants, ranked`;''')
R('''  fetchJSON("wisconsin.json").then(j => {''', '''  fetchJSON("michigan.json").then(j => {''')
R('''  $("#tagchips").innerHTML = TAGS.map(([k, l]) => `<button class="chip" type="button" data-v="${k}" aria-pressed="false">${l}</button>`).join("");''',
  '''  $("#tagchips").innerHTML = TAGS.map(([k, l]) => `<button class="chip" type="button" data-v="${k}" aria-pressed="false">${l}</button>`).join("");
  $("#l-tags").hidden = $("#tagchips").hidden = !TAGS.length;   // no hand-checked guide yet: no empty filter''')
for word in ("Wisconsin", "Milwaukee", "Dane County", "custard", "WI Score", "wi_", "Colorado", "Denver", "Boulder", "green chile", "CO Score",
             "Texas", "TABC", "Austin", "El Paso", "Arlington", "TX Score", "tx_", "brisket", "Comptroller"):
    hits = [m.start() for m in re.finditer(re.escape(word), s)]
    if hits:
        print(f"note: {len(hits)} '{word}' left, e.g. {s[max(0, hits[0]-60):hits[0]+40]!r}")
open(os.path.join(ROOT, "site", "index.html"), "w").write(s)
print("wrote site/index.html", len(s) // 1024, "KB")
