#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para analizar qué números del CSV son móviles (tienen WhatsApp)
y cuántos son fijos (no tienen WhatsApp).
"""

import csv
import re
import sys

# Configurar la consola para UTF-8 en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def es_movil(telefono):
    """Verifica si un teléfono es móvil (empieza por 6 o 7 después del prefijo 34)."""
    if not telefono or not telefono.strip():
        return False
    
    # Limpiar el número
    clean = re.sub(r'[\s\-\.\(\)]', '', telefono.strip())
    
    # Si empieza por +, quitar el +
    if clean.startswith('+'):
        clean = clean[1:]
    
    # Añadir prefijo 34 si no lo tiene
    prefix = "34"
    if not clean.startswith(prefix):
        clean = prefix + clean
    
    # Verificar que después del 34 empieza por 6 o 7
    if len(clean) >= 3:
        numero_sin_prefijo = clean[2:]
        if numero_sin_prefijo and numero_sin_prefijo[0] in ('6', '7'):
            return True
    
    return False

def main():
    csv_file = "bares_restaurantes_ciudad_real_sin_web_20260430_115507.csv"
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        moviles = []
        fijos = []
        sin_telefono = []
        
        for row in reader:
            nombre = row['nombre']
            telefono = row['telefono']
            rating = row['rating']
            reseñas = row['reseñas']
            tipos = row['tipos']
            
            if not telefono or not telefono.strip():
                sin_telefono.append({
                    'nombre': nombre,
                    'rating': rating,
                    'reseñas': reseñas
                })
            elif es_movil(telefono):
                moviles.append({
                    'nombre': nombre,
                    'telefono': telefono,
                    'rating': rating,
                    'reseñas': reseñas,
                    'tipos': tipos
                })
            else:
                fijos.append({
                    'nombre': nombre,
                    'telefono': telefono,
                    'rating': rating,
                    'reseñas': reseñas,
                    'tipos': tipos
                })
    
    print("=" * 60)
    print("📊 ANÁLISIS DE TELÉFONOS - BARES Y RESTAURANTES")
    print("=" * 60)
    print(f"\n📱 MÓVILES (tienen WhatsApp): {len(moviles)}")
    print(f"📞 FIJOS (NO tienen WhatsApp): {len(fijos)}")
    print(f"❌ SIN TELÉFONO: {len(sin_telefono)}")
    print(f"📋 TOTAL: {len(moviles) + len(fijos) + len(sin_telefono)}")
    
    print("\n" + "=" * 60)
    print("📱 NEGOCIOS CON MÓVIL (pueden recibir WhatsApp)")
    print("=" * 60)
    print(f"\n{'Nombre':<40} {'Teléfono':<15} {'Rating':<7} {'Reseñas':<10}")
    print("-" * 80)
    for neg in sorted(moviles, key=lambda x: float(x['rating']), reverse=True):
        print(f"{neg['nombre'][:39]:<40} {neg['telefono']:<15} {neg['rating']:<7} {neg['reseñas']:<10}")
    
    print("\n" + "=" * 60)
    print("📞 NEGOCIOS CON TELÉFONO FIJO (NO pueden recibir WhatsApp)")
    print("=" * 60)
    print(f"\n{'Nombre':<40} {'Teléfono':<15} {'Rating':<7} {'Reseñas':<10}")
    print("-" * 80)
    for neg in sorted(fijos, key=lambda x: float(x['rating']), reverse=True):
        print(f"{neg['nombre'][:39]:<40} {neg['telefono']:<15} {neg['rating']:<7} {neg['reseñas']:<10}")
    
    print("\n" + "=" * 60)
    print("❌ NEGOCIOS SIN TELÉFONO")
    print("=" * 60)
    print(f"\n{'Nombre':<40} {'Rating':<7} {'Reseñas':<10}")
    print("-" * 60)
    for neg in sorted(sin_telefono, key=lambda x: float(x['rating']) if x['rating'] else 0, reverse=True):
        print(f"{neg['nombre'][:39]:<40} {neg['rating']:<7} {neg['reseñas']:<10}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRIORIDAD")
    print("=" * 60)
    
    # Alta prioridad: móvil + rating >= 4.0 + reseñas >= 100
    alta_prioridad = [n for n in moviles if float(n['rating']) >= 4.0 and int(n['reseñas']) >= 100]
    media_prioridad = [n for n in moviles if float(n['rating']) >= 3.5 and int(n['reseñas']) >= 50]
    
    print(f"\n🎯 ALTA PRIORIDAD (Móvil + Rating ≥4.0 + ≥100 reseñas): {len(alta_prioridad)}")
    for neg in sorted(alta_prioridad, key=lambda x: float(x['rating']), reverse=True):
        print(f"   ⭐ {neg['nombre'][:40]} ({neg['rating']}) - {neg['reseñas']} reseñas - {neg['telefono']}")
    
    print(f"\n⚠️  PRIORIDAD MEDIA (Móvil + Rating ≥3.5 + ≥50 reseñas): {len(media_prioridad)}")
    for neg in sorted(media_prioridad, key=lambda x: float(x['rating']), reverse=True):
        if neg not in alta_prioridad:
            print(f"   ⭐ {neg['nombre'][:40]} ({neg['rating']}) - {neg['reseñas']} reseñas - {neg['telefono']}")
    
    print("\n" + "=" * 60)
    print("✅ CONCLUSIÓN")
    print("=" * 60)
    print(f"\nDe {len(moviles) + len(fijos) + len(sin_telefono)} negocios totales:")
    print(f"• Solo {len(moviles)} tienen WhatsApp ({len(moviles)/(len(moviles) + len(fijos) + len(sin_telefono))*100:.1f}%)")
    print(f"• {len(fijos)} tienen teléfono fijo (NO tienen WhatsApp)")
    print(f"• {len(sin_telefono)} no tienen teléfono")
    print(f"\n🎯 Objetivo: Contactar a los {len(alta_prioridad)} de alta prioridad primero")

if __name__ == "__main__":
    main()