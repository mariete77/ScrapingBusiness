# Cómo buscar bares y restaurantes en Ciudad Real

Este documento explica cómo buscar bares y restaurantes en Ciudad Real que no tienen página web, usando el script de scraping.

## Archivo de configuración

Ya he creado el archivo `config_ciudad_real_bares.json` con la siguiente configuración:

```json
{
  "api_key": "TU_API_KEY_AQUI",
  "location": "38.9860,-3.9293",
  "location_name": "Ciudad Real",
  "radius": 15000,
  "search_type": "bar, restaurant",
  "output_prefix": "bares_restaurantes_ciudad_real_sin_web",
  "max_results": 150,
  "language": "es"
}
```

## Configuración del archivo

- **api_key**: Debes poner tu API key de Google Places aquí
- **location**: Coordenadas de Ciudad Real (38.9860, -3.9293)
- **location_name**: Nombre de la ciudad
- **radius**: Radio de búsqueda en metros (15000m = 15km)
- **search_type**: Tipos de negocios a buscar ("bar, restaurant")
- **output_prefix**: Prefijo para el nombre del archivo CSV generado
- **max_results**: Número máximo de resultados sin web a buscar (150)
- **language**: Idioma de los resultados ("es" para español)

## Pasos para usar el script

### 1. Configurar tu API key

Si no tienes una API key de Google Places:

1. Ve a: https://console.cloud.google.com/apis/library/places-backend.googleapis.com
2. Crea un proyecto y habilita la "Places API (New)"
3. Crea credenciales → API key
4. Copia la API key

### 2. Editar el archivo de configuración

Abre `config_ciudad_real_bares.json` y reemplaza `TU_API_KEY_AQUI` con tu API key:

```json
{
  "api_key": "AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  ...
}
```

### 3. Ejecutar el script

```bash
python scraping-script-v2.py config_ciudad_real_bares.json
```

## Qué obtendrás

El script:
1. Buscará bares y restaurantes en un radio de 15km desde Ciudad Real
2. Filtrará los que NO tienen página web
3. Guardará hasta 150 negocios sin web en un archivo CSV
4. El archivo tendrá el nombre: `bares_restaurantes_ciudad_real_sin_web_YYYYMMDD_HHMMSS.csv`

## Campos del CSV generado

- **fecha_buscado**: Fecha y hora de la búsqueda
- **nombre**: Nombre del negocio
- **direccion**: Dirección completa
- **telefono**: Teléfono nacional
- **correo**: Siempre vacío (Google no proporciona emails)
- **tiene_web**: "SI" o "NO"
- **website**: URL de la web o "NO"
- **rating**: Puntuación media (0-5)
- **reseñas**: Número de reseñas
- **tipos**: Tipos de negocio según Google

## Modificar la configuración

### Cambiar el radio de búsqueda

Edita `config_ciudad_real_bares.json`:

```json
{
  "radius": 10000,  // 10km en lugar de 15km
  ...
}
```

### Buscar solo bares o solo restaurantes

```json
{
  "search_type": "bar",  // Solo bares
  // o
  "search_type": "restaurant",  // Solo restaurantes
  ...
}
```

### Aumentar el número de resultados

```json
{
  "max_results": 200,  // Buscar hasta 200 negocios sin web
  ...
}
```

## Diferencias con la búsqueda de peluquerías

| Aspecto | Peluquerías | Bares/Restaurantes |
|---------|-------------|-------------------|
| search_type | "hair salon,barber shop" | "bar, restaurant" |
| location | Madrid (40.416775,-3.703790) | Ciudad Real (38.9860,-3.9293) |
| radius | 10000m (10km) | 15000m (15km) |
| output_prefix | "peluquerias_barberias_sin_web" | "bares_restaurantes_ciudad_real_sin_web" |

## Solución de problemas

### Error: "Debes configurar tu API key"

- Verifica que has puesto tu API key en `config_ciudad_real_bares.json`
- Asegúrate de no tener el texto "TU_API_KEY_AQUI" en el archivo

### Error: "PERMISSION_DENIED"

- Asegúrate de haber habilitado "Places API (New)" en Google Cloud Console
- Verifica que tu API key tiene los permisos correctos

### No se encuentran resultados

- Aumenta el radio de búsqueda
- Verifica que las coordenadas son correctas
- Intenta cambiar el search_type

## Siguientes pasos

Después de obtener el CSV:

1. Revisa los negocios encontrados
2. Filtra por rating o número de reseñas si lo deseas
3. Prepara tu estrategia de outreach
4. Contacta a los negocios sin web ofreciendo tus servicios