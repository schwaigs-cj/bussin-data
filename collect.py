#!/usr/bin/env python3
"""Append one JSONL row per active NYU shuttle to data/YYYY-MM-DD.jsonl (UTC).

Run by GitHub Actions every ~15 minutes. Passio's getBuses feed includes
paxLoad (riders aboard, from the bus's own counter) and totalCap per bus.
"""
import datetime
import json
import pathlib
import urllib.parse
import urllib.request

URL = "https://passio3.com/www/mapGetData.php?getBuses=2"
LETTERED = {"74768", "74769", "74770", "74771", "74772", "74773", "74774"}

body = urllib.parse.urlencode({"json": json.dumps({"s0": "1007", "sA": 1})}).encode()
req = urllib.request.Request(URL, data=body,
                             headers={"Content-Type": "application/x-www-form-urlencoded"})
raw = json.load(urllib.request.urlopen(req, timeout=30))

buses = raw.get("buses") or {}
if not isinstance(buses, dict):   # PHP emits [] when empty
    buses = {}

now = datetime.datetime.now(datetime.timezone.utc)
rows = []
for group in buses.values():
    for b in group:
        if b.get("routeId") not in LETTERED:
            continue
        rows.append({
            "ts": now.isoformat(timespec="seconds"),
            "routeId": b.get("routeId"),
            "route": b.get("route"),
            "bus": b.get("bus"),
            "riders": b.get("paxLoad"),
            "capacity": b.get("totalCap"),
            "lat": b.get("latitude"),
            "lng": b.get("longitude"),
            "outOfService": b.get("outOfService"),
            "outdated": b.get("outdated"),
        })

out = pathlib.Path("data") / f"{now:%Y-%m-%d}.jsonl"
out.parent.mkdir(exist_ok=True)
with out.open("a") as f:
    for r in rows:
        f.write(json.dumps(r) + "\n")
print(f"appended {len(rows)} rows to {out}")
