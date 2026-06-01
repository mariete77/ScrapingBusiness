# 🦊 Buscador de Negocios Sin Web en Madrid

Script de Python para encontrar negocios pequeños en Madrid que NO tienen página web — tus clientes potenciales.

## 📋 Requisitos

- Python 3.7 o superior
- API key de Google Places (gratis, $200 de crédito mensual)

## 🚀 Instalación

1. Instala Python si no lo tienes:
   - Windows: https://python.org/downloads/
   - Mac: `brew install python3`
   - Linux: `sudo apt install python3`

2. Instala la librería `requests`:
   ```bash
   pip install requests
   ```

## 🔑 Obtener API Key de Google Places

1. Ve a: https://console.cloud.google.com/apis/library/places-backend.googleapis.com

2. Crea un proyecto nuevo o selecciona uno existente

3. Habilita la API "Places API"

4. Ve a: https://console.cloud.google.com/apis/credentials

5. Click en "Create Credentials" → "API key"

6. Copia la API key (empieza con `AIza...`)

7. **IMPORTANTE:** Restringe la API key:
   - Click en la API key que acabas de crear
   - En "Application restrictions", elige "IP addresses" (si vas a ejecutar localmente)
   - O "None" para pruebas rápidas

8. Configura la cuota de la API:
   - Ve a: https://console.cloud.google.com/apis/api/places-backend.googleapis.com/quotas
   - La cuota gratis es de $200/mes (~200,000 requests)

## ⚙️ Configurar el Script

1. Abre el archivo `scraping-script.py`

2. Busca la línea 23:
   ```python
   API_KEY = "TU_API_KEY_AQUI"
   ```

3. Reemplaza "TU_API_KEY_AQUI" con tu API key de Google Places:
   ```python
   API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
   ```

4. (Opcional) Ajusta los parámetros de búsqueda:
   ```python
   LOCATION = "40.416775,-3.703790"  # Madrid (latitud, longitud)
   RADIUS = 10000  # Radio en metros (10km = zona centro)
   SEARCH_TYPE = "accounting"  # Tipo de negocio
   ```

## 🏪 Tipos de Negocios Disponibles

Cambia `SEARCH_TYPE` para buscar diferentes tipos de negocios:

| Tipo | Descripción |
|------|-------------|
| `accounting` | Gestorías, asesorías fiscales |
| `restaurant` | Restaurantes, bares |
| `store` | Tiendas, comercios |
| `health` | Clínicas, dentistas, médicos |
| `lawyer` | Abogados, despachos |
| `real_estate_agent` | Inmobiliarias |
| `beauty_salon` | Peluquerías, salones de belleza |
| `car_repair` | Talleres mecánicos |
| `pharmacy` | Farmacias |
| `gym` | Gimnasios |
| `school` | Academias, escuelas |

## 🎯 Ejecutar el Script

### Windows
1. Abre PowerShell o CMD
2. Ve al directorio donde guardaste el script
3. Ejecuta:
   ```bash
   python scraping-script.py
   ```

### Mac/Linux
1. Abre Terminal
2. Ve al directorio donde guardaste el script
3. Ejecuta:
   ```bash
   python3 scraping-script.py
   ```

## 📊 Resultados

El script creará un archivo CSV con los negocios que NO tienen web:

**Archivo generado:** `negocios_sin_web_madrid_YYYYMMDD_HHMMSS.csv`

**Columnas:**
- `nombre`: Nombre del negocio
- `direccion`: Dirección completa
- `telefono`: Número de teléfono
- `tiene_web`: "SI" o "NO"
- `website`: URL (si tiene)
- `rating`: Calificación (0-5)
- `reseñas`: Número de reseñas
- `tipos`: Categorías del negocio

## 📈 Estadísticas de Salida

Al final de la ejecución, el script mostrará:

```
📊 Estadísticas:
   - Total buscados: 50
   - Sin web: 15
   - Con web: 35
```

## 📱 Envío de WhatsApp a Negocios

Una vez tienes el CSV con negocios sin web, puedes enviarles mensajes de oferta directamente por WhatsApp.

### Modos de funcionamiento

