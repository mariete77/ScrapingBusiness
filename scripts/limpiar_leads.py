#!/usr/bin/env python3
"""
Limpia un CSV de leads y lo separa en dos listas segun tengan web o no.

- Descarta entidades publicas (ayuntamientos, juzgados, Hacienda...) que la
  Places API devuelve mezcladas con las asesorias reales.
- Descarta los que no tienen telefono: sin telefono no hay outreach posible.
- Escribe dos CSV con las MISMAS columnas que el original, para que
  whatsapp_sender.py pueda leerlos sin cambios.

Uso (desde la carpeta de la region):
    python ..\\scripts\\limpiar_leads.py asesorias_huelva_provincia_20260802_201012.csv
"""

import csv
import os
import sys
from typing import Dict, List

# Forzar UTF-8 en la consola de Windows para soportar emojis
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Nombres que delatan una entidad publica, no un negocio al que vender
PALABRAS_PUBLICAS = (
    "ayuntamiento",
    "juzgado",
    "registro de la propiedad",
    "administracion de hacienda",
    "administración de hacienda",
    "agencia tributaria",
    "agencia gestion tributaria",
    "agencia gestión tributaria",
    "mancomunidad",
    "oficina municipal",
    "omic",
    "diputacion",
    "diputación",
    "seguridad social",
    "tesoreria general",
    "tesorería general",
    "aqualia",
)


def es_publica(nombre: str) -> bool:
    """True si el nombre corresponde a una entidad publica."""
    n = nombre.lower()
    return any(p in n for p in PALABRAS_PUBLICAS)


def cargar(ruta: str) -> List[Dict]:
    with open(ruta, mode='r', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def escribir(ruta: str, filas: List[Dict], fieldnames: List[str]) -> None:
    with open(ruta, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(filas)


def main() -> None:
    if len(sys.argv) < 2:
        print("❌ ERROR: falta el CSV de entrada")
        print("   Uso: python ..\\scripts\\limpiar_leads.py <archivo.csv>")
        sys.exit(1)

    entrada = sys.argv[1]
    if not os.path.exists(entrada):
        print(f"❌ ERROR: no existe '{entrada}'")
        sys.exit(1)

    filas = cargar(entrada)
    if not filas:
        print(f"⚠️ '{entrada}' no tiene filas")
        sys.exit(1)

    fieldnames = list(filas[0].keys())

    publicas = [r for r in filas if es_publica(r['nombre'])]
    candidatas = [r for r in filas if not es_publica(r['nombre'])]
    sin_telefono = [r for r in candidatas if not r['telefono'].strip()]
    contactables = [r for r in candidatas if r['telefono'].strip()]

    sin_web = [r for r in contactables if r['tiene_web'] == 'NO']
    con_web = [r for r in contactables if r['tiene_web'] == 'SI']

    base = os.path.splitext(os.path.basename(entrada))[0]
    # El prefijo "negocios_sin_web_" es el que whatsapp_sender.py busca por defecto
    ruta_sin_web = f"negocios_sin_web_{base}.csv"
    ruta_con_web = f"con_web_{base}.csv"

    escribir(ruta_sin_web, sin_web, fieldnames)
    escribir(ruta_con_web, con_web, fieldnames)

    print("=" * 60)
    print(f"🧹 Limpieza de {entrada}")
    print("=" * 60)
    print(f"   Filas de entrada:        {len(filas)}")
    print(f"   - Entidades publicas:    {len(publicas)} (descartadas)")
    print(f"   - Sin telefono:          {len(sin_telefono)} (descartadas)")
    print(f"   = Contactables:          {len(contactables)}")
    print()
    print(f"📄 {ruta_sin_web}")
    print(f"   {len(sin_web)} sin web  → oferta: pagina web")
    print(f"📄 {ruta_con_web}")
    print(f"   {len(con_web)} con web  → oferta: partner tecnologico / automatizacion")
    print("=" * 60)

    if publicas:
        print("\n🏛️ Descartadas por publicas:")
        for r in publicas:
            print(f"   - {r['nombre'][:55]}")


if __name__ == "__main__":
    main()
