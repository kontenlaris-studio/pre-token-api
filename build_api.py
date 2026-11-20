#!/usr/bin/env python3
"""Build the static Pre-Token API (JSON files for GitHub Pages).

Reads source.jsonl + stats.json (the published dataset snapshot) and emits:
  api/v1/index.json       — meta, endpoints, attribution, product links
  api/v1/all.json         — all protocols, compact fields
  api/v1/top.json         — top 50 by TVL
  api/v1/categories.json  — per-category counts & combined TVL
  api/v1/category/<slug>.json — protocols per category
Every payload carries the same meta block (snapshot date + attribution +
links) so API consumers always meet the products behind the data.
"""
import json, os, re

BASE = "https://kontenlaris-studio.github.io/pre-token-api/api/v1"
META_LINKS = {
    "analysis_app": "https://pre-token-screener.skillsafe.ai/",
    "model_licensing": "https://kontenlaris-studio.github.io/engine-licensing/",
    "cli": "https://github.com/kontenlaris-studio/kontenlaris-cli",
    "dataset": "https://github.com/kontenlaris-studio/pre-token-protocols-dataset",
}
FIELDS = ("name", "slug", "category", "tvl_usd", "change_1d_pct",
          "change_7d_pct", "primary_chain", "chain_count", "url")


def slugify(s):
    return re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")


def main():
    rows = [json.loads(l) for l in open("source.jsonl") if l.strip()]
    stats = json.load(open("stats.json"))
    meta = {
        "name": "Pre-Token Protocols API",
        "version": "v1",
        "snapshot_date": stats["snapshot_date"],
        "source": "DefiLlama protocols snapshot via the Pre-Token Protocols dataset (CC BY 4.0)",
        "attribution": "Data: Kontenlaris Studio — Pre-Token Protocols dataset",
        "count": len(rows),
        "links": META_LINKS,
    }
    rows.sort(key=lambda r: float(r.get("tvl_usd") or 0), reverse=True)
    compact = [{k: r.get(k) for k in FIELDS} for r in rows]

    os.makedirs("api/v1/category", exist_ok=True)

    def dump(path, data):
        payload = {"meta": meta, "data": data}
        with open(path, "w") as f:
            json.dump(payload, f, separators=(",", ":"))

    dump("api/v1/all.json", compact)
    dump("api/v1/top.json", compact[:50])

    cats = {}
    for r in compact:
        cats.setdefault(r["category"] or "Other", []).append(r)
    summary = [{"category": c, "slug": slugify(c), "count": len(v),
                "combined_tvl_usd": sum(float(x["tvl_usd"] or 0) for x in v),
                "endpoint": f"{BASE}/category/{slugify(c)}.json"}
               for c, v in cats.items()]
    summary.sort(key=lambda x: x["combined_tvl_usd"], reverse=True)
    dump("api/v1/categories.json", summary)
    for c, v in cats.items():
        dump(f"api/v1/category/{slugify(c)}.json", v)

    index = dict(meta)
    index["endpoints"] = {
        "all": f"{BASE}/all.json",
        "top50": f"{BASE}/top.json",
        "categories": f"{BASE}/categories.json",
        "by_category": f"{BASE}/category/<slug>.json",
    }
    index["usage"] = ("Free for any use with attribution (CC BY 4.0). "
                      "Static snapshot API — refresh follows dataset updates.")
    with open("api/v1/index.json", "w") as f:
        json.dump(index, f, indent=2)
    print(f"built: {len(compact)} protocols, {len(cats)} categories, "
          f"snapshot {stats['snapshot_date']}")


if __name__ == "__main__":
    main()
