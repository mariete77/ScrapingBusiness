# 🔧 Reformas y oficios sin web — Provincia de Huelva

Campaña de outreach a **reformas, electricistas, fontaneros, cerrajeros y carpinteros** sin web en
la provincia de Huelva. Todo se ejecuta con doble clic en los `.bat` (no hace falta escribir
comandos).

## Archivos de esta campaña

Todos en la carpeta `huelva\`:

| Archivo | Para qué |
|---------|----------|
| `buscar_reformas_huelva.bat` | **Paso 1** — busca los negocios sin web y crea el CSV |
| `enviar_whatsapp_huelva_reformas.bat` | **Paso 2** — envía los WhatsApp |
| `config_huelva_reformas.json` | Config del buscador (sectores, zonas, API key) |
| `whatsapp_config_huelva_reformas.json` | Config del envío (mensajes, límites) |
| `envios_whatsapp_huelva_reformas.log` | Registro de a quién se ha enviado (se crea solo) |

> Es una campaña **separada** de los restaurantes: log propio, config propio. No se mezclan.

## Cómo se usa (3 pasos)

### Paso 1 — Buscar negocios
Doble clic en **`buscar_reformas_huelva.bat`**.
Al terminar habrá creado un CSV llamado algo como:
`reformas_huelva_provincia_sin_web_20260608_173000.csv`

### Paso 2 — Pegar el nombre del CSV (lo único manual)
1. Abre `whatsapp_config_huelva_reformas.json`.
2. Busca la línea `"archivo_csv": "PEGA_AQUI_EL_CSV_GENERADO.csv"`.
3. Sustituye ese texto por el **nombre exacto** del CSV que se creó en el paso 1.
4. Guarda.

> Si se te olvida, el envío te avisará con un error claro en vez de mandar nada raro.

### Paso 3 — Enviar WhatsApp
1. Abre **WhatsApp Web** en el navegador y comprueba que tienes la sesión iniciada.
2. Doble clic en **`enviar_whatsapp_huelva_reformas.bat`**.
3. No toques el ratón ni el teclado mientras envía (usa el modo automático).

Límites de seguridad ya puestos: 20 por ejecución, 40 al día, pausa de 10 min cada 5, delay
aleatorio de 60–120 s, y solo móviles (6xx/7xx). No reenvía a quien ya está en el log.

## El guion que cierra (importante)

El `.bat` solo manda el **primer mensaje** (el gancho). El cierre lo haces tú a mano:

1. **1er mensaje (automático):** *"Hola 👋 ¿hablo con el responsable de {nombre}?"* (rota 5 variantes).
2. **2º mensaje (tú, cuando digan "soy yo / dime"):**
   > *"Genial 🙌 Soy Mario de ayanip.es. Vi que {nombre} sale en Google pero sin web propia, así
   > que quien busca un fontanero/electricista en {zona} acaba llamando a otro. Os he montado una
   > demo de cómo os llegarían presupuestos desde Google 👇 [link]. Échale un ojo, sin compromiso."*
3. **Cierre:** *"Si te encaja, te la dejo funcionando en 2-3 días por X€. ¿Te llamo 5 min mañana?"*

El gancho para oficios es **"te traigo clientes/presupuestos de Google"**, no "una web".

## Para repetir en otra zona o sector

Copia los dos `.json` y los dos `.bat`, y cambia dentro: `search_type` y `output_prefix` (buscador),
y `archivo_csv` y `log_envios` (envío). El resto funciona igual.
