# Runbook: Añadir una provincia nueva al pipeline de outreach

Guía genérica, replicable, para cualquier provincia. El ejemplo canónico es `cadiz/` (la última añadida). Si ya la has hecho una vez, esta doc la haces en 10 minutos.

## Resumen en 4 líneas

1. Crear `<provincia>/` con un config de scraping, un config de WhatsApp y un `.bat`.
2. Entrar en la carpeta, ejecutar el scraper, copiar el nombre del CSV al config de WhatsApp.
3. Ejecutar el `.bat`. Confirmar. Listo.

El sistema ya deduplica por nombre entre llamadas a la API y por teléfono entre ejecuciones (log + columna `estado_envio` en el CSV), así que puedes re-lanzar el scraper o el sender sin miedo a duplicar.

---

## Requisitos previos

- Python con `requests` (base) y, si vas a usar `modo: "web"`, también `pywhatkit` + `pyautogui`. Ver `scripts/requirements.txt`.
- API key de Google Places (New). Si ya tienes una funcionando, reutilízala — Google cobra por request y una sola key vale para todas las provincias.
- WhatsApp Web ya logueado en el navegador (solo para `modo: "web"` / `"web_directo"`).

---

## Estructura de una carpeta de provincia

Cada provincia vive en su propia carpeta en la raíz, autocontenida:

```
<provincia>/
  config_<provincia>_<sector>.json   # config del scraper (1+ por sector)
  whatsapp_config_<provincia>[_<sector>].json  # config del sender
  enviar_whatsapp_<provincia>.bat    # wrapper opcional con confirmación
  .gitignore                         # *.csv, *.log, PyWhatKit_DB.txt
  *.csv                              # outputs (gitignored)
  *.log                              # logs de envío (gitignored)
```

Convenciones de nombres (consistentes con `ciudad_real/`, `huelva/`, `madrid/`, `toledo/`, `pais_vasco/`):

- `config_<provincia>_<sector>.json` — p. ej. `config_cadiz_restaurantes.json`, `config_huelva_reformas.json`.
- `whatsapp_config_<provincia>.json` — si solo hay un sector. Si hay varios, sufijar: `whatsapp_config_huelva.json`, `whatsapp_config_huelva_reformas.json`.
- `output_prefix` en el config del scraper — `<sector>_<provincia>_provincia_sin_web` (singular o plural según el sector: `restaurantes_…`, `reformas_…`).

---

## Paso 1 — Definir cobertura geográfica

Decide qué municipios cubre la provincia. Como regla práctica:

- **Mínimo viable:** 5–8 puntos (capital + 4–7 grandes municipios).
- **Cobertura ampliada (recomendada):** 12–20 puntos. Es lo que usamos en `huelva/` y `cadiz/`.
- No te pases de ~25 puntos o el scraper tarda mucho y los resultados de municipios pequeños se solapan con los grandes.

Para cada municipio necesitas:

1. Coordenadas `lat,lng` — búscalas en Google Maps (clic derecho → "¿Qué hay aquí?").
2. Nombre humano — lo usará el log y `_archivo_csv_explicacion`.

Ordena `locations_extra` y `locations_extra_names` igual (son arrays `;`-separados, índice a índice). La `location` principal es la capital.

**Ejemplo real (Cádiz, 17 puntos):**

```json
"location": "36.5298,-6.2924",
"location_name": "Cádiz (capital)",
"locations_extra": "36.6850,-6.1261;36.1408,-5.3532;36.4669,-6.1949;…",
"locations_extra_names": "Jerez de la Frontera;Algeciras;San Fernando;…"
```

`radius: 40000` (40 km) funciona bien para municipios de tamaño medio. Para capitales densas puedes bajar a 20000–25000.

---

## Paso 2 — Crear `config_<provincia>_<sector>.json`

Copia uno existente y adapta. Partiendo de `cadiz/config_cadiz_restaurantes.json`:

```json
{
  "api_key": "<RELLENAR>",
  "location": "<lat>,<lng>",
  "location_name": "<Ciudad> (capital)",
  "locations_extra": "<lat>,<lng>;<lat>,<lng>;…",
  "locations_extra_names": "Municipio1;Municipio2;…",
  "radius": 40000,
  "search_type": "restaurant",
  "output_prefix": "restaurantes_<provincia>_provincia_sin_web",
  "max_results": 500,
  "language": "es"
}
```

Decisiones por sector:

| Sector | `search_type` | Notas |
|---|---|---|
| Restaurantes / bares | `restaurant` | El filtro fino lo hace el sender (`filtrar_tipos: ["restaurant","bar"]`). |
| Reformas / oficios | `reformas, electricista, fontanero, cerrajero, carpintero` | Sectores mezclados; en el sender, `filtrar_tipos: []` y `excluir_tipos` agresivo para quitar hostelería y peluquerías. |
| Peluquerías | `hair_salon` | — |
| Un sector solo | valor único sin comas | El script lo trata igual. |

