#!/usr/bin/env python3
import csv, re, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# All Ciudad Real CSVs
csv_files = glob.glob("negocios_sin_web_ciudad_real_*.csv")

all_businesses = []
for f in csv_files:
    with open(f, 'r', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            row['_source'] = f
            all_businesses.append(row)

# Extract unique towns from addresses
towns = set()
for b in all_businesses:
    addr = b.get('direccion', '')
    # Extract town from address (usually last part before "España")
    if 'España' in addr:
        parts = addr.split(',')
        for p in parts:
            p = p.strip()
            # CP pattern: 5 digits
            match = re.match(r'\d{5}\s+(.+)', p)
            if match:
                town = match.group(1).strip()
                towns.add(town)

# Count by town
from collections import Counter
town_counts = Counter()
for b in all_businesses:
    addr = b.get('direccion', '')
    if 'España' in addr:
        parts = addr.split(',')
        for p in parts:
            p = p.strip()
            match = re.match(r'\d{5}\s+(.+)', p)
            if match:
                town_counts[match.group(1).strip()] += 1

# Deduplicated total
seen = set()
unique = []
for b in all_businesses:
    key = b.get('nombre', '').lower().strip()
    if key not in seen:
        seen.add(key)
        unique.append(b)

print("=" * 70)
print("COBERTURA ACTUAL - PROVINCIA DE CIUDAD REAL")
print("=" * 70)
print(f"CSVs encontrados: {len(csv_files)}")
for f in csv_files:
    print(f"  - {f}")
print(f"\nTotal registros (con duplicados): {len(all_businesses)}")
print(f"Total negocios únicos (por nombre): {len(unique)}")

print(f"\n{'─' * 70}")
print(f"CIUDADES/PUEBLOS ENCONTRADOS ({len(town_counts)}):")
print(f"{'─' * 70}")
for town, count in sorted(town_counts.items(), key=lambda x: -x[1]):
    print(f"  {town:<35s} → {count:3d} negocios")

print(f"\n{'─' * 70}")
print("UBICACIONES CONFIGURADAS ACTUALMENTE (config.json):")
print(f"{'─' * 70}")
locations = [
    ("Ciudad Real", "38.9866,-3.9304"),
    ("Alcázar de San Juan", "39.3935,-3.2085"),
    ("Valdepeñas", "38.7612,-3.3838"),
    ("Puertollano", "38.6867,-4.1070"),
    ("Tomelloso", "39.1749,-3.0240"),
]
for name, coord in locations:
    print(f"  ✅ {name:<25s} ({coord})")

# Major towns in Ciudad Real province NOT covered
print(f"\n{'─' * 70}")
print("CIUDADES IMPORTANTES DE CIUDAD REAL NO CUBIERTAS:")
print(f"{'─' * 70}")
missing = [
    ("Manzanares", "38.9998,-3.3700", "~18.000 hab"),
    ("Daimiel", "39.0725,-3.6170", "~17.000 hab"),
    ("La Solana", "38.7069,-3.3524", "~16.000 hab"),
    ("Villarrubia de los Ojos", "39.2089,-3.6229", "~10.000 hab"),
    ("San Clemente", "39.4013,-2.4244", "~7.000 hab"),
    ("Villanueva de los Infantes", "38.4738,-3.0215", "~5.500 hab"),
    ("Malagón", "38.8310,-3.7510", "~9.000 hab"),
    ("Almadén", "38.7776,-4.8274", "~6.000 hab"),
    ("Navalmoral de la Mata", "39.8919,-5.5404", "NOT CR"),
]
for name, coord, hab in missing:
    print(f"  ❌ {name:<30s} ({coord}) - {hab}")