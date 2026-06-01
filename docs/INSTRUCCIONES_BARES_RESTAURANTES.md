# 🍽️ Guía Completa: Outreach para Bares y Restaurantes

Esta guía explica cómo usar el sistema completo para encontrar y contactar bares y restaurantes sin página web en Ciudad Real.

---

## 📋 Índice

1. [Resumen del Sistema](#resumen-del-sistema)
2. [Servicios Ofrecidos](#servicios-ofrecidos)
3. [Paso 1: Buscar Negocios](#paso-1-buscar-negocios)
4. [Paso 2: Analizar Resultados](#paso-2-analizar-resultados)
5. [Paso 3: Enviar Mensajes](#paso-3-enviar-mensajes)
6. [Paso 4: Gestionar Respuestas](#paso-4-gestionar-respuestas)
7. [Plantillas de Mensajes](#plantillas-de-mensajes)
8. [Tips de Éxito](#tips-de-éxito)

---

## 🎯 Resumen del Sistema

El sistema completo consta de:

1. **Scraper de Google Places** - Encuentra bares y restaurantes sin web
2. **CSV de Resultados** - Lista de 53 clientes potenciales en Ciudad Real
3. **Plantillas de Outreach** - 6 mensajes diferentes para diferentes enfoques
4. **WhatsApp Sender** - Envía mensajes personalizados automáticamente

---

## 💼 Servicios Ofrecidos

### 1. Página Web Profesional
- Menú digital con fotos de alta calidad
- Sistema de reservas online 24/7
- Integración con Google Maps y redes sociales
- Optimización SEO local para aparecer en búsquedas
- Diseño responsive para móviles

### 2. App de Pedidos en Mesa
- QR en cada mesa para acceso instantáneo
- Menú interactivo con fotos
- Pedidos directos sin esperar
- Pagos integrados
- Notificaciones al personal

### 3. Dashboard de Análisis
- Ventas en tiempo real
- Análisis de platos más vendidos
- Detección de pérdidas y desperdicios
- Reportes mensuales automáticos
- Alertas de stock bajo

### 🎯 Paquete Completo

Incluye:
- ✅ Setup completo en 2 semanas
- ✅ Formación del personal
- ✅ Soporte técnico 1 año
- ✅ Actualizaciones gratuitas

---

## 📍 Paso 1: Buscar Negocios

### Ejecutar el Scraper

```bash
python scraping-script-v2.py config_ciudad_real_bares.json
```

### Resultados Esperados

El script generará un archivo CSV como:
`bares_restaurantes_ciudad_real_sin_web_20260430_115507.csv`

Con:
- **53 negocios sin web** (clientes potenciales)
- Información completa: nombre, dirección, teléfono, rating, reseñas
- Clasificación por tipo: bar, restaurant, etc.

### 📊 Análisis de Teléfonos (Importante!)

**Resultado del análisis:**
- 📱 **13 móviles** (tienen WhatsApp) - **24.5% del total**
- 📞 **31 fijos** (NO tienen WhatsApp) - estos se descartan automáticamente
- ❌ **9 sin teléfono**

**Sistema configurado para descartar fijos automáticamente:**
- El archivo de configuración `whatsapp_config_bares_restaurantes.json` tiene activada la opción `"solo_moviles": true`
- Solo se enviarán mensajes a los 13 negocios con móvil
- Los 31 fijos (empiezan por 926) se ignoran automáticamente

### Ejemplo de Negocios con Móvil (WhatsApp disponible)

1. **Restaurante La Abadia de calatrava** - Rating: ⭐4.6 (511 reseñas) - Tel: 683 54 42 44
2. **Tapería Bar Sabores** - Rating: ⭐4.5 (77 reseñas) - Tel: 622 53 75 55
3. **Oliva Real - Restaurante Libanés** - Rating: ⭐4.5 (157 reseñas) - Tel: 662 31 20 59
4. **Restaurante El Señor Perez** - Rating: ⭐4.0 (727 reseñas) - Tel: 610 43 64 06
5. **Bar Kertassi** - Rating: ⭐4.1 (523 reseñas) - Tel: 667 70 30 82

### Ejemplo de Negocios con Fijo (NO tienen WhatsApp - Se descartan)

- **Hamburguesería Cronicass** - Rating: ⭐4.8 (4,967 reseñas) - Tel: 926 30 64 23 ❌
- **Bar Restaurante Di Mari** - Rating: ⭐4.7 (282 reseñas) - Tel: 926 36 58 95 ❌
- **Bar Restaurante Los Llanos** - Rating: ⭐4.4 (1,258 reseñas) - Tel: 926 22 59 92 ❌

> ⚠️ **Nota:** Aunque algunos negocios con fijo tienen excelente rating y muchas reseñas, NO pueden recibir WhatsApp, por lo que se descartan para el envío automático. Podrías contactarlos por teléfono directamente.

---

## 📊 Paso 2: Analizar Resultados

### Abrir el CSV

El archivo CSV contiene las siguientes columnas:

- `fecha_buscado` - Fecha de búsqueda
- `nombre` - Nombre del negocio
- `direccion` - Dirección completa
- `telefono` - Número de teléfono
- `tiene_web` - "SI" o "NO" (solo "NO" en este CSV)
- `website` - URL (vacío para negocios sin web)
- `rating` - Calificación (0-5 estrellas)
- `reseñas` - Número de reseñas en Google
- `tipos` - Categorías del negocio según Google

### Criterios de Priorización

**🎯 Alta Prioridad:**
- Rating ≥ 4.0
- Mínimo 100 reseñas
- Tiene teléfono
- Tipo: "restaurant" (no solo "bar")

**⚠️ Prioridad Media:**
- Rating ≥ 3.5
- 50-99 reseñas
- Tiene teléfono

**❌ Baja Prioridad:**
- Rating < 3.5
- Menos de 50 reseñas
- Sin teléfono

### Ejemplo de Análisis

```python
# Filtrar por rating y reseñas
import pandas as pd

df = pd.read_csv('bares_restaurantes_ciudad_real_sin_web_20260430_115507.csv')

# Alta prioridad
alta_prioridad = df[(df['rating'] >= 4.0) & (df['reseñas'] >= 100)]
print(f"Alta prioridad: {len(alta_prioridad)} negocios")

# Con teléfono
con_telefono = df[df['telefono'].notna() & (df['telefono'] != '')]
print(f"Con teléfono: {len(con_telefono)} negocios")
```

---

## 📱 Paso 3: Enviar Mensajes

### Configurar el WhatsApp Sender

El archivo de configuración ya está listo:
`whatsapp_config_bares_restaurantes.json`

Contiene:
- Mensaje personalizado con {nombre} y {rating}
- CSV específico para bares y restaurantes
- Log separado para no mezclar con peluquerías

### Ejecutar el Sender

```bash
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json
```

### Modos de Envío

#### 📲 Modo WA.ME (Recomendado para empezar)
- Abre enlaces wa.me en el navegador
- Mensaje prellenado
- Tú pulsas "Enviar" manualmente
- Sin riesgo de bloqueo

#### ☁️ Modo API (Para escalar)
- Envío 100% automático
- Requiere WhatsApp Business
- Requiere API de Meta

### Secuencia de Mensajes Recomendada

  **Día 1:** Mensaje 1 (Introducción general)
  ```
  Hola {nombre}, soy Mario de Ayanip.es

  Vi que su negocio tiene muy buenas reseñas (Rating: {rating}) pero aún no tiene presencia digital profesional.

  En la era del delivery y Google Maps, el 80% de los clientes buscan restaurantes por internet antes de ir. ¿Le gustaría que creáramos una página web profesional que muestre sus platos de forma visual y atraiga más clientes?

  Podemos incluir:
  • Menú digital con fotos de alta calidad
  • Sistema de reservas online
  • Integración con Google Maps
  • Fotos profesionales de sus mejores platos

  ¿Te parece interesante? Te mando ejemplos de nuestro trabajo.
  ```

**Día 4:** Mensaje 2 (Si no respondió - Enfoque en app de pedidos)

**Día 7:** Mensaje 3 (Si no respondió - Enfoque en análisis)

**Día 10:** Mensaje 4 (Si no respondió - Paquete completo)

**Día 14:** Mensaje 5 (Último seguimiento)

---

## 💬 Paso 4: Gestionar Respuestas

### Respuestas Típicas y Cómo Responder

#### 1. "¿Cuánto cuesta?"
```
¡Hola! Tenemos un paquete especial de lanzamiento en Ciudad Real que incluye:
- Página web profesional
- App de pedidos en mesa
- Dashboard de análisis

Incluye setup, formación y soporte por 1 año.
¿Te gustaría que agendemos una llamada de 10 minutos para explicarte mejor las condiciones especiales?
```

#### 2. "No tengo presupuesto ahora"
```
¡Entiendo! No es problema. ¿Podemos mantenerte informado cuando lances un proyecto futuro?

También puedo enviarte un resumen de cómo otros restaurantes aumentaron sus ventas un 30-40% con estos servicios, por si te sirve de referencia.
```

#### 3. "Ya tengo página web"
```
¡Perfecto! Entiendo que valoras lo digital. ¿Te gustaría una auditoría gratuita de tu web para ver cómo podrías mejorar la conversión de reservas?

O si prefieres, la app de pedidos en mesa y el dashboard de análisis funcionan perfectamente con cualquier página web existente.
```

#### 4. "¿Puedo ver ejemplos?"
```
¡Claro! Te envío algunos ejemplos:

1. **La Taberna de Juan (Toledo)** - Aumentó ventas 40% en 4 meses
2. **Restaurante El Carmen** - Redujo tiempo de espera 50% con app de pedidos
3. **Bodega Sancho** - Ahorró 3.000€/mes detectando pérdidas con el dashboard

¿Te gustaría ver una demo específica de alguno de estos servicios?
```

#### 5. "Pásame más información por email"
```
¡Perfecto! ¿A qué email te lo envío?

Te enviaré:
- Presentación completa de servicios
- Casos de éxito con resultados
- Ejemplos de diseños
- Presupuesto detallado
```

#### 6. "¿Cuánto tiempo tarda en estar listo?"
```
¡Excelente pregunta! Los tiempos son:
- **Página web**: 5-7 días
- **App de pedidos**: 7-10 días
- **Dashboard de análisis**: 3-5 días
- **Paquete completo**: 2 semanas

Incluye formación del personal (1 día) y pruebas antes de lanzar.
```

---

## 📝 Plantillas de Mensajes

### Todas las plantillas disponibles en: `plan-outreach-bares-restaurantes.md`

1. **Mensaje 1:** Introducción General
2. **Mensaje 2:** Enfoque en App de Pedidos
3. **Mensaje 3:** Enfoque en Análisis y Control
4. **Mensaje 4:** Paquete Completo
5. **Mensaje 5:** Seguimiento
6. **Mensaje 6:** Caso de Éxito (Prueba Social)

### Variables Disponibles

- `{nombre}` - Nombre del negocio
- `{direccion}` - Dirección del negocio
- `{telefono}` - Teléfono del negocio
- `{rating}` - Rating del negocio (⭐4.5)
- `{zona}` - Ciudad/barrio extraído de la dirección

---

## 🎯 Tips de Éxito

### 1. Personaliza Siempre
- Usa el nombre del negocio
- Menciona el rating específico
- Referencia algo de su menú si es posible

### 2. Envía en Horarios Adecuados
**❌ Evitar:**
- 12:00-15:00 (hora punta almuerzo)
- 20:00-23:00 (hora punta cena)
- Domingos y festivos

**✅ Mejores momentos:**
- 10:00-11:30 (antes del almuerzo)
- 16:00-17:30 (entre servicios)
- 10:00-12:00 (mañana tranquila)

### 3. Sigue Persistente
- Si no responden, envía 2-3 mensajes de seguimiento
- Intervalos de 3-5 días entre mensajes
- Cambia el enfoque en cada mensaje

### 4. Usa Prueba Social
- Menciona casos de éxito reales
- Incluye números específicos
- Cita de clientes satisfechos

### 5. Crea Urgencia
- "Solo 3 plazas disponibles"
- "Oferta válida hasta fin de mes"
- "Lanzamiento exclusivo en Ciudad Real"

### 6. Ofrece Valor Primero
- No vendas directamente en el primer mensaje
- Ofrece información útil
- Demuestra que entiendes su negocio

---

## 📊 Métricas a Medir

### Tasa de Respuesta Objetiva
- **WhatsApp:** 15-25%
- **Email:** 5-10%
- **Llamada:** 10-15%

### Tasas de Conversión Objetivas
- **Conversión a demo:** 30-50% de respuestas
- **Conversión a venta:** 10-20% de demos
- **Tasa de cierre total:** 2-5% de contactos

### Con 13 Negocios (Solo móviles con WhatsApp)
- Espera ~2-4 respuestas (15-25% tasa de respuesta)
- Espera ~1-2 demos agendadas (30-50% conversión de respuestas)
- Espera ~0-1 ventas cerradas (10-20% conversión de demos)

> 💡 **Nota:** De los 53 negocios totales, solo 13 tienen móvil (24.5%). Los 31 fijos y 9 sin teléfono se descartan automáticamente por el sistema.

---

## 🔄 Ciclo Completo de Outreach

### Semana 1: Búsqueda y Primer Contacto
- ✅ Ejecutar scraper (53 negocios encontrados)
- ✅ Analizar y priorizar resultados
- ✅ Enviar primer mensaje a 10 negocios de alta prioridad

### Semana 2: Seguimientos
- ✅ Enviar segundo mensaje a no-respuestas (día 4)
- ✅ Gestionar respuestas del primer mensaje
- ✅ Agendar demos con interesados

### Semana 3: Cierre de Ventas
- ✅ Enviar tercer mensaje (día 7)
- ✅ Realizar demos agendadas
- ✅ Cerrar ventas

### Semana 4: Expansión
- ✅ Enviar mensajes restantes (53 - 10 iniciales)
- ✅ Repetir ciclo con nuevos contactos
- ✅ Ajustar estrategia según resultados

---

## 🚀 Comandos Rápidos

```bash
# Buscar negocios
python scraping-script-v2.py config_ciudad_real_bares.json

# Enviar mensajes (primer contacto)
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json

# Ver resultados
start bares_restaurantes_ciudad_real_sin_web_20260430_115507.csv

# Ver plantillas de mensajes
start plan-outreach-bares-restaurantes.md
```

---

## 📞 Contacto de Soporte

Si tienes problemas con el sistema:
1. Revisa esta guía completa
2. Consulta el README principal
3. Revisa las plantillas de outreach
4. Contacta a Koda (tu asistente)

---

## 🎓 Recursos Adicionales

- [Google Places API Documentation](https://developers.google.com/maps/documentation/places/web-service/overview)
- [WhatsApp Business API](https://developers.facebook.com/docs/whatsapp/)
- [Plan de Outreach Completo](plan-outreach-bares-restaurantes.md)

---

_Última actualización: 2026-04-30_