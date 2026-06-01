#!/usr/bin/env python3
"""
Analiza PyWhatKit_DB.txt para clasificar los tipos de negocio contactados.
"""

import re
import sys
import io

# Forzar salida UTF-8 en Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Leer el archivo
with open("PyWhatKit_DB.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Extraer todos los mensajes (solo los que tienen nombre de negocio)
# Patrón: cada bloque tiene Date, Time, Phone Number, Message
blocks = content.split("--------------------\n")

# Categorías con palabras clave
categories = {
    "💈 Peluquería / Barbería / Estilismo": [
        "peluquer", "barber", "barbershop", "estilista", "hair", "peluquero",
        "caballero", "barba", "navaja", "navaj", "corte", "rapado"
    ],
    "💅 Estética / Belleza / Clínica Estética": [
        "estética", "estetica", "belleza", "clínica estética", "clinica estética",
        "clinica xiluet", "salón de belleza", "salon de belleza", "beauty",
        "bienestar", "relax", "cosmetics"
    ],
    "🔧 Taller Mecánico / Automoción / Neumáticos": [
        "taller", "mecánic", "mecanic", "automoci", "automovil", "neumátic",
        "neumatic", "motor", "moto ", "coche", "fragauto", "centralita",
        "reprogramación", "talleres", "jezcomovil"
    ],
    "📊 Gestoría / Asesoría / Contabilidad": [
        "gestoría", "gestoria", "asesor", "contabl", "contabilidad", "auditor",
        "fiscal", "renta", "accountancy", "icac", "pymeséxito", "pymes",
        "société express", "audidat"
    ],
    "⚡ Electricidad / Instalaciones Eléctricas": [
        "electri", "instalacion", "instalación"
    ],
    "🔧 Fontanería / Saneamientos / Baños": [
        "fontaner", "saneamiento", "baño", "calefacci"
    ],
    "💄 Maquillaje / Uñas": [
        "maquill", "uñas", "maquillaje"
    ],
    "🐾 Peluquería Canina / Veterinaria": [
        "canina", "peludito", "veterinar"
    ],
    "🧪 Pruebas (Test)": [
        "esto es una prueba"
    ],
}

# Categorizar cada negocio
business_names = []
for block in blocks:
    block = block.strip()
    if not block:
        continue
    
    # Extraer nombre del negocio del mensaje
    msg_match = re.search(r"Message: (.+)", block)
    if not msg_match:
        continue
    
    message = msg_match.group(1).strip()
    
    # Extraer nombre del negocio
    # Patrón 1: "Hola NOMBRE, soy Mario"
    name_match = re.search(r"Hola\s+(.+?),\s+soy Mario", message)
    if name_match:
        business_name = name_match.group(1).strip()
    else:
        # Patrón 2: "pregunto por el responsable de NOMBRE, soy Mario"
        name_match2 = re.search(r"responsable de (.+?), soy Mario", message)
        if name_match2:
            business_name = name_match2.group(1).strip()
        else:
            business_name = "DESCONOCIDO"
    
    business_names.append((business_name, message))

# Clasificar cada negocio
results = {}
uncategorized = []

for name, msg in business_names:
    msg_lower = msg.lower()
    name_lower = name.lower()
    combined = msg_lower + " " + name_lower
    
    categorized = False
    for cat_name, keywords in categories.items():
        for keyword in keywords:
            if keyword in combined:
                if cat_name not in results:
                    results[cat_name] = []
                results[cat_name].append(name)
                categorized = True
                break
        if categorized:
            break
    
    if not categorized:
        uncategorized.append(name)

# Mostrar resultados
print("=" * 70)
print("📊 ANÁLISIS DE TIPOS DE NEGOCIO CONTACTADOS")
print("=" * 70)
print()

# Ordenar por cantidad
sorted_results = sorted(results.items(), key=lambda x: len(x[1]), reverse=True)

total_contacted = sum(len(v) for v in results.values()) + len(uncategorized)

for cat_name, businesses in sorted_results:
    count = len(businesses)
    pct = (count / total_contacted) * 100
    bar = "█" * int(pct / 2)
    print(f"{cat_name}")
    print(f"   Cantidad: {count} ({pct:.1f}%) {bar}")
    print()

if uncategorized:
    print(f"❓ Otros / No clasificados")
    print(f"   Cantidad: {len(uncategorized)} ({(len(uncategorized)/total_contacted)*100:.1f}%)")
    for u in uncategorized:
        print(f"      - {u}")
    print()

print("=" * 70)
print(f"📋 TOTAL MENSAJES ENVIADOS: {total_contacted}")
print()

print("🏆 TOP 3 MÁS CONTACTADOS:")
for i, (cat_name, businesses) in enumerate(sorted_results[:3]):
    print(f"   {i+1}. {cat_name}: {len(businesses)} contactos")
print()

print("📉 TOP 3 MENOS CONTACTADOS:")
for i, (cat_name, businesses) in enumerate(sorted_results[-3:]):
    print(f"   {i+1}. {cat_name}: {len(businesses)} contactos")
print()

# Detalle por categoría
print("=" * 70)
print("📋 DETALLE POR CATEGORÍA:")
print("=" * 70)
for cat_name, businesses in sorted_results:
    print(f"\n{cat_name} ({len(businesses)}):")
    for b in businesses:
        print(f"   • {b}")

if uncategorized:
    print(f"\n❓ No clasificados ({len(uncategorized)}):")
    for b in uncategorized:
        print(f"   • {b}")