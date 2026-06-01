#!/usr/bin/env python3
"""
Script para enviar mensajes de WhatsApp a negocios sin web.

Modos:
  - web:     Automatiza WhatsApp Web directamente con pywhatkit.
             Abre wa.me, escribe el mensaje y pulsa Enter.
             NO necesita WhatsApp Business ni API de Meta.
             Solo necesita WhatsApp Web abierto en el navegador.
  
  - web_directo:  Abre WhatsApp Web directamente con el mensaje prellenado.
                  Solo necesitas pulsar Enter para enviar.
                  Más rápido que el modo 'web' y más directo que 'wame'.
  
  - wame:    Abre enlaces wa.me con mensaje prellenado (tú envías manualmente).
  
  - api:     WhatsApp Cloud API de Meta (envío 100% automatizado, sí necesita Business).

Autor: Koda (AI Assistant)
Fecha: 2026-04-04
"""

import sys
import csv
import json
import os
import re
import time
import random
import glob
import webbrowser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from urllib.parse import quote

# Forzar UTF-8 en la consola de Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


class WhatsAppSender:
    """Envía mensajes de WhatsApp a negocios desde un CSV."""

    def __init__(self, config_file: str = "whatsapp_config.json"):
        self.config = self._load_config(config_file)
        self.enviados = []
        self.fallidos = []
        self.omitidos = []
        self._csv_path = None
        self._csv_fieldnames = None

    def _load_config(self, config_file: str) -> Dict:
        if not os.path.exists(config_file):
            print(f"❌ ERROR: Archivo '{config_file}' no encontrado.")
            print(f"\n📝 Pasos:")
            print(f"1. Copia 'whatsapp_config.example.json' a 'whatsapp_config.json'")
            print(f"2. Edita el mensaje template y ajusta los parámetros")
            print(f"3. Vuelve a ejecutar el script")
            exit(1)

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            config = {k: v for k, v in config.items() if not k.startswith('_')}

        if 'mensaje_template' not in config and 'mensajes_templates' not in config:
            print("❌ ERROR: Falta 'mensaje_template' o 'mensajes_templates' en la configuración")
            exit(1)

        # Normalizar: siempre trabajar con lista de templates
        if 'mensajes_templates' in config:
            config['_templates'] = config['mensajes_templates']
        else:
            config['_templates'] = [config['mensaje_template']]

        modo = config.get('modo', 'web')
        if modo not in ('web', 'web_directo', 'wame', 'api'):
            print(f"❌ ERROR: Modo '{modo}' no reconocido. Usa 'web', 'web_directo', 'wame' o 'api'")
            exit(1)

        if modo == 'api':
            api_config = config.get('whatsapp_api', {})
            if not api_config.get('access_token') or not api_config.get('phone_number_id'):
                print("❌ ERROR: Para modo 'api' necesitas configurar:")
                print("   - whatsapp_api.access_token")
                print("   - whatsapp_api.phone_number_id")
                print("\n💡 Obtén las credenciales en: https://developers.facebook.com/apps/")
                exit(1)

        return config

    def _find_latest_csv(self) -> Optional[str]:
        pattern = os.path.join(".", "negocios_sin_web_*.csv")
        csv_files = glob.glob(pattern)
        if not csv_files:
            return None
        csv_files.sort(key=os.path.getmtime, reverse=True)
        return csv_files[0]

    def _load_csv(self, filepath: str) -> List[Dict]:
        self._csv_path = filepath
        businesses = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self._csv_fieldnames = list(reader.fieldnames)
            if 'estado_envio' not in self._csv_fieldnames:
                self._csv_fieldnames.append('estado_envio')
            for row in reader:
                row.setdefault('estado_envio', '')
                businesses.append(row)
        # Sincronizar envíos previos del log que no estén marcados
        self._sincronizar_log_csv(businesses)
        return businesses

    def _sincronizar_log_csv(self, businesses: List[Dict]):
        """Marca en el CSV los envíos que ya están en el log pero sin marcar."""
        log_file = self.config.get('log_envios', 'envios_whatsapp.log')
        if not os.path.exists(log_file):
            return
        # Leer log: phone -> status
        log_entries = {}
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 3:
                    phone = parts[1].strip()
                    status = parts[2].strip()
                    if phone not in log_entries or status == 'OK':
                        log_entries[phone] = status
        # Marcar en businesses
        changed = False
        for b in businesses:
            raw_phone = b.get('telefono', '').strip()
            clean = re.sub(r'[\s\-\.\(\)\+]', '', raw_phone)
            prefix = self.config.get('prefijo_pais', '34')
            if not clean.startswith(prefix):
                clean = prefix + clean
            if clean in log_entries and b.get('estado_envio', '') == '':
                b['estado_envio'] = log_entries[clean]
                changed = True
        if changed:
            self._guardar_csv(businesses)
            print(f"📋 Sincronizados {sum(1 for b in businesses if b.get('estado_envio'))} envíos previos en el CSV")

    def _guardar_csv(self, businesses: List[Dict]):
        """Sobreescribe el CSV con el estado actualizado."""
        if not self._csv_path or not self._csv_fieldnames:
            return
        with open(self._csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self._csv_fieldnames)
            writer.writeheader()
            for b in businesses:
                row = {k: b.get(k, '') for k in self._csv_fieldnames}
                writer.writerow(row)

    def _marcar_envio_csv(self, phone: str, status: str):
        """Marca una fila del CSV con el estado de envío (lectura/escritura directa)."""
        if not self._csv_path or not self._csv_fieldnames:
            return
        prefix = self.config.get('prefijo_pais', '34')
        rows = []
        with open(self._csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_phone = row.get('telefono', '').strip()
                clean = re.sub(r'[\s\-\.\(\)\+]', '', raw_phone)
                if not clean.startswith(prefix):
                    clean = prefix + clean
                if clean == phone:
                    row['estado_envio'] = status
                rows.append(row)
        with open(self._csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=self._csv_fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

    def _clean_phone(self, phone: str) -> Optional[str]:
        if not phone or not phone.strip():
            return None
        cleaned = re.sub(r'[\s\-\.\(\)]', '', phone.strip())
        if cleaned.startswith('+'):
            cleaned = cleaned[1:]
        prefix = self.config.get('prefijo_pais', '34')
        if not cleaned.startswith(prefix):
            cleaned = prefix + cleaned
        if not cleaned.isdigit():
            return None
        if len(cleaned) < 10 or len(cleaned) > 15:
            return None
        # Filtro de móviles (España: después del 34, empieza por 6 o 7)
        if self.config.get('solo_moviles', False):
            numero_sin_prefijo = cleaned[len(prefix):]
            if not numero_sin_prefijo or numero_sin_prefijo[0] not in ('6', '7'):
                return None
        return cleaned

    def _extraer_zona(self, direccion: str) -> str:
        """Extrae la zona/barrio de una dirección completa.
        Ej: 'Calle Gran Vía 45, 28013 Madrid' → 'Madrid'
            'Calle Alcalá 20, 28001 Madrid, Spain' → 'Madrid'
        """
        if not direccion:
            return 'la zona'
        
        # Split por comas y tomar las partes relevantes
        partes = [p.strip() for p in direccion.split(',')]
        
        # Buscar código postal + ciudad (formato típico: "28013 Madrid")
        for parte in partes:
            match = re.match(r'\d{5}\s+(.+)', parte)
            if match:
                ciudad = match.group(1).strip()
                # Quitar "Spain" o "España" si aparece
                ciudad = re.sub(r'\s*(Spain|España)\s*$', '', ciudad, flags=re.IGNORECASE).strip()
                if ciudad:
                    return ciudad
        
        # Si no encuentra patrón de CP, buscar "Madrid" o ciudad conocida
        dir_lower = direccion.lower()
        ciudades_conocidas = [
            'Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Málaga', 
            'Bilbao', 'Zaragoza', 'Toledo', 'Getafe', 'Leganés',
            'Alcorcón', 'Fuenlabrada', 'Móstoles', 'Alcalá de Henares',
            'Torrejón de Ardoz', 'Parla', 'Alcobendas', 'San Sebastián de los Reyes',
            'Pozuelo de Alarcón', 'Boadilla del Monte', 'Las Rozas',
            'Majadahonda', 'Villanueva de la Cañada', 'Tres Cantos',
            'Colmenar Viejo', 'Rivas-Vaciamadrid', 'Arganda del Rey',
            'Coslada', 'San Fernando de Henares', 'Cobenza', 'Usera',
            'Carabanchel', 'Latina', 'Vallecas', 'Chamberí', 'Salamanca',
            'Retiro', 'Centro', 'Arganzuela', 'Tetuán', 'Moncloa',
            'Fuencarral', 'Hortaleza', 'Barajas', 'Villa de Vallecas',
            'Vicálvaro', 'San Blas', 'Ciudad Lineal', 'Moratalaz',
            'Puente de Vallecas', 'Carabanchel', 'Latina', 'Usera',
            'Villaverde', 'Villa de Vallecas', 'Chamartín', 'Sol'
        ]
        for ciudad in ciudades_conocidas:
            if ciudad.lower() in dir_lower:
                return ciudad
        
        # Último recurso: segunda parte de la dirección
        if len(partes) >= 2:
            return partes[-2] if len(partes) > 2 else partes[-1]
        
        return 'la zona'

    # Filtros por tipo de negocio
    _FILTROS_TIPO = {
        'peluqueria': {
            'tipos_google': ['hair_salon', 'hair_care', 'barber_shop', 'beauty_salon', 'beautician'],
            'keywords_nombre': [
                'peluquer', 'barber', 'barberia', 'barbería', 'estilista', 'hair',
                'peluquero', 'caballero', 'estética', 'estetica', 'belleza',
                'salón de belleza', 'salon de belleza', 'beauty', 'imagen',
            ],
            'excluir_keywords': ['canina', 'canino', 'perro', 'mascota', 'veterinaria'],
        },
    }

    def _es_tipo_negocio(self, negocio: Dict, tipo: str) -> bool:
        """Comprueba si un negocio pertenece a un tipo determinado usando tipos Google + nombre."""
        filtro = self._FILTROS_TIPO.get(tipo)
        if not filtro:
            return True  # Tipo desconocido → no filtrar

        nombre = negocio.get('nombre', '').lower()
        tipos_raw = negocio.get('tipos', '').lower()

        # Exclusiones primero
        for kw in filtro.get('excluir_keywords', []):
            if kw in nombre:
                return False

        # Comprobar por tipos de Google
        tipos_google = filtro.get('tipos_google', [])
        if tipos_google:
            for tg in tipos_google:
                if tg in tipos_raw:
                    return True

        # Comprobar por nombre
        for kw in filtro.get('keywords_nombre', []):
            if kw in nombre:
                return True

        return False

    def _extraer_tipo_negocio(self, negocio: Dict) -> str:
        """Devuelve 'peluquería', 'barbería', 'estética', etc. según el nombre."""
        nombre = negocio.get('nombre', '').lower()
        tipos = {
            'barbería': ['barber', 'barberia', 'barbería'],
            'peluquería': ['peluquer', 'peluquero', 'peluquera'],
            'estética': ['estética', 'estetica', 'belleza', 'beauty'],
        }
        for tipo, keywords in tipos.items():
            for kw in keywords:
                if kw in nombre:
                    return tipo
        return 'un negocio'

    def _personalizar_mensaje(self, template: str, negocio: Dict) -> str:
        msg = template
        msg = msg.replace('{nombre}', negocio.get('nombre', 'Su negocio'))
        msg = msg.replace('{direccion}', negocio.get('direccion', ''))
        msg = msg.replace('{telefono}', negocio.get('telefono', ''))
        msg = msg.replace('{rating}', negocio.get('rating', ''))
        msg = msg.replace('{zona}', self._extraer_zona(negocio.get('direccion', '')))
        msg = msg.replace('{tipo_negocio}', self._extraer_tipo_negocio(negocio))
        return msg

    def _cargar_log_envios(self) -> set:
        log_file = self.config.get('log_envios', 'envios_whatsapp.log')
        enviados = set()
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('['):
                        parts = line.split('|')
                        if len(parts) >= 2:
                            enviados.add(parts[1].strip())
        return enviados

    def _guardar_log(self, phone: str, nombre: str, status: str, error: str = ""):
        log_file = self.config.get('log_envios', 'envios_whatsapp.log')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"{timestamp} | {phone} | {status} | {nombre}"
        if error:
            entry += f" | {error}"
        entry += "\n"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(entry)

    def _enviar_web(self, phone: str, message: str, nombre: str) -> bool:
        """Automatiza WhatsApp Web con pywhatkit — envía sin intervención."""
        try:
            import pywhatkit
            import pyautogui
        except ImportError:
            print("   ❌ Error: pywhatkit/pyautogui no está instalado.")
            print("   💡 Ejecuta: python -m pip install pywhatkit pyautogui")
            return False

        wait_time = self.config.get('wait_time_web', 15)
        print(f"   🤖 Enviando vía WhatsApp Web (espera {wait_time}s para cargar)...")
        try:
            pywhatkit.sendwhatmsg_instantly(
                phone_no=f"+{phone}",
                message=message,
                wait_time=wait_time,
                tab_close=False
            )
            # Fallback: si pywhatkit no pulsó Enter, pyautogui lo hace
            print(f"   ⏳ Pulsando Enter...")
            time.sleep(2)
            pyautogui.press('enter')
            print(f"   ✅ Mensaje enviado")
            return True
        except Exception as e:
            err_str = str(e)
            if "page not found" in err_str.lower() or "could not" in err_str.lower():
                print(f"   ❌ No se pudo abrir WhatsApp Web. ¿Está abierto en el navegador?")
            else:
                print(f"   ❌ Error: {e}")
            return False

    def _enviar_web_directo(self, phone: str, message: str, nombre: str) -> bool:
        """Abre WhatsApp Web directamente con el mensaje prellenado."""
        url = f"https://web.whatsapp.com/send?phone={phone}&text={quote(message)}"
        print(f"   🌐 Abriendo WhatsApp Web con mensaje prellenado...")
        print(f"   ⏳ Solo necesitas pulsar Enter para enviar")
        try:
            webbrowser.open(url)
            # Esperar un poco para que se abra el navegador
            time.sleep(2)
            # Esperar confirmación manual del usuario
            input("   ⏸️  Presiona Enter cuando hayas enviado el mensaje...")
            return True
        except Exception as e:
            print(f"   ❌ Error abriendo navegador: {e}")
            return False

    def _enviar_wame(self, phone: str, message: str, nombre: str) -> bool:
        url = f"https://wa.me/{phone}?text={quote(message)}"
        print(f"   📲 Abriendo: wa.me/{phone}")
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"   ❌ Error abriendo navegador: {e}")
            return False

    def _enviar_api(self, phone: str, message: str, nombre: str) -> bool:
        api_config = self.config['whatsapp_api']
        api_version = api_config.get('api_version', 'v21.0')
        phone_number_id = api_config['phone_number_id']
        access_token = api_config['access_token']
        url = f"https://graph.facebook.com/{api_version}/{phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"preview_url": False, "body": message}
        }
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            data = response.json()
            if response.status_code == 200:
                msg_id = data.get('messages', [{}])[0].get('id', 'unknown')
                print(f"   ✅ Enviado (ID: {msg_id[:20]}...)")
                return True
            else:
                error_info = data.get('error', {})
                error_code = error_info.get('code', 'N/A')
                error_msg = error_info.get('message', 'Sin detalle')
                print(f"   ❌ Error API ({error_code}): {error_msg}")
                return False
        except requests.exceptions.Timeout:
            print(f"   ❌ Timeout de conexión")
            return False
        except Exception as e:
            print(f"   ❌ Error de conexión: {e}")
            return False

    def _contar_envios_hoy(self) -> int:
        """Cuenta cuántos mensajes se enviaron hoy desde el log."""
        log_file = self.config.get('log_envios', 'envios_whatsapp.log')
        hoy = datetime.now().strftime("%Y-%m-%d")
        count = 0
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith(hoy) and '| OK |' in line:
                        count += 1
        return count

    def enviar(self):
        modo = self.config['modo']
        max_envios = self.config.get('max_mensajes_por_ejecucion', 10)
        max_diario = self.config.get('max_mensajes_por_dia', 10)
        templates = self.config['_templates']

        # Delays aleatorios anti-bloqueo
        delay_min = self.config.get('delay_min', 60)
        delay_max = self.config.get('delay_max', 120)
        pausa_cada = self.config.get('pausa_cada', 5)
        pausa_minutos = self.config.get('pausa_minutos', 10)

        # Comprobar límite diario
        enviados_hoy = self._contar_envios_hoy()
        if enviados_hoy >= max_diario:
            print(f"⛔ LÍMITE DIARIO ALCANZADO: Ya enviaste {enviados_hoy}/{max_diario} hoy.")
            print(f"   Para no recibir bloqueo de spam, espera hasta mañana.")
            return
        if enviados_hoy > 0:
            disponibles = max_diario - enviados_hoy
            print(f"📊 Ya enviados hoy: {enviados_hoy}/{max_diario}. Quedan: {disponibles}")
            max_envios = min(max_envios, disponibles)

        csv_path = self.config.get('archivo_csv', '')
        if not csv_path:
            csv_path = self._find_latest_csv()
            if not csv_path:
                print("❌ ERROR: No se encontró ningún CSV de negocios sin web.")
                exit(1)
            print(f"📂 Usando CSV más reciente: {csv_path}")
        elif not os.path.exists(csv_path):
            print(f"❌ ERROR: El archivo CSV '{csv_path}' no existe.")
            exit(1)

        businesses = self._load_csv(csv_path)
        if not businesses:
            print("❌ ERROR: El CSV no contiene registros.")
            exit(1)

        ya_enviados = self._cargar_log_envios()
        filtrar_tipos = self.config.get('filtrar_tipos', [])
        excluir_tipos = self.config.get('excluir_tipos', [])

        candidatos = []
        for b in businesses:
            tipos_raw = b.get('tipos', '').lower()
            
            # Filtro de exclusión: omitir si está en la lista de tipos no deseados
            if excluir_tipos:
                tiene_tipo_excluido = False
                for tipo in excluir_tipos:
                    if tipo in tipos_raw:
                        self.omitidos.append((b.get('nombre', '?'), f'Tipo excluido: {tipo}'))
                        tiene_tipo_excluido = True
                        break
                if tiene_tipo_excluido:
                    continue
            
            # Filtro de inclusión: solo si está en la lista de tipos deseados
            if filtrar_tipos:
                tiene_tipo_deseado = False
                for tipo in filtrar_tipos:
                    if tipo in tipos_raw:
                        tiene_tipo_deseado = True
                        break
                if not tiene_tipo_deseado:
                    self.omitidos.append((b.get('nombre', '?'), f'No es {"/".join(filtrar_tipos)}'))
                    continue
            raw_phone = b.get('telefono', '').strip()
            phone = self._clean_phone(raw_phone)
            if not phone:
                if raw_phone and self.config.get('solo_moviles', False):
                    self.omitidos.append((b.get('nombre', '?'), 'Teléfono fijo (no WhatsApp)'))
                elif raw_phone:
                    self.omitidos.append((b.get('nombre', '?'), 'Teléfono no válido'))
                else:
                    self.omitidos.append((b.get('nombre', '?'), 'Sin teléfono'))
                continue
            if phone in ya_enviados:
                self.omitidos.append((b.get('nombre', '?'), 'Ya enviado anteriormente'))
                continue
            candidatos.append({**b, '_phone_clean': phone})

        if not candidatos:
            print("\n⚠️ No hay negocios nuevos a los que enviar mensajes.")
            print(f"   Omitidos: {len(self.omitidos)}")
            return

        a_enviar = candidatos[:max_envios]

        # Info del modo
        modo_info = {
            'web': '🤖 WEB AUTOMÁTICO — pywhatkit escribe y envía por ti en WhatsApp Web',
            'web_directo': '🌐 WEB DIRECTO — Abre WhatsApp Web con mensaje, tú pulsas Enter',
            'wame': '📲 WA.ME — Abre el enlace, tú pulsas "Enviar" manualmente',
            'api': '☁️ CLOUD API — Envío 100% automático vía Meta (requiere WhatsApp Business)'
        }

        print(f"\n{'=' * 60}")
        print(f"📱 WhatsApp Sender - Modo: {modo.upper()}")
        print(f"{'=' * 60}")
        if filtrar_tipos:
            print(f"🍽️  Filtro: solo {', '.join(filtrar_tipos)}")
        if excluir_tipos:
            print(f"🚫 Excluyendo: {', '.join(excluir_tipos)}")
        print(f"📂 CSV: {csv_path}")
        print(f"📊 Total en CSV: {len(businesses)}")
        print(f"📞 Con teléfono válido: {len(candidatos)}")
        print(f"⏭️  Omitidos: {len(self.omitidos)}")
        print(f"📤 A enviar ahora: {len(a_enviar)}")
        print(f"⏱️  Delay aleatorio: {delay_min}-{delay_max}s entre mensajes")
        if pausa_cada and len(a_enviar) > pausa_cada:
            print(f"☕ Pausa larga de {pausa_minutos}min cada {pausa_cada} envíos")
        print(f"📝 {len(templates)} variantes de mensaje (rotación aleatoria)")
        print(f"\n{modo_info[modo]}")

        if modo == 'web':
            wait = self.config.get('wait_time_web', 15)
            print(f"   ⚠️  Tiempo de espera por mensaje: {wait}s (para que cargue WhatsApp Web)")
            print(f"   ⚠️  NO muevas el ratón ni cambies de pestaña mientras se envía")
            print(f"   ⚠️  Asegúrate de tener WhatsApp Web abierto y con sesión activa")
        elif modo == 'web_directo':
            print(f"   ✅ Abre WhatsApp Web directamente con el mensaje prellenado")
            print(f"   ⚠️  Solo necesitas pulsar Enter para enviar cada mensaje")
            print(f"   ⚠️  Asegúrate de tener sesión iniciada en WhatsApp Web")
        elif modo == 'wame':
            print(f"   Asegúrate de tener WhatsApp Web abierto en tu navegador.")

        print(f"\n{'─' * 60}")
        print(f"📝 Ejemplo de mensaje (variante aleatoria):")
        ejemplo_template = random.choice(templates)
        ejemplo_msg = self._personalizar_mensaje(ejemplo_template, a_enviar[0])
        print(f'   "{ejemplo_msg[:120]}..."')
        print(f"\n{'─' * 60}")

        if '--yes' not in sys.argv and '-y' not in sys.argv:
            confirmar = input(f"¿Enviar {len(a_enviar)} mensajes? [s/N]: ").strip().lower()
        else:
            confirmar = 's'
            print(f"✅ Auto-confirmado (--yes)")
        if confirmar not in ('s', 'si', 'sí', 'y', 'yes'):
            print("⛔ Cancelado por el usuario.")
            return

        if modo == 'web':
            print(f"\n⏳ Empieza el envío automático. NO toques el teclado/ratón...")
            time.sleep(3)

        enviar_fn = {
            'web': self._enviar_web,
            'web_directo': self._enviar_web_directo,
            'wame': self._enviar_wame,
            'api': self._enviar_api
        }[modo]

        for i, negocio in enumerate(a_enviar, 1):
            phone = negocio['_phone_clean']
            nombre = negocio.get('nombre', 'Desconocido')
            # Rotación aleatoria de templates anti-bloqueo
            template_elegido = random.choice(templates)
            mensaje = self._personalizar_mensaje(template_elegido, negocio)

            print(f"\n[{i}/{len(a_enviar)}] 📞 {phone} - {nombre[:40]}")

            try:
                exito = enviar_fn(phone, mensaje, nombre)
                if exito:
                    self.enviados.append((phone, nombre))
                    self._guardar_log(phone, nombre, 'OK')
                    self._marcar_envio_csv(phone, 'OK')
                else:
                    self.fallidos.append((phone, nombre, 'Error en envío'))
                    self._guardar_log(phone, nombre, 'FAIL', 'Error en envío')
                    self._marcar_envio_csv(phone, 'FAIL')
            except Exception as e:
                self.fallidos.append((phone, nombre, str(e)))
                self._guardar_log(phone, nombre, 'FAIL', str(e))
                self._marcar_envio_csv(phone, 'FAIL')
                print(f"   ❌ Excepción: {e}")

            if i < len(a_enviar):
                # Pausa larga cada X envíos
                if pausa_cada and i % pausa_cada == 0:
                    print(f"\n☕ Pausa larga de {pausa_minutos} minutos (anti-bloqueo)...")
                    for m in range(pausa_minutos):
                        for s in range(60):
                            print(f"\r   ⏳ {pausa_minutos - m - 1}min {60 - s}s restantes...", end='', flush=True)
                            time.sleep(1)
                    print(f"\r   ✅ Pausa terminada{' ' * 20}")
                
                # Delay aleatorio entre mensajes
                delay = random.randint(delay_min, delay_max)
                print(f"   ⏳ Esperando {delay}s (delay aleatorio)...")
                remaining = delay
                for sec in range(delay):
                    print(f"\r   ⏳ {remaining}s...", end='', flush=True)
                    time.sleep(1)
                    remaining -= 1
                print(f"\r   ✅ Listo{' ' * 20}")

        self._print_resumen()

    def _print_resumen(self):
        print(f"\n{'=' * 60}")
        print(f"📊 Resumen de envíos")
        print(f"{'=' * 60}")
        print(f"✅ Enviados:   {len(self.enviados)}")
        print(f"❌ Fallidos:   {len(self.fallidos)}")
        print(f"⏭️  Omitidos:   {len(self.omitidos)}")
        print(f"{'─' * 60}")

        if self.fallidos:
            print(f"\n❌ Detalle de fallidos:")
            for phone, nombre, error in self.fallidos:
                print(f"   - {phone} | {nombre[:30]} | {error}")

        if self.omitidos:
            print(f"\n⏭️  Detalle de omitidos:")
            for nombre, razon in self.omitidos:
                print(f"   - {nombre[:30]} | {razon}")

        if self.enviados:
            print(f"\n✅ Enviados correctamente:")
            for phone, nombre in self.enviados:
                print(f"   - {phone} | {nombre[:30]}")

        print(f"\n📋 Log guardado en: {self.config.get('log_envios', 'envios_whatsapp.log')}")
        print(f"{'=' * 60}")


def main():
    print("=" * 60)
    print("📱 Koda - WhatsApp Sender para Negocios Sin Web")
    print("=" * 60)
    print()

    start_time = time.perf_counter()

    # Determinar archivo de configuración
    config_file = "whatsapp_config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        if not os.path.exists(config_file):
            print(f"❌ ERROR: Archivo de configuración '{config_file}' no encontrado.")
            print(f"\n📝 Uso:")
            print(f"   python whatsapp_sender.py [archivo_config.json]")
            print(f"\n💡 Ejemplo:")
            print(f"   python whatsapp_sender.py whatsapp_config_bares_restaurantes.json")
            print(f"\n📋 Archivos de configuración disponibles:")
            for f in os.listdir('.'):
                if f.startswith('whatsapp_config') and f.endswith('.json') and 'example' not in f:
                    print(f"   - {f}")
            sys.exit(1)

    try:
        sender = WhatsAppSender(config_file)
        sender.enviar()
    except SystemExit:
        return

    elapsed = time.perf_counter() - start_time
    print(f"\n⏱️  Tiempo total: {elapsed:.1f} segundos")


if __name__ == "__main__":
    main()