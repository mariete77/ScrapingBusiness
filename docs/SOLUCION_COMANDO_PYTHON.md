# Solución al problema del comando Python

## El problema

Cuando intentas ejecutar el script con `py`, obtienes este error:

```
py : El término 'py' no se reconoce como nombre de un cmdlet, función, archivo de script o programa ejecutable.
```

## La causa

Este problema ocurre por una de estas razones:

1. **El comando `py` no está en tu PATH** del sistema
2. **El Python Launcher para Windows** no está instalado correctamente
3. **Tu terminal tiene configuraciones diferentes** a las del entorno de desarrollo

## La solución: Usa el archivo .bat (MÁS FÁCIL) ⭐

### ✅ Comando RECOMENDADO (funciona siempre):

```powershell
enviar_whatsapp.bat --yes
```

### ✅ Opción 2: Usar `python` (ahora funciona):

```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### ✅ Opción 3: Usar ruta completa:

```powershell
C:\Users\mario\AppData\Local\Python\bin\python.exe whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### ❌ Comando que NO funciona en tu terminal:

```powershell
py whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

## Pasos para verificar

### 1. Verificar qué comando funciona

Ejecuta estos comandos en tu PowerShell:

```powershell
# Prueba 1: ¿Funciona el archivo .bat? (RECOMENDADO)
enviar_whatsapp.bat

# Prueba 2: ¿Funciona con ruta completa?
C:\Users\mario\AppData\Local\Python\bin\python.exe --version

# Prueba 3: ¿Funciona python?
python --version

# Prueba 4: ¿Funciona py?
py --version

# Prueba 5: ¿Funciona python3?
python3 --version
```

**Usa el comando que te devuelva una versión de Python o ejecute el script.**

### 2. Ver ubicación de Python

```powershell
dir C:\Users\mario\AppData\Local\Python\bin\python.exe
```

**Output esperado:**
```
 Directorio de C:\Users\mario\AppData\Local\Python\bin

04/04/2026  19:42           605.016 python.exe
               1 archivos        605.016 bytes
```

### 3. Prueba del archivo .bat

El archivo `.bat` ya está creado y usa la ruta completa de Python:

```powershell
enviar_whatsapp.bat
```

Esto siempre funcionará porque usa la ruta completa: `C:\Users\mario\AppData\Local\Python\bin\python.exe`

## Soluciones permanentes

### Opción 1: Usar el archivo .bat (MÁS FÁCIL Y RECOMENDADO) ⭐

**Ventajas:**
- ✅ Siempre funciona (usa ruta completa)
- ✅ Muy fácil de recordar: `enviar_whatsapp.bat`
- ✅ Acepta parámetros: `enviar_whatsapp.bat --yes`
- ✅ No requiere configuración adicional

**Simplemente usa:**
```powershell
enviar_whatsapp.bat --yes
```

### Opción 2: Crear un alias en PowerShell

Agrega esto a tu perfil de PowerShell (`$PROFILE`):

```powershell
function py {
    & python $args
}
```

Para crear el perfil si no existe:
```powershell
New-Item -Type File -Path $PROFILE -Force
notepad $PROFILE
```

Luego agrega la función y recarga PowerShell:
```powershell
. $PROFILE
```

### Opción 3: Arreglar el PATH del sistema

1. Presiona `Win + X` → Sistema
2. Ve a **Acerca de** → **Configuración avanzada del sistema**
3. Haz clic en **Variables de entorno**
4. En **Variables del sistema**, busca `Path` → Editar
5. Agrega estas rutas:
   ```
   C:\Users\mario\AppData\Local\Python\bin
   C:\Users\mario\AppData\Local\Microsoft\WindowsApps
   ```
6. Reinicia PowerShell

### Opción 4: Reinstalar Python Launcher

1. Descarga Python desde: https://www.python.org/downloads/
2. Durante la instalación, MARCA la casilla **"Add Python to PATH"**
3. Instala también el **Python Launcher for Windows**
4. Reinicia tu computadora

## Resumen de comandos según tu situación

### SOLUCIÓN RECOMENDADA (siempre funciona):

```powershell
enviar_whatsapp.bat --yes
```

### Si quieres usar `python` (ahora funciona):

```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### Si quieres usar la ruta completa:

```powershell
C:\Users\mario\AppData\Local\Python\bin\python.exe whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### Si `py` funciona:

```powershell
py whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

### Si `python3` funciona:

```powershell
python3 whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

## Verificar que funciona

Ejecuta el script para confirmar:

```powershell
enviar_whatsapp.bat
```

Deberías ver:
```
============================================================
📱 Koda - WhatsApp Sender para Negocios Sin Web
============================================================
...
```

**Nota:** Si ya alcanzaste el límite diario de 10 mensajes, verás:
```
⛔ LÍMITE DIARIO ALCANZADO: Ya enviaste 10/10 hoy.
   Para no recibir bloqueo de spam, espera hasta mañana.
```
Esto es normal, espera hasta mañana para enviar más.

## Comandos útiles de diagnóstico

```powershell
# Ver todas las versiones de Python instaladas
where python

# Ver variables de entorno relacionadas con Python
Get-ChildItem Env: | Where-Object Name -like "*python*"

# Ver el registro para instalaciones de Python
Get-ItemProperty 'HKLM:\Software\Python\PythonCore' -ErrorAction SilentlyContinue
```

## Diferencia entre `py`, `python` y `python3`

| Comando | Descripción | Funciona en tu sistema |
|---------|-------------|----------------------|
| `enviar_whatsapp.bat` | Archivo .batch con ruta completa | ✅ SÍ (RECOMENDADO) |
| `python` | Ejecuta Python directamente | ✅ SÍ (ahora funciona) |
| `C:\Users\mario\AppData\Local\Python\bin\python.exe` | Ruta completa de Python | ✅ SÍ |
| `py` | Python Launcher para Windows | ❌ NO |
| `python3` | Python versión 3 (Linux/Mac) | ❌ NO |

## Contactar soporte

Si nada funciona, verifica:

1. **¿Python está instalado?**
   ```powershell
   python --version
   ```

2. **¿Estás en la carpeta correcta?**
   ```powershell
   Get-Location
   ```

3. **¿El archivo existe?**
   ```powershell
   Test-Path whatsapp_sender.py
   ```

---

## Instalación de dependencias

Si te sale el error `ModuleNotFoundError: No module named 'requests'`, ejecuta:

```powershell
python -m pip install requests
```

O con la ruta completa:
```powershell
C:\Users\mario\AppData\Local\Python\bin\python.exe -m pip install requests
```

**Conclusión:** En tu terminal actual, puedes usar **`enviar_whatsapp.bat`** (recomendado) o **`python`** (ahora funciona). Ambas opciones funcionan perfectamente.

**¿Por qué funciona `python` ahora?**
Se reinició el entorno o se configuró el PATH correctamente durante una actualización del sistema.

**¿Por qué funciona el archivo .bat?**
El archivo `enviar_whatsapp.bat` contiene:
```batch
C:\Users\mario\AppData\Local\Python\bin\python.exe whatsapp_sender.py whatsapp_config_bares_restaurantes.json %*
```

Esto significa que siempre usa la ruta completa de Python, por lo que no depende del PATH del sistema y siempre funcionará.
