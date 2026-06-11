import tkinter as tk
import urllib.request
import json
import socket
import threading

# ---- Configuracion WiFi ----
PICO_IP = "172.20.10.5"  # IP de la Raspberry Pi Pico W en la red
PICO_PUERTO = 5000        # puerto donde escucha el servidor de la Pico

# ---- Datos de la maquina ----
stock = [9, 9, 9]         # stock actual de cada producto
ventas = [0, 0, 0]        # cantidad de ventas por producto
PRECIO = 250              # precio en colones de cada producto
mantenimiento = False     # True si la maquina esta en mantenimiento
initial_stock = [9, 9, 9] # stock inicial para calcular ventas

# ---- Nombres de los productos ----
PRODUCTOS = ["Pockie", "Soda", "Chips"]  # nombres que se muestran en la interfaz

# ---- Configuracion de la API ----
TIPO_CAMBIO_URL = "https://api.exchangerate-api.com/v4/latest/USD"  # URL de la API de tipo de cambio
TIPO_CAMBIO_MONEDA = "CRC"  # codigo de la moneda costarricense

# ---- Conexion con la Pico ----
cliente = None  # guarda el socket activo con la Pico

def conectar_pico():
    # Crea un socket TCP y se conecta a la IP y puerto de la Pico
    # Si se conecta exitosamente inicia un hilo para escuchar mensajes
    global cliente
    try:
        cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cliente.connect((PICO_IP, PICO_PUERTO))
        cliente.setblocking(False)
        label_conexion.config(text=f'Conexion: conectado a {PICO_IP}')
        print("Conectado a la Pico W")
        # inicia escuchar_pico en segundo plano para no congelar la interfaz
        hilo = threading.Thread(target=escuchar_pico, daemon=True)
        hilo.start()
    except Exception as e:
        label_conexion.config(text='Conexion: no se pudo conectar')
        print("Error al conectar:", e)

def mandar_mensaje(mensaje):
    # Convierte el mensaje a bytes y lo envia a la Pico por el socket
    global cliente
    try:
        cliente.setblocking(True)
        cliente.send(mensaje.encode())
        cliente.setblocking(False)
    except Exception as e:
        print("Error al mandar mensaje:", e)

def escuchar_pico():
    # Corre en segundo plano esperando mensajes que manda la Pico
    # Cuando recibe un mensaje actualiza el stock y las ventas en la interfaz
    global stock, ventas
    while True:
        try:
            cliente.setblocking(True)
            datos = cliente.recv(64).decode().strip()  # lee hasta 64 bytes
            cliente.setblocking(False)
            if not datos:
                continue

            # La Pico mando el estado completo: "STOCK:9,9,9;MANT:0"
            # se separa el string y se actualiza el stock de cada producto
            if datos.startswith("STOCK:"):
                partes = datos.split(";")
                numeros = partes[0].replace("STOCK:", "").split(",")
                stock[0] = int(numeros[0])
                stock[1] = int(numeros[1])
                stock[2] = int(numeros[2])
                ventas = [initial_stock[i] - stock[i] for i in range(3)]
                ventana.after(0, actualizar_labels)  # actualiza la pantalla

            # La Pico avisa que se hizo una venta: "VENTA:0"
            # se incrementa la venta y se decrementa el stock del producto
            elif datos.startswith("VENTA:"):
                producto = int(datos.replace("VENTA:", ""))
                ventas[producto] += 1
                stock[producto] -= 1
                ventana.after(0, actualizar_labels)  # actualiza la pantalla

        except:
            continue  # si no hay mensajes nuevos continua esperando

# ---- Ventana principal ----
ventana = tk.Tk()
ventana.title('CE VENDING MACHINE')
ventana.geometry('700x500')
ventana.config(bg='#A81AA8')

# ---- Titulo ----
tk.Label(
    ventana,
    text='CE VENDING MACHINE',
    font=('Arial', 22, 'bold'),
    bg='#A81AA8',
    fg='white',
).pack(pady=15)

# ---- Frame de productos ----
# contenedor donde se muestran las 3 tarjetas de productos
frame_productos = tk.Frame(ventana, bg='#A81AA8')
frame_productos.pack(pady=10)

labels_stock = []  # lista para guardar las etiquetas de stock de cada producto

# crea una tarjeta por cada producto con su nombre y stock
for i in range(3):
    frame = tk.Frame(frame_productos, borderwidth=1, relief='solid', padx=20, pady=15, bg='white')
    frame.grid(row=0, column=i, padx=10)

    # etiqueta gris con el numero de producto
    tk.Label(
        frame,
        text=f'Producto {i + 1}',
        font=('Arial', 11),
        bg='white',
        fg='gray'
    ).pack()

    # etiqueta negra con el nombre del producto
    tk.Label(
        frame,
        text=PRODUCTOS[i],
        font=('Arial', 14, 'bold'),
        bg='white',
        fg='black'
    ).pack()

    # etiqueta que muestra el stock actual del producto
    label_stock = tk.Label(
        frame,
        text=f'Stock: {stock[i]}',
        font=('Arial', 12),
        bg='white'
    )
    label_stock.pack(pady=5)
    labels_stock.append(label_stock)  # se guarda para poder actualizarla despues

