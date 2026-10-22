"""Official records for Michigan -> one table of licensed / inspected food and drink businesses.

Sources (see playbook/12-sources.md):
- "lhd": Michigan Department of Agriculture and Rural Development (MDARD), "Michigan Restaurants and Commissaries"
         (gisagomdard.state.mi.us ArcGIS FeatureServer RestaurantsCommissariesOpenData/0): every food service establishment
         licensed by Michigan's 45 local health departments, statewide, with its license key, the location name, address, county,
         health department and a point. Active licenses only. OrganizationName is the license holder: never shown.
- "det": Detroit Health Department, "Restaurant Inspections" establishments layer (data.detroitmi.gov item
         ffd4ed9aa12a4df5ad13d81175da4e49, layer 0): establishment id, name, address, license, type, status, point.
- "liq": City of Detroit, "Liquor Licenses" (data.detroitmi.gov item 990a559e64754eb4a2e3cf34fce6516f): licenses the Michigan Liquor
         Control Commission issued to Detroit businesses, refreshed by the City from the State's list on the first of each month.
         Detroit only (the MLCC's statewide list is on michigan.gov, which answers our requests with a bot check).

load() returns: jur, lic (our id), name, keys (name keys), addr, city, zip, num, street, lat, lon, kind, active.
kind: restaurant | bar | brewery | retail | venue | food | other.
"""
import os, re, json
import numpy as np, pandas as pd
from common import norm_name, RAW, name_sim, _stems, GENERIC, canon_city

OFF = os.path.join(RAW, "official")
DIRS = {"N": "N", "S": "S", "E": "E", "W": "W", "NORTH": "N", "SOUTH": "S", "EAST": "E", "WEST": "W"}
TYPES = set("ST STREET AVE AV AVENUE BLVD BOULEVARD RD ROAD DR DRIVE LN LANE CT COURT PL PLACE PKWY PARKWAY TER TRL TRAIL WAY HWY CIR "
            "CIRCLE PLZ SQ MALL BND PASS XING RUN ROW WALK RDG LOOP FWY FREEWAY EXPY EXPRESSWAY".split())


def road(a):
    """One spelling for numbered roads: 'US HIGHWAY 31' = 'US-31' = 'US 31'; 'M-22' = 'M 22' = 'STATE HIGHWAY 22';
    'INTERSTATE 75' = 'I-75' = 'I 75'; 'COUNTY ROAD 612' = 'CR 612'; 'BUSINESS LOOP I-96' stays a road."""
    a = re.sub(r"(\d)\s*&\s*(\d)", r"\1-\2", a.upper())
    a = re.sub(r"\b(US|M|CR|I|BL|BR)-(\w)", r"\1 \2", a)
    a = re.sub(r"\b(?:INTERSTATE(?: HIGHWAY| HWY)?|IH|I H)\s*(?=\d)", "I ", a)
    a = re.sub(r"\b(?:US|U S)\s+(?:HIGHWAY|HWY)\b", "US", a)
    a = re.sub(r"\b(?:STATE (?:HIGHWAY|HWY|ROAD|RD)|MICHIGAN (?:HIGHWAY|HWY)|MI (?:HIGHWAY|HWY)|HWY M|HIGHWAY M)\b(?=\s*\d)", "M", a)
    a = re.sub(r"\b(?:COUNTY (?:HIGHWAY|HWY|ROAD|RD)|CO RD|CTY (?:HWY|RD)|CR)\b", "CR", a)
    a = re.sub(r"\bHIGHWAY\b", "HWY", a)
    return re.sub(r"\b(US|M|CR|HWY|I) (\w+)\s*-\s*\w+", r"\1 \2", a)


ORD = {"FIRST": "1ST", "SECOND": "2ND", "THIRD": "3RD", "FOURTH": "4TH", "FIFTH": "5TH", "SIXTH": "6TH", "SEVENTH": "7TH",
       "EIGHTH": "8TH", "NINTH": "9TH", "TENTH": "10TH", "ELEVENTH": "11TH", "TWELFTH": "12TH"}