| Modo | Descripción | Ideal para |
|------|-------------|------------|
| `wame` | Abre enlaces wa.me en el navegador con mensaje prellenado | Pruebas iniciales, pocos mensajes |
| `api` | WhatsApp Cloud API de Meta (envío automatizado) | Envío masivo, escala |

### Configuración rápida

1. Copia el config de ejemplo:
   ```bash
   copy whatsapp_config.example.json whatsapp_config.json
   ```

2. Edita `whatsapp_config.json` y personaliza el mensaje:
   ```json
   {
     "modo": "wame",
      "mensaje_template": "Hola {nombre}, soy Mario de Ayanip.es. Vi que su negocio no tiene pagina web...",
     "prefijo_pais": "34",
     "delay_entre_mensajes": 8,
     "max_mensajes_por_ejecucion": 10
   }
   ```

3. Variables disponibles en el template:
   - `{nombre}` — Nombre del negocio
   - `{direccion}` — Dirección
   - `{telefono}` — Teléfono

### Ejecutar

```bash
python whatsapp_sender.py
```

El script automáticamente:
- Busca el CSV más reciente
- Filtra negocios con teléfono válido
- **No reenvía** a contactos ya contactados (registro en `envios_whatsapp.log`)
- Pide confirmación antes de enviar
- Muestra resumen de enviados/fallidos/omitidos

### Modo wa.me (recomendado para empezar)

1. Abre [WhatsApp Web](https://web.whatsapp.com) en tu navegador y haz login
2. Ejecuta `python whatsapp_sender.py`
3. Por cada contacto se abrirá una pestaña con el mensaje prellenado
4. Pulsa "Enviar" manualmente en cada una
5. El script espera 8 segundos entre cada apertura (configurable)

### Modo API (para escalar)

Requiere un número de WhatsApp Business registrado en Meta:

1. Ve a [Meta Developer](https://developers.facebook.com/apps/) y crea una app
2. Añade el producto "WhatsApp" y obtén el `access_token` y `phone_number_id`
3. En `whatsapp_config.json`, cambia el modo a `"api"` y rellena las credenciales:
   ```json
   {
     "modo": "api",
     "whatsapp_api": {
       "access_token": "EAAXxxxx...",
       "phone_number_id": "1234567890",
       "api_version": "v21.0"
     }
   }
   ```
4. Ejecuta el script — el envío es completamente automático

> ⚠️ **Nota:** Para enviar a números que no te tienen en agenda, WhatsApp requiere que el destinatario haya interactuado contigo antes (respondiendo a un mensaje tuyo). El modo wa.me evita esta restricción porque tú pulsas "Enviar" manualmente.

## 🔄 Próximos Pasos

1. **Ejecuta el scraping** → obtén el CSV de negocios sin web
2. **Ejecuta el sender de WhatsApp** → contacta a los negocios
3. **Revisa respuestas** en WhatsApp y cierra ventas → Ingreso extra 🎉

## ⚠️ Limitaciones

- **Cuota de API:** $200/mes gratis (~200,000 requests)
- **Precisión:** Google Places puede no tener todos los negocios
- **Frecuencia:** No hagas más de 10-15 requests/segundo para evitar bloqueos
- **Geolocalización:** Usa las coordenadas exactas de Madrid para mejores resultados

## 🛠️ Solución de Problemas

### Error: "API key invalid"
- Verifica que copiaste correctamente la API key
- Asegúrate de que habilitaste la "Places API" en Google Console

### Error: "OVER_QUERY_LIMIT"
- Has excedido tu cuota de API
- Espera hasta que se renueve tu cuota (mensual)
- O aumenta tu cuota con un plan de pago

### No se encuentran resultados
- Verifica las coordenadas de ubicación
- Aumenta el radio de búsqueda (RADIUS)
- Cambia el tipo de negocio (SEARCH_TYPE)

## 📚 Recursos Útiles

- [Google Places API Documentation](https://developers.google.com/maps/documentation/places/web-service/overview)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Coordinates de Madrid](https://www.latlong.net/place/madrid-spain-255378.html)

## 🦊 Soporte

Si tienes problemas:
1. Revisa el README
2. Verifica tu API key
3. Revisa la cuota de uso en Google Console
4. Contacta a Koda (tu asistente)

---

_Última actualización: 2026-03-30_
