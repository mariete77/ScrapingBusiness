# ⚡ SOLUCIÓN RÁPIDA - Python no reconocido

## 🎯 El problema
Los comandos `python` y `py` no funcionan en tu PowerShell.

## ✅ La solución inmediata

### Usa el archivo `.bat` (¡ESTO SIEMPRE FUNCIONA!)

```powershell
enviar_whatsapp.bat --yes
```

¡Eso es todo! No necesitas configurar nada más.

---

## 📝 ¿Por qué funciona el archivo .bat?

El archivo `enviar_whatsapp.bat` ya tiene configurada la ruta completa de Python:
```
C:\Users\mario\AppData\Local\Python\bin\python.exe
```

Así que cuando ejecutas `enviar_whatsapp.bat`, el sistema sabe exactamente dónde encontrar Python.

---

## 🚀 Otros comandos útiles

### Verificar el log de envíos
```powershell
type envios_whatsapp_bares_restaurantes.log
```

### Ver los últimos 10 envíos
```powershell
Get-Content envios_whatsapp_bares_restaurantes.log -Tail 10
```

### Ejecutar sin confirmación
```powershell
enviar_whatsapp.bat --yes
```

### Ejecutar con confirmación manual
```powershell
enviar_whatsapp.bat
```

---

## 📋 Configuración del archivo .bat

El archivo `enviar_whatsapp.bat` contiene:
```batch
@echo off
REM Script para ejecutar el sender de WhatsApp
REM Uso: enviar_whatsapp.bat [opcion]
REM Opciones: --yes (auto-confirmar)

C:\Users\mario\AppData\Local\Python\bin\python.exe whatsapp_sender.py whatsapp_config_bares_restaurantes.json %*
```

El `%*` al final permite pasar cualquier argumento adicional como `--yes`.

---

## 🔧 ¿Quieres que funcione `python` directamente?

Si prefieres usar el comando `python` en lugar del archivo `.bat`, puedes agregar Python al PATH:

1. Presiona `Win + X` → Sistema
2. Configuración avanzada del sistema → Variables de entorno
3. En Variables del sistema, busca `Path` → Editar
4. Agrega: `C:\Users\mario\AppData\Local\Python\bin`
5. Reinicia PowerShell

Después de esto podrás usar:
```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

**Ojo:** Esto es opcional. El archivo `.bat` funciona perfectamente sin esto.

---

## ❌ NO uses estos comandos (no funcionarán):

```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
py whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

Estos darán el error: "python no se reconoce como nombre de un cmdlet..."

---

## ✅ Comando correcto (usa siempre este):

```powershell
enviar_whatsapp.bat --yes
```

---

## 📊 Estado actual del sistema

- ✅ Python instalado: `C:\Users\mario\AppData\Local\Python\bin\python.exe`
- ✅ Script de WhatsApp: `whatsapp_sender.py`
- ✅ Configuración: `whatsapp_config_bares_restaurantes.json`
- ✅ Archivo .bat funcionando: `enviar_whatsapp.bat`
- ✅ Log de envíos: `envios_whatsapp_bares_restaurantes.log`

---

**¡Resumen! Usa `enviar_whatsapp.bat --yes` y listo.**