def street_key(a):
    """'2505 Monroe St' -> ('2505', 'MONROE'); '1000 OSAGE STREET' -> ('1000', 'OSAGE'); 'E Jefferson Ave' keeps 'JEFFERSON'."""
    if not isinstance(a, str):
        return None, None
    a = re.sub(r"[.,#]", " ", road(a))
    m = re.match(r"^\s*(\d+)[A-Z]?(?:\s*-\s*\d+[A-Z]?)?\s+(.*)$", a)
    if not m:
        return None, None
    words = [w for w in m.group(2).split() if w]
    if len(words) > 1 and words[0] in DIRS:
        words = words[1:]
    core = []
    for w in words:
        if w in TYPES and core:
            break
        core.append(w)
    core = [ORD.get(w, w) for w in core]
    return m.group(1), " ".join(core[:3]) or None


def street_compat(a, b):
    """Same street, or one is a whole-word prefix of the other (a record that truncates "1206 CENTAUR" = Centaur Village Dr)."""
    if not isinstance(a, str) or not isinstance(b, str) or not a or not b:
        return False
    return a == b or a.startswith(b + " ") or b.startswith(a + " ")


def street_nums(a):
    """'157-159 W Main St' -> {'157', '159'}; '2505 Monroe St' -> {'2505'}."""
    if not isinstance(a, str):
        return set()
    a = road(a)
    m = re.match(r"^\s*(\d+)[A-Z]?(?:\s*-\s*(\d+)[A-Z]?)?\s", a.upper() + " ")
    if not m:
        return set()
    lo = int(m.group(1)); hi = int(m.group(2)) if m.group(2) else lo
    if hi < lo:   # "1500-02"
        hi = int(str(lo)[: len(str(lo)) - len(m.group(2))] + m.group(2)) if m.group(2) else lo
    return {str(x) for x in range(lo, hi + 1, 2 if (hi - lo) % 2 == 0 else 1)} if 0 <= hi - lo <= 12 else {str(lo)}


def _names(*vals):
    out = []
    for v in vals:
        if not isinstance(v, str):
            continue
        v = re.sub(r"\s*\((?:MOBILE|MOBILE UNIT|COMMISSARY|CATERING|SPECIAL EVENT|SPEC EVENT|TEMP(?:ORARY)? EVENT|CP|INSIDE [^)]*)\)\s*$", "", v, flags=re.I)
        for part in re.split(r"\s*/\s*|\s+\bdba\b\s+|\s+&\s+(?=[A-Z][a-z])|\s*\(\s*|\s*\)\s*", v, flags=re.I):
            k = norm_name(re.sub(r"\b(?:LLC|INC|CORP|CORPORATION|LTD|CO)\b\.?", "", part, flags=re.I))
            if k and k not in out:
                out.append(k)
    return out


# MLCC license types (Detroit's copy of the State list). On-premises: Class C (bars and restaurants, spirits), Tavern (beer and wine),
# Club, B-Hotel, Brew Pub and makers' tasting rooms. Specially Designated Merchant / Distributor are stores (beer and wine to go, spirits
# to go), the rest makers, wholesalers and event permits.
LIQ_KIND = {"Class C": "bar", "Tavern": "bar", "Club": "venue", "B-Hotel": "venue", "Brew Pub": "brewery", "Micro Brewer": "brewery",
            "Small Distiller": "brewery", "Small Wine Maker": "brewery", "Wine Maker": "brewery", "On-Premises Tasting Room Permit": "brewery",
            "Specially Designated Merchant": "retail", "Specially Designated Distributor": "retail", "Off-Premises Tasting Room": "retail",
            "Watercraft": "other", "Wholesale": "other", "Consumer Sampling Event": "other", "Manufacturer of Mixed Spirits": "other",
            "Warehouser": "other", "Manufacturer of Spirits": "other", "Outstate Seller of Wine": "other"}
