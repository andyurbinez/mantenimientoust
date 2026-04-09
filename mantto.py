import psutil
import platform
import os
from datetime import datetime
from fpdf import FPDF

def obtener_info_sistema():
    # Análisis de Salud (La función que "vende")
    ram = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    
    # Lógica de salud
    if ram.percent > 85 or disco.percent > 90:
        estado_salud = "CRITICO - Requiere Intervencion Inmediata"
    elif ram.percent > 60 or disco.percent > 70:
        estado_salud = "ADVERTENCIA - Se recomienda Mantenimiento"
    else:
        estado_salud = "OPTIMO - Sistema Saludable"

    info = {
        "sistema": platform.system(),
        "version": platform.release(),
        "maquina": platform.machine(),
        "ram_total": f"{ram.total / (1024**3):.2f} GB",
        "ram_uso_pct": f"{ram.percent}%",
        "disco_total": f"{disco.total / (1024**3):.2f} GB",
        "disco_libre": f"{disco.free / (1024**3):.2f} GB",
        "disco_uso_pct": disco.percent,
        "salud": estado_salud
    }
    return info

def generar_reporte():
    info = obtener_info_sistema()
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado Profesional
    pdf.set_font("Arial", "B", 16)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 10, "URBINEZ SERVICIOS TECNOLOGICOS", ln=True, align="C")
    pdf.set_font("Arial", "I", 10)
    pdf.cell(0, 10, f"Reporte Generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)

    # SECCIÓN DE SALUD (Lo que impresiona al cliente)
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "ESTADO GENERAL DE SALUD DEL EQUIPO:", ln=True, fill=True)
    pdf.set_font("Arial", "B", 14)
    
    # Color según estado
    if "OPTIMO" in info["salud"]:
        pdf.set_text_color(0, 128, 0) # Verde
    elif "ADVERTENCIA" in info["salud"]:
        pdf.set_text_color(255, 140, 0) # Naranja
    else:
        pdf.set_text_color(220, 20, 60) # Rojo
        
    pdf.cell(0, 12, f" >> {info['salud']}", ln=True, align="C")
    pdf.ln(5)
    
    # Detalle Técnico
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "DETALLES TECNICOS:", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"[+] Sistema: {info['sistema']} {info['version']}", ln=True)
    pdf.cell(0, 8, f"[+] RAM Total: {info['ram_total']} (Uso: {info['ram_uso_pct']})", ln=True)
    pdf.cell(0, 8, f"[+] Capacidad Disco: {info['disco_total']}", ln=True)
    pdf.cell(0, 8, f"[+] Espacio Libre: {info['disco_libre']} ({100-info['disco_uso_pct']}% disponible)", ln=True)
    
    # Barra visual de disco
    pdf.ln(5)
    pdf.set_draw_color(50, 50, 50)
    pdf.cell(info['disco_uso_pct'], 10, f"USO DISCO: {info['disco_uso_pct']}%", border=1, fill=True)

    # Guardar con fecha y hora para evitar sobrescribir
    ahora = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_final = f"/sdcard/Download/Reporte_Urbinez_{ahora}.pdf"

    try:
        pdf.output(ruta_final)
        print("\n" + "="*40)
        print("   URBIÑEZ SERVICIOS TECNOLOGICOS")
        print("="*40)
        print(f"[+] SALUD: {info['salud']}")
        print(f"[OK] Reporte profesional guardado en Descargas.")
        print("="*40)
    except Exception as e:
        pdf.output(f"Reporte_{ahora}.pdf")
        print(f"[!] Error al guardar en Descargas, guardado en carpeta local.")

if __name__ == "__main__":
    generar_reporte()
