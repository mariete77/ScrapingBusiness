# 📱 Instrucciones de Envío WhatsApp - Restaurantes Toledo y País Vasco

## 📍 Resumen de Disponibilidad

### Provincia de Toledo
- **Total restaurantes**: 218
- **Archivo**: `restaurantes_toledo_provincia_sin_web_20260504_152652.csv`
- **Configuración**: `whatsapp_config_toledo.json`
- **Script**: `enviar_whatsapp_toledo.bat`
- **Log**: `envios_whatsapp_toledo.log`

### País Vasco
- **Total restaurantes**: 34
- **Archivo**: `restaurantes_pais_vasco_sin_web_20260504_120205.csv`
- **Configuración**: `whatsapp_config_pais_vasco.json`
- **Script**: `enviar_whatsapp_pais_vasco.bat`
- **Log**: `envios_whatsapp_pais_vasco.log`

**TOTAL COMBINADO**: 252 restaurantes

---

## 🚀 Cómo Usar

### Opción 1: Enviar a Toledo (218 restaurantes)

1. Doble clic en `enviar_whatsapp_toledo.bat`
2. Lee las instrucciones y presiona cualquier tecla
3. El script enviará hasta 20 mensajes por ejecución
4. Si necesitas enviar más, ejecuta el script de nuevo

### Opción 2: Enviar al País Vasco (34 restaurantes)

1. Doble clic en `enviar_whatsapp_pais_vasco.bat`
2. Lee las instrucciones y presiona cualquier tecla
3. El script enviará hasta 20 mensajes por ejecución
4. Como solo hay 34 restaurantes, puedes completarlos en 2 ejecuciones

---

## ⚙️ Configuración de Envío

### Parámetros Actuales

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| **Modo** | `web` | Automatiza con pywhatkit (espera 15s por mensaje) |
| **Delay entre mensajes** | 60-120s | Aleatorio para evitar bloqueos |
| **Pausa** | Cada 5 mensajes | 10 minutos de descanso |
| **Máximo por ejecución** | 20 mensajes | Para ir poco a poco |
| **Solo móviles** | Sí | Solo números 6xx y 7xx |
| **Filtrar tipos** | restaurant, bar | Solo restaurantes y bares |

### Tipos de Mensajes

El sistema tiene **6 templates** diferentes que rotan automáticamente:

1. Mensaje formal enfocado en presencia digital profesional
2. Mensaje casual con emojis (👋) enfocado en visibilidad
3. Mensaje de diseñador web especializado
4. Mensaje enfocado en demo y ejemplos
5. Mensaje breve y directo con oferta de ver ejemplo
6. Mensaje destacando el rating y beneficios rápidos

### Variables del Mensaje

- `{nombre}` - Nombre del restaurante
- `{rating}` - Rating (ej: ⭐4.5)
- `{zona}` - Ciudad/barrio extraído automáticamente

---

## ⏱️ Tiempos Estimados

### Para Toledo (218 restaurantes)
- **Mensajes por día**: 40
- **Días necesarios**: ~5.5 días
- **Tiempo por ejecución**: ~25-30 minutos (20 mensajes)

### Para País Vasco (34 restaurantes)
- **Mensajes por día**: 40
- **Días necesarios**: ~1 día
- **Tiempo por ejecución**: ~25-30 minutos (20 mensajes)

**Tiempo total combinado**: ~6.5 días para completar ambas campañas

---

## 📊 Ejemplo de Ejecución

```
=====================================================
  ENVIANDO WHATSAPP A RESTAURANTES - PROVINCIA DE TOLEDO
=====================================================

Configuracion: whatsapp_config_toledo.json
Archivo: restaurantes_toledo_provincia_sin_web_20260504_152652.csv
Total restaurantes: 218

========================================
  IMPORTANTE - LEER ANTES DE EJECUTAR
========================================

1. Este script enviara mensajes a restaurantes sin web
2. Maximo 20 mensajes por ejecucion
3. Pausa de 10 minutos cada 5 mensajes
4. Delay aleatorio de 60-120 segundos entre mensajes
5. Solo se enviara a numeros moviles (6xx, 7xx)

========================================

Presiona cualquier tecla para continuar...

Iniciando envio de mensajes...

[Iniciando envío a 218 restaurantes...]
[Mensaje 1/20] Enviando a Restaurante Ejemplo - Rating: 4.5
✓ Enviado
...
[Pausa de 10 minutos después de 5 mensajes...]
...
```