ONPREM = ("restaurant", "bar", "brewery")
LIST_DATE = "2026-10-22"   # Detroit liquor licenses fetched (the City refreshes it from the State list on the 1st of each month)
MDARD_DATE = "2026-10-22"  # MDARD restaurants and commissaries fetched (item modified 2026-04-09)


def liq_kind(t):
    return LIQ_KIND.get(re.sub(r"\s*\(.*$", "", t or ""))


def _zip(z):
    z = re.sub(r"\D", "", str(z or ""))
    return z[:5] if len(z) >= 5 else ""


OTHER = re.compile(r"\((?:MOBILE|MOBILE UNIT|COMMISSARY|CATERING|SPECIAL EVENT|TEMP(?:ORARY)? EVENT)\)|\b(?:SCHOOLS?|ELEMENTARY|MIDDLE SCHOOL|HIGH SCHOOL|"
                   r"ACADEMY|PRESCHOOL|CHILDCARE|CHILD CARE|DAYCARE|DAY CARE|HOSPITAL|JAIL|DETENTION|CORRECTIONAL|FOOD BANK|SENIOR|NURSING|"
                   r"MOBILE|FOOD TRUCK|CATERING|CATERER|COMMISSARY|CONCESSIONS?|BOOSTERS?|PTA|PTO|BOARD OF EDUCATION|PUBLIC SCHOOLS|"
                   r"LITTLE LEAGUE|ATHLETIC ASSOCIATION|SNACK SHACK|CAMP)\b", re.I)


def _row(jur, lic, name, addr, city, z, la, lo, kind, active=True, ltype=None, holder=None, county=None, lhd=None):
    num, st = street_key(addr)
    if OTHER.search(name or ""):
        kind = "other"
    return {"jur": jur, "lic": lic, "name": name, "dba": name, "holder": holder, "keys": _names(name), "addr": addr, "city": city,
            "zip": _zip(z), "num": num, "street": st, "lat": la, "lon": lo, "kind": kind, "active": active, "ltype": ltype,
            "county": county, "lhd": lhd}


def load_mdard():
    rows = []
    for r in json.load(open(f"{OFF}/mdard/restaurants_commissaries.json")):
        kind = "food" if r["LicensetypeName"] == "Food Service - Fixed Establishment" else "other"
        street = re.split(r",|\s+(?:STE|SUITE|UNIT|#)\b", r["AddressLine1"] or "", flags=re.I)[0].strip()
        cty = (r.get("County") or "").strip()
        rows.append(_row("lhd", "MI-" + r["Licensekey"], (r["LocationName"] or "").strip(), street, canon_city(r["City"]), r["Zip"],
                         r["LocationLatitude"], r["LocationLongitude"], kind, active=r["CurrentLicenseStatus"] == "Active",
                         ltype=r["LicensetypeName"], holder=(r.get("OrganizationName") or "").strip() or None,
                         county=(cty + " County") if cty else None, lhd=r.get("RegionName")))
    return pd.DataFrame(rows)


DET_LIVE = {"Open", "Seasonal", "New License", "New Owner/Complete Reconstruct", "Temporarily Closed"}


def load_detroit():
    d = pd.read_csv(f"{OFF}/detroit/establishments.csv", encoding="utf-8-sig", dtype=str).fillna("")
    rows = []
    for _, r in d.iterrows():
        kind = "food" if r["Establishment Type"] == "Food Service Establishment" else "other"
        la = float(r.Latitude) if r.Latitude else np.nan
        lo = float(r.Longitude) if r.Longitude else np.nan
        rows.append(_row("det", "DET-" + r["Establishment ID"], r["Establishment Name"].strip(), r.Address.strip(), "Detroit", r["Zip Code"],
                         la, lo, kind, active=r.Status.strip() in DET_LIVE, ltype=r["Establishment Type"],
                         county="Wayne County", lhd="Detroit Health Department"))
    return pd.DataFrame(rows)


