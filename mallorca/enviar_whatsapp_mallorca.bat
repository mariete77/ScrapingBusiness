@echo off
echo =====================================================
echo   ENVIANDO WHATSAPP A RESTAURANTES - ISLA DE MALLORCA
echo =====================================================
echo.
echo Configuracion: whatsapp_config_mallorca.json
echo CSV: se usara el mas reciente (restaurantes_mallorca_provincia_sin_web_*.csv)
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
echo ========================================
echo.
echo Presiona cualquier tecla para continuar...
pause > nul

echo.
echo Iniciando envio de mensajes...
echo.

C:\Users\mario\AppData\Local\Python\bin\python.exe ..\scripts\whatsapp_sender.py whatsapp_config_mallorca.json

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
echo.
echo Revisa el log: envios_whatsapp_mallorca.log
echo.
echo Sincronizando con el repositorio Git...
git -C "%~dp0.." add -A
git -C "%~dp0.." commit -m "Actualizacion automatica: %~n0" >nul 2>&1
git -C "%~dp0.." push
echo.
pause
