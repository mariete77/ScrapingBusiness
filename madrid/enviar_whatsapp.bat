@echo off
REM Script para ejecutar el sender de WhatsApp
REM Uso: enviar_whatsapp.bat [opcion]
REM Opciones: --yes (auto-confirmar)

C:\Users\mario\AppData\Local\Python\bin\python.exe ..\scripts\whatsapp_sender.py whatsapp_config.json %*

echo.
echo Sincronizando con el repositorio Git...
git -C "%~dp0.." add -A
git -C "%~dp0.." commit -m "Actualizacion automatica: %~n0" >nul 2>&1
git -C "%~dp0.." push