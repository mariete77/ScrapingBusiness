# Instrucciones Rápidas - PowerShell Windows

## Comando para enviar mensajes

### Opción 1: Usar `python` (MÁS FÁCIL) ⭐

```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### Opción 2: Usar el archivo .bat

```powershell
enviar_whatsapp.bat --yes
```

### Opción 3: Usar la ruta completa de Python

```powershell
C:\Users\mario\AppData\Local\Python\bin\python.exe whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

## ¿Qué hace este comando?

1. **Ejecuta el script de WhatsApp** usando Python
2. **Usa la configuración** de bares y restaurantes
3. **Omite la confirmación** manual (`--yes`)

## Flujo de envío

1. El script abre **WhatsApp Web** automáticamente
2. El mensaje aparece **ya escrito** en el campo de texto
3. Solo debes **presionar Enter** para enviar
4. El script espera **60-120 segundos** entre mensajes
5. Repite para todos los mensajes

## Modo actual: web_directo

✅ Abre WhatsApp Web directamente  
✅ Mensaje prellenado automáticamente  
✅ Solo presionas Enter para enviar  

## Comprobar estado

```powershell
# Ver el log de envíos
Get-Content envios_whatsapp_bares_restaurantes.log

# Ver los últimos envíos
Get-Content envios_whatsapp_bares_restaurantes.log -Tail 10
```

## Verificar instalación de Python

```powershell
# Verificar que Python está instalado
python --version

# Ver ubicación de Python
where python
```

## Solución de problemas

### Error: "python no se reconoce" o "py no se reconoce"

**Usa el archivo .bat (siempre funciona):**
```powershell
enviar_whatsapp.bat --yes
```

**O usa la ruta completa:**
```powershell
C:\Users\mario\AppData\Local\Python\bin\python.exe whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### Error: "ModuleNotFoundError: No module named 'requests'"

**Instala el módulo faltante:**
```powershell
python -m pip install requests
```

**¿Por qué pasa esto?**
- El script requiere el módulo `requests` para funcionar
- Este error ocurre cuando las dependencias no están instaladas

**¿Por qué funciona `python` ahora?**
El PATH se configuró correctamente o se reinició el entorno, permitiendo que `python` funcione directamente.

**Solución permanente (opcional):**
1. Presiona `Win + X` → Sistema
2. Configuración avanzada del sistema → Variables de entorno
3. En Variables del sistema, busca `Path` → Editar
4. Agrega: `C:\Users\mario\AppData\Local\Python\bin`
5. Reinicia PowerShell

**Después de esto podrás usar:**
```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### Error: No se abre WhatsApp Web

```powershell
# Verificar navegador predeterminado
# Asegúrate de tener sesión iniciada en web.whatsapp.com
```

### Cambiar el número de mensajes

Edita `whatsapp_config_bares_restaurantes.json`:

```json
{
  "max_mensajes_por_ejecucion": 5
}
```

## Configuración actual

- **Modo**: web_directo
- **Máximo por ejecución**: 10 mensajes
- **Solo móviles**: true (solo números que empiezan por 6 o 7)
- **Delay entre mensajes**: 60-120 segundos (aleatorio)

---
**Última actualización**: 30 de abril de 2026