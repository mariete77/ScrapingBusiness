#!/usr/bin/env python3
"""
Script para combinar múltiples CSVs de negocios en uno solo.
Elimina duplicados basándose en el teléfono.
"""

import sys
import csv
import os

# Forzar UTF-8 en la consola de Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
import glob
import os
import re
from datetime import datetime

def limpiar_telefono(telefono):
    """Limpia y normaliza el número de teléfono."""
    if not telefono:
        return None
    cleaned = re.sub(r'[\s\-\.\(\)]', '', str(telefono).strip())
    if cleaned.startswith('+'):
        cleaned = cleaned[1:]
    # Añadir prefijo 34 si no lo tiene
    if not cleaned.startswith('34'):
        cleaned = '34' + cleaned
    return cleaned

def combinar_csvs():
    """Combina todos los CSVs de negocios sin web en uno solo."""
    
    # Buscar todos los CSVs de negocios sin web
    patterns = [
        "bares_restaurantes_*_sin_web_*.csv",
        "negocios_sin_web_ciudad_real*.csv"
    ]
    csv_files = []
    for pattern in patterns:
        csv_files.extend(glob.glob(pattern))
    
    # Eliminar duplicados en la lista
    csv_files = list(set(csv_files))
    
    if not csv_files:
        print("❌ No se encontraron archivos CSV de restaurantes sin web")
        return
    
    print(f"📂 Encontrados {len(csv_files)} archivos CSV:")
    for f in csv_files:
        print(f"   - {f}")
    
    # Diccionario para eliminar duplicados: telefono limpio -> datos
    negocios = {}
    origen_archivo = {}
    
    # Leer todos los CSVs
    for csv_file in csv_files:
        print(f"\n📖 Leyendo: {csv_file}")
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                count = 0
                for row in reader:
                    telefono_raw = row.get('telefono', '').strip()
                    telefono_limpio = limpiar_telefono(telefono_raw)
                    
                    if not telefono_limpio or len(telefono_limpio) < 10:
                        continue
                    
                    # Usar el teléfono como clave para eliminar duplicados
                    if telefono_limpio not in negocios:
                        row['telefono_normalizado'] = telefono_limpio
                        negocios[telefono_limpio] = row
                        origen_archivo[telefono_limpio] = csv_file
                        count += 1
                    else:
                        print(f"   ⚠️  Duplicado: {row.get('nombre', '?')} ({telefono_raw})")
                
                print(f"   ✅ Leídos {count} únicos de este archivo")
        except Exception as e:
            print(f"   ❌ Error leyendo {csv_file}: {e}")
    
    # Generar nombre de archivo de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"bares_restaurantes_ciudad_real_provincia_sin_web_{timestamp}.csv"
    
    if not negocios:
        print("\n❌ No hay negocios para combinar")
        return
    
    # Escribir CSV combinado
    print(f"\n💾 Escribiendo archivo combinado: {output_file}")
    
    # Definir columnas
    fieldnames = [
        'nombre', 'direccion', 'telefono', 'rating', 
        'resenas', 'tipos', 'estado_envio', 'telefono_normalizado'
    ]
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        
        for telefono, negocio in negocios.items():
            writer.writerow(negocio)
    
    # Estadísticas
    print(f"\n{'=' * 60}")
    print(f"📊 Resumen de la combinación")
    print(f"{'=' * 60}")
    print(f"📂 Archivos procesados: {len(csv_files)}")
    print(f"📞 Total de negocios únicos: {len(negocios)}")
    print(f"💾 Archivo de salida: {output_file}")
    
    # Contar por origen
    print(f"\n📋 Negocios por archivo de origen:")
    por_origen = {}
    for telefono, origen in origen_archivo.items():
        por_origen[origen] = por_origen.get(origen, 0) + 1
    
    for origen, count in sorted(por_origen.items()):
        print(f"   - {origen}: {count} negocios")
    
    print(f"\n✅ ¡Listo! Puedes usar este archivo para enviar mensajes:")
    print(f"   python whatsapp_sender.py --yes")
    
    # Actualizar configuración para usar el nuevo archivo
    print(f"\n📝 Para usar el nuevo archivo, actualiza:")
    print(f'   "archivo_csv": "{output_file}"')
    print(f"   en tu archivo de configuración JSON")

if __name__ == "__main__":
    print("=" * 60)
    print("📋 Combinador de CSVs - Negocios Sin Web")
    print("=" * 60)
    print()
    
    combinar_csvs()