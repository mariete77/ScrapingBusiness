#!/usr/bin/env python3
"""
Script para buscar negocios en Madrid sin web usando Google Places API (Nueva).

Autor: Koda (AI Assistant)
Fecha: 2026-03-30
Actualizado: 2026-04-04 - Migrado a nueva Places API (places.googleapis.com/v1)

Requisitos:
- Python 3.7+
- API key de Google Places (gratis: https://console.cloud.google.com/apis/library/places-backend.googleapis.com)
  ⚠️ Debes habilitar "Places API (New)" en la consola de Google Cloud, no solo la antigua.
"""

import sys
import requests
import csv
import json
import time
import os
from typing import List, Dict, Optional
from datetime import datetime

# Forzar UTF-8 en la consola de Windows para soportar emojis
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class BusinessFinder:
    def __init__(self, config_file: str = "config.json"):
        """Inicializa el buscador con configuración desde JSON."""
        self.config = self._load_config(config_file)
        self.base_url = "https://places.googleapis.com/v1/places"
        self.headers = {
            "X-Goog-Api-Key": self.config['api_key'],
            "X-Goog-FieldMask": (
                "places.id,places.displayName,places.formattedAddress,"
                "places.nationalPhoneNumber,places.websiteUri,places.rating,"
                "places.userRatingCount,places.types,nextPageToken"
            )
        }
        self.results = []
        self.total_found = 0
        self.without_website_count = 0
        self._seen_names = set()  # para deduplicar
        # "sin_web" (por defecto), "con_web" o "todos"
        self.filtro_web = self.config.get('filtro_web', 'sin_web')

    def _load_config(self, config_file: str) -> Dict:
        """Carga configuración desde archivo JSON."""
        if not os.path.exists(config_file):
            print(f"❌ ERROR: Archivo de configuración '{config_file}' no encontrado")
            print(f"\n📝 Pasos:")
            print(f"1. Copia 'config.example.json' a '{config_file}'")
            print(f"2. Edita '{config_file}' y pon tu API key de Google Places")
            print(f"3. Vuelve a ejecutar el script")
            exit(1)

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # Validar campos requeridos
        required_fields = ['api_key', 'location', 'radius', 'search_type']
        for field in required_fields:
            if field not in config:
                print(f"❌ ERROR: Campo '{field}' faltante en configuración")
                exit(1)

        # Validar filtro de web
        filtro = config.get('filtro_web', 'sin_web')
        if filtro not in ('sin_web', 'con_web', 'todos'):
            print(f"❌ ERROR: 'filtro_web' debe ser 'sin_web', 'con_web' o 'todos' (recibido: '{filtro}')")
            exit(1)

        # Validar API key
        if config['api_key'] == "TU_API_KEY_AQUI":
            print(f"❌ ERROR: Debes configurar tu API key en {config_file}")
            print("\n📝 Pasos para obtener API key:")
            print("1. Ve a: https://console.cloud.google.com/apis/library/places-backend.googleapis.com")
            print("2. Crea un proyecto y habilita la 'Places API (New)'")
            print("3. Crea credenciales → API key")
            print(f"4. Copia la API key y pégala en {config_file}")
            print("\n💰 La API key tiene $200 de crédito mensual GRATIS")
            exit(1)

        return config

    def search_places(self) -> List[Dict]:
        """Busca lugares usando Google Places API (New) - Text Search."""
        url = f"{self.base_url}:searchText"

        # Query de búsqueda
        query = f"{self.config['search_type']} {self.config.get('location_name', 'Madrid')}"

        # Parsear coordenadas
        try:
            lat, lng = self.config['location'].split(',')
            latitude = float(lat.strip())
            longitude = float(lng.strip())
        except ValueError:
            print(f"❌ ERROR: Formato de ubicación inválido: '{self.config['location']}'")
            print("   Usa el formato: '40.416775,-3.703790'")
            return []

        # Body de la petición
        body = {
            "textQuery": query,
            "languageCode": self.config.get('language', 'es'),
            "pageSize": 20,
            "locationBias": {
                "circle": {
                    "center": {
                        "latitude": latitude,
                        "longitude": longitude
                    },
                    "radius": self.config['radius']
                }
            }
        }

        try:
            print(f"🔍 Buscando: {query}")
            print(f"📍 Ubicación: {self.config['location']} (radio: {self.config['radius']}m)")
            response = requests.post(url, json=body, headers=self.headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            # La nueva API devuelve errores en data["error"]
            if "error" in data:
                error = data["error"]
                print(f"❌ Error en API: {error.get('status', 'DESCONOCIDO')}")
                print(f"Mensaje: {error.get('message', 'Sin detalles')}")
                if error.get('status') == 'PERMISSION_DENIED':
                    print("\n💡 Solución: Asegúrate de haber habilitado 'Places API (New)' en:")
                    print("   https://console.cloud.google.com/apis/library/places-backend.googleapis.com")
                return []

            places = data.get("places", [])
            print(f"✅ Encontrados {len(places)} negocios")

            # Procesar resultados (ya incluyen websiteUri, no necesitan petición aparte)
            self._process_places(places)

            # Paginación si hay más resultados
            next_page_token = data.get("nextPageToken")
            page_count = 0
            max_pages = 20  # Límite de páginas para evitar loops infinitos

            while (next_page_token and
                   len(self.results) < self.config.get('max_results', 100) and
                   page_count < max_pages):

                print(f"📄 Obteniendo más resultados... (página {page_count + 2})")
                time.sleep(2)  # Google requiere esperar entre peticiones

                body["pageToken"] = next_page_token
                response = requests.post(url, json=body, headers=self.headers, timeout=30)
                response.raise_for_status()
                data = response.json()

                if "error" in data:
                    error = data["error"]
                    print(f"⚠️ Error en paginación: {error.get('status', 'DESCONOCIDO')} - {error.get('message', '')}")
                    break

                places = data.get("places", [])
                if places:
                    self._process_places(places)
                    page_count += 1
                else:
                    break

                next_page_token = data.get("nextPageToken")
                # Limpiar pageToken del body para la siguiente iteración
                if "pageToken" in body:
                    del body["pageToken"]

            return places

        except requests.exceptions.Timeout:
            print("❌ Error: Timeout de conexión (más de 30 segundos)")
            return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red: {e}")
            return []
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []

    def _debe_guardar(self, website: str) -> bool:
        """Decide si el negocio entra en el CSV según 'filtro_web'."""
        if self.filtro_web == 'todos':
            return True
        if self.filtro_web == 'con_web':
            return bool(website)
        return not website

    def _process_places(self, places: List[Dict]):
        """Procesa los lugares y aplica el filtro de web configurado."""
        for place in places:
            try:
                self.total_found += 1

                # Extraer datos con la estructura de la nueva API
                name = place.get("displayName", {}).get("text", "")
                website = place.get("websiteUri", "")

                business_info = {
                    "nombre": name,
                    "direccion": place.get("formattedAddress", ""),
                    "telefono": place.get("nationalPhoneNumber", ""),
                    "correo": "",  # Google Places API no proporciona emails
                    "website": website if website else "NO",
                    "rating": place.get("rating", 0) or 0,
                    "reseñas": place.get("userRatingCount", 0) or 0,
                    "tipos": ", ".join(place.get("types", [])),
                    "tiene_web": "SI" if website else "NO",
                    "fecha_buscado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                if not website:
                    self.without_website_count += 1

                # Guardar según 'filtro_web' (evitar duplicados)
                etiqueta = "Con web" if website else "Sin web"
                if not self._debe_guardar(website):
                    print(f"⏭️ Descartado ({etiqueta.lower()}): {name[:40]}...")
                    continue

                name_key = name.lower().strip()
                if name_key in self._seen_names:
                    print(f"🔁 Duplicado: {name[:40]}...")
                    continue
                self._seen_names.add(name_key)
                self.results.append(business_info)
                print(f"📌 {etiqueta}: {business_info['nombre'][:40]}... (⭐{business_info['rating']})")

                # Pequeña pausa para no exceder cuota
                time.sleep(0.1)

            except Exception as e:
                print(f"❌ Error procesando negocio: {e}")
                continue

    def export_to_csv(self):
        """Exporta los resultados a CSV."""
        if not self.results:
            print(f"\n⚠️ No hay negocios que cumplan el filtro '{self.filtro_web}' para exportar")
            print("💡 Intenta:")
            print("   - Aumentar el radio de búsqueda (radius)")
            print("   - Cambiar el tipo de negocio (search_type)")
            print("   - Cambiar 'filtro_web' ('sin_web', 'con_web' o 'todos')")
            print("   - Verificar que la API key está correcta y que 'Places API (New)' está habilitada")
            return

        # Crear nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{self.config.get('output_prefix', 'negocios_sin_web')}_{timestamp}.csv"

        # Definir columnas
        fieldnames = [
            "fecha_buscado",
            "nombre",
            "direccion",
            "telefono",
            "correo",
            "tiene_web",
            "website",
            "rating",
            "reseñas",
            "tipos"
        ]

        try:
            with open(output_filename, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.results)

            print(f"\n✅ Exportados {len(self.results)} negocios a {output_filename}")
            print(f"📊 Estadísticas:")
            print(f"   - Total buscados: {self.total_found}")
            print(f"   - Sin web: {self.without_website_count} ({self._percentage(self.without_website_count, self.total_found)}%)")
            print(f"   - Con web: {self.total_found - self.without_website_count} ({self._percentage(self.total_found - self.without_website_count, self.total_found)}%)")
            print(f"   - Filtro aplicado: {self.filtro_web}")
            print(f"\n🎯 LISTO! Tienes {len(self.results)} clientes potenciales")
            print(f"\n📋 Siguientes pasos:")
            print(f"1. Abre el CSV: {output_filename}")
            print(f"2. Revisa los negocios exportados")
            print(f"3. Haz outreach con las plantillas en plan-outreach.md")

        except Exception as e:
            print(f"❌ Error exportando CSV: {e}")

    def _percentage(self, part: int, total: int) -> float:
        """Calcula el porcentaje."""
        if total == 0:
            return 0
        return round((part / total) * 100, 1)


def main():
    """Función principal."""
    print("=" * 60)
    print("🦊 Koda - Buscador de Negocios Sin Web")
    print("=" * 60)
    print()

    start_time = time.perf_counter()

    # Determinar archivo de configuración
    config_file = "config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        print(f"📁 Usando configuración: {config_file}")
        print()

    # Crear buscador
    try:
        finder = BusinessFinder(config_file)
    except SystemExit:
        return

    # Buscar lugares
    print(f"🏢 Tipo: {finder.config['search_type']}")
    print(f"📊 Resultados máximos: {finder.config.get('max_results', 100)}")
    print()

    # Construir lista de ubicaciones
    locations = [(finder.config['location'], finder.config.get('location_name', ''))]
    extra_locs = finder.config.get('locations_extra', '')
    extra_names = finder.config.get('locations_extra_names', '')
    if extra_locs:
        coords = [c.strip() for c in extra_locs.split(';') if c.strip()]
        names = [n.strip() for n in extra_names.split(';') if n.strip()]
        for i, coord in enumerate(coords):
            name = names[i] if i < len(names) else coord
            locations.append((coord, name))

    # Construir lista de tipos de búsqueda
    search_types = [s.strip() for s in finder.config['search_type'].split(',')]

    multi = len(search_types) > 1 or len(locations) > 1
    if multi:
        print(f"📊 Ubicaciones: {', '.join(n for _, n in locations)}")
        print(f"📊 Sectores: {', '.join(search_types)}")
        print()

    for loc_coord, loc_name in locations:
        if len(finder.results) >= finder.config.get('max_results', 100):
            break
        finder.config['location'] = loc_coord
        finder.config['location_name'] = loc_name
        for stype in search_types:
            if len(finder.results) >= finder.config.get('max_results', 100):
                break
            if multi:
                print(f"{'─' * 60}")
                print(f"📍 {loc_name} → {stype}")
                print(f"{'─' * 60}")
            finder.config['search_type'] = stype
            finder.search_places()
            time.sleep(2)

    # Restaurar config original
    finder.config['location'] = locations[0][0]
    finder.config['location_name'] = locations[0][1]
    finder.config['search_type'] = ', '.join(search_types)

    # Exportar resultados
    finder.export_to_csv()

    # Estadísticas finales
    print("\n" + "=" * 60)
    print("📈 Resumen de la ejecución")
    print("=" * 60)
    elapsed = time.perf_counter() - start_time
    print(f"Tiempo total: {elapsed:.2f} segundos")
    print(f"Negocios encontrados: {finder.total_found}")
    print(f"Sin web: {finder.without_website_count}")
    print(f"Con web: {finder.total_found - finder.without_website_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()