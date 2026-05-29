import machine
import time

potenciometro = machine.ADC(26)
#se le asigna un GP a cada led
led1 = machine.Pin(15, machine.Pin.OUT)
led2 = machine.Pin(14, machine.Pin.OUT)
led3 = machine.Pin(13, machine.Pin.OUT)
ledv1 = machine.Pin(12, machine.Pin.OUT)
ledv2 =machine.Pin(11, machine.Pin.OUT)
ledv3 =machine.Pin(10, machine.Pin.OUT)
ledman =machine.Pin(9, machine.Pin.OUT)

while True:
    lectura = potenciometro.read_u16()
    valor = lectura // 655  #0 a 100 

    

    # Encender el LED según el intervalo
    if valor <= 33:
        #if stock:
        led1.value(1)
        led2.value(0)
        led3.value(0)
        #else
        ledv1.value(1)
        ledv2.value(0)
        ledv3.value(0)
        
        
    elif valor <= 66:
        #if stock
        led1.value(0)
        led2.value(1)
        led3.value(0)
        #else
        ledv1.value(0)
        ledv2.value(1)   
        ledv3.value(0)
    else:
        #if stock
        led1.value(0)
        led2.value(0)
        led3.value(1)
        #else
        ledv1.value(0)
        ledv2.value(0)
        ledv3.value(1)

    print("Porcentaje", valor)
    time.sleep(0.1)