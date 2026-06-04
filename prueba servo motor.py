from machine import Pin, PWM
from time import sleep

servo = PWM(Pin(8))
servo.freq(50)

posicion_actual = 0

def mover_servo(angulo):
    global posicion_actual

    angulo = max(0, min(180, angulo))

    min_u16 = 2000
    max_u16 = 8000

    duty = int(min_u16 + (max_u16 - min_u16) * angulo / 180)
    servo.duty_u16(duty)

    posicion_actual = angulo

while True:

    print("Abriendo...")
    for angulo in range(0, 150):
        mover_servo(angulo)
        sleep(0.01)
        servo.duty_u16(0)

    sleep(1)

    print("Cerrando...")
    for angulo in range(150, -1, -1):
        mover_servo(angulo)
        sleep(0.01)
        servo.duty_u16(0)

    sleep(1)
    