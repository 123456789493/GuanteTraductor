# src/app_movil.py
#python traductor_en_vivo.py
#python src/app_movil.py
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import serial
import serial.tools.list_ports
from datetime import datetime

class AppMovilFixed:
    def __init__(self, root):
        self.root = root
        self.root.title("👋 Traductor de Señas - App Móvil")
        self.root.geometry("450x650")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        
        # Estado de la aplicación
        self.conectado = False
        self.puerto_serial = None
        self.puerto_seleccionado = None
        
        self.setup_interfaz()
        self.detectar_puertos_seriales_mejorado()
        
    def detectar_puertos_seriales_mejorado(self):
        """Detección MEJORADA de puertos seriales"""
        self.puertos_disponibles = []
        
        print("=== DETECCIÓN DE PUERTOS SERIALES ===")
        
        try:
            # Método 1: Usar serial.tools.list_ports
            puertos = list(serial.tools.list_ports.comports())
            print(f"Sistema encontró {len(puertos)} puertos")
            
            for i, puerto in enumerate(puertos):
                print(f"  {i+1}. {puerto.device} - {puerto.description}")
                self.puertos_disponibles.append({
                    "nombre": puerto.device,
                    "descripcion": puerto.description or "Dispositivo Serial",
                    "hwid": getattr(puerto, 'hwid', 'N/A')
                })
                
        except Exception as e:
            print(f"Error en detección automática: {e}")
        
        # Método 2: Agregar puertos comunes de Windows
        puertos_comunes_windows = ['COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8']
        
        for puerto in puertos_comunes_windows:
            # Solo agregar si no existe
            if not any(p['nombre'] == puerto for p in self.puertos_disponibles):
                self.puertos_disponibles.append({
                    "nombre": puerto,
                    "descripcion": "Puerto Serial (COM)",
                    "hwid": "SIMULADO_WINDOWS"
                })
                print(f"Agregado puerto común: {puerto}")
        
        # Método 3: Si NO HAY NINGÚN PUERTO, forzar algunos
        if not self.puertos_disponibles:
            print("⚠️  No se detectaron puertos, forzando lista...")
            self.puertos_disponibles = [
                {"nombre": "COM3", "descripcion": "Arduino Uno", "hwid": "SIMULADO"},
                {"nombre": "COM4", "descripcion": "HC-05 Bluetooth", "hwid": "SIMULADO"},
                {"nombre": "COM5", "descripcion": "ESP32", "hwid": "SIMULADO"},
                {"nombre": "COM6", "descripcion": "Puerto Serial", "hwid": "SIMULADO"}
            ]
        
        print(f"Total de puertos disponibles: {len(self.puertos_disponibles)}")
        
        for i, puerto in enumerate(self.puertos_disponibles):
            print(f"  {i+1}. {puerto['nombre']} - {puerto['descripcion']}")
        
        self.log_evento(f"📡 {len(self.puertos_disponibles)} puertos detectados")

    def setup_interfaz(self):
        """Interfaz simple y funcional"""
        
        # Header
        header_frame = tk.Frame(self.root, bg='#3498db', height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="👋 TRADUCTOR DE SEÑAS", 
                font=('Arial', 16, 'bold'), bg='#3498db', fg='white').pack(expand=True)
        tk.Label(header_frame, text="App Móvil", 
                font=('Arial', 10), bg='#3498db', fg='#ecf0f1').pack()

        # Contenido principal
        main_frame = tk.Frame(self.root, bg='#ecf0f1')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # ================= CONEXIÓN =================
        conexion_frame = tk.LabelFrame(main_frame, text="🔗 CONEXIÓN", 
                                      font=('Arial', 10, 'bold'),
                                      bg='#ecf0f1', fg='#2c3e50',
                                      padx=10, pady=8)
        conexion_frame.pack(fill=tk.X, pady=(0, 8))

        # Estado
        estado_frame = tk.Frame(conexion_frame, bg='#ecf0f1')
        estado_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(estado_frame, text="Estado:", font=('Arial', 9, 'bold'), 
                bg='#ecf0f1').pack(side=tk.LEFT)
        
        self.estado_label = tk.Label(estado_frame, text="DESCONECTADO", 
                                   font=('Arial', 9, 'bold'), bg='#e74c3c', fg='white',
                                   padx=8, pady=2)
        self.estado_label.pack(side=tk.RIGHT)

        # Puerto
        puerto_frame = tk.Frame(conexion_frame, bg='#ecf0f1')
        puerto_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(puerto_frame, text="Puerto:", font=('Arial', 9), 
                bg='#ecf0f1').pack(side=tk.LEFT)
        
        self.puerto_label = tk.Label(puerto_frame, text="Ninguno seleccionado", 
                                   font=('Arial', 9), bg='#ecf0f1')
        self.puerto_label.pack(side=tk.RIGHT)

        # Botones
        botones_frame = tk.Frame(conexion_frame, bg='#ecf0f1')
        botones_frame.pack(fill=tk.X, pady=5)

        self.btn_seleccionar = tk.Button(botones_frame, text="📱 SELECCIONAR PUERTO",
                                       font=('Arial', 9), bg='#9b59b6', fg='white',
                                       command=self.mostrar_puertos, width=20, height=1)
        self.btn_seleccionar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_conectar = tk.Button(botones_frame, text="🔗 CONECTAR",
                                    font=('Arial', 9), bg='#27ae60', fg='white',
                                    command=self.conectar_serial, state="disabled", 
                                    width=12, height=1)
        self.btn_conectar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_desconectar = tk.Button(botones_frame, text="❌ DESCONECTAR",
                                       font=('Arial', 9), bg='#e74c3c', fg='white',
                                       command=self.desconectar_serial, state="disabled", 
                                       width=12, height=1)
        self.btn_desconectar.pack(side=tk.LEFT)

        # ================= TRADUCCIÓN =================
        trad_frame = tk.LabelFrame(main_frame, text="TRADUCCIÓN", 
                                  font=('Arial', 10, 'bold'),
                                  bg='#ecf0f1', fg='#2c3e50',
                                  padx=10, pady=8)
        trad_frame.pack(fill=tk.X, pady=(0, 8))

        self.traduccion_label = tk.Label(trad_frame, text="---", 
                                       font=('Arial', 28, 'bold'), bg='#34495e', fg='white',
                                       height=2)
        self.traduccion_label.pack(fill=tk.X, pady=5)

        conf_frame = tk.Frame(trad_frame, bg='#ecf0f1')
        conf_frame.pack(fill=tk.X)

        tk.Label(conf_frame, text="Confianza:", font=('Arial', 9), 
                bg='#ecf0f1').pack(side=tk.LEFT)
        
        self.confianza_label = tk.Label(conf_frame, text="--%", 
                                      font=('Arial', 9, 'bold'), bg='#ecf0f1', fg='#e67e22')
        self.confianza_label.pack(side=tk.RIGHT)

        self.progressbar = ttk.Progressbar(trad_frame, orient='horizontal', 
                                         length=200, mode='determinate')
        self.progressbar.pack(fill=tk.X, pady=3)

        # ================= DATOS =================
        datos_frame = tk.LabelFrame(main_frame, text="📊 DATOS RECIBIDOS", 
                                   font=('Arial', 10, 'bold'),
                                   bg='#ecf0f1', fg='#2c3e50',
                                   padx=10, pady=8)
        datos_frame.pack(fill=tk.X, pady=(0, 8))

        self.datos_text = tk.Text(datos_frame, height=4, font=('Consolas', 8),
                                bg='#2c3e50', fg='#ecf0f1', wrap=tk.WORD)
        self.datos_text.pack(fill=tk.BOTH, expand=True)
        self.datos_text.insert(tk.END, "Esperando conexión...")
        self.datos_text.config(state="disabled")

        # ================= LOGS =================
        logs_frame = tk.LabelFrame(main_frame, text="📝 ACTIVIDAD", 
                                  font=('Arial', 10, 'bold'),
                                  bg='#ecf0f1', fg='#2c3e50',
                                  padx=10, pady=8)
        logs_frame.pack(fill=tk.BOTH, expand=True)

        self.logs_text = tk.Text(logs_frame, height=6, font=('Consolas', 8),
                               bg='#1a1a1a', fg='#00ff00', wrap=tk.WORD)
        self.logs_text.pack(fill=tk.BOTH, expand=True)
        self.log_evento("App iniciada. Selecciona un puerto.")

    def mostrar_puertos(self):
        """Muestra TODOS los puertos disponibles"""
        if not self.puertos_disponibles:
            messagebox.showwarning("Sin puertos", "No se detectaron puertos seriales.")
            return
        
        ventana = tk.Toplevel(self.root)
        ventana.title("Seleccionar Puerto Serial")
        ventana.geometry("400x300")
        ventana.configure(bg='#ecf0f1')
        
        tk.Label(ventana, text="🔌 PUERTOS SERIALES DISPONIBLES", 
                font=('Arial', 12, 'bold'), bg='#ecf0f1').pack(pady=15)
        
        tk.Label(ventana, text="Selecciona el puerto donde está el traductor:", 
                font=('Arial', 9), bg='#ecf0f1').pack(pady=(0, 10))
        
        # Frame con scroll para muchos puertos
        frame_container = tk.Frame(ventana, bg='#ecf0f1')
        frame_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Mostrar cada puerto disponible
        for i, puerto in enumerate(self.puertos_disponibles):
            btn_text = f"🔌 {puerto['nombre']} - {puerto['descripcion']}"
            if puerto.get('hwid', '').startswith('SIMULADO'):
                btn_text += " [SIMULADO]"
            
            btn = tk.Button(frame_container, text=btn_text,
                          font=('Arial', 9), bg='#3498db', fg='white',
                          command=lambda p=puerto: self.seleccionar_puerto(p, ventana),
                          width=45, height=2, anchor='w', justify='left')
            btn.pack(fill=tk.X, pady=2)

    def seleccionar_puerto(self, puerto, ventana):
        self.puerto_seleccionado = puerto
        self.puerto_label.config(text=puerto['nombre'])
        self.btn_conectar.config(state="normal")
        self.log_evento(f"✅ Puerto seleccionado: {puerto['nombre']}")
        ventana.destroy()

    # ... (el resto de las funciones se mantienen igual: conectar_serial, desconectar_serial, etc.)

    def conectar_serial(self):
        if not self.puerto_seleccionado:
            messagebox.showerror("Error", "Selecciona un puerto primero")
            return
        
        self.log_evento(f"🔗 Conectando a {self.puerto_seleccionado['nombre']}...")
        self.estado_label.config(text="CONECTANDO...", bg='#f39c12')
        
        def conectar():
            try:
                self.puerto_serial = serial.Serial(
                    port=self.puerto_seleccionado['nombre'],
                    baudrate=9600,
                    timeout=1
                )
                time.sleep(2)
                self.root.after(0, self.conexion_exitosa)
            except Exception as e:
                self.root.after(0, lambda: self.conexion_fallida(str(e)))
        
        threading.Thread(target=conectar, daemon=True).start()

    def conexion_exitosa(self):
        self.conectado = True
        self.estado_label.config(text="CONECTADO", bg='#27ae60')
        self.btn_conectar.config(state="disabled")
        self.btn_desconectar.config(state="normal")
        self.btn_seleccionar.config(state="disabled")
        self.log_evento("¡Conectado! Recibiendo traducciones...")
        self.iniciar_recepcion()

    def conexion_fallida(self, error):
        self.estado_label.config(text="ERROR", bg='#e74c3c')
        messagebox.showerror("Error", f"No se pudo conectar:\n{error}")
        self.log_evento(f"Error: {error}")

    def desconectar_serial(self):
        self.conectado = False
        if self.puerto_serial:
            self.puerto_serial.close()
        
        self.estado_label.config(text="DESCONECTADO", bg='#e74c3c')
        self.btn_conectar.config(state="normal")
        self.btn_desconectar.config(state="disabled")
        self.btn_seleccionar.config(state="normal")
        
        self.traduccion_label.config(text="---", bg='#34495e')
        self.confianza_label.config(text="--%")
        self.progressbar['value'] = 0
        
        self.datos_text.config(state="normal")
        self.datos_text.delete(1.0, tk.END)
        self.datos_text.insert(tk.END, "Desconectado")
        self.datos_text.config(state="disabled")
        
        self.log_evento("🔒 Desconectado")

    def iniciar_recepcion(self):
        if self.conectado:
            self.leer_datos()

    def leer_datos(self):
        if not self.conectado:
            return
        
        try:
            if self.puerto_serial and self.puerto_serial.in_waiting > 0:
                linea = self.puerto_serial.readline().decode('utf-8').strip()
                if linea:
                    self.procesar_datos(linea)
            
            if self.conectado:
                self.root.after(100, self.leer_datos)
        except Exception as e:
            self.log_evento(f"Error lectura: {e}")
            if self.conectado:
                self.root.after(1000, self.leer_datos)

    def procesar_datos(self, datos):
        try:
            if ',' in datos:
                gesto, confianza = datos.split(',')
                confianza = int(confianza)
                
                self.traduccion_label.config(text=gesto.upper())
                
                color = "#27ae60" if confianza >= 85 else "#f39c12" if confianza >= 70 else "#e74c3c"
                self.traduccion_label.config(bg=color)
                
                self.confianza_label.config(text=f"{confianza}%")
                self.progressbar['value'] = confianza
                
                timestamp = datetime.now().strftime("%H:%M:%S")
                self.datos_text.config(state="normal")
                self.datos_text.delete(1.0, tk.END)
                self.datos_text.insert(tk.END, f"[{timestamp}] {gesto} - {confianza}%")
                self.datos_text.config(state="disabled")
                
                self.log_evento(f"{gesto} ({confianza}%)")
                
        except Exception as e:
            self.log_evento(f"Error procesando: {e}")

    def log_evento(self, mensaje):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs_text.insert(tk.END, f"[{timestamp}] {mensaje}\n")
        self.logs_text.see(tk.END)

def main():
    root = tk.Tk()
    app = AppMovilFixed(root)
    root.mainloop()

if __name__ == "__main__":
    main()