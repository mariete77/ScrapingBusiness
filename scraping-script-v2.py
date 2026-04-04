#!/usr/bin/env python3
"""
Script para buscar negocios en Madrid sin web usando Google Places API.

Autor: Koda (AI Assistant)
Fecha: 2026-03-30

Requisitos:
- Python 3.7+
- API key de Google Places (gratis: https://console.cloud.google.com/apis/library/places-backend.googleapis.com)
"""

import requests
import csv
import json
import time
import os
from typing import List, Dict, Optional
from datetime import datetime


class BusinessFinder:
    def __init__(self, config_file: str = "config.json"):
        """Inicializa el buscador con configuración desde JSON."""
        self.config = self._load_config(config_file)
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.businesses_without_website = []
        self.total_found = 0
        self.without_website_count = 0

    def _load_config(self, config_file: str) -> Dict:
        """Carga configuración desde archivo JSON."""
        if not os.path.exists(config_file):
            print(f"❌ ERROR: Archivo de configuración '{config_file}' no encontrado")
            print(f"\n📝 Pasos:")
            print(f"1. Copia 'config.example.json' a 'config.json'")
            print(f"2. Edita 'config.json' y pon tu API key de Google Places")
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

        # Validar API key
        if config['api_key'] == "TU_API_KEY_AQUI":
            print("❌ ERROR: Debes configurar tu API key en config.json")
            print("\n📝 Pasos para obtener API key:")
            print("1. Ve a: https://console.cloud.google.com/apis/library/places-backend.googleapis.com")
            print("2. Crea un proyecto y habilita la 'Places API'")
            print("3. Crea credenciales → API key")
            print("4. Copia la API key y pégala en config.json")
            print("\n💰 La API key tiene $200 de crédito mensual GRATIS")
            exit(1)

        return config

    def search_places(self) -> List[Dict]:
        """Busca lugares usando Google Places API (Text Search)."""
        url = f"{self.base_url}/textsearch/json"

        # Query de búsqueda
        query = f"{self.config['search_type']} {self.config.get('location_name', 'Madrid')}"

        params = {
            "query": query,
            "location": self.config['location'],
            "radius": self.config['radius'],
            "key": self.config['api_key'],
            "language": self.config.get('language', 'es')
        }

        try:
            print(f"🔍 Buscando: {query}")
            print(f"📍 Ubicación: {self.config['location']} (radio: {self.config['radius']}m)")
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "OK":
                places = data.get("results", [])
                print(f"✅ Encontrados {len(places)} negocios")

                # Obtener detalles de cada negocio
                self._get_places_details(places)

                # Paginación si hay más resultados
                next_page_token = data.get("next_page_token")
                page_count = 0
                max_pages = 5  # Límite de páginas para evitar loops infinitos

                while (next_page_token and
                       len(self.businesses_without_website) < self.config.get('max_results', 100) and
                       page_count < max_pages):

                    print(f"📄 Obteniendo más resultados... (página {page_count + 2})")
                    time.sleep(2)  # Google requiere esperar entre peticiones
                    more_places = self._get_next_page(next_page_token)
                    if more_places:
                        places.extend(more_places)
                        self._get_places_details(more_places)
                        data = {"next_page_token": None}  # Reset para siguiente iteración
                        page_count += 1
                    else:
                        break

                return places
            else:
                print(f"❌ Error en API: {data.get('status')}")
                print(f"Mensaje: {data.get('error_message', 'Sin detalles')}")
                return []

        except requests.exceptions.Timeout:
            print("❌ Error: Timeout de conexión (más de 30 segundos)")
            return []
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de red: {e}")
            return []
        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []

    def _get_next_page(self, next_page_token: str) -> Optional[List[Dict]]:
        """Obtiene la siguiente página de resultados."""
        url = f"{self.base_url}/textsearch/json"

        params = {
            "pagetoken": next_page_token,
            "key": self.config['api_key']
        }

        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "OK":
                return data.get("results", [])
            else:
                print(f"⚠️ Error en paginación: {data.get('status')}")
                return None

        except Exception as e:
            print(f"❌ Error en paginación: {e}")
            return None

    def _get_places_details(self, places: List[Dict]):
        """Obtiene detalles de cada negocio, incluyendo website."""
        url = f"{self.base_url}/details/json"

        for place in places:
            try:
                place_id = place.get("place_id")
                if not place_id:
                    continue

                self.total_found += 1

                params = {
                    "place_id": place_id,
                    "key": self.config['api_key'],
                    "fields": "name,formatted_address,formatted_phone_number,website,rating,review_count,types"
                }

                response = requests.get(url, params=params, timeout=15)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "OK":
                    result = data.get("result", {})

                    # Extraer información
                    business_info = {
                        "nombre": result.get("name", ""),
                        "direccion": result.get("formatted_address", ""),
                        "telefono": result.get("formatted_phone_number", ""),
                        "website": result.get("website", "NO"),
                        "rating": result.get("rating", 0),
                        "reseñas": result.get("review_count", 0),
                        "tipos": ", ".join(result.get("types", [])),
                        "tiene_web": "SI" if result.get("website") else "NO",
                        "fecha_buscado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # Solo guardar los que NO tienen web
                    if not result.get("website"):
                        self.businesses_without_website.append(business_info)
                        self.without_website_count += 1
                        print(f"📌 Sin web: {business_info['nombre'][:40]}... (⭐{business_info['rating']})")
                    else:
                        print(f"✅ Con web: {business_info['nombre'][:40]}... (⭐{business_info['rating']})")

                    # Pequeña pausa para no exceder cuota
                    time.sleep(0.1)

                else:
                    print(f"⚠️ Error obteniendo detalles: {data.get('status')}")

            except Exception as e:
                print(f"❌ Error obteniendo detalles: {e}")
                continue

    def export_to_csv(self):
        """Exporta los resultados a CSV."""
        if not self.businesses_without_website:
            print("\n⚠️ No hay negocios sin web para exportar")
            print("💡 Intenta:")
            print("   - Aumentar el radio de búsqueda (radius)")
            print("   - Cambiar el tipo de negocio (search_type)")
            print("   - Verificar que la API key está correcta")
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
                writer.writerows(self.businesses_without_website)

            print(f"\n✅ Exportados {len(self.businesses_without_website)} negocios a {output_filename}")
            print(f"📊 Estadísticas:")
            print(f"   - Total buscados: {self.total_found}")
            print(f"   - Sin web: {self.without_website_count} ({self._percentage(self.without_website_count, self.total_found)}%)")
            print(f"   - Con web: {self.total_found - self.without_website_count} ({self._percentage(self.total_found - self.without_website_count, self.total_found)}%)")
            print(f"\n🎯 LISTO! Tienes {len(self.businesses_without_website)} clientes potenciales")
            print(f"\n📋 Siguientes pasos:")
            print(f"1. Abre el CSV: {output_filename}")
            print(f"2. Revisa los negocios sin web")
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

    # Crear buscador
    try:
        finder = BusinessFinder("config.json")
    except SystemExit:
        return

    # Buscar lugares
    print(f"🏢 Tipo: {finder.config['search_type']}")
    print(f"📊 Resultados máximos: {finder.config.get('max_results', 100)}")
    print()

    places = finder.search_places()

    # Exportar resultados
    finder.export_to_csv()

    # Estadísticas finales
    print("\n" + "=" * 60)
    print("📈 Resumen de la ejecución")
    print("=" * 60)
    print(f"Tiempo total: {time.perf_counter():.2f} segundos")
    print(f"Negocios encontrados: {finder.total_found}")
    print(f"Sin web: {finder.without_website_count}")
    print(f"Con web: {finder.total_found - finder.without_website_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
