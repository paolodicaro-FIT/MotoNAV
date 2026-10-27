#!/usr/bin/env python3
"""MotoNAV: export explicit OSM speed limits from a .osm.pbf to compact GeoJSON.
Usage: pip install osmium
       python3 tools/export-maxspeed.py lombardia.osm.pbf --bbox 9.16,45.44,9.24,45.51 --out maxspeed-milano.geojson
Bounding box: west,south,east,north. No network requests or paid services.
"""
import argparse, json, re
import osmium

p=argparse.ArgumentParser()
p.add_argument("pbf")
p.add_argument("--bbox",required=True,help="west,south,east,north")
p.add_argument("--out",default="maxspeed.geojson")
args=p.parse_args()
west,south,east,north=map(float,args.bbox.split(","))
if not(west<east and south<north):p.error("Invalid bbox")
valid=re.compile(r"^\s*(\d{1,3})(?:\s*km/h)?\s*$",re.I)
def parse(v):
 m=valid.match(v or "")
 if not m:return None
 n=int(m.group(1))
 return n if 10<=n<=140 else None
class Extract(osmium.SimpleHandler):
 def __init__(self):
  super().__init__();self.features=[];self.seen=0
 def way(self,w):
  t=w.tags
  if "highway" not in t:return
  tags={k:str(t[k]) for k in ("maxspeed","maxspeed:forward","maxspeed:backward","maxspeed:conditional","maxspeed:forward:conditional","maxspeed:backward:conditional","oneway","highway","name") if k in t}
  if not any(k.startswith("maxspeed") for k in tags):return
  if not any(parse(tags.get(k)) for k in ("maxspeed","maxspeed:forward","maxspeed:backward")):return
  try:coords=[[round(n.lon,7),round(n.lat,7)] for n in w.nodes]
  except osmium.InvalidLocationError:return
  if len(coords)<2:return
  if max(c[0] for c in coords)<west or min(c[0] for c in coords)>east or max(c[1] for c in coords)<south or min(c[1] for c in coords)>north:return
  self.features.append({"type":"Feature","id":int(w.id),"properties":tags,"geometry":{"type":"LineString","coordinates":coords}})
  self.seen+=1
h=Extract();h.apply_file(args.pbf,locations=True)
with open(args.out,"w",encoding="utf-8") as f:json.dump({"type":"FeatureCollection","metadata":{"source":"OpenStreetMap contributors (ODbL)","bbox":[west,south,east,north],"note":"Explicit maxspeed tags only; not verified legal limits"},"features":h.features},f,separators=(",",":"),ensure_ascii=False)
print(f"Exported {h.seen} ways to {args.out}")
