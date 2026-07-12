@echo off
echo =====================================================
echo   BUSCANDO REFORMAS Y OFICIOS SIN WEB - PROVINCIA DE HUELVA
echo =====================================================
echo.
echo Configuracion: config_huelva_reformas.json
echo Sectores: reformas, electricista, fontanero, cerrajero, carpintero
echo Zonas: Huelva capital + 8 pueblos
echo.
echo Esto consume cuota de tu API de Google Places.
echo Al terminar generara un CSV: reformas_huelva_provincia_sin_web_FECHA.csv
echo.
echo Presiona cualquier tecla para empezar la busqueda...
pause > nul

echo.
echo Buscando negocios sin web...
echo.

C:\Users\mario\AppData\Local\Python\bin\python.exe ..\scripts\scraping-script-v2.py config_huelva_reformas.json

echo.
echo ========================================
echo   BUSQUEDA COMPLETADA
echo ========================================
echo.
echo SIGUIENTE PASO:
echo 1. Mira el nombre del CSV que se acaba de crear (arriba).
echo 2. Abre whatsapp_config_huelva_reformas.json
echo 3. Pega ese nombre en el campo "archivo_csv"
echo 4. Ejecuta enviar_whatsapp_huelva_reformas.bat
echo.
pause
