# 🎯 Resumen: Restaurantes Disponibles para Campaña WhatsApp

## 📊 Resumen General

**Total de restaurantes disponibles**: 252

| Región | Cantidad | Archivo CSV | Configuración JSON | Script .BAT |
|--------|----------|-------------|-------------------|-------------|
| **Provincia de Toledo** | 218 | `restaurantes_toledo_provincia_sin_web_20260504_152652.csv` | `whatsapp_config_toledo.json` | `enviar_whatsapp_toledo.bat` |
| **País Vasco** | 34 | `restaurantes_pais_vasco_sin_web_20260504_120205.csv` | `whatsapp_config_pais_vasco.json` | `enviar_whatsapp_pais_vasco.bat` |

---

## 🚀 Para Comenzar Inmediatamente

### Opción 1: Enviar a Toledo (218 restaurantes)
```
Doble clic en: enviar_whatsapp_toledo.bat
```

### Opción 2: Enviar al País Vasco (34 restaurantes)
```
Doble clic en: enviar_whatsapp_pais_vasco.bat
```

---

## ⏱️ Estimación de Envíos

### Nota Importante sobre Números Telefónicos

- **Toledo**: Prefijo 925 = Números FIJOS (NO tienen WhatsApp)
- **País Vasco**: Prefijos 943, 945, 946 = Números FIJOS (NO tienen WhatsApp)
- Solo se enviarán a **números móviles** (6xx, 7xx)

### Estimación Realista

Dado que ~25-30% de restaurantes tienen móvil:

| Región | Total | Estimación con móvil | Mensajes reales |
|--------|-------|---------------------|-----------------|
| Toledo | 218 | 50-70 | 50-70 |
| País Vasco | 34 | 8-12 | 8-12 |
| **TOTAL** | **252** | **58-82** | **58-82** |

---

## 📱 Configuración de Envío

| Parámetro | Valor |
|-----------|-------|
| Modo | web (automatizado con pywhatkit) |
| Delay entre mensajes | 60-120 segundos (aleatorio) |
| Pausa | 10 minutos cada 5 mensajes |
| Máximo por ejecución | 20 mensajes |
| Máximo por día | 40 mensajes |
| Solo móviles | Sí (6xx, 7xx) |
| Tipos filtrados | restaurant, bar |

---

## 📝 Mensajes Disponibles

El sistema tiene **6 templates** que rotan automáticamente:

1. ✉️ Mensaje formal enfocado en presencia digital profesional
2. 👋 Mensaje casual con emojis enfocado en visibilidad
3. 💻 Mensaje de diseñador web especializado
4. 📱 Mensaje enfocado en demo y ejemplos
5. 🍽️ Mensaje breve y directo con oferta de ver ejemplo
6. 🌟 Mensaje destacando el rating y beneficios rápidos

### Variables Incluidas

- `{nombre}` - Nombre del restaurante
- `{rating}` - Rating (ej: ⭐4.5)
- `{zona}` - Ciudad/barrio extraído automáticamente

---

## ⏳ Tiempos Estimados de Campaña

### Escenario Optimista (58 mensajes reales)
- **Días necesarios**: ~1.5 días
- **Ejecuciones por día**: 2-3
- **Tiempo total**: ~40-50 minutos

### Escenario Pesimista (82 mensajes reales)
- **Días necesarios**: ~2 días
- **Ejecuciones por día**: 2-3
- **Tiempo total**: ~60-70 minutos

---

## 📂 Archivos Creados

### Configuraciones
- ✅ `whatsapp_config_toledo.json` - Configuración para Toledo
- ✅ `whatsapp_config_pais_vasco.json` - Configuración para País Vasco

### Scripts de Envío
- ✅ `enviar_whatsapp_toledo.bat` - Ejecutar para enviar a Toledo
- ✅ `enviar_whatsapp_pais_vasco.bat` - Ejecutar para enviar al País Vasco

### Instrucciones
- ✅ `INSTRUCCIONES_TOLEDO_PAIS_VASCO.md` - Guía detallada completa

### Logs (se crearán al ejecutar)
- 📝 `envios_whatsapp_toledo.log` - Seguimiento de Toledo
- 📝 `envios_whatsapp_pais_vasco.log` - Seguimiento de País Vasco

---

## 🎯 Recomendación de Estrategia

### Día 1: Test con País Vasco
- Ejecutar `enviar_whatsapp_pais_vasco.bat`
- 34 restaurantes → ~8-12 mensajes reales
- Ver respuestas y ajustar si es necesario

### Día 2-3: Toledo - Primera tanda
- Ejecutar `enviar_whatsapp_toledo.bat`
- Primeros 20 mensajes
- Analizar tasa de respuesta

### Día 4-6: Toledo - Continuación
- Continuar con el resto de Toledo
- 20-40 mensajes por día
- Ajustar mensajes según respuesta

### Día 7+: Seguimiento
- Reenviar a los que no respondieron
- Usar otro template diferente
- Seguir conversaciones iniciadas

---

## ⚠️ Precauciones

1. **No exceder 40 mensajes por día** en total
2. **Mantener delays configurados** (60-120s)
3. **Respetar pausas** (10 min cada 5 mensajes)
4. **Usar horarios adecuados** (10:00-14:00 o 17:00-20:00)
5. **No ejecutar múltiples scripts simultáneamente**

---

## ✅ Checklist Antes de Empezar

- [ ] WhatsApp Web abierto y funcionando
- [ ] Conexión a internet estable
- [ ] Tiempo disponible (25-30 min por ejecución)
- [ ] Horario adecuado (evitar horas punta de servicio)
- [ ] No has enviado otros mensajes recientemente

---

## 📞 Soporte

Para ver instrucciones detalladas:
```
Abrir: INSTRUCCIONES_TOLEDO_PAIS_VASCO.md
```

Para ver progreso pendiente:
```bash
C:\Users\mario\AppData\Local\Python\bin\python.exe check_pending.py restaurantes_toledo_provincia_sin_web_20260504_152652.csv
```

---

## 📈 Métricas a Seguir

- **Tasa de apertura**: Revisa cuántos abren el mensaje
- **Tasa de respuesta**: Cuántos responden
- **Mejor horario**: A qué hora responden más
- **Mejor template**: Cuál de los 6 mensajes funciona mejor

---

## 🎉 ¡Listo para Empezar!

1. Elige la región (Toledo o País Vasco)
2. Doble clic en el script correspondiente
3. Sigue las instrucciones
4. ¡Comienza la campaña!

**Creado el**: 4 de mayo de 2026  
**Estado**: ✅ Todo listo para ejecutar