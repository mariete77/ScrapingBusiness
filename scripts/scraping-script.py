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
from typing import List, Dict, Optional
from datetime import datetime

# Configuración
API_KEY = "TU_API_KEY_AQUI"  # Reemplaza esto con tu API key de Google Places

# Parámetros de búsqueda
LOCATION = "40.416775,-3.703790"  # Madrid (latitud, longitud)
RADIUS = 10000  # Radio en metros (10km = zona centro de Madrid)
SEARCH_TYPE = "accounting"  # Tipo de negocio: "accounting" = gestorías/asesorías
# Otros tipos posibles:
# - "restaurant" = restaurantes
# - "store" = tiendas
# - "health" = salud
# - "lawyer" = abogados
# - "real_estate_agent" = inmobiliarias
# - etc.

# Archivo de salida
OUTPUT_FILE = "negocios_sin_web_madrid.csv"

class BusinessFinder:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.businesses_without_website = []
        self.total_found = 0
        self.without_website_count = 0

    def search_places(self, location: str, radius: int, place_type: str) -> List[Dict]:
        """
        Busca lugares usando Google Places API (Text Search).
        """
        url = f"{self.base_url}/textsearch/json"

        # Query de búsqueda
        query = f"gestorias accounting asesoria {place_type} Madrid"

        params = {
            "query": query,
            "location": location,
            "radius": radius,
            "key": self.api_key,
            "language": "es"
        }

        try:
            print(f"🔍 Buscando: {query}")
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
                while next_page_token and len(self.businesses_without_website) < 100:
                    print("📄 Obteniendo más resultados...")
                    time.sleep(2)  # Google requiere esperar entre peticiones
                    more_places = self._get_next_page(next_page_token)
                    if more_places:
                        places.extend(more_places)
                        self._get_places_details(more_places)
                        next_page_token = data.get("next_page_token")
                    else:
                        break

                return places
            else:
                print(f"❌ Error en API: {data.get('status')}")
                print(f"Mensaje: {data.get('error_message', 'Sin detalles')}")
                return []

        except Exception as e:
            print(f"❌ Error en búsqueda: {e}")
            return []

    def _get_next_page(self, next_page_token: str) -> Optional[List[Dict]]:
        """
        Obtiene la siguiente página de resultados.
        """
        url = f"{self.base_url}/textsearch/json"

        params = {
            "pagetoken": next_page_token,
            "key": self.api_key
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
        """
        Obtiene detalles de cada negocio, incluyendo website.
        """
        url = f"{self.base_url}/details/json"

        for place in places:
            try:
                place_id = place.get("place_id")
                if not place_id:
                    continue

                self.total_found += 1

                params = {
                    "place_id": place_id,
                    "key": self.api_key,
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
                        "tiene_web": "SI" if result.get("website") else "NO"
                    }

                    # Solo guardar los que NO tienen web
                    if not result.get("website"):
                        self.businesses_without_website.append(business_info)
                        self.without_website_count += 1
                        print(f"📌 Sin web: {business_info['nombre']} - {business_info['direccion']}")
                    else:
                        print(f"✅ Con web: {business_info['nombre']}")

                    # Pequeña pausa para no exceder cuota
                    time.sleep(0.1)

                else:
                    print(f"⚠️ Error obteniendo detalles: {data.get('status')}")

            except Exception as e:
                print(f"❌ Error obteniendo detalles: {e}")
                continue

    def export_to_csv(self, filename: str):
        """
        Exporta los resultados a CSV.
        """
        if not self.businesses_without_website:
            print("⚠️ No hay negocios sin web para exportar")
            return

        # Definir columnas
        fieldnames = [
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
            with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.businesses_without_website)

            print(f"\n✅ Exportados {len(self.businesses_without_website)} negocios a {filename}")
            print(f"📊 Estadísticas:")
            print(f"   - Total buscados: {self.total_found}")
            print(f"   - Sin web: {self.without_website_count}")
            print(f"   - Con web: {self.total_found - self.without_website_count}")

        except Exception as e:
            print(f"❌ Error exportando CSV: {e}")


def main():
    """
    Función principal.
    """
    print("=" * 60)
    print("🦊 Koda - Buscador de Negocios Sin Web en Madrid")
    print("=" * 60)

    # Verificar API key
    if API_KEY == "TU_API_KEY_AQUI":
        print("\n❌ ERROR: Debes configurar tu API key de Google Places")
        print("\n📝 Pasos para obtener API key:")
        print("1. Ve a: https://console.cloud.google.com/apis/library/places-backend.googleapis.com")
        print("2. Crea un nuevo proyecto o selecciona uno existente")
        print("3. Habilita la API 'Places API'")
        print("4. Ve a: https://console.cloud.google.com/apis/credentials")
        print("5. Crea credenciales → API key")
        print("6. Copia la API key y pégala en este script (línea 23)")
        print("\n💰 La API key tiene $200 de crédito mensual GRATIS")
        print("\n🔄 Cuando tengas la API key, vuelve a ejecutar este script")
        return

    # Crear buscador
    finder = BusinessFinder(API_KEY)

    # Buscar lugares
    print(f"\n📍 Buscando negocios en Madrid (radio: {RADIUS}m)")
    print(f"🏢 Tipo: {SEARCH_TYPE}")
    print(f"📍 Ubicación: {LOCATION}")

    places = finder.search_places(LOCATION, RADIUS, SEARCH_TYPE)

    # Exportar resultados
    if finder.businesses_without_website:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"negocios_sin_web_madrid_{timestamp}.csv"
        finder.export_to_csv(output_filename)

        print(f"\n🎯 LISTO! Tienes {len(finder.businesses_without_website)} clientes potenciales")
        print(f"\n📋 Siguientes pasos:")
        print(f"1. Abre el CSV: {output_filename}")
        print(f"2. Revisa los negocios sin web")
        print(f"3. Haz outreach con las plantillas en plan-outreach.md")
    else:
        print("\n⚠️ No se encontraron negocios sin web en esta búsqueda")


if __name__ == "__main__":
    main()
