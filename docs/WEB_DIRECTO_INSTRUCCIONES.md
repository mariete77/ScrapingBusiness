# Modo WEB_DIRECTO - Instrucciones de Uso

## ¿Qué es el modo "web_directo"?

El modo **web_directo** es una nueva opción de envío que abre **WhatsApp Web directamente** con el mensaje ya escrito en el campo de texto. Solo necesitas presionar **Enter** para enviar cada mensaje.

## Ventajas del modo web_directo

✅ **Más rápido que el modo "web"**: No requiere esperar 15 segundos por mensaje
✅ **Más directo que el modo "wame"**: Abre directamente WhatsApp Web, no requiere pasos adicionales
✅ **Fácil de usar**: Solo presiona Enter para enviar
✅ **Mantiene el control**: Tú verificas cada mensaje antes de enviarlo

## Diferencia entre modos

| Modo | Descripción | Interacción requerida |
|------|-------------|----------------------|
| **web_directo** ⭐ | Abre WhatsApp Web con mensaje prellenado | Solo presionar Enter |
| **web** | Automatización completa con pywhatkit | Ninguna (espera 15s) |
| **wame** | Abre enlace wa.me | Abrir WhatsApp Web + enviar |
| **api** | WhatsApp Cloud API | Ninguna (requiere API) |

## Cómo usar el modo web_directo

### 1. Configurar el archivo

Edita tu archivo de configuración JSON (ej: `whatsapp_config_bares_restaurantes.json`):

```json
{
  "modo": "web_directo",
  ...
}
```

### 2. Requisitos previos

- ✅ Tener **WhatsApp Web abierto** en tu navegador preferido
- ✅ Estar **logueado** con tu cuenta de WhatsApp
- ✅ Mantener la pestaña de WhatsApp Web activa

### 3. Ejecutar el script

**En PowerShell (Windows):**
```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

**En CMD (Windows):**
```cmd
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

