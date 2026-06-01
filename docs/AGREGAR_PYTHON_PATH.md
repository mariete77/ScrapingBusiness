# 🐍 Añadir Python al PATH en Windows 10

## 📍 Ubicación de Python

Python está instalado en:
```
C:\Users\mario\AppData\Local\Python\bin
```

Esta es la ruta que debes añadir al PATH.

---

## 📋 Instrucciones paso a paso

### Método 1: Interfaz gráfica (Recomendado)

1. **Abre el menú de configuración del sistema**
   - Presiona `Win + X`
   - Selecciona **Sistema**

2. **Abre las variables de entorno**
   - En la ventana de Configuración, busca "Variables de entorno"
   - O haz clic en: **Configuración avanzada del sistema** → **Variables de entorno**

3. **Edita el PATH del sistema**
   - En la sección "Variables del sistema" (abajo)
   - Busca la variable **Path**
   - Selecciona **Path** → Haz clic en **Editar...**

4. **Añade la ruta de Python**
   - Haz clic en **Nuevo**
   - Escribe: `C:\Users\mario\AppData\Local\Python\bin`
   - Haz clic en **Aceptar** en todas las ventanas

5. **Reinicia PowerShell**
   - Cierra todas las ventanas de PowerShell
   - Abre una nueva ventana de PowerShell

6. **Verifica que funciona**
   ```powershell
   python --version
   ```

---

### Método 2: Usando PowerShell (Método avanzado)

Si prefieres hacerlo desde PowerShell con un solo comando:

```powershell
# Añadir Python al PATH del sistema (requiere permisos de administrador)
setx PATH "$env:PATH;C:\Users\mario\AppData\Local\Python\bin" /M
```

Luego reinicia PowerShell y verifica:
```powershell
python --version
```

⚠️ **Nota:** Necesitas ejecutar PowerShell como administrador para este método.

---

## ✅ Verificar que funcionó

Después de reiniciar PowerShell, prueba estos comandos:

```powershell
# Ver versión de Python
python --version

# Ver ubicación de Python
where python

# Ejecutar tu script
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

Si funciona, verás la versión de Python (ejemplo: `Python 3.14.0`).

---

## 🔍 Si no funciona después de añadirlo

### 1. Verifica que la ruta está correcta
```powershell
echo $env:PATH
```
Deberías ver `C:\Users\mario\AppData\Local\Python\bin` en la salida.

### 2. Verifica que Python existe en esa ubicación
```powershell
dir "C:\Users\mario\AppData\Local\Python\bin"
```
Deberías ver archivos como `python.exe`, `pip.exe`, etc.

### 3. Reinicia completamente
- Cierra TODAS las ventanas de PowerShell
- Abre una nueva ventana
- Vuelve a probar `python --version`

### 4. Si aún no funciona, prueba con la ruta completa
```powershell
& "C:\Users\mario\AppData\Local\Python\bin\python.exe" --version
```

Si esto funciona, el problema es solo el PATH. Si no funciona, puede haber un problema con la instalación de Python.

---

## 📝 Resumen

**Ruta a añadir:**
```
C:\Users\mario\AppData\Local\Python\bin
```

**Después de añadir al PATH, podrás usar:**
```powershell
python whatsapp_sender.py whatsapp_config_bares_restaurantes.json --yes
```

**Si prefieres no modificar el PATH, sigue usando:**
```powershell
enviar_whatsapp.bat --yes
```

---

## ⚖️ ¿Modificar el PATH o usar el archivo .bat?

### Usar el archivo .bat (Actual) ✅
- ✅ Funciona ya mismo
- ✅ No requiere configuración
- ✅ Es más simple
- ❌ Tienes que recordar usar el .bat

### Modificar el PATH (Opcional)
- ✅ Puedes usar `python` directamente
- ✅ Más estándar y común
- ✅ Útil para otros proyectos de Python
- ❌ Requiere configuración
- ❌ Necesitas reiniciar PowerShell

**Mi recomendación:** Usa el archivo `.bat` por ahora. Solo modifica el PATH si planeas hacer muchos proyectos de Python o prefieres usar comandos estándar.