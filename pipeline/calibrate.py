"""How often is a map listing a real, licensed food business? Measured against official lists -> data/mi/calibration*.json

Adapted from tx-eats/pipeline/calibrate.py. Michigan has what Texas lacked: one statewide list of every food service establishment
the 45 local health departments license (MDARD, "Michigan Restaurants and Commissaries", active licenses).
- Statewide: every cleaned listing against that list. A fixed food service license covers restaurants, cafés, bars that serve food,
  coffee shops and caterers, so this is the full test, county by county. (Bars that serve no food and some seasonal stands hold no
  food license, so the rate is a slight under-count for "bar" listings.)
- Detroit: against the Detroit Health Department's own establishment list (open, seasonal and new) plus MDARD.
A match is the same business name nearby, or the same street address with a distinctive name word in common.
"""
import json
import numpy as np, pandas as pd
from shapely.geometry import shape, Point
from shapely.prepared import prep
from common import MI
from listings_util import official_match

o = pd.read_pickle(f"{MI}/stage1.pkl")
F = pd.read_pickle(f"{MI}/official.pkl")
from shapely import STRtree
_CN = json.load(open(f"{MI}/mi_counties_detail.geojson"))
_NAMES = list(_CN)
_GEOMS = [shape(_CN[n]).buffer(0.0003) for n in _NAMES]
_TREE = STRtree(_GEOMS)


def county_of(la, lo):
    if la != la:
        return None
    p = Point(lo, la)
    for i in _TREE.query(p):
        if _GEOMS[i].contains(p):
            return _NAMES[i]
    return None


o["county"] = [county_of(la, lo) for la, lo in zip(o.lat, o.lon)]
# MDARD rows carry their county; a point outside every county outline (a lakeshore point a little offshore) keeps the record's own
F["county"] = [county_of(la, lo) or (c if isinstance(c, str) and c else None)
               for la, lo, c in zip(F.lat, F.lon, F.get("county", pd.Series([None] * len(F))))]
o.to_pickle(f"{MI}/stage1.pkl")
F.to_pickle(f"{MI}/official.pkl")
base = ~o.j_junk & ~o.j_outside
print("listings with a county:", int(o.county.notna().sum()), "of", len(o))


def groups(L, app=False):
    s = L.src.fillna("none")
    if app:
        conf = L.confidence.fillna(0)
        return np.select([L.ov_closed | L.j_closedname, (s == "meta") & (conf >= 0.95), (s == "meta") & (conf >= 0.9),
                          s.isin(["AllThePlaces", "DAC"]), (s == "BrightQuery") & (conf >= 0.95), s == "meta"],
                         ["closed per Overture/name", "meta_high", "meta_mid", "brand_feed", "bq_high", "meta_low"], "other_sources")
    return np.select([L.closed21, L.ov_closed, (s == "meta") & L.in21, s == "meta", s.isin(["AllThePlaces", "DAC"]) & L.in21,
                      s.isin(["AllThePlaces", "DAC"]), L.in21, s == "Foursquare", s == "BrightQuery", s == "Microsoft"],
                     ["Google 2021 says closed", "Overture says closed", "Meta + open in Google 2021", "Meta only",
                      "brand feed + Google 2021", "brand feed only", "Foursquare/BrightQuery/Microsoft + Google 2021",
                      "Foursquare only", "BrightQuery only", "Microsoft only"], "other")


AREAS = {"Michigan (statewide)": (None, F.jur.isin(["lhd"]) & F.active, "lhd"),
         "Detroit": ("Wayne County", F.jur.isin(["det", "lhd"]) & F.active, "det")}
res, app = {}, {}
for label, (cty, sel, own) in AREAS.items():
    L = o[base & (o.county.notna() if cty is None else o.county == cty)].reset_index(drop=True)
    R = F[sel & (F.county.notna() if cty is None else F.county == cty)].reset_index(drop=True)
    if own == "det":
        L = L[L.city.eq("Detroit")].reset_index(drop=True); R = R[R.city.eq("Detroit")].reset_index(drop=True)
        m = official_match(L, R)
    else:   # county by county: "100 Main St" exists in dozens of towns
        m = {}
        for c_, gl in L.groupby("county").groups.items():
            gr = R.index[R.county == c_]
            if not len(gr):
                continue
            for i_, j_ in official_match(L.loc[gl].reset_index(drop=True), R.loc[gr].reset_index(drop=True)).items():
                m[gl[i_]] = gr[j_]
    L["hit"] = L.index.map(lambda i: i in m)
    L["hit_food"] = L.index.map(lambda i: i in m and R.kind.iat[m[i]] in ("restaurant", "bar", "brewery", "food"))
    for mode, store in ((False, res), (True, app)):
        L["grp"] = groups(L, mode)
        t = L.groupby("grp").agg(n=("id", "size"), official=("hit", "mean"), food=("hit_food", "mean")).sort_values("n", ascending=False)
        print(f"\n== {label} ({'app grouping' if mode else 'web grouping'}): {len(L)} listings, {len(R)} official records")
        print(t.assign(official=(t.official * 100).round(1), food=(t.food * 100).round(1)).to_string())
        store[label] = {"listings": int(len(L)), "official_records": int(len(R)),
                        "groups": {g: {"n": int(r.n), "official": round(float(r.official), 3), "food": round(float(r.food), 3)} for g, r in t.iterrows()}}
    # the other direction: how many official food businesses do the (cleaned, open) map listings hold?
    keepish = ~(L.ov_closed | L.j_closedname | L.closed21)
    got = set(R.biz.iloc[[m[i] for i in L.index[keepish] if i in m]])
    Rr = R[(R.jur == own) & R.kind.isin(["restaurant", "bar", "food"])].drop_duplicates("biz")
    cover = float(np.mean([b in got for b in Rr.biz])) if len(Rr) else None
    print(f"{label}: official food businesses found among open map listings: {cover*100:.1f}% of {len(Rr)}")
    res[label]["coverage"] = round(cover, 3)
    res[label]["official_food"] = int(len(Rr))
    if own == "lhd":
        L["county"] = L.county
        per = L.groupby("county").agg(listings=("id", "size"), lhd_match=("hit", "mean"))
        per["lhd_records"] = Rr.groupby("county").size().reindex(per.index).fillna(0).astype(int)
        per["lhd_found"] = [float(np.mean([b in got for b in Rr[Rr.county == c].biz])) if (Rr.county == c).any() else None for c in per.index]
        print("\n== per county\n" + per.sort_values("listings", ascending=False).round(3).to_string())
        PER = per

json.dump({"areas": res, "per_county": {c: {k: (round(float(v), 3) if isinstance(v, float) else int(v)) for k, v in r.items() if v == v}
                                          for c, r in PER.iterrows()},
           "unplaced_official_records": int(F.lat.isna().sum())},
          open(f"{MI}/calibration.json", "w"), indent=1)
json.dump(app, open(f"{MI}/calibration_app.json", "w"), indent=1)
