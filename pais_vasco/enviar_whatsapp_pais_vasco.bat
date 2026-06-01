@echo off
echo =====================================================
echo   ENVIANDO WHATSAPP A RESTAURANTES - PAIS VASCO
echo =====================================================
echo.
echo Configuracion: whatsapp_config_pais_vasco.json
echo Archivo: restaurantes_pais_vasco_sin_web_20260504_120205.csv
echo Total restaurantes: 34
echo.
echo ========================================
echo   IMPORTANTE - LEER ANTES DE EJECUTAR
echo ========================================
echo.
echo 1. Este script enviara mensajes a restaurantes sin web
echo 2. Maximo 20 mensajes por ejecucion
echo 3. Pausa de 10 minutos cada 5 mensajes
echo 4. Delay aleatorio de 60-120 segundos entre mensajes
echo 5. Solo se enviara a numeros moviles (6xx, 7xx)
echo.
echo ZONAS INCLUIDAS:
echo - Bilbao (Bizkaia)
echo - San Sebastian (Gipuzkoa)
echo - Vitoria-Gasteiz (Araba)
echo.
echo ========================================
echo.
echo Presiona cualquier tecla para continuar...
pause > nul

echo.
echo Iniciando envio de mensajes...
echo.

C:\Users\mario\AppData\Local\Python\bin\python.exe ..\scripts\whatsapp_sender.py whatsapp_config_pais_vasco.json

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
echo.
echo Revisa el log: envios_whatsapp_pais_vasco.log
echo.
pause