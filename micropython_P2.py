from machine import Pin, PWM, ADC
import time

# ---------------- POTENCIOMETRO ----------------
potenciometro = ADC(26)

# ---------------- LEDS ROJOS (sin stock) ----------------
led1 = Pin(15, Pin.OUT)
led2 = Pin(14, Pin.OUT)
led3 = Pin(13, Pin.OUT)

# ---------------- LEDS VERDES (con stock) ----------------
ledv1 = Pin(12, Pin.OUT)
ledv2 = Pin(11, Pin.OUT)
ledv3 = Pin(10, Pin.OUT)

# ---------------- SERVO ----------------
servo = PWM(Pin(8))
servo.freq(50)

# ---------------- BOTON ----------------
boton = Pin(17, Pin.IN, Pin.PULL_UP)

# ---------------- 7 SEGMENTOS ----------------
pin_a = Pin(1, Pin.OUT)
pin_b = Pin(2, Pin.OUT)
pin_f = Pin(3, Pin.OUT)
pin_g = Pin(4, Pin.OUT)
pin_c = Pin(5, Pin.OUT)
pin_d = Pin(6, Pin.OUT)
pin_e = Pin(7, Pin.OUT)

# ---------------- STOCK ----------------
stock = [9, 9, 9]  # stock de cada producto

# ---------------- FUNCIONES 7 SEGMENTOS ----------------
def mostrar_numero(numero):
    if numero == 0:
        pin_a.value(0)
        pin_b.value(0)
        pin_f.value(0)
        pin_g.value(1)
        pin_c.value(0)
        pin_d.value(0)
        pin_e.value(0)
    elif numero == 1:
        pin_a.value(1)
        pin_b.value(0)
        pin_f.value(1)
        pin_g.value(1)
        pin_c.value(0)
        pin_d.value(1)
        pin_e.value(1)
    elif numero == 2:
        pin_a.value(0)
        pin_b.value(0)
        pin_f.value(1)
        pin_g.value(0)
        pin_c.value(1)
        pin_d.value(0)
        pin_e.value(0)
    elif numero == 3:
        pin_a.value(0)
        pin_b.value(0)
        pin_f.value(1)
        pin_g.value(0)
        pin_c.value(0)
        pin_d.value(0)
        pin_e.value(1)
    elif numero == 4:
        pin_a.value(1)
        pin_b.value(0)
        pin_f.value(0)
        pin_g.value(0)
        pin_c.value(0)
        pin_d.value(1)
        pin_e.value(1)
    elif numero == 5:
        pin_a.value(0)
        pin_b.value(1)
        pin_f.value(0)
        pin_g.value(0)
        pin_c.value(0)
        pin_d.value(0)
        pin_e.value(1)
    elif numero == 6:
        pin_a.value(0)
        pin_b.value(1)
        pin_f.value(0)
        pin_g.value(0)
        pin_c.value(0)
        pin_d.value(0)
        pin_e.value(0)
    elif numero == 7:
        pin_a.value(0)
        pin_b.value(0)
        pin_f.value(1)
        pin_g.value(1)
        pin_c.value(0)
        pin_d.value(1)
        pin_e.value(1)
    elif numero == 8:
        pin_a.value(0)
        pin_b.value(0)
        pin_f.value(0)
        pin_g.value(0)
        pin_c.value(0)
        pin_d.value(0)
        pin_e.value(0)
    elif numero == 9:
        pin_a.value(0)
        pin_b.value(0)
        pin_f.value(0)
        pin_g.value(0)
        pin_c.value(0)
        pin_d.value(1)
        pin_e.value(1)

# ---------------- FUNCIONES SERVO ----------------
def mover_servo(angulo):
    angulo = max(0, min(180, angulo))
    duty = int(2000 + (8000 - 2000) * angulo / 180)
    servo.duty_u16(duty)

def abrir_servo():
    for angulo in range(0, 46):
        mover_servo(angulo)
        time.sleep(0.03)

def cerrar_servo():
    for angulo in range(45, -1, -1):
        mover_servo(angulo)
        time.sleep(0.03)

#posicion inicial del servo
mover_servo(0)

# ---------------- PRINCIPAL ----------------
while True:
    #Lee el potenciometro
    lectura = potenciometro.read_u16()
    valor = lectura // 655  # 0 a 100

    #producto seleccionado
    if valor <= 33:
        producto_actual = 0
    elif valor <= 66:
        producto_actual = 1
    else:
        producto_actual = 2

    # Mostrar stock del producto en 7 segmentos
    mostrar_numero(stock[producto_actual])

    # Actualizar LEDs segun stock
    leds_rojos = [led1, led2, led3]
    leds_verdes = [ledv1, ledv2, ledv3]

    if stock[producto_actual] > 0:
        leds_verdes[producto_actual].value(1)  # verde ON
        leds_rojos[producto_actual].value(0)   # rojo OFF
    else:
        leds_verdes[producto_actual].value(0)  # verde OFF
        leds_rojos[producto_actual].value(1)   # rojo ON

    # Apagar LEDs de los otros productos
    for i in range(3):
        if i != producto_actual:
            leds_rojos[i].value(0)
            leds_verdes[i].value(0)

    # Verificar si se presiono el boton
    if boton.value() == 0:
        if stock[producto_actual] > 0:  # solo si hay stock
            print(f"Comprando producto {producto_actual + 1}")
            stock[producto_actual] -= 1  # restar una unidad

            abrir_servo()
            time.sleep(3)
            cerrar_servo()

            # Esperar a que suelte el boton
            while boton.value() == 0:
                time.sleep(0.01)
            time.sleep(0.2)  # anti rebote

        else:
            print(f"Producto {producto_actual + 1} sin stock")

    time.sleep(0.1)