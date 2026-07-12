# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A two-stage lead-generation pipeline for an outreach business (ayanip.es): find small Spanish
businesses that have **no website** via Google Places, then message them on WhatsApp offering web
design. The code is plain Python scripts (no framework, no build step); all docs and runtime output
are in Spanish.

## Architecture

Two scripts in `scripts/` form the pipeline; everything else is helpers or generated data.

1. **`scripts/scraping-script-v2.py`** — Reads a `config.json`, queries the **Google Places API
   (New)** (`places.googleapis.com/v1`, Text Search with `locationBias`), keeps only businesses
   where `websiteUri` is empty, dedupes by name, and writes a timestamped
   `{output_prefix}_YYYYMMDD_HHMMSS.csv`. Supports multiple sectors (`search_type` as comma list)
   and multiple coordinates (`locations_extra` / `locations_extra_names`, `;`-separated), iterating
   every location × sector until `max_results` is hit. `scraping-script.py` is the legacy
   (old Places API) version — prefer v2.

2. **`scripts/whatsapp_sender.py`** — Reads a `whatsapp_config.json`, picks the target CSV
   (`archivo_csv` or newest `negocios_sin_web_*.csv` in cwd), filters candidates, and sends one
   message per business. Four delivery `modo`s: `web` (pywhatkit fully automates WhatsApp Web),
   `web_directo` (opens prefilled WhatsApp Web, you press Enter), `wame` (opens wa.me link), `api`
   (Meta WhatsApp Cloud API — needs WhatsApp Business). Anti-block design is the core of this
   script: random `delay_min`–`delay_max` between sends, a long `pausa_minutos` break every
   `pausa_cada` sends, per-execution and per-day caps, and random rotation over
   `mensajes_templates`.

### Dedup / idempotency model (important)

Re-sends are prevented across runs by tracking sent phone numbers. Both the **log file**
(`envios_whatsapp.log`, one `timestamp | phone | OK/FAIL | name` line per attempt) and an
**`estado_envio` column** appended to the CSV are sources of truth. On load the sender syncs the
log into the CSV, skips any phone already in the log, and the daily cap counts `| OK |` lines dated
today. Phone normalization (strip separators, force `prefijo_pais` e.g. `34`, optionally
`solo_moviles` = starts with 6/7) must stay consistent across `_clean_phone`,
`_sincronizar_log_csv`, and `_marcar_envio_csv` or dedup silently breaks.

### Per-region working directories

Each region is a top-level folder (`madrid/`, `ciudad_real/`, `pais_vasco/`, `toledo/`, `huelva/`)
holding its **own** `config*.json`, `whatsapp_config*.json`, generated CSVs, and `*.log`. The
scripts resolve config, CSV glob, and log paths **relative to the current working directory**, so
they are meant to be run *from inside a region folder*, invoking the script by relative path. A
region can have several configs (e.g. one per town or per business sector) passed as the first CLI
argument.

## Common commands

```bash
pip install -r scripts/requirements.txt          # base dep: requests
pip install pywhatkit pyautogui                   # only for whatsapp_sender modo "web"
```

Run from inside a region directory so relative paths resolve:

```powershell
cd madrid
python ..\scripts\scraping-script-v2.py config.json
python ..\scripts\whatsapp_sender.py whatsapp_config.json        # prompts before sending
python ..\scripts\whatsapp_sender.py whatsapp_config_bares.json --yes   # skip confirmation
```

`scripts/test_whatsapp.py` sends a single message to your own number (edit `TU_TELEFONO` at the top)
without touching daily limits or the CSV — use it to sanity-check WhatsApp Web before a real batch.

There is **no test suite, linter, or CI**. The `scripts/analyze_*.py`, `check_pending.py`, and
`combinar_csvs.py` files are one-off analysis/maintenance utilities with hardcoded filenames; treat
them as throwaway, not a stable API.

## Config schema note

`docs/config.example.json` and `docs/whatsapp_config.example.json` are starting points but are
**stale** relative to the code. The real `whatsapp_config` schema the sender reads uses
`mensajes_templates` (array), `filtrar_tipos`/`excluir_tipos` (arrays of Google `types`),
`solo_moviles`, `delay_min`/`delay_max`, `pausa_cada`/`pausa_minutos`,
`max_mensajes_por_ejecucion`/`max_mensajes_por_dia`, and `log_envios`. Keys starting with `_` are
treated as comments and stripped on load. See `ciudad_real/whatsapp_config_bares_restaurantes.json`
for an accurate, complete example. Message templates support `{nombre}`, `{direccion}`,
`{telefono}`, `{rating}`, `{zona}` (parsed from address), and `{tipo_negocio}` (guessed from name).

## Conventions

- Both main scripts force UTF-8 stdout on Windows (`sys.stdout.reconfigure`) for emoji output —
  keep this when adding entry points.
- Secrets live in `config.json` / `whatsapp_config.json` containing the Google API key and Meta
  tokens; `.gitignore` excludes those exact names plus `*.csv` and `envios_whatsapp.log`.
  Region-specific copies use different filenames and so are intentionally committed — do not commit
  a real API key into a newly added `config.json`.
- `docs/` holds extensive Spanish how-to guides and the outreach plan; `docs/CLAUDE.md` carries the
  Karpathy behavioral guidelines (also mirrored in `.cursor/rules/`), and `docs/AGENTS.md`
  documents the optional `agentmemory` MCP server.
