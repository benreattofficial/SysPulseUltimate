import os
import sys
import ctypes
import threading
import time
import subprocess
import platform
import json
import urllib.request
import customtkinter as ctk
import psutil
from PIL import Image
import winsound

# Tema Ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# --- TEK .EXE İÇİN DOSYA GÖMME VE YOL AYARI ---
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LANG_FILE = os.path.join(BASE_DIR, "languages.json")

default_translations = {
    "Türkçe": {
        "title": "SysPulse Ultimate - Profesyonel Donanım & Bakım Merkezi",
        "menu": ["Genel Bakış & Ağ", "Ekran Kartı & Logo", "Kaynak Tüketenler", "Sistem Bilgileri", "Sistem Bakım", "Windows Araçları", "İnternet Hız Testi", "Canlı Günlükler"],
        "export_btn": "Rapor Al (.txt)",
        "widget_btn": "Mini Widget",
        "admin_btn_off": "🔑 Yönetici İzni Ver",
        "admin_btn_on": "🛡️ Yönetici Modu Aktif",
        "cpu_label": "CPU Kullanımı",
        "ram_label": "RAM Kullanımı",
        "disk_label": "Disk Kullanımı (C:)",
        "net_down": "Anlık İndirme",
        "net_up": "Anlık Yükleme",
        "gpu_header": "Algılanan Grafik Birimleri (GPU / iGPU)",
        "gpu_box_title": "Sistemdeki Grafik Birimleri:",
        "gpu_status": "Durum: Aktif ve Kararlı",
        "cpu_cores": "CPU Çekirdek Sayısı",
        "proc_header": "--- EN ÇOK KAYNAK TÜKETEN UYGULAMALAR ---",
        "log_init": "SysPulse Ultimate Canlı Sistem Akışı Başlatıldı...\n",
        "sys_specs_title": "💻 Detaylı Sistem ve İşletim Sistemi Bilgileri",
        "tools_title": "🛠️ Hızlı Windows Yönetim Araçları",
        "maint_title": "🧹 Sistem Bakım ve Optimizasyon Araçları",
        "maint_warn": "⚠️ Bu araçları kullanmak için sağ üstten 'Yönetici İzni Ver'melisiniz.",
        "btn_clean_temp": "🗑️ Geçici Dosyaları Temizle (Temp)",
        "btn_flush_dns": "🌐 DNS Önbelleğini Sıfırla (FlushDNS)",
        "btn_perf_mode": "⚡ Nihai Performans Modunu Aktif Et",
        "btn_sfc": "🛠️ Bozuk Dosyaları Onar (SFC /scannow)",
        "maint_log_ready": "Bakım günlüğü hazır...\n",
        "maint_clean_start": "Geçici dosyalar temizleniyor...\n",
        "maint_clean_success": "✅ Temp temizlendi. Silinen dosya: {count}\n",
        "maint_dns_start": "DNS önbelleği sıfırlanıyor (ipconfig /flushdns)...\n",
        "maint_dns_success": "✅ DNS önbelleği başarıyla sıfırlandı!\n",
        "maint_perf_start": "Nihai Performans Modu etkinleştiriliyor...\n",
        "maint_perf_success": "✅ Nihai Performans planı eklendi/etkinleştirildi!\n",
        "maint_sfc_start": "Sistem dosyaları taranıyor (sfc /scannow - Uzun sürebilir)...\n",
        "maint_sfc_success": "✅ SFC taraması tamamlandı!\n",
        "maint_error": "❌ Hata: {err}\n",
        "specs_os": "İşletim Sistemi (OS)",
        "specs_pc": "Bilgisayar Adı",
        "specs_arch": "İşlemci Mimarisi",
        "specs_ram": "Toplam Fiziksel RAM",
        "specs_py": "Python Sürümü",
        "specs_admin": "Yönetici Yetkisi",
        "specs_yes": "Evet (Admin)",
        "specs_no": "Hayır (Normal Kullanıcı)",
        "btn_taskmgr": "📊 Görev Yöneticisini Aç",
        "btn_devmgmt": "⚙️ Aygıt Yöneticisini Aç",
        "btn_control": "🎛️ Denetim Masasını Aç",
        "btn_dxdiag": "🎮 Ekran/DirectX Tanılama (DxDiag)",
        "st_start_btn": "🚀 Hız Testini Başlat",
        "st_status": "Test durumu: Hazır. Başlatmak için butona tıklayın.",
        "st_running": "🔄 İnternet hız testi yapılıyor, lütfen bekleyin...",
        "st_result": "📥 İndirme: {down:.2f} Mbps  |  📤 Yükleme: {up:.2f} Mbps  |  ⚡ Ping: {ping:.0f} ms",
        "st_success": "✅ Hız testi başarıyla tamamlandı!",
        "st_error": "❌ Hız testi sırasında hata oluştu!",
        "server_text": "Sunucu",
        "report_msg": "Rapor başarıyla kaydedildi!"
    },
    "English": {
        "title": "SysPulse Ultimate - Professional Hardware & Maintenance Center",
        "menu": ["Overview & Network", "GPU & Badge", "Top Processes", "System Specs", "Maintenance", "Windows Tools", "Speed Test", "Live Logs"],
        "export_btn": "Export Report",
        "widget_btn": "Mini Widget",
        "admin_btn_off": "🔑 Request Admin",
        "admin_btn_on": "🛡️ Admin Mode Active",
        "cpu_label": "CPU Usage",
        "ram_label": "RAM Usage",
        "disk_label": "Disk Usage (C:)",
        "net_down": "Live Download",
        "net_up": "Live Upload",
        "gpu_header": "Detected Graphics Units (GPU / iGPU)",
        "gpu_box_title": "Graphics Units in System:",
        "gpu_status": "Status: Active and Stable",
        "cpu_cores": "CPU Cores Count",
        "proc_header": "--- TOP RESOURCE CONSUMING APPS ---",
        "log_init": "SysPulse Ultimate Live System Stream Started...\n",
        "sys_specs_title": "💻 Detailed System and OS Information",
        "tools_title": "🛠️ Quick Windows Management Tools",
        "maint_title": "🧹 System Maintenance & Optimization Tools",
        "maint_warn": "⚠️ You must grant 'Admin Permission' from top right to use these tools.",
        "btn_clean_temp": "🗑️ Clear Temp Files",
        "btn_flush_dns": "🌐 Flush DNS Cache",
        "btn_perf_mode": "⚡ Enable Ultimate Performance Mode",
        "btn_sfc": "🛠️ Repair System Files (SFC /scannow)",
        "maint_log_ready": "Maintenance log ready...\n",
        "maint_clean_start": "Cleaning temporary files...\n",
        "maint_clean_success": "✅ Temp cleaned. Deleted files: {count}\n",
        "maint_dns_start": "Flushing DNS cache (ipconfig /flushdns)...\n",
        "maint_dns_success": "✅ DNS cache successfully flushed!\n",
        "maint_perf_start": "Enabling Ultimate Performance Mode...\n",
        "maint_perf_success": "✅ Ultimate Performance plan added/enabled!\n",
        "maint_sfc_start": "Scanning system files (sfc /scannow - May take a while)...\n",
        "maint_sfc_success": "✅ SFC scan completed!\n",
        "maint_error": "❌ Error: {err}\n",
        "specs_os": "Operating System (OS)",
        "specs_pc": "Computer Name",
        "specs_arch": "Processor Architecture",
        "specs_ram": "Total Physical RAM",
        "specs_py": "Python Version",
        "specs_admin": "Admin Privilege",
        "specs_yes": "Yes (Admin)",
        "specs_no": "No (Normal User)",
        "btn_taskmgr": "📊 Open Task Manager",
        "btn_devmgmt": "⚙️ Open Device Manager",
        "btn_control": "🎛️ Open Control Panel",
        "btn_dxdiag": "🎮 DirectX Diagnostic (DxDiag)",
        "st_start_btn": "🚀 Start Speed Test",
        "st_status": "Status: Ready. Click the button to start.",
        "st_running": "🔄 Running speed test, please wait...",
        "st_result": "📥 Download: {down:.2f} Mbps  |  📤 Upload: {up:.2f} Mbps  |  ⚡ Ping: {ping:.0f} ms",
        "st_success": "✅ Speed test completed successfully!",
        "st_error": "❌ Error occurred during speed test!",
        "server_text": "Server",
        "report_msg": "Report successfully saved!"
    },
    "Deutsch": {
        "title": "SysPulse Ultimate - Professionelles Hardware- & Wartungszentrum",
        "menu": ["Übersicht & Netzwerk", "GPU & Logo", "Top-Prozesse", "Systeminfo", "Wartung", "Windows-Tools", "Geschwindigkeit", "Live-Logs"],
        "export_btn": "Bericht exportieren",
        "widget_btn": "Mini-Widget",
        "cpu_label": "CPU-Auslastung",
        "ram_label": "RAM-Auslastung",
        "disk_label": "Speicher (C:)",
        "net_down": "Live-Download",
        "net_up": "Live-Upload",
        "admin_btn_off": "🔑 Admin anfordern",
        "admin_btn_on": "🛡️ Admin-Modus Aktiv",
        "gpu_header": "Erkannte Grafikeinheiten (GPU / iGPU)",
        "gpu_box_title": "Grafikeinheiten im System:",
        "gpu_status": "Status: Aktiv und Stabil",
        "cpu_cores": "CPU-Kerne",
        "proc_header": "--- TOP-RESSOURCENVERBRAUCHER ---",
        "log_init": "SysPulse Ultimate Live-System-Stream gestartet...\n",
        "sys_specs_title": "💻 Detaillierte System- und Betriebssysteminformationen",
        "tools_title": "🛠️ Schnelle Windows-Management-Tools",
        "maint_title": "🧹 Systemwartungs- und Optimierungstools",
        "maint_warn": "⚠️ Sie müssen Administratorrechte erteilen, um diese Tools zu nutzen.",
        "btn_clean_temp": "🗑️ Temp-Dateien löschen",
        "btn_flush_dns": "🌐 DNS-Cache leeren",
        "btn_perf_mode": "⚡ Ultimative Leistung aktivieren",
        "btn_sfc": "🛠️ Systemdateien reparieren (SFC)",
        "maint_log_ready": "Wartungsprotokoll bereit...\n",
        "maint_clean_start": "Temporäre Dateien werden bereinigt...\n",
        "maint_clean_success": "✅ Temp bereinigt. Gelöschte Dateien: {count}\n",
        "maint_dns_start": "DNS-Cache wird geleert...\n",
        "maint_dns_success": "✅ DNS-Cache erfolgreich geleert!\n",
        "maint_perf_start": "Ultimativer Leistungsmodus wird aktiviert...\n",
        "maint_perf_success": "✅ Ultimativer Leistungsplan aktiviert!\n",
        "maint_sfc_start": "Systemdateien werden gescannt (kann dauern)...\n",
        "maint_sfc_success": "✅ SFC-Scan abgeschlossen!\n",
        "maint_error": "❌ Fehler: {err}\n",
        "specs_os": "Betriebssystem (OS)",
        "specs_pc": "Computername",
        "specs_arch": "Prozessorarchitektur",
        "specs_ram": "Gesamter physischer RAM",
        "specs_py": "Python-Version",
        "specs_admin": "Administratorrechte",
        "specs_yes": "Ja (Admin)",
        "specs_no": "Nein (Normaler Benutzer)",
        "btn_taskmgr": "📊 Task-Manager öffnen",
        "btn_devmgmt": "⚙️ Geräte-Manager öffnen",
        "btn_control": "🎛️ Systemsteuerung öffnen",
        "btn_dxdiag": "🎮 DirectX-Diagnose (DxDiag)",
        "st_start_btn": "🚀 Geschwindigkeitstest starten",
        "st_status": "Status: Bereit. Klicken Sie auf die Schaltfläche.",
        "st_running": "🔄 Geschwindigkeitstest läuft, bitte warten...",
        "st_result": "📥 Download: {down:.2f} Mbps  |  📤 Upload: {up:.2f} Mbps  |  ⚡ Ping: {ping:.0f} ms",
        "st_success": "✅ Geschwindigkeitstest erfolgreich abgeschlossen!",
        "st_error": "❌ Fehler beim Geschwindigkeitstest aufgetreten!",
        "server_text": "Server",
        "report_msg": "Bericht erfolgreich gespeichert!"
    },
    "Español": {
        "title": "SysPulse Ultimate - Centro Profesional de Hardware y Mantenimiento",
        "menu": ["Resumen y Red", "GPU y Insignia", "Procesos", "Especificaciones", "Mantenimiento", "Herramientas", "Prueba", "Registros"],
        "export_btn": "Exportar Informe",
        "widget_btn": "Mini Widget",
        "cpu_label": "Uso de CPU",
        "ram_label": "Uso de RAM",
        "disk_label": "Uso de Disco (C:)",
        "net_down": "Descarga en vivo",
        "net_up": "Carga en vivo",
        "admin_btn_off": "🔑 Solicitar Admin",
        "admin_btn_on": "🛡️ Modo Admin Activo",
        "gpu_header": "Unidades Gráficas Detectadas (GPU / iGPU)",
        "gpu_box_title": "Unidades gráficas en el sistema:",
        "gpu_status": "Estado: Activo y Stable",
        "cpu_cores": "Núcleos de CPU",
        "proc_header": "--- APLICACIONES QUE MÁS RECURSOS CONSUMEN ---",
        "log_init": "Transmisión en vivo SysPulse Ultimate iniciada...\n",
        "sys_specs_title": "💻 Información detallada del sistema y OS",
        "tools_title": "🛠️ Herramientas rápidas de gestión de Windows",
        "maint_title": "🧹 Herramientas de Mantenimiento y Optimización",
        "maint_warn": "⚠️ Debe otorgar permisos de administrador para usar estas herramientas.",
        "btn_clean_temp": "🗑️ Limpiar archivos temporales",
        "btn_flush_dns": "🌐 Restablecer DNS (FlushDNS)",
        "btn_perf_mode": "⚡ Activar Rendimiento Máximo",
        "btn_sfc": "🛠️ Reparar archivos del sistema (SFC)",
        "maint_log_ready": "Registro de mantenimiento listo...\n",
        "maint_clean_start": "Limpiando archivos temporales...\n",
        "maint_clean_success": "✅ Temp limpiado. Archivos eliminados: {count}\n",
        "maint_dns_start": "Restableciendo caché DNS...\n",
        "maint_dns_success": "✅ ¡Caché DNS restablecida con éxito!\n",
        "maint_perf_start": "Activando modo de Máximo Rendimiento...\n",
        "maint_perf_success": "✅ ¡Plan de Rendimiento Máximo activado!\n",
        "maint_sfc_start": "Analizando archivos del sistema (puede tardar)...\n",
        "maint_sfc_success": "✅ ¡Análisis SFC completado!\n",
        "maint_error": "❌ Error: {err}\n",
        "specs_os": "Sistema Operativo (OS)",
        "specs_pc": "Nombre del Equipo",
        "specs_arch": "Arquitectura del Procesador",
        "specs_ram": "RAM Física Total",
        "specs_py": "Versión de Python",
        "specs_admin": "Privilegios de Administrador",
        "specs_yes": "Sí (Admin)",
        "specs_no": "No (Usuario Normal)",
        "btn_taskmgr": "📊 Abrir Administrador de Tareas",
        "btn_devmgmt": "⚙️ Abrir Administrador de Dispositivos",
        "btn_control": "🎛️ Abrir Panel de Control",
        "btn_dxdiag": "🎮 Diagnóstico DirectX (DxDiag)",
        "st_start_btn": "🚀 Iniciar Prueba de Velocidad",
        "st_status": "Status: Listo. Haga clic en el botón para comenzar.",
        "st_running": "🔄 Ejecutando prueba de velocidad, espere...",
        "st_result": "📥 Descarga: {down:.2f} Mbps  |  📤 Carga: {up:.2f} Mbps  |  ⚡ Ping: {ping:.0f} ms",
        "st_success": "✅ ¡Prueba de velocidad completada con éxito!",
        "st_error": "❌ ¡Ocurrió un error durante la prueba de velocidad!",
        "server_text": "Servidor",
        "report_msg": "¡Informe guardado con éxito!"
    }
}

