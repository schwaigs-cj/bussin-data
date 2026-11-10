# bussin-data

Ridership logging for [Bussin](https://github.com/building-with-ai-f26/cjs10016-bussin),
the NYU shuttle app. A GitHub Action polls Passio GO's public feed for NYU
(system 1007) every ~15 minutes and appends one JSONL row per active shuttle to
`data/YYYY-MM-DD.jsonl`: timestamp (UTC), route, bus number, riders aboard
(`paxLoad`, from the bus's own passenger counter), capacity, and position.

The point: real riders-by-route-by-hour data to back route suggestions to NYU
Transportation. Collection runs continuously; analysis lives in the main repo.

Run once locally: `python3 collect.py`
