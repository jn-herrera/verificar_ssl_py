import socket
import ssl
from datetime import datetime, timezone

# Lista de dominios a verificar
dominios = [
    "itop.marandu.com.ar",
    "cn.marandu.com.ar",
    "ipam.marandu.com.ar",
    "eros.geogridmaps.com.br",
    "unifi.marandu.com.ar",
    "noc.h.marandu.com.ar",
    "portal.masmisiones.com.ar",
    "marandu.com.ar",
    "grafana.marandu.com.ar",
    "us-e1-s14-l6naypky2x.cloud.cambiumnetworks.com",
    

]

def obtener_fecha_vencimiento_ssl(host, port=443):
    contexto = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=5) as sock:
        with contexto.wrap_socket(sock, server_hostname=host) as ssock:
            cert = ssock.getpeercert()
            fecha_str = cert['notAfter']
            fecha_vencimiento = datetime.strptime(fecha_str, "%b %d %H:%M:%S %Y %Z")
            # Convertimos a timezone-aware en UTC
            return fecha_vencimiento.replace(tzinfo=timezone.utc)

print("🔐 Verificación de certificados SSL:\n")

for dominio in dominios:
    try:
        vencimiento = obtener_fecha_vencimiento_ssl(dominio)
        ahora_utc = datetime.now(timezone.utc)
        dias_restantes = (vencimiento - ahora_utc).days
        print(f"{dominio} => Expira el {vencimiento} ({dias_restantes} días restantes)")
    except Exception as e:
        print(f"{dominio} => Error: {e}")