def load_liquor():
    d = pd.read_csv(f"{OFF}/detroit/liquor.csv", encoding="utf-8-sig", dtype=str).fillna("")
    rows = []
    for _, r in d.iterrows():
        kind = LIQ_KIND.get(r["License Type"], "other")
        la = float(r.Latitude) if r.Latitude else np.nan
        lo = float(r.Longitude) if r.Longitude else np.nan
        name = r["Doing Business As"].strip() or r["Account Name"].strip()
        row = _row("liq", "MLCC-DET-" + r.ObjectId, name, r["Street Address"].strip(), "Detroit", r["Zip Code"], la, lo, kind,
                   active=r.Status in ("Active", "Conditional"), ltype=r["License Type"], holder=r["Account Name"].strip() or None,
                   county="Wayne County", lhd=None)
        row["keys"] = _names(r["Doing Business As"], r["Account Name"])
        row["dba"] = r["Doing Business As"].strip() or None
        rows.append(row)
    return pd.DataFrame(rows)


def load():
    df = pd.concat([load_mdard(), load_detroit(), load_liquor()], ignore_index=True)
    # one business can hold several records (an MDARD license, a Detroit establishment, a liquor license): same address and a name in common
    df["biz"] = np.arange(len(df))
    town = df.city.fillna("").str.upper().str.strip()
    for num, g in df[df.num.notna() & df.street.notna()].groupby("num"):
        idx = list(g.index)
        if len(idx) < 2 or len(idx) > 400:
            continue
        for x in range(len(idx)):
            for y in range(x + 1, len(idx)):
                a, b = idx[x], idx[y]
                if not street_compat(df.at[a, "street"], df.at[b, "street"]):
                    continue
                if not ((df.at[a, "zip"] and df.at[a, "zip"] == df.at[b, "zip"]) or (town[a] and town[a] == town[b])):
                    continue
                ka, kb = df.at[a, "keys"], df.at[b, "keys"]
                if not ka or not kb:
                    continue
                if any(name_sim(p, q) >= 85 or ((_stems(p) - GENERIC) & (_stems(q) - GENERIC)) for p in ka for q in kb):
                    old, new = df.at[b, "biz"], df.at[a, "biz"]
                    df.loc[df.biz == old, "biz"] = new
    return df


# ---------------------------------------------------------------- inspections: the Detroit Health Department's own result, never recomputed
ROUTINE = {"Routine Inspection", "Complaint / Routine", "Routine/Partial", "New Owner/Routine"}


def detroit_inspections():
    """One row per routine inspection (the types the City's placard rule rests on; attempted visits, closures, complaints and plan reviews
    carry no result): establishment, date, the City's own is_in_compliance flag and the counts of Priority, Priority Foundation and
    Core violations it cited. Oldest first."""
    d = pd.read_csv(f"{OFF}/detroit/inspections_l1.csv", encoding="utf-8-sig", dtype=str)
    d = d[d.inspection_type.isin(ROUTINE)]
    out = pd.DataFrame({"lic": "DET-" + d.establishment_id, "d": d.inspection_date.str[:10], "typ": d.inspection_type,
                        "ok": d.is_in_compliance.eq("True"), "p": pd.to_numeric(d.num_priority_violations, errors="coerce").fillna(0).astype(int),
                        "pf": pd.to_numeric(d.num_foundation_violations, errors="coerce").fillna(0).astype(int),
                        "c": pd.to_numeric(d.num_core_violations, errors="coerce").fillna(0).astype(int),
                        "iid": pd.to_numeric(d.inspection_id, errors="coerce")})
    return out.sort_values(["lic", "d", "iid"]).reset_index(drop=True)