**En Linux/Mac:**
```bash
python3 whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

**Nota:** 
- El flag `--yes` omite la confirmación manual y ejecuta el envío automáticamente
- Si `python` no funciona, prueba con `py` o `python3`
- Usa el comando que funcione en tu sistema: `python --version` para verificar

### 4. Flujo de trabajo

1. El script muestra el resumen de envíos
2. Confirmas con `s` o `si`
3. El script **abre WhatsApp Web** automáticamente con el primer mensaje prellenado
4. **Presionas Enter** para enviar el mensaje
5. El script espera el tiempo de delay configurado (ej: 8 segundos)
6. Repite los pasos 3-5 para cada mensaje

## Configuración recomendada para web_directo

```json
{
  "modo": "web_directo",
  "solo_moviles": true,
  "delay_entre_mensajes": 8,
  "max_mensajes_por_ejecucion": 10
}
```

**Parámetros importantes:**

- `delay_entre_mensajes`: Tiempo entre mensajes en segundos (recomendado: 8-15s)
- `max_mensajes_por_ejecucion`: Cuántos mensajes enviar por ejecución (recomendado: 10)
- `pausa_cada`: Pausa larga cada X mensajes (opcional, para envíos masivos)

## Consejos para evitar bloqueos

1. **No envíes más de 10-15 mensajes seguidos** sin hacer una pausa larga
2. **Usa delays de 8-15 segundos** entre mensajes
3. **Varía los mensajes** usando múltiples templates (configura `mensajes_templates`)
4. **No envíes a números que ya recibieron mensajes** (el script lo controla automáticamente)
5. **Evita horarios nocturnos** (envía solo en horario laboral)

## Solución de problemas

### Problema: "python no se reconoce" o "py no se reconoce"

**Solución:**
1. Verifica qué comando funciona:
   ```powershell
   python --version
   py --version
   python3 --version
   ```

2. Usa el comando que te devuelva una versión de Python

3. Si ninguno funciona, reinstala Python desde: https://www.python.org/downloads/
   - **IMPORTANTE**: Marca la casilla "Add Python to PATH" durante la instalación

4. Si sigue sin funcionar, usa la ruta completa:
   ```powershell
   C:\Users\mario\AppData\Local\Python\bin\python.exe whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
   ```

### Problema: No se abre WhatsApp Web

**Solución:**
- Verifica que tu navegador predeterminado esté configurado correctamente
- Asegúrate de que `webbrowser` de Python funcione:
  ```python
  import webbrowser
  webbrowser.open("https://web.whatsapp.com")
  ```

### Problema: El mensaje no aparece prellenado

**Solución:**
- Asegúrate de tener sesión iniciada en WhatsApp Web
- Recarga la página de WhatsApp Web antes de empezar
- Verifica que el URL tenga el formato correcto: `web.whatsapp.com/send?phone=...&text=...`

### Problema: Se abre una pestaña nueva cada vez

**Solución:**
- Esto es normal para el modo web_directo
- Puedes cerrar las pestañas anteriores después de enviar
- Considera usar el modo "web" con pywhatkit si prefieres automatización completa

## Actualización desde el modo wame

Si venías usando el modo "wame", el cambio a "web_directo" es muy simple:

1. Cambia `"modo": "wame"` por `"modo": "web_directo"` en tu configuración
2. Ejecuta el script normalmente
3. Ahora se abrirá WhatsApp Web directamente en lugar de wa.me

¡Ya no necesitas el paso extra de abrir WhatsApp Web manualmente!

## ¿Cuándo usar cada modo?

- **web_directo**: Para envíos manuales controlados, cuando quieres rapidez pero con supervisión
- **web**: Para automatización completa cuando no puedes estar presente (requiere pywhatkit)
- **wame**: Para pruebas rápidas o cuando prefieres usar el enlace corto
- **api**: Para envíos masivos profesionales (requiere configuración de WhatsApp Business API)

## Ejemplo de uso completo

**En PowerShell (Windows):**
```powershell
# Ejecutar con configuración específica y auto-confirmación
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

**En CMD (Windows):**
```cmd
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

**Si `python` no funciona, prueba:**
```powershell
# Opción 1
py whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes

# Opción 2
python3 whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes

# Opción 3 (ruta completa)
C:\Users\mario\AppData\Local\Python\bin\python.exe whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

# Output esperado:
# ========================================
# 📱 WhatsApp Sender - Modo: WEB_DIRECTO
# ========================================
# 📂 CSV: bares_restaurantes_ciudad_real_sin_web_20260430_115507.csv
# 📞 Con teléfono válido (todos): 15
# 📤 A enviar ahora: 10
# ⏱️  Delay aleatorio: 60-120s entre mensajes
# 
# 🌐 WEB DIRECTO — Abre WhatsApp Web con mensaje, tú pulsas Enter
#    ✅ Abre WhatsApp Web directamente con el mensaje prellenado
#    ⚠️  Solo necesitas pulsar Enter para enviar cada mensaje
#    ⚠️  Asegúrate de tener sesión iniciada en WhatsApp Web
# 
# ¿Enviar 10 mensajes? [s/N]: s
# 
# [1/10] 📞 34612345678 - Bar Restaurante El Patio
#    🌐 Abriendo WhatsApp Web con mensaje prellenado...
#    ⏳ Solo necesitas pulsar Enter para enviar
#    ⏳ Esperando 8s (delay aleatorio)...
#    ✅ Listo
```

## Cambios realizados

- ✅ Nuevo método `_enviar_web_directo()` en `whatsapp_sender.py`
- ✅ Actualización del modo web_directo en la configuración
- ✅ Documentación completa de uso y solución de problemas
- ✅ Integración con el sistema existente de logs y CSV

---
**Fecha**: 30 de abril de 2026  
**Autor**: Cline (AI Assistant)  
**Versión**: 1.0