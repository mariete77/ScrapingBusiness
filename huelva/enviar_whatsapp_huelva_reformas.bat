@echo off
echo =====================================================
echo   ENVIANDO WHATSAPP A REFORMAS Y OFICIOS - PROVINCIA DE HUELVA
echo =====================================================
echo.
echo Configuracion: whatsapp_config_huelva_reformas.json
echo.
echo ========================================
echo   IMPORTANTE - LEER ANTES DE EJECUTAR
echo ========================================
echo.
echo 1. Antes ejecuta buscar_reformas_huelva.bat y pega el CSV en el config
echo 2. Este script enviara mensajes a reformas/oficios sin web
echo 3. Maximo 20 mensajes por ejecucion (40 al dia)
echo 4. Pausa de 10 minutos cada 5 mensajes
echo 5. Delay aleatorio de 60-120 segundos entre mensajes
echo 6. Solo se enviara a numeros moviles (6xx, 7xx)
echo 7. Ten WhatsApp Web abierto y con sesion iniciada
echo.
echo ========================================
echo.
echo Presiona cualquier tecla para continuar...
pause > nul

echo.
echo Iniciando envio de mensajes...
echo.

C:\Users\mario\AppData\Local\Python\bin\python.exe ..\scripts\whatsapp_sender.py whatsapp_config_huelva_reformas.json

echo.
echo ========================================
echo   PROCESO COMPLETADO
echo ========================================
echo.
echo Revisa el log: envios_whatsapp_huelva_reformas.log
echo.
echo Sincronizando con el repositorio Git...
git -C "%~dp0.." add -A
git -C "%~dp0.." commit -m "Actualizacion automatica: %~n0" >nul 2>&1
git -C "%~dp0.." push
echo.
pause
