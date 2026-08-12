@echo off
echo =====================================================
echo   ENVIANDO WHATSAPP A ASESORIAS - PROVINCIA DE HUELVA
echo =====================================================
echo.
echo Configuracion: whatsapp_config_asesorias_huelva.json
echo CSV: negocios_sin_web_asesorias_huelva_provincia_20260802_201012.csv
echo.
echo ========================================
echo   IMPORTANTE - LEER ANTES DE EJECUTAR
echo ========================================
echo.
echo 1. Este script enviara mensajes a asesorias y gestorias sin web
echo 2. Maximo 10 mensajes por ejecucion (15 por dia)
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

C:\Users\mario\AppData\Local\Python\bin\python.exe ..\scripts\whatsapp_sender.py whatsapp_config_asesorias_huelva.json

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
echo.
echo Revisa el log: envios_whatsapp_asesorias_huelva.log
echo.
echo Sincronizando con el repositorio Git...
git -C "%~dp0.." add -A
git -C "%~dp0.." commit -m "Actualizacion automatica: %~n0" >nul 2>&1
git -C "%~dp0.." push
echo.
pause
