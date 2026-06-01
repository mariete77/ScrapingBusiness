# Configuración de WhatsApp - Bares y Restaurantes

## Resumen de la configuración actual

Esta configuración está optimizada para evitar bloqueos de spam y maximizar la efectividad de los mensajes.

### Parámetros principales

| Parámetro | Valor | Explicación |
|-----------|-------|-------------|
| **Modo** | `web_directo` | Abre WhatsApp Web con mensaje prellenado |
| **Delay entre mensajes** | 60-120s | Tiempo aleatorio para evitar detección |
| **Pausa larga** | Cada 5 mensajes | 10 minutos de descanso |
| **Variantes de mensaje** | 6 diferentes | Rotación aleatoria |
| **Límite diario** | 30 mensajes | Para evitar bloqueos |
| **Límite por ejecución** | 20 mensajes | Para ir poco a poco |
| **Solo móviles** | Sí | Solo números 6xx y 7xx |

### Comando para ejecutar

```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

## Características anti-spam

### 1. Tiempos aleatorios (60-120 segundos)

En lugar de usar un tiempo fijo, el script espera un tiempo aleatorio entre 60 y 120 segundos entre cada mensaje. Esto hace que el patrón de envío sea más natural y menos detectable como spam.

**Ejemplo:**
- Mensaje 1 → Espera 85 segundos → Mensaje 2
- Mensaje 2 → Espera 112 segundos → Mensaje 3
- Mensaje 3 → Espera 67 segundos → Mensaje 4

### 2. Pausa larga cada 5 mensajes

Cada 5 mensajes enviados, el script hace una pausa de 10 minutos. Esto es importante para evitar que WhatsApp detecte actividad masiva.

**Ejemplo:**
- Mensajes 1-5 enviados
- **Pausa de 10 minutos**
- Mensajes 6-10 enviados
- **Pausa de 10 minutos**
- Mensajes 11-15 enviados
- Y así sucesivamente...

### 3. Rotación de mensajes (6 variantes)

El script usa 6 mensajes diferentes que se seleccionan aleatoriamente. Esto evita enviar el mismo mensaje a todos los negocios, lo que sería más fácil de detectar como spam.

**Variantes de mensaje:**
1. Mensaje principal detallado con lista de beneficios
2. Mensaje corto y directo con 80% de estadística
3. Mensaje con emoji 💻 y enfoque en diseño web
4. Mensaje con emoji 📱 y mención de zona
5. Mensaje simple y conciso
6. Mensaje con emoji 🌟 y enfoque en visibilidad

### 4. Límites diarios y por ejecución

- **Límite diario:** 30 mensajes por día
- **Límite por ejecución:** 20 mensajes por ejecución

Esto permite:
- Enviar 20 mensajes en una sesión
- Hacer una pausa larga
- Enviar otros 10 mensajes más tarde
- Sin superar el límite diario de 30

## Flujo de envío completo

### Paso 1: Ejecutar el comando
```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### Paso 2: Ver el resumen
```
============================================================
📱 Koda - WhatsApp Sender para Negocios Sin Web
============================================================

📊 Ya enviados hoy: 10/30. Quedan: 20

============================================================
📱 WhatsApp Sender - Modo: WEB_DIRECTO
============================================================
📂 CSV: bares_restaurantes_ciudad_real_sin_web_20260430_115507.csv
📊 Total en CSV: 53
📞 Con teléfono válido (todos): 3
⏭️  Omitidos: 50
📤 A enviar ahora: 3
⏱️  Delay aleatorio: 60-120s entre mensajes
📝 6 variantes de mensaje (rotación aleatoria)
```

### Paso 3: WhatsApp Web se abre automáticamente

El script abre WhatsApp Web con el mensaje ya escrito en el campo de texto.

### Paso 4: Enviar el mensaje

Presiona **Enter** en WhatsApp Web para enviar el mensaje.

### Paso 5: Confirmar en la consola

Vuelve a la consola y presiona **Enter** para confirmar que enviaste el mensaje.

### Paso 6: Esperar el delay aleatorio

El script espera entre 60 y 120 segundos (mostrando una cuenta regresiva).

### Paso 7: Repetir

El script continúa automáticamente con el siguiente mensaje.

### Paso 8: Pausa larga (cada 5 mensajes)

```
☕ Pausa larga de 10 minutos (anti-bloqueo)...
```

## Por qué esta configuración es mejor

### Comparación con la configuración anterior

| Aspecto | Anterior | Actual | Mejora |
|---------|----------|--------|--------|
| Delay entre mensajes | 8 segundos fijo | 60-120s aleatorio | ✅ Más natural |
| Pausas largas | No | Sí (cada 5 mensajes) | ✅ Evita detección |
| Mensajes | 1 variante | 6 variantes | ✅ Menos spam |
| Límite diario | 10 | 30 | ✅ Más mensajes |
| Límite por ejecución | 10 | 20 | ✅ Más eficiente |

### Beneficios de la nueva configuración

1. **Menos riesgo de bloqueo**
   - Tiempos aleatorios parecen comportamiento humano
   - Pausas largas reducen actividad masiva
   - Mensajes variados parecen personalizados

2. **Más mensajes por día**
   - 30 mensajes vs 10 anteriores
   - Sin aumentar el riesgo de bloqueo

3. **Mayor efectividad**
   - Mensajes variados adaptados a diferentes tipos de negocios
   - Más tiempo entre mensajes permite respuestas intermedias

## Configuración JSON completa

