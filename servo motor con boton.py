from machine import Pin, PWM
from time import sleep

# ---------------- CONFIGURACIÓN ----------------

PIN_SERVO = 8
PIN_BOTON = 17

ANGULO_CERRADO = 0
ANGULO_ABIERTO = 45

TIEMPO_APERTURA = 0.03      # Mayor valor = movimiento más lento
TIEMPO_ABIERTO = 3          # Segundos que permanece abierto

MIN_U16 = 2000
MAX_U16 = 8000

# ---------------- HARDWARE ----------------

servo = PWM(Pin(PIN_SERVO))
servo.freq(50)

boton = Pin(PIN_BOTON, Pin.IN, Pin.PULL_UP)

# ---------------- FUNCIONES ----------------

def mover_servo(angulo):
    """Mueve el servo al ángulo indicado."""
    
    angulo = max(ANGULO_CERRADO, min(180, angulo))

    duty = int(
        MIN_U16 +
        (MAX_U16 - MIN_U16) * angulo / 180
    )

    servo.duty_u16(duty)


def abrir_servo():
    """Abre el servo gradualmente."""
    
    for angulo in range(ANGULO_CERRADO, ANGULO_ABIERTO + 1):
        mover_servo(angulo)
        sleep(TIEMPO_APERTURA)


def cerrar_servo():
    """Cierra el servo gradualmente."""
    
    for angulo in range(ANGULO_ABIERTO, ANGULO_CERRADO - 1, -1):
        mover_servo(angulo)
        sleep(TIEMPO_APERTURA)


# Posición inicial
mover_servo(ANGULO_CERRADO)

# ---------------- BUCLE PRINCIPAL ----------------

while True:

    # Con PULL_UP:
    # 1 = sin presionar
    # 0 = presionado
    if boton.value() == 0:

        print("Botón presionado")
        print("Abriendo...")

        abrir_servo()

        print("Manteniéndose abierto...")
        sleep(TIEMPO_ABIERTO)

        print("Cerrando...")
        cerrar_servo()

        # Esperar a que el usuario suelte el botón
        while boton.value() == 0:
            sleep(0.01)

        # Anti-rebote
        sleep(0.2)