---

## 🔍 Seguimiento y Logs

### Archivos de Log

Cada región tiene su propio log:

- `envios_whatsapp_toledo.log` - Seguimiento de Toledo
- `envios_whatsapp_pais_vasco.log` - Seguimiento de País Vasco

El log incluye:
- Fecha y hora de cada envío
- Nombre del restaurante
- Estado (OK/FAIL)
- Mensaje enviado

### Ver Progreso

Para ver cuántos restaurantes quedan pendientes:

```bash
C:\Users\mario\AppData\Local\Python\bin\python.exe check_pending.py restaurantes_toledo_provincia_sin_web_20260504_152652.csv
```

---

## ⚠️ Recomendaciones

### Para Evitar Bloqueos

1. **No envíes más de 40 mensajes por día** en total
2. **Usa los scripts de forma alternada**: un día Toledo, otro País Vasco
3. **Mantén los delays configurados**: 60-120s entre mensajes
4. **Respeta las pausas**: 10 minutos cada 5 mensajes
5. **No ejecutes múltiples scripts simultáneamente**

### Para Mejorar Respuestas

1. **Varía los mensajes**: Los 6 templates rotan automáticamente
2. **Personaliza**: El sistema extrae la zona y el rating automáticamente
3. **Horarios óptimos**: Envía entre 10:00-14:00 o 17:00-20:00 (horarios de restaurantes)
4. **Días**: Evita lunes y martes (días menos ajetreados)

---

## 🔄 Continuar Campaña

### Después de Enviar los Primeros 20 Mensajes

Para continuar con los siguientes 20:

1. Simplemente ejecuta el mismo script de nuevo
2. El sistema detectará automáticamente cuáles ya se enviaron
3. Continuará desde donde lo dejó

### Reiniciar Campaña

Si necesitas reiniciar desde cero:

1. Abre el archivo CSV correspondiente
2. Elimina la columna `estado_envio` o pon todos los valores como ""
3. Guarda el archivo
4. Ejecuta el script nuevamente

---

## 📞 Soporte

Si tienes problemas:

1. Revisa el log correspondiente
2. Verifica que WhatsApp Web esté abierto
3. Asegúrate de tener conexión a internet estable
4. Comprueba que el archivo CSV existe y tiene el formato correcto

---

## 📝 Notas Importantes

### Números Telefónicos

- **País Vasco**: Muchos fijos (943, 945, 946) - NO tienen WhatsApp
- **Toledo**: Prefijo 925 - FIJOS, NO tienen WhatsApp
- Solo se enviarán a móviles (6xx, 7xx)

### Estimación de Envíos Reales

Dado que muchos restaurantes tienen números fijos:

- **Toledo**: De 218, posiblemente 50-70 tengan móvil (~25-30%)
- **País Vasco**: De 34, posiblemente 8-12 tengan móvil (~25-30%)

**Total esperado de envíos**: 58-82 mensajes

---

## ✅ Checklist Antes de Enviar

- [ ] WhatsApp Web está abierto y funcionando
- [ ] Tienes conexión a internet estable
- [ ] Has leído los mensajes templates
- [ ] Tienes tiempo disponible (25-30 min por ejecución)
- [ ] Es un horario adecuado (10:00-14:00 o 17:00-20:00)
- [ ] No has enviado otros mensajes recientemente (espaciado)
- [ ] Has revisado el log anterior para evitar duplicados

---

## 🎯 Estrategia Recomendada

### Día 1
- Ejecutar `enviar_whatsapp_pais_vasco.bat` (34 restaurantes)
- Esperar respuestas

### Día 2-3
- Ejecutar `enviar_whatsapp_toledo.bat` (primeros 20)
- Esperar respuestas

### Día 4-6
- Continuar con Toledo (restantes ~198)
- 20-40 mensajes por día

### Día 7+
- Seguimiento de respuestas
- Reenvío a los que no respondieron (con otro template)

---

## 📈 Métricas a Seguir

- **Tasa de apertura**: Revisa cuántos abren el mensaje
- **Tasa de respuesta**: Cuántos responden
- **Mejor horario**: A qué hora responden más
- **Mejor template**: Cuál de los 6 mensajes funciona mejor

---

**Última actualización**: 4 de mayo de 2026
**Total restaurantes disponibles**: 252
**Región principal**: Toledo (218) + País Vasco (34)