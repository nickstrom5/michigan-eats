"""Overture address points for Michigan -> data/mi/addresses_mi.parquet

Places official records that have no coordinates (MLCC licenses, Detroit's inspection list) and researched addresses
the map listings lack. Adapted from co-eats/pipeline/fetch_extras.py.
"""
import os, time
import duckdb

RELEASE = "2026-09-23.1"
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "mi")
t = time.time()
con = duckdb.connect()
con.execute("INSTALL httpfs; LOAD httpfs; INSTALL spatial; LOAD spatial; SET s3_region='us-west-2';")
addr = f"s3://overturemaps-us-west-2/release/{RELEASE}/theme=addresses/type=address/*.parquet"
con.execute(f"""COPY (SELECT number, street, unit, postcode, postal_city, address_levels[1].value AS state, address_levels[-1].value AS muni,
  ST_Y(geometry) lat, ST_X(geometry) lon FROM read_parquet('{addr}', hive_partitioning=1)
  WHERE country = 'US' AND bbox.xmin BETWEEN -90.45 AND -82.1 AND bbox.ymin BETWEEN 41.68 AND 48.32)
  TO '{OUT}/addresses_mi.parquet' (FORMAT PARQUET)""")
print(con.execute(f"select count(*), count(*) filter (where state='MI') from '{OUT}/addresses_mi.parquet'").fetchall(), round(time.time() - t), "s")
