#!/usr/bin/env python3
"""
Script de prueba para enviar un mensaje WhatsApp a tu propio teléfono.
No afecta límites diarios ni marca el CSV.
"""

import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# === CONFIGURACIÓN DE PRUEBA ===
TU_TELEFONO = "696038421"  # ← Pon tus 9 dígitos aquí (sin el 34, se añade solo)
MODO = "web"  # "web" (automático) o "wame" (manual)
# =================================

MENSAJE = """¡Hola Mario! 👋

Soy Mario de ayanip.es y echando un ojo en Google, vi que tu negocio no aparece con página web.

💡 Hoy el 80% de clientes te buscan en el móvil antes de ir. Sin web, esos clientes se van a la competencia.

✅ Página web profesional y rápida

🚀 Aparecer en Google cuando te buscan

💎 Mejorar procesos (citas, reservas, atención)

📊 Aumentar clientes recurrentes

👉 Mira algunos trabajos aquí: https://ayanip.es

Sin compromiso — te cuento en 2 minutos cómo lo haríamos.

¿Te parece bien que hablemos?"""

def test_web(phone, mensaje):
    try:
        import pywhatkit
        import pyautogui
    except ImportError:
        print("❌ Instala dependencias: python -m pip install pywhatkit pyautogui")
        return

    print(f"🤖 Enviando a +{phone} vía WhatsApp Web...")
    print(f"⏳ Espera 15 segundos (NO toques el ratón)...")
    try:
        pywhatkit.sendwhatmsg_instantly(
            phone_no=f"+{phone}",
            message=mensaje,
            wait_time=15,
            tab_close=False
        )
        time.sleep(2)
        pyautogui.press('enter')
        print("✅ Mensaje enviado. Revisa tu otro teléfono.")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_wame(phone, mensaje):
    from urllib.parse import quote
    import webbrowser
    url = f"https://wa.me/{phone}?text={quote(mensaje)}"
    print(f"📲 Abriendo: {url}")
    webbrowser.open(url)
    print("👉 Pulsa 'Enviar' en WhatsApp Web para probar.")

def main():
    phone = TU_TELEFONO
    if phone.endswith("X"):
        print("⚠️  Teléfono incompleto. Edita el script y pon tus 9 dígitos en TU_TELEFONO")
        return
    if not phone.startswith("34"):
        phone = "34" + phone

    print("=" * 50)
    print("🧪 TEST WhatsApp — Mensaje de prueba")
    print("=" * 50)
    print(f"📞 Destino: +{phone}")
    print(f"🔧 Modo: {MODO}")
    print()

    print("📝 Mensaje:")
    print("─" * 50)
    print(MENSAJE)
    print("─" * 50)

    confirmar = input(f"\n¿Enviar prueba a +{phone}? [s/N]: ").strip().lower()
    if confirmar not in ('s', 'si', 'sí', 'y', 'yes'):
        print("⛔ Cancelado.")
        return

    if MODO == "web":
        test_web(phone, MENSAJE)
    else:
        test_wame(phone, MENSAJE)

if __name__ == "__main__":
    main()