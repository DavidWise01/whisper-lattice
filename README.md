# Whisper Lattice (WL) — 1 → 3 → 1

A ROOT0 / TriPod LLC **technical design**: a deterministic agent pipeline.

**1 input** (a record from a public source — Wikipedia / Wikimedia Commons)
**→ 3 agents** (Ingest → Synthesize → Witness)
**→ 1 output** (an append-only, hash-chained log).

The signature of each cycle is `prim = SHA-256(content_hash ‖ previous_prim)`, so the log is a
tamper-evident chain (git's trick, applied to a reading loop). The transform is deterministic;
the input (a random article) is not — and the design says so. **No AI in the loop.**

- **`index.html`** — the technical design (architecture, the three agents, data contracts, sources) + full .dlw.
- **`artifact.html`** — a **live, working** reference: fetches a random Wikipedia article (public API, CC BY-SA 4.0, attributed) and runs the 1→3→1 pipeline client-side, chaining each prim into an on-page log.
- **`bridge/whisper_lattice_git_bridge.py`** — the local control plane that commits each entry to git.
- **Live session log:** [whisper-lattice-log](https://github.com/DavidWise01/whisper-lattice-log).

## Sources
- Wikipedia / MediaWiki Action API (`action=query&origin=*`) — content under **CC BY-SA 4.0**.
- Wikimedia Commons — media under various free licenses (attribute per file).
- SHA-256 (FIPS 180-4) via the Web Crypto API; the hash-chain follows the Merkle / git-commit idea.
- Determinism lineage: Lovelace & Babbage (the Analytical Engine, "Ada's Mill", 1843); ROOT0's 0root / F-M-B design.

Rebuilt clean & IP-scrubbed (no film quotes, no reused artifact). Catalogued into UD0 (LOGISMÓS). CC-BY-ND-4.0 · TRIPOD-IP-v1.1.
