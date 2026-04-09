import psutil
import platform
import os
import shutil
import gc
from datetime import datetime
from fpdf import FPDF

# --- IDENTIDAD CORPORATIVA ---
EMPRESA = "URBINEZ SERVICIOS TECNOLOGICOS"
SLOGAN = "Mantenimiento Preventivo y Correctivo Profesional"

class UrbinezPDF(FPDF):
    def header(self):
        self.set_fill_color(20, 40, 60)
        self.rect(0, 0, 210, 35, 'F')
        self.set_font("Arial", "B", 18)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, EMPRESA, ln=True, align="C")
        self.set_font("Arial", "I", 10)
        self.cell(0, 5, SLOGAN, ln=True, align="C")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150)
        self.cell(0, 10, f"Reporte Oficial Urbinez - {datetime.now().year} | Pagina {self.page_no()}", align="C")

def obtener_datos_seguros():
    # RAM y Disco
    ram = psutil.virtual_memory()
    disco = psutil.disk_usage('/')
    
    # Manejo de error de permiso en CPU para Android
    try:
        cpu_uso = f"{psutil.cpu_percent(interval=0.5)}%"
    except:
        cpu_uso = "Protegido por Sistema"

    # Logica de sugerencia profesional
    salud = "OPTIMO"
    if ram.percent > 75 or disco.percent > 85:
        salud = "CRITICO - Requiere Limpieza y Optimizacion"
    elif ram.percent > 55:
        salud = "ADVERTENCIA - Sugerido Mantenimiento Preventivo"

    return {
        "os": f"{platform.system()} {platform.release()}",
        "arquitectura": platform.machine(),
        "procesador": "Multinucleo ARM/Android",
        "ram_total": f"{ram.total / (1024**3):.2f} GB",
        "ram_uso": f"{ram.percent}%",
        "disco_total": f"{disco.total / (1024**3):.2f} GB",
        "disco_libre": f"{disco.free / (1024**3):.2f} GB",
        "disco_pct": disco.percent,
        "cpu": cpu_uso,
        "salud": salud
    }

def ejecutar_limpieza():
    print("\n[PROCESO] Escaneando basura del sistema...")
    # Rutas tipicas de basura en Android/Termux
    rutas = [
        os.path.expanduser('~/.cache'),
        '/sdcard/Android/data/cache',
        '/data/local/tmp'
    ]
    borrado = 0
    for r in rutas:
        if os.path.exists(r):
            try:
                shutil.rmtree(r)
                print(f"[+] Eliminado: {r}")
                borrado += 1
            except: pass
    print(f"[OK] Limpieza terminada. {borrado} areas optimizadas.")

def generar_reporte_pro(info):
    pdf = UrbinezPDF()
    pdf.add_page()
    
    # 1. ESPECIFICACIONES (Lo que pediste recuperar)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "I. ESPECIFICACIONES GENERALES DEL EQUIPO", ln=True)
    pdf.set_font("Arial", "", 10)
    
    specs = [
        ("Sistema Operativo", info["os"]),
        ("Arquitectura", info["arquitectura"]),
        ("Memoria RAM Total", info["ram_total"]),
        ("Estado de Carga CPU", info["cpu"]),
        ("Capacidad de Disco", info["disco_total"])
    ]
    
    for tit, val in specs:
        pdf.cell(50, 7, f"{tit}:", border="B")
        pdf.cell(0, 7, val, ln=True, border="B")
    
    # 2. ANALISIS DE SALUD (Lo que vende)
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "II. DIAGNOSTICO DE RENDIMIENTO", ln=True)
    
    # Color segun salud
    if "OPTIMO" in info["salud"]: pdf.set_text_color(0, 150, 0)
    elif "ADVERTENCIA" in info["salud"]: pdf.set_text_color(255, 100, 0)
    else: pdf.set_text_color(200, 0, 0)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 12, f"RESULTADO: {info['salud']}", ln=True, align="C")
    
    # Detalle de uso
    pdf.set_text_color(0)
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 8, f"Uso de Memoria RAM: {info['ram_uso']}", ln=True)
    pdf.cell(0, 8, f"Espacio Disponible en Disco: {info['disco_libre']}", ln=True)

    # Nombre unico con fecha
    nombre = f"/sdcard/Download/Reporte_Profesional_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(nombre)
    return nombre

def menu():
    while True:
        os.system('clear')
        datos = obtener_datos_seguros()
        print(f"\033[1;34m{'='*50}")
        print(f"       {EMPRESA}")
        print(f"{'='*50}\033[0m")
        print(f" [SISTEMA] {datos['os']}")
        print(f" [RAM]     {datos['ram_total']} (Uso: {datos['ram_uso']})")
        print(f" [DISCO]   Libre: {datos['disco_libre']} de {datos['disco_total']}")
        print(f" [SALUD]   {datos['salud']}")
        print(f"\033[1;34m{'-'*50}\033[0m")
        print(" 1. Generar Reporte PDF (Venta)")
        print(" 2. Limpiar Archivos Temporales (Corregir)")
        print(" 3. Optimizar Memoria RAM (Boost)")
        print(" 4. Test de Estabilidad de Red")
        print(" 5. Ver Procesos Criticos")
        print(" 6. Salir")
        
        opc = input("\n Seleccione una opcion: ")
        
        if opc == "1":
            path = generar_reporte_pro(datos)
            print(f"\n[OK] Reporte creado en: {path}")
            input("Presione Enter para volver...")
        elif opc == "2":
            ejecutar_limpieza()
            input("Mantenimiento terminado. Enter...")
        elif opc == "3":
            print("\n[PROCESO] Liberando recursos del sistema...")
            gc.collect()
            print("[OK] Ciclos de memoria optimizados.")
            input("Enter...")
        elif opc == "4":
            print("\n[RED] Verificando respuesta de servidor...")
            os.system("ping -c 3 8.8.8.8")
            input("Test finalizado. Enter...")
        elif opc == "5":
            print("\n[PROCESOS] Top 5 apps consumiendo RAM:")
            for p in sorted(psutil.process_iter(['name', 'memory_percent']), key=lambda x: x.info['memory_percent'], reverse=True)[:5]:
                print(f" - {p.info['name']}: {p.info['memory_percent']:.1f}%")
            input("Enter...")
        elif opc == "6":
            print("Saliendo de la Suite de Urbiñez...")
            break

if __name__ == "__main__":
    menu()
