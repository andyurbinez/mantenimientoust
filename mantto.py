import psutil
import platform
import os
import socket
from fpdf import FPDF
from datetime import datetime

# Identidad de Marca
MARCA = "URBIÑEZ SERVICIOS TECNOLOGICOS"
SISTEMA = platform.system()

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, MARCA, 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Soporte Tecnico e Infraestructura - Milan, IT', 0, 1, 'C')
        self.ln(10)

def obtener_datos_completos():
    # Ajuste de ruta para espacio REAL (Android vs Windows)
    ruta_disco = '/sdcard' if os.path.exists('/sdcard') else '/'
    disco = psutil.disk_usage(ruta_disco)
    ram = psutil.virtual_memory()
    
    return {
        "so": f"{SISTEMA} {platform.release()}",
        "procesador": platform.processor() or "Procesador Multinucleo ARM/x86",
        "maquina": platform.machine(),
        "ram_total": f"{ram.total / (1024**3):.2f} GB",
        "ram_uso_pct": ram.percent,
        "disco_capacidad": f"{disco.total / (1024**3):.2f} GB",
        "disco_libre": f"{disco.free / (1024**3):.2f} GB",
        "disco_uso_pct": disco.percent
    }

def auditoria_red():
    # Concepto Cisco: Verificacion de puertos criticos
    puertos = [21, 22, 80, 443, 445, 3389]
    abiertos = []
    for p in puertos:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.01)
            if s.connect_ex(('127.0.0.1', p)) == 0: abiertos.append(p)
    return "ESTADO SEGURO" if not abiertos else f"ALERTA: Puertos {abiertos} activos"

def generar_reporte():
    info = obtener_datos_completos()
    red = auditoria_red()
    
    # Visual en Pantalla (Termux)
    os.system('cls' if SISTEMA == 'Windows' else 'clear')
    print("="*50)
    print(f" {MARCA} ".center(50, "="))
    print("="*50)
    print(f"\n[+] SISTEMA:      {info['so']}")
    print(f"[+] PROCESADOR:   {info['procesador']} ({info['maquina']})")
    print(f"[+] RAM TOTAL:    {info['ram_total']} (Uso: {info['ram_uso_pct']}%)")
    print(f"[+] DISCO TOTAL:  {info['disco_capacidad']}")
    print(f"[+] DISCO LIBRE:  {info['disco_libre']} ({100 - info['disco_uso_pct']:.1f}% disponible)")
    print(f"[+] SEGURIDAD:    {red}")
    print("\n" + "="*50)

    # Generar PDF Profesional
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 10, f"FECHA DEL REPORTE: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True, fill=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "1. ESPECIFICACIONES DE HARDWARE", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"- Procesador: {info['procesador']}", ln=True)
    pdf.cell(0, 8, f"- Arquitectura: {info['maquina']}", ln=True)
    pdf.cell(0, 8, f"- Memoria RAM: {info['ram_total']} (Carga: {info['ram_uso_pct']}%)", ln=True)
    
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "2. ALMACENAMIENTO REAL", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"- Capacidad Total: {info['disco_capacidad']}", ln=True)
    pdf.cell(0, 8, f"- Espacio Disponible: {info['disco_libre']}", ln=True)
    
    # Barra visual de disco en PDF
    pdf.ln(5)
    pdf.set_draw_color(50, 50, 50)
    pdf.cell(info['disco_uso_pct'], 10, f"USO: {info['disco_uso_pct']}%", fill=True, border=1)
    
    # Guardar en Descargas automáticamente
    ruta_final = "/sdcard/Download/Reporte_Urbinez.pdf" if SISTEMA != "Windows" else os.path.join(os.path.expanduser('~'), 'Downloads', 'Reporte_Urbinez.pdf')
    
    try:
        pdf.output(ruta_final)
        print(f"[OK] Reporte guardado en: {ruta_final}")
    except:
        pdf.output("Reporte_Urbinez.pdf")
        print("[!] Guardado en carpeta local (Verifica permisos de almacenamiento)")

if __name__ == "__main__":
    generar_reporte()
