@echo off
echo =====================================================
echo   ENVIANDO WHATSAPP A BARES/RESTAURANTES - CIUDAD REAL
echo =====================================================
echo.
echo Configuracion: whatsapp_config_bares_restaurantes.json
echo.
echo ========================================
echo   IMPORTANTE - LEER ANTES DE EJECUTAR
echo ========================================
echo.
echo 1. Este script enviara mensajes a bares y restaurantes sin web
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

C:\Users\mario\AppData\Local\Python\bin\python.exe ..\scripts\whatsapp_sender.py whatsapp_config_bares_restaurantes.json

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
echo.
echo Revisa el log: envios_whatsapp_bares_restaurantes.log
echo.
pause