```json
{
  "modo": "web_directo",
  
  "mensajes_templates": [
    "Hola {nombre}, soy Mario de Ayanip.es\n\nVi que su negocio tiene muy buenas reseñas (Rating: {rating}) pero aún no tiene presencia digital profesional.\n\nEn la era del delivery y Google Maps, el 80% de los clientes buscan restaurantes por internet antes de ir. ¿Le gustaría que creáramos una página web profesional que muestre sus platos de forma visual y atraiga más clientes?\n\nPodemos incluir:\n• Menú digital con fotos de alta calidad\n• Sistema de reservas online\n• Integración con Google Maps\n• Fotos profesionales de sus mejores platos\n\n¿Te parece interesante? Te mando ejemplos de nuestro trabajo y agendamos una breve llamada de 10 minutos para contarte más.",
    "Hola {nombre} 👋 Soy Mario de Ayanip.es. He visto que vuestro restaurante tiene excelentes reseñas ({rating}) pero no tenéis página web.\n\nHoy en día, el 80% de los clientes buscan por internet antes de ir a un restaurante. Una web simple con menú y reservas online os ayudaría a conseguir más mesas.\n\n¿Os gustaría ver un ejemplo de cómo podría quedar vuestra web?",
    "Buenos días {nombre}, soy Mario 💻 Diseño web especializado en restaurantes.\n\nVi vuestro negocio en Google Maps ({rating} estrellas ⭐) y noté que no tienen presencia digital. Podríamos crear una web que muestre vuestros mejores platos y permita hacer reservas online 24/7.\n\n¿Te interesa que te enseñe un ejemplo rápido?",
    "Hola {nombre}, te escribo Mario desde ayanip.es 📱 Estuve buscando restaurantes en {zona} y encontré el tuyo. Me pareció que con vuestro rating ({rating}) merecéis una web que potencie aún más vuestra visibilidad.\n\nPodríamos incluir:\n• Menú digital atractivo\n• Sistema de reservas por WhatsApp\n• Galería de fotos de vuestros platos\n• Información de contacto y horarios\n\n¿Te gustaría ver una demo de cómo quedaría?",
    "Hola {nombre} 👋 Soy Mario, diseñador web. He visto que vuestro restaurante no tiene página web a pesar de tener tan buenas reseñas ({rating}).\n\nPodríamos montaros algo sencillo para que los clientes vean el menú, fotos de los platos y pidan mesa directamente desde WhatsApp.\n\n¿Os interesa ver un ejemplo?",
    "Hola {nombre}, soy Mario de Ayanip.es 🌟 Vi vuestro negocio con un excelente rating de {rating} y me gustaría ayudaros a tener más visibilidad.\n\nUna web profesional con menú digital, reservas online y fotos de alta calidad os ayudaría a atraer más clientes. Podemos tenerla lista en menos de 1 semana.\n\n¿Te parece interesante? Te muestro ejemplos de nuestro trabajo."
  ],
  
  "prefijo_pais": "34",
  
  "solo_moviles": true,
  
  "delay_min": 60,
  "delay_max": 120,
  
  "pausa_cada": 5,
  "pausa_minutos": 10,
  
  "max_mensajes_por_ejecucion": 20,
  "max_mensajes_por_dia": 30,
  
  "filtrar_tipo": "",
  
  "archivo_csv": "bares_restaurantes_ciudad_real_sin_web_20260430_115507.csv",
  "log_envios": "envios_whatsapp_bares_restaurantes.log",
  
  "whatsapp_api": {
    "access_token": "",
    "phone_number_id": "",
    "api_version": "v21.0"
  }
}
```

## Solución de problemas

### Problema: El delay es muy largo

**Solución:** Si necesitas enviar más rápido temporalmente, puedes reducir los valores:

```json
{
  "delay_min": 30,
  "delay_max": 60,
  "pausa_cada": 10,
  "pausa_minutos": 5
}
```

⚠️ **Advertencia:** Esto aumenta el riesgo de bloqueo. Úsalo con cuidado.

### Problema: No necesito pausas tan largas

**Solución:** Ajusta el parámetro `pausa_cada` a un valor más alto:

```json
{
  "pausa_cada": 10
}
```

### Problema: Quiero enviar más de 30 mensajes al día

**Solución:** Aumenta el límite diario:

```json
{
  "max_mensajes_por_dia": 50
}
```

⚠️ **Advertencia:** WhatsApp puede bloquearte si envías demasiados mensajes. Comienza con valores conservadores.

## Monitoreo de envíos

### Ver el log de envíos

```powershell
Get-Content envios_whatsapp_bares_restaurantes.log
```

### Ver los últimos 10 envíos

```powershell
Get-Content envios_whatsapp_bares_restaurantes.log -Tail 10
```

### Ver estadísticas

```powershell
# Contar envíos hoy
(Get-Content envios_whatsapp_bares_restaurantes.log | Select-String (Get-Date -Format "yyyy-MM-dd")).Count
```

## Resumen

Esta configuración está diseñada para:

✅ **Maximizar mensajes por día** (30)  
✅ **Minimizar riesgo de bloqueo** (tiempos aleatorios, pausas largas)  
✅ **Evitar detección como spam** (mensajes variados)  
✅ **Mantener control humano** (modo web_directo)  
✅ **Ser eficiente** (hasta 20 mensajes por ejecución)

**Comando para ejecutar:**
```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

---
**Fecha:** 30 de abril de 2026  
**Basado en:** Configuración exitosa de peluquerías  
**Versión:** 2.0 (Optimizada para anti-spam)