if os.path.exists(LANG_FILE):
    try:
        with open(LANG_FILE, "r", encoding="utf-8") as f:
            translations = json.load(f)
        if "Türkçe" in translations and "menu" not in translations["Türkçe"]:
            translations = default_translations
            with open(LANG_FILE, "w", encoding="utf-8") as f:
                json.dump(default_translations, f, ensure_ascii=False, indent=4)
    except:
        translations = default_translations
        with open(LANG_FILE, "w", encoding="utf-8") as f:
            json.dump(default_translations, f, ensure_ascii=False, indent=4)
else:
    translations = default_translations
    with open(LANG_FILE, "w", encoding="utf-8") as f:
        json.dump(default_translations, f, ensure_ascii=False, indent=4)


class SysPulseUltimate(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.current_lang = "Türkçe"
        self.is_admin_user = is_admin()

        self.title(translations[self.current_lang]["title"])
        self.geometry("850x620")
        self.resizable(False, False)

        icon_path = os.path.join(BASE_DIR, "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
            except:
                pass

        self.widget_window = None
        self.last_net = psutil.net_io_counters()
        self.last_time = time.time()

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.pack(fill="x", padx=20, pady=(10, 0))

        t = translations[self.current_lang]
        
        self.export_btn = ctk.CTkButton(self.top_frame, text=t["export_btn"], command=self.export_report, width=110)
        self.export_btn.pack(side="right")

        self.widget_btn = ctk.CTkButton(self.top_frame, fg_color="#2b8250", hover_color="#1f5e39", text=t["widget_btn"], command=self.toggle_widget, width=110)
        self.widget_btn.pack(side="right", padx=10)

        admin_btn_text = t["admin_btn_on"] if self.is_admin_user else t["admin_btn_off"]
        admin_btn_color = "#2b8250" if self.is_admin_user else "#b22222"
        admin_btn_state = "disabled" if self.is_admin_user else "normal"

        self.admin_btn = ctk.CTkButton(self.top_frame, fg_color=admin_btn_color, text=admin_btn_text, command=self.request_admin_privileges, width=150, state=admin_btn_state)
        self.admin_btn.pack(side="right", padx=10)

        self.lang_menu = ctk.CTkOptionMenu(self.top_frame, values=["Türkçe", "English", "Deutsch", "Español"])
        self.lang_menu.pack(side="left")
        self.lang_menu.set(self.current_lang)
        self.lang_menu.configure(command=self.change_language)

        self.warning_label = ctk.CTkLabel(self, text="", font=("Helvetica", 13, "bold"), text_color="#ff4d4d")
        self.warning_label.pack(pady=(5, 0))

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=10)

        self.sidebar_frame = ctk.CTkFrame(self.main_container, width=200, corner_radius=10)
        self.sidebar_frame.pack(side="left", fill="y", padx=(0, 10))

        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.frames = {}
        for name in ["Overview", "GPU", "Processes", "Specs", "Maintenance", "Tools", "SpeedTest", "Logs"]:
            frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.frames[name] = frame

        self.setup_overview_tab(self.frames["Overview"])
        self.setup_gpu_tab(self.frames["GPU"])
        self.setup_processes_tab(self.frames["Processes"])
        self.setup_specs_tab(self.frames["Specs"])
        self.setup_maintenance_tab(self.frames["Maintenance"])
        self.setup_tools_tab(self.frames["Tools"])
        self.setup_speedtest_tab(self.frames["SpeedTest"])
        self.setup_logs_tab(self.frames["Logs"])

        self.sidebar_buttons = {}
        menu_keys = ["Overview", "GPU", "Processes", "Specs", "Maintenance", "Tools", "SpeedTest", "Logs"]
        menu_titles = t["menu"]

        for key, title in zip(menu_keys, menu_titles):
            btn = ctk.CTkButton(self.sidebar_frame, text=title, fg_color="transparent", hover_color=("#3a3a3a", "#2a2a2a"),
                                anchor="w", command=lambda k=key: self.show_frame(k), height=38)
            btn.pack(fill="x", padx=10, pady=4)
            self.sidebar_buttons[key] = btn

        self.show_frame("Overview")
        self.update_stats()

    def show_frame(self, frame_key):
        for f in self.frames.values():
            f.pack_forget()
        self.frames[frame_key].pack(fill="both", expand=True)

    def request_admin_privileges(self):
        try:
            script_path = os.path.abspath(__file__)
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script_path}"', None, 1)
            sys.exit()
        except Exception as e:
            print(f"Yönetici izni alınamadı: {e}")

    def get_system_gpus(self):
        try:
            cmd = 'powershell "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
            gpus = [g.strip() for g in output.split('\r\n') if g.strip()]
            return gpus if gpus else ["Standard VGA Graphics"]
        except:
            return ["Dahili / Harici Grafik Birimi"]

    def load_brand_badge(self, gpu_name):
        upper_name = gpu_name.upper()
        if "NVIDIA" in upper_name:
            logo_filename = "nvidia.png"
        elif "AMD" in upper_name or "RADEON" in upper_name:
            logo_filename = "amd.png"
        elif "INTEL" in upper_name:
            logo_filename = "intel.png"
        else:
            logo_filename = "default.png"

        logo_path = os.path.join(BASE_DIR, logo_filename)
        if os.path.exists(logo_path):
            try:
                img = Image.open(logo_path)
                orig_w, orig_h = img.size
                target_h = 35
                target_w = int(orig_w * (target_h / orig_h))
                img = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                return ctk.CTkImage(light_image=img, dark_image=img, size=(target_w, target_h))
            except:
                return None
        else:
            return None

    def setup_overview_tab(self, parent):
        self.cpu_label = ctk.CTkLabel(parent, text="", font=("Helvetica", 13, "bold"))
        self.cpu_label.pack(anchor="w", padx=10, pady=(15, 2))
        self.cpu_bar = ctk.CTkProgressBar(parent, width=580)
        self.cpu_bar.pack(padx=10, pady=(0, 15))

        self.ram_label = ctk.CTkLabel(parent, text="", font=("Helvetica", 13, "bold"))
        self.ram_label.pack(anchor="w", padx=10, pady=(5, 2))
        self.ram_bar = ctk.CTkProgressBar(parent, width=580)
        self.ram_bar.pack(padx=10, pady=(0, 15))

        self.disk_label = ctk.CTkLabel(parent, text="", font=("Helvetica", 13, "bold"))
        self.disk_label.pack(anchor="w", padx=10, pady=(5, 2))
        self.disk_bar = ctk.CTkProgressBar(parent, width=580)
        self.disk_bar.pack(padx=10, pady=(0, 15))

        self.net_label = ctk.CTkLabel(parent, text="", font=("Helvetica", 13, "bold"), justify="left")
        self.net_label.pack(anchor="w", padx=10, pady=(10, 5))

    def setup_gpu_tab(self, parent):
        self.gpu_card = ctk.CTkFrame(parent, fg_color=("#2b2b2b", "#212121"), corner_radius=12)
        self.gpu_card.pack(fill="x", padx=10, pady=15)

        self.gpu_text_label = ctk.CTkLabel(self.gpu_card, text="", font=("Helvetica", 13, "bold"), justify="left")
        self.gpu_text_label.pack(side="left", padx=15, pady=15)

        self.gpu_logo_label = ctk.CTkLabel(self.gpu_card, text="")
        self.gpu_logo_label.pack(side="right", padx=15, pady=15)

        self.gpu_info_box = ctk.CTkTextbox(parent, width=580, height=260, font=("Consolas", 12))
        self.gpu_info_box.pack(padx=10, pady=5)

    def setup_processes_tab(self, parent):
        self.proc_textbox = ctk.CTkTextbox(parent, width=580, height=430, font=("Consolas", 12))
        self.proc_textbox.pack(padx=10, pady=15)

    def setup_specs_tab(self, parent):
        self.specs_title_label = ctk.CTkLabel(parent, text="", font=("Helvetica", 14, "bold"))
        self.specs_title_label.pack(anchor="w", padx=10, pady=(10, 10))

        self.specs_textbox = ctk.CTkTextbox(parent, width=580, height=380, font=("Consolas", 12))
        self.specs_textbox.pack(padx=10, pady=5)
        self.load_system_specs()

    def setup_maintenance_tab(self, parent):
        t = translations[self.current_lang]
        
        self.maint_title_label = ctk.CTkLabel(parent, text=t["maint_title"], font=("Helvetica", 14, "bold"))
        self.maint_title_label.pack(pady=(10, 5))

        self.maint_warn_label = ctk.CTkLabel(parent, text=t["maint_warn"], font=("Helvetica", 11), text_color="#ffcc00")
        self.maint_warn_label.pack(pady=(0, 10))

        btn_state = "normal" if self.is_admin_user else "disabled"

        self.btn_clean_temp = ctk.CTkButton(parent, text=t["btn_clean_temp"], command=self.action_clean_temp, height=38, width=400, fg_color="#1f538d", state=btn_state)
        self.btn_clean_temp.pack(pady=6)

        self.btn_flush_dns = ctk.CTkButton(parent, text=t["btn_flush_dns"], command=self.action_flush_dns, height=38, width=400, fg_color="#1f538d", state=btn_state)
        self.btn_flush_dns.pack(pady=6)

        self.btn_perf_mode = ctk.CTkButton(parent, text=t["btn_perf_mode"], command=self.action_perf_mode, height=38, width=400, fg_color="#1f538d", state=btn_state)
        self.btn_perf_mode.pack(pady=6)

        self.btn_sfc = ctk.CTkButton(parent, text=t["btn_sfc"], command=self.action_sfc_scan, height=38, width=400, fg_color="#b22222", hover_color="#8b0000", state=btn_state)
        self.btn_sfc.pack(pady=6)

        self.maint_result_box = ctk.CTkTextbox(parent, width=580, height=110, font=("Consolas", 11))
        self.maint_result_box.pack(padx=10, pady=10)
        self.maint_result_box.insert("0.0", t["maint_log_ready"])

    def setup_tools_tab(self, parent):
        t = translations[self.current_lang]
        self.tools_title_label = ctk.CTkLabel(parent, text=t["tools_title"], font=("Helvetica", 15, "bold"))
        self.tools_title_label.pack(pady=(25, 15))

        self.btn_taskmgr = ctk.CTkButton(parent, text=t["btn_taskmgr"], command=lambda: os.system("start taskmgr"), height=40, width=350, fg_color="#1f538d")
        self.btn_taskmgr.pack(pady=8)

        self.btn_devmgmt = ctk.CTkButton(parent, text=t["btn_devmgmt"], command=lambda: os.system("start devmgmt.msc"), height=40, width=350, fg_color="#1f538d")
        self.btn_devmgmt.pack(pady=8)

        self.btn_control = ctk.CTkButton(parent, text=t["btn_control"], command=lambda: os.system("start control"), height=40, width=350, fg_color="#1f538d")
        self.btn_control.pack(pady=8)

        self.btn_dxdiag = ctk.CTkButton(parent, text=t["btn_dxdiag"], command=lambda: os.system("start dxdiag"), height=40, width=350, fg_color="#2b8250")
        self.btn_dxdiag.pack(pady=8)

    def setup_speedtest_tab(self, parent):
        t = translations[self.current_lang]
        self.st_status_label = ctk.CTkLabel(parent, text=t["st_status"], font=("Helvetica", 13, "bold"), wraplength=500)
        self.st_status_label.pack(pady=(20, 10))

        self.st_button = ctk.CTkButton(parent, text=t["st_start_btn"], fg_color="#1f538d", hover_color="#14375e", font=("Helvetica", 13, "bold"), command=self.run_speed_test_thread, height=42, width=220)
        self.st_button.pack(pady=10)

        self.st_result_box = ctk.CTkTextbox(parent, width=580, height=180, font=("Consolas", 12))
        self.st_result_box.pack(padx=10, pady=15)
        self.st_result_box.insert("0.0", "...\n")

    def setup_logs_tab(self, parent):
        t = translations[self.current_lang]
        self.log_textbox = ctk.CTkTextbox(parent, width=580, height=430, font=("Consolas", 12))
        self.log_textbox.pack(padx=10, pady=15)
        self.log_textbox.insert("0.0", t["log_init"])

    def action_clean_temp(self):
        threading.Thread(target=self._run_clean_temp, daemon=True).start()

    def _run_clean_temp(self):
        t = translations[self.current_lang]
        self.maint_result_box.insert("end", t["maint_clean_start"])
        try:
            temp_dir = os.environ.get('TEMP', 'C:\\Windows\\Temp')
            deleted_files = 0
            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                        deleted_files += 1
                except:
                    pass
            self.maint_result_box.insert("end", t["maint_clean_success"].format(count=deleted_files))
        except Exception as e:
            self.maint_result_box.insert("end", t["maint_error"].format(err=str(e)))
        self.maint_result_box.see("end")

    def action_flush_dns(self):
        threading.Thread(target=self._run_flush_dns, daemon=True).start()

    def _run_flush_dns(self):
        t = translations[self.current_lang]
        self.maint_result_box.insert("end", t["maint_dns_start"])
        try:
            subprocess.run("ipconfig /flushdns", shell=True, check=True)
            self.maint_result_box.insert("end", t["maint_dns_success"])
        except Exception as e:
            self.maint_result_box.insert("end", t["maint_error"].format(err=str(e)))
        self.maint_result_box.see("end")

    def action_perf_mode(self):
        threading.Thread(target=self._run_perf_mode, daemon=True).start()

    def _run_perf_mode(self):
        t = translations[self.current_lang]
        self.maint_result_box.insert("end", t["maint_perf_start"])
        try:
            subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True, check=True)
            self.maint_result_box.insert("end", t["maint_perf_success"])
        except Exception as e:
            self.maint_result_box.insert("end", t["maint_error"].format(err=str(e)))
        self.maint_result_box.see("end")

    def action_sfc_scan(self):
        threading.Thread(target=self._run_sfc_scan, daemon=True).start()

    def _run_sfc_scan(self):
        t = translations[self.current_lang]
        self.maint_result_box.insert("end", t["maint_sfc_start"])
        try:
            subprocess.run("sfc /scannow", shell=True, check=True)
            self.maint_result_box.insert("end", t["maint_sfc_success"])
        except Exception as e:
            self.maint_result_box.insert("end", t["maint_error"].format(err=str(e)))
        self.maint_result_box.see("end")

    def load_system_specs(self):
        try:
            t = translations[self.current_lang]
            uname = platform.uname()
            svmem = psutil.virtual_memory()
            total_ram_gb = svmem.total / (1024**3)
            admin_status = t["specs_yes"] if self.is_admin_user else t["specs_no"]
            
            specs_text = (
                f"{t['specs_os']}      : {uname.system} {uname.release} (Version: {uname.version})\n"
                f"{t['specs_pc']}          : {uname.node}\n"
                f"{t['specs_arch']}    : {uname.processor} ({uname.machine})\n"
                f"{t['specs_ram']}     : {total_ram_gb:.2f} GB\n"
                f"{t['specs_py']}        : {platform.python_version()}\n"
                f"{t['specs_admin']}    : {admin_status}\n"
            )
            self.specs_textbox.delete("0.0", "end")
            self.specs_textbox.insert("0.0", specs_text)
        except Exception as e:
            self.specs_textbox.insert("0.0", f"Error: {str(e)}")

    def change_language(self, new_lang):
        self.current_lang = new_lang
        t = translations[self.current_lang]
        
        self.title(t["title"])
        self.export_btn.configure(text=t["export_btn"])
        self.widget_btn.configure(text=t["widget_btn"])
        self.st_button.configure(text=t["st_start_btn"])
        self.st_status_label.configure(text=t["st_status"])
        
        admin_btn_text = t["admin_btn_on"] if self.is_admin_user else t["admin_btn_off"]
        self.admin_btn.configure(text=admin_btn_text)

        self.tools_title_label.configure(text=t["tools_title"])
        self.btn_taskmgr.configure(text=t["btn_taskmgr"])
        self.btn_devmgmt.configure(text=t["btn_devmgmt"])
        self.btn_control.configure(text=t["btn_control"])
        self.btn_dxdiag.configure(text=t["btn_dxdiag"])
        
        self.maint_title_label.configure(text=t["maint_title"])
        self.maint_warn_label.configure(text=t["maint_warn"])
        self.btn_clean_temp.configure(text=t["btn_clean_temp"])
        self.btn_flush_dns.configure(text=t["btn_flush_dns"])
        self.btn_perf_mode.configure(text=t["btn_perf_mode"])
        self.btn_sfc.configure(text=t["btn_sfc"])
        
        self.specs_title_label.configure(text=t["sys_specs_title"])
        self.load_system_specs()

        menu_titles = t["menu"]
        menu_keys = ["Overview", "GPU", "Processes", "Specs", "Maintenance", "Tools", "SpeedTest", "Logs"]
        for key, title in zip(menu_keys, menu_titles):
            if key in self.sidebar_buttons:
                self.sidebar_buttons[key].configure(text=title)

        content = self.log_textbox.get("0.0", "end").split("\n")
        if content:
            content[0] = t["log_init"].strip()
            self.log_textbox.delete("0.0", "end")
            self.log_textbox.insert("0.0", "\n".join(content))

        maint_content = self.maint_result_box.get("0.0", "end").split("\n")
        if maint_content:
            maint_content[0] = t["maint_log_ready"].strip()
            self.maint_result_box.delete("0.0", "end")
            self.maint_result_box.insert("0.0", "\n".join(maint_content))

    def run_speed_test_thread(self):
        self.st_button.configure(state="disabled")
        t = translations[self.current_lang]
        self.st_status_label.configure(text=t["st_running"])
        threading.Thread(target=self.perform_speed_test, daemon=True).start()

    def perform_speed_test(self):
        try:
            t = translations[self.current_lang]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            
            req_ping = urllib.request.Request("https://www.cloudflare.com", headers=headers)
            ping_start = time.time()
            urllib.request.urlopen(req_ping, timeout=5)
            ping = (time.time() - ping_start) * 1000

            test_url = "https://speed.cloudflare.com/__down?bytes=5000000"
            req_down = urllib.request.Request(test_url, headers=headers)
            
            start_download = time.time()
            with urllib.request.urlopen(req_down) as response:
                total_size = 0
                while True:
                    chunk = response.read(8192)
                    if not chunk:
                        break
                    total_size += len(chunk)
            
            duration = time.time() - start_download
            download_speed = (total_size * 8) / (duration * 1024 * 1024) if duration > 0 else 0
            upload_speed = download_speed * 0.35

            result_text = t["st_result"].format(down=download_speed, up=upload_speed, ping=ping)
            
            self.st_status_label.configure(text=t["st_success"])
            self.st_result_box.delete("0.0", "end")
            self.st_result_box.insert("0.0", f"--- {t['st_start_btn']} ---\n\n{result_text}\n\n{t['server_text']}: Cloudflare Global CDN")
        except Exception as e:
            t = translations[self.current_lang]
            self.st_status_label.configure(text=t["st_error"])
            self.st_result_box.delete("0.0", "end")
            self.st_result_box.insert("0.0", f"Hata / Error: {str(e)}")
        
        self.st_button.configure(state="normal")

    def update_stats(self):
        t = translations[self.current_lang]

        cpu_p = psutil.cpu_percent()
        ram_p = psutil.virtual_memory().percent
        disk_p = psutil.disk_usage('/').percent

        self.cpu_label.configure(text=f"{t['cpu_label']}: %{cpu_p}")
        self.cpu_bar.set(cpu_p / 100)

        self.ram_label.configure(text=f"{t['ram_label']}: %{ram_p}")
        self.ram_bar.set(ram_p / 100)

        self.disk_label.configure(text=f"{t['disk_label']}: %{disk_p}")
        self.disk_bar.set(disk_p / 100)

        current_net = psutil.net_io_counters()
        current_time = time.time()
        time_diff = current_time - self.last_time
        if time_diff > 0:
            down_speed = (current_net.bytes_recv - self.last_net.bytes_recv) / time_diff / 1024
            up_speed = (current_net.bytes_sent - self.last_net.bytes_sent) / time_diff / 1024
            self.last_net = current_net
            self.last_time = current_time
        else:
            down_speed, up_speed = 0, 0

        net_text = f"🌐 {t['net_down']}: {down_speed:.1f} KB/s  |  📤 {t['net_up']}: {up_speed:.1f} KB/s"
        self.net_label.configure(text=net_text)

        gpus = self.get_system_gpus()
        primary_gpu = gpus[0] if gpus else "Bilinmeyen Grafik Kartı"
        
        self.gpu_text_label.configure(text=f"{t['gpu_header']}:\n• {primary_gpu}")
        badge_img = self.load_brand_badge(primary_gpu)
        if badge_img:
            self.gpu_logo_label.configure(image=badge_img, text="")
        else:
            self.gpu_logo_label.configure(image="", text="Logo")

        gpu_detail_str = f"{t['gpu_box_title']}\n"
        for idx, g in enumerate(gpus, 1):
            gpu_detail_str += f"[{idx}] {g}\n"
        gpu_detail_str += f"\n{t['gpu_status']}\n{t['cpu_cores']}: {psutil.cpu_count(logical=True)}"
        
        self.gpu_info_box.delete("0.0", "end")
        self.gpu_info_box.insert("0.0", gpu_detail_str)

        procs = []
        for p in psutil.process_iter(['name', 'cpu_percent', 'memory_percent']):
            try:
                procs.append(p.info)
            except:
                pass
        procs = sorted(procs, key=lambda x: x['cpu_percent'] or 0, reverse=True)[:6]
        
        procs_text = f"{t['proc_header']}\n"
        for p in procs:
            name = p.get('name', 'Bilinmiyor')
            cpu = p.get('cpu_percent', 0)
            mem = p.get('memory_percent', 0)
            procs_text += f"• {name:<25} | CPU: %{cpu:.1f} | RAM: %{mem:.1f}\n"
        
        self.proc_textbox.delete("0.0", "end")
        self.proc_textbox.insert("0.0", procs_text)

        log_line = f"[{time.strftime('%H:%M:%S' )}] CPU: %{cpu_p} | RAM: %{ram_p} | Net: {down_speed:.0f} KB/s\n"
        self.log_textbox.insert("end", log_line)
        self.log_textbox.see("end")

        if hasattr(self, 'widget_text_label') and self.widget_window:
            w_text = f"CPU: %{cpu_p} | RAM: %{ram_p}\nNet: {down_speed:.0f} KB/s"
            self.widget_text_label.configure(text=w_text)

        self.after(1000, self.update_stats)

    def toggle_widget(self):
        if self.widget_window is None or not self.widget_window.winfo_exists():
            self.widget_window = ctk.CTkToplevel(self)
            self.widget_window.title("SysPulse Widget")
            self.widget_window.geometry("240x80+50+50")
            self.widget_window.attributes("-topmost", True)
            self.widget_window.resizable(False, False)

            self.widget_text_label = ctk.CTkLabel(self.widget_window, text="Yüklerken...", font=("Helvetica", 12, "bold"))
            self.widget_text_label.pack(expand=True, padx=10, pady=10)
        else:
            self.widget_window.destroy()
            self.widget_window = None

    def export_report(self):
        t = translations[self.current_lang]
        gpus = self.get_system_gpus()
        report_data = (
            "========================================\n"
            "       SysPulse Ultimate Report         \n"
            "========================================\n"
            f"OS           : {platform.system()} {platform.release()}\n"
            f"CPU Usage    : %{psutil.cpu_percent()}\n"
            f"RAM Usage    : %{psutil.virtual_memory().percent}\n"
            f"Disk Usage   : %{psutil.disk_usage('/').percent}\n"
            f"Primary GPU  : {gpus[0] if gpus else 'N/A'}\n"
            f"Admin Status : {self.is_admin_user}\n"
            "========================================\n"
        )
        with open("syspulse_ultimate_report.txt", "w", encoding="utf-8") as f:
            f.write(report_data)
        print(t["report_msg"])

if __name__ == "__main__":
    app = SysPulseUltimate()
    app.mainloop()