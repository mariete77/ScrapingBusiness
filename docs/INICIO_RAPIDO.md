# 🚀 Inicio Rápido - Buscador de Negocios Sin Web

Configura y ejecuta el script en 5 minutos.

---

## Paso 1: Obtener API Key (3 minutos)

1. Ve a: https://console.cloud.google.com/apis/library/places-backend.googleapis.com

2. **Crea un proyecto:**
   - Click en "Select a project" → "New Project"
   - Nombre: "Buscador Negocios" (o lo que quieras)
   - Click en "Create"

3. **Habilita la API:**
   - Busca "Places API"
   - Click en "Enable"

4. **Crea API Key:**
   - Ve a: https://console.cloud.google.com/apis/credentials
   - Click en "Create Credentials" → "API key"
   - Copia la API key (empieza con `AIza...`)

💰 **Gratis:** $200 de crédito mensual

---

## Paso 2: Configurar el Script (1 minuto)

1. Copia el archivo de configuración:
   ```bash
   cp config.example.json config.json
   ```

2. Edita `config.json` y pega tu API key:
   ```json
   {
     "api_key": "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
     "location": "40.416775,-3.703790",
     "location_name": "Madrid",
     "radius": 10000,
     "search_type": "accounting"
   }
   ```

---

## Paso 3: Instalar Python (si no lo tienes)

### Windows
1. Descarga: https://python.org/downloads/
2. Instala y marca "Add Python to PATH"
3. Verifica: `python --version`

### Mac
```bash
brew install python3
python3 --version
```

### Linux
```bash
sudo apt install python3
python3 --version
```

---

## Paso 4: Instalar dependencias (30 segundos)

```bash
pip install requests
```

O desde el archivo requirements:
```bash
pip install -r requirements.txt
```

---

## Paso 5: Ejecutar el Script (1 minuto)

```bash
python3 scraping-script-v2.py
```

**Si usas Windows:**
```bash
python scraping-script-v2.py
```

---

## 📊 Ver Resultados

El script generará un archivo CSV:
```
negocios_sin_web_madrid_20260330_163045.csv
```

Ábrelo en Excel, Google Sheets, o cualquier visor de CSV.

---

## 🎯 ¿Qué sigue?

1. **Revisa el CSV** con los negocios sin web
2. **Haz outreach** usando las plantillas en `plan-outreach.md`
3. **Cierra ventas** → Ingreso extra 🎉

---

## 🏪 Cambiar Tipo de Negocio

Edita `config.json`:

```json
{
  "search_type": "restaurant"  // Restaurantes
}
```

**Tipos disponibles:**
- `accounting` → Gestorías
- `restaurant` → Restaurantes
- `store` → Tiendas
- `health` → Salud
- `lawyer` → Abogados
- `real_estate_agent` → Inmobiliarias
- `beauty_salon` → Peluquerías
- `gym` → Gimnasios

---

## ❌ Problemas Comunes

### Error: "No module named 'requests'"
```bash
pip install requests
```

### Error: "API key invalid"
- Verifica que copiaste correctamente la API key
- Asegúrate de que habilitaste la "Places API"

### Error: "config.json not found"
```bash
cp config.example.json config.json
```

### No encuentra resultados
- Aumenta el `radius` en config.json
- Cambia el `search_type`
- Verifica las coordenadas de ubicación

---

## 📞 ¿Necesitas ayuda?

Revisa:
- `README.md` → Documentación completa
- `plan-outreach.md` → Plantillas de ventas
- Contacta a Koda (tu asistente) si tienes problemas

---

_Última actualización: 2026-03-30_