Sobre la `api_key`: el `.gitignore` excluye `config.json` y `whatsapp_config.json` literales, **no** los `config_<provincia>_*.json` con prefijo. Revisa `git status` antes de commitear — si tu key tiene restricciones por IP, no la pongas en un JSON que vaya al repo. Opciones:

- Poner la key real y confiar en que solo tú clonas el repo.
- Poner un placeholder y exportarla con variable de entorno (requiere tocar el script — no soportado todavía).
- Reutilizar la key de `huelva/config_huelva_restaurantes.json` (que ya está committed). Es lo que hicimos con Cádiz.

---

## Paso 3 — Crear `whatsapp_config_<provincia>[_<sector>].json`

Copia el de Huelva/Cádiz y adapta. Los campos que **siempre** se cambian entre provincias:

| Campo | Qué poner | Por qué |
|---|---|---|
| `_comentario` | Provincia + sector | Solo orientativo. |
| `mensajes_templates` | 5–15 mensajes rotando, todos con `{nombre}` | Cuantos más, menos patrón detectable. |
| `prefijo_pais` | `34` (España) | Constante. |
| `solo_moviles` | `true` | Fijos no tienen WhatsApp, se descartan automáticamente. |
| `filtrar_tipos` | `["restaurant","bar"]` (sector hostelería) o `[]` (sector donde el scraper ya filtra) | Ver tabla arriba. |
| `excluir_tipos` | Sector específico | Hostelería: `hair_salon, barber_shop, beauty_salon, car_repair, electrician, plumber, locksmith`. Reformas: `restaurant, bar, cafe, food, hair_salon, barber_shop, beauty_salon, lodging, store`. |
| `delay_min` / `delay_max` | 60 / 120 segundos | Por debajo de 60s te bloquean en horas. |
| `pausa_cada` / `pausa_minutos` | 5 / 10 | Una pausa larga cada 5 mensajes reduce ratio de spam. |
| `max_mensajes_por_ejecucion` | 20 | Para ir poco a poco y reaccionar si algo va mal. |
| `max_mensajes_por_dia` | 40 | Tope absoluto diario. |
| `archivo_csv` | `""` al principio | Se rellena tras ejecutar el scraper. |
| `log_envios` | `envios_whatsapp_<provincia>[_<sector>].log` | Log separado, una línea por intento. |

**Variables disponibles en `mensajes_templates`:** `{nombre}`, `{direccion}`, `{telefono}`, `{rating}`, `{zona}` (parseada de la dirección), `{tipo_negocio}` (inferido del nombre).

Las claves que empiezan por `_` son comentarios y se ignoran al cargar — úsalas para documentar cada campo en línea.

---

## Paso 4 — Crear el `.bat` (opcional pero recomendado)

Plantilla, copia y adapta:

```bat
@echo off
echo =====================================================
echo   ENVIANDO WHATSAPP A <SECTOR> - PROVINCIA DE <PROVINCIA>
echo =====================================================
echo.
echo Configuracion: whatsapp_config_<provincia>[_<sector>].json
echo CSV: se usara el mas reciente (<output_prefix>_*.csv)
echo.
echo ========================================
echo   IMPORTANTE - LEER ANTES DE EJECUTAR
echo ========================================
echo.
echo 1. Este script enviara mensajes a <sector> sin web
echo 2. Maximo 20 mensajes por ejecucion
echo 3. Pausa de 10 minutos cada 5 mensajes
echo 4. Delay aleatorio de 60-120 segundos entre mensajes
echo 5. Solo se enviara a numeros moviles (6xx, 7xx)
echo.
echo ========================================
echo.
echo Presiona cualquier tecla para continuar...
pause > nul

echo.
echo Iniciando envio de mensajes...
echo.

C:\Users\mario\AppData\Local\Python\bin\python.exe ..\scripts\whatsapp_sender.py whatsapp_config_<provincia>[_<sector>].json

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
echo.
echo Revisa el log: envios_whatsapp_<provincia>[_<sector>].log
echo.
pause
```

Ajusta la ruta del ejecutable de Python a tu instalación si no es esa.

---

## Paso 5 — Ejecutar el scraper

**Importante:** el script resuelve `config.json` y el output CSV relativos al **directorio actual**. Hay que ejecutarlo desde dentro de la carpeta de la provincia.

```powershell
cd D:\Repos\ScrapingBusiness\<provincia>
python ..\scripts\scraping-script-v2.py config_<provincia>_<sector>.json
```

Salida esperada:

- Para cada municipio: lista de negocios con `Con web` / `Sin web` y su rating.
- Al final: un CSV `restaurantes_<provincia>_provincia_sin_web_AAAAMMDD_HHMMSS.csv` + estadísticas (`Total buscados`, `Sin web`, `Con web`).
- Tiempo total orientativo: 4 minutos por cada 1.000 negocios (17 municipios en Cádiz = 4 min).

