# Pre-Token Protocols API

Free static JSON API over the [Pre-Token Protocols dataset](https://github.com/kontenlaris-studio/pre-token-protocols-dataset): **838 DeFi protocols with TVL > $1M that have not launched a token** (DefiLlama snapshot, 2026-11-20). No key, no signup. Data CC BY 4.0 with attribution.

**Docs & live demo:** https://kontenlaris-studio.github.io/pre-token-api/

| Endpoint | Content |
|---|---|
| `api/v1/index.json` | meta, endpoint map, product links |
| `api/v1/all.json` | all 838 protocols, TVL-sorted |
| `api/v1/top.json` | top 50 by TVL |
| `api/v1/categories.json` | 53 categories: counts + combined TVL |
| `api/v1/category/<slug>.json` | protocols per category |

Every payload includes a `meta` block (snapshot date, source, attribution, links to the Token Radar screener app, the model-licensing catalog, and the `kontenlaris` CLI). Rebuild after a dataset refresh: drop the new `pre_token_protocols.jsonl` + `stats.json` next to `build_api.py` and run it.

By Kontenlaris Studio.
