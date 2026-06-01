#!/usr/bin/env python3
import csv, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

log_phones = set()
with open('envios_whatsapp.log', 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split('|')
        if len(parts) >= 3:
            log_phones.add(parts[1].strip())

with open('negocios_sin_web_ciudad_real_20260405_205915.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    businesses = list(reader)

ya_enviados = []
sin_telefono = []
fijos = []
pendientes = []

for b in businesses:
    nombre = b.get('nombre', '?')
    raw_phone = b.get('telefono', '').strip()
    if not raw_phone:
        sin_telefono.append(nombre)
        continue
    cleaned = re.sub(r'[\s\-\.\(\)\+]', '', raw_phone)
    if not cleaned.startswith('34'):
        cleaned = '34' + cleaned
    if not cleaned.isdigit() or len(cleaned) < 10 or len(cleaned) > 15:
        continue
    numero = cleaned[2:]
    if numero[0] not in ('6', '7'):
        fijos.append((nombre, raw_phone))
        continue
    if cleaned in log_phones:
        ya_enviados.append((nombre, cleaned))
    else:
        pendientes.append((nombre, raw_phone))

print('=' * 70)
print('CSV ACTIVO: negocios_sin_web_ciudad_real_20260405_205915.csv')
print('Ciudad: Ciudad Real | Config: solo_moviles=true')
print('=' * 70)
print(f'Total en CSV:        {len(businesses)}')
print(f'Ya enviados (OK):    {len(ya_enviados)}')
print(f'Pendientes (movil):  {len(pendientes)}')
print(f'Telefonos fijos:     {len(fijos)}')
print(f'Sin telefono:        {len(sin_telefono)}')
print()
print('-' * 70)
print(f'DISPONIBLES PARA ENVIAR ({len(pendientes)} negocios):')
print('-' * 70)
for i, (nombre, raw) in enumerate(pendientes, 1):
    print(f'  {i:3d}. {nombre[:50]:<50s} | {raw}')