Si la API key no funciona o se acaba la cuota, el script falla con un error HTTP claro — no hay fallback.

---

## Paso 6 — Apuntar el CSV en el config de WhatsApp y enviar

1. Abre `whatsapp_config_<provincia>.json` y rellena `archivo_csv` con el nombre exacto del CSV generado.
2. Ejecuta el `.bat` (o `python ..\scripts\whatsapp_sender.py whatsapp_config_<provincia>.json`).
3. El sender muestra resumen y pide confirmación. Pásale `--yes` o `-y` para saltarla (útil en `modo: "web_directo"` donde cada envío requiere que pulses Enter igualmente).

El sender:

- Carga el CSV.
- Filtra por `filtrar_tipos` / `excluir_tipos` / `solo_moviles`.
- Sincroniza el log contra el CSV (cualquier teléfono ya enviado se salta).
- Envía uno por uno con delay + pausas + caps.
- Acepta `Ctrl+C` para parar de forma limpia (cierra sesión, no rompe contadores).

---

## Métricas típicas que verás

Por provincia (basado en Huelva, Cádiz, Ciudad Real):

- **~1.000–1.100 negocios** totales revisados en cobertura ampliada (12–17 municipios).
- **~35–45 % sin web** (varía: Cádiz 39,6 %, Huelva similar).
- **~70–80 % de los sin web** con teléfono.
- **~25–35 % de los teléfonos** son móviles (el resto son fijos, no sirven para WhatsApp).
- Resultado práctico: **60–120 leads enviables** por provincia.
- Con cap de 40/día, una provincia se trabaja en **2–3 tandas** separadas al menos un día.

---

## Cosas que NO hay que tocar

- `scripts/scraping-script-v2.py` y `scripts/whatsapp_sender.py`. No son tuyos para una provincia; los modifica solo el dueño del repo.
- El `.gitignore` raíz — ya excluye `*.csv` y `envios_whatsapp.log`. La regla local de la carpeta es complementaria.
- La lógica de dedup (log + `estado_envio` en CSV). Si la tocas, rompes idempotencia entre ejecuciones.

---

## Añadir un segundo sector a una provincia existente

Ejemplo: ya tienes `cadiz/` con restaurantes, quieres añadir reformas.

1. Crea `cadiz/config_cadiz_reformas.json` con `search_type` y `output_prefix` distintos.
2. Crea `cadiz/whatsapp_config_cadiz_reformas.json` con sus propios `mensajes_templates`, `filtrar_tipos` / `excluir_tipos`, `archivo_csv` y `log_envios`.
3. (Opcional) Crea `cadiz/enviar_whatsapp_cadiz_reformas.bat`.
4. Ejecuta el scraper y luego el sender con el config del sector nuevo. Los logs y CSVs viven separados, no se mezclan.

El patrón es el mismo de Huelva: dos `config_*` + dos `whatsapp_config_*` + dos `*.bat` en la misma carpeta.

---

## Troubleshooting

| Síntoma | Causa probable | Solución |
|---|---|---|
| `ERROR: Archivo de configuración '…' no encontrado` | Estás ejecutando desde `scripts/` o desde la raíz | `cd` a la carpeta de la provincia. |
| Scraper termina con `❌ HTTP 400` / `403` | API key inválida o sin permisos para Places API (New) | Verifica en Google Cloud Console que Places API (New) está habilitada y la key sin restricciones, o restringida a tu IP. |
| Scraper devuelve 0 negocios en un municipio | `search_type` no existe en Google Places para esa zona | Prueba con `"restaurant"` o mira la lista oficial de tipos. |
| Sender salta todos los teléfonos | `solo_moviles: true` y los teléfonos del CSV son fijos | Revisa `prefijo_pais` y, para probar, pon `solo_moviles: false` y mira qué hay. |
| WhatsApp Web no se abre | Falta sesión en el navegador | Loguéate en `web.whatsapp.com` antes de la primera ejecución. |
| "Demasiados intentos" / bloqueo de WhatsApp | Demasiados mensajes en poco tiempo | Sube `delay_min`/`delay_max` y baja `max_mensajes_por_dia`. No mandar desde IP compartida con otros WhatsApps Web. |

---

## Lista de control — nueva provincia

- [ ] Carpeta `<provincia>/` creada en la raíz
- [ ] `config_<provincia>_<sector>.json` con `api_key`, municipios, `search_type`, `output_prefix`
- [ ] `whatsapp_config_<provincia>[_<sector>].json` con mensajes, filtros, caps, log
- [ ] `enviar_whatsapp_<provincia>[_<sector>].bat` con la ruta correcta de Python
- [ ] `.gitignore` local con `*.csv`, `*.log`, `PyWhatKit_DB.txt`
- [ ] Probado el scraper y revisado el CSV
- [ ] `archivo_csv` actualizado en el config del sender
- [ ] Primer batch enviado (20 mensajes, máximo)

---

_Inspirado en la primera ejecución real con Cádiz, 2026-06-10._