# ---- Frame estadisticas ----
# cuadro blanco que muestra ventas, ganancias y estado de conexion
frame_stats = tk.Frame(ventana, borderwidth=1, relief='solid', padx=15, pady=15, bg='white')
frame_stats.pack(pady=10, fill='x', padx=20)

tk.Label(frame_stats, text='Estadisticas', font=('Arial', 14, 'bold'), bg='white').pack()

# etiqueta que muestra cuantas unidades se vendieron por producto
label_ventas = tk.Label(frame_stats, text='Ventas: Chips: 0  Soda: 0  Pockie: 0  Total: 0', font=('Arial', 12), bg='white')
label_ventas.pack(pady=5)

# etiqueta que muestra las ganancias en colones y dolares
label_ganancias = tk.Label(frame_stats, text='Ganancias: ₡0  =  $0.00', font=('Arial', 12), bg='white')
label_ganancias.pack(pady=5)

# etiqueta que muestra si la interfaz esta conectada a la Pico o no
label_conexion = tk.Label(frame_stats, text='Conexion: sin conectar', font=('Arial', 12), bg='white')
label_conexion.pack(pady=5)

# ---- Estado mantenimiento ----
# etiqueta que muestra si la maquina esta activa o en mantenimiento
label_estado = tk.Label(ventana, text='Estado: ACTIVA', font=('Arial', 13), fg='green', bg='#A81AA8')
label_estado.pack(pady=5)

# ---- Funciones ----
def obtener_tipo_cambio():
    # Consulta la API externa para obtener cuantos colones vale 1 dolar
    # Si la API no responde devuelve None
    try:
        with urllib.request.urlopen(TIPO_CAMBIO_URL, timeout=5) as respuesta:
            datos = json.load(respuesta)
        return datos["rates"][TIPO_CAMBIO_MONEDA]
    except Exception:
        return None

def actualizar_labels():
    # Recalcula ventas y ganancias y actualiza todas las etiquetas de la pantalla
    total_ventas = sum(ventas)
    ganancias_colones = total_ventas * PRECIO
    tipo_cambio = obtener_tipo_cambio()  # consulta el tipo de cambio actual

    # si la API no esta disponible muestra un aviso
    if tipo_cambio is None:
        texto_ganancias = f'Ganancias: ₡{ganancias_colones}  =  API no disponible'
    else:
        dolares = round(ganancias_colones / tipo_cambio, 2)
        texto_ganancias = f'Ganancias: ₡{ganancias_colones}  =  ${dolares}'

    label_ventas.config(
        text=f'Ventas: Pockie: {ventas[0]}  Soda: {ventas[1]}  Chips: {ventas[2]}  Total: {total_ventas}'
    )
    label_ganancias.config(text=texto_ganancias)

    # actualiza el stock en cada tarjeta de producto
    for i in range(3):
        labels_stock[i].config(text=f'Stock: {stock[i]}')

def toggle_mantenimiento():
    # Cambia el modo mantenimiento entre activo y desactivado
    # Ademas le avisa a la Pico para que encienda o apague el LED amarillo
    global mantenimiento
    mantenimiento = not mantenimiento
    if mantenimiento:
        label_estado.config(text='Estado: MANTENIMIENTO', fg='red')
        btn_mantenimiento.config(text='Desactivar Mantenimiento')
        mandar_mensaje("MANT_ON")   # la Pico enciende el LED amarillo
    else:
        label_estado.config(text='Estado: ACTIVA', fg='green')
        btn_mantenimiento.config(text='Activar Mantenimiento')
        mandar_mensaje("MANT_OFF")  # la Pico apaga el LED amarillo

def pedir_estado():
    # Le pide a la Pico el stock y modo actuales
    mandar_mensaje("GET_STATUS")

# ---- Botones ----
# boton para activar o desactivar el modo mantenimiento
btn_mantenimiento = tk.Button(
    ventana,
    text='Activar Mantenimiento',
    font=('Arial', 12),
    command=toggle_mantenimiento,
    bg='#e74c3c',
    fg='white',
    padx=10,
    pady=5,
)
btn_mantenimiento.pack(pady=5)

# ---- Arranque ----
actualizar_labels()  # muestra los datos iniciales en la pantalla
conectar_pico()      # intenta conectarse a la Pico al abrir la app
ventana.mainloop()   # inicia el bucle principal de la interfaz grafica