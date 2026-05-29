from machine import Pin
import time
#Valores de los pines
pin_a = Pin(1,Pin.OUT)
pin_b = Pin(2, Pin.OUT)
pin_f = Pin(3,Pin.OUT)
pin_g = Pin(4, Pin.OUT)
pin_c = Pin(5,Pin.OUT)
pin_d = Pin(6, Pin.OUT)
pin_e = Pin(7, Pin.OUT)


#funciones para imprimir el numero
def imprimir_cero():
    pin_a.value(0)
    pin_b.value(0)
    pin_f.value(0)
    pin_g.value(1)
    pin_c.value(0)
    pin_d.value(0)
    pin_e.value(0)
    
def imprimir_uno():
    pin_a.value(1)
    pin_b.value(0)
    pin_f.value(1)
    pin_g.value(1)
    pin_c.value(0)
    pin_d.value(1)
    pin_e.value(1)
    
def imprimir_dos():
    pin_a.value(0)
    pin_b.value(0)
    pin_f.value(1)
    pin_g.value(0)
    pin_c.value(1)
    pin_d.value(0)
    pin_e.value(0)
    
def imprimir_tres():
    pin_a.value(0)
    pin_b.value(0)
    pin_f.value(1)
    pin_g.value(0)
    pin_c.value(0)
    pin_d.value(0)
    pin_e.value(1)
    
def imprimir_cuatro():
    pin_a.value(1)
    pin_b.value(0)
    pin_f.value(0)
    pin_g.value(0)
    pin_c.value(0)
    pin_d.value(1)
    pin_e.value(1)
    
def imprimir_cinco():
    pin_a.value(0)
    pin_b.value(1)
    pin_f.value(0)
    pin_g.value(0)
    pin_c.value(0)
    pin_d.value(0)
    pin_e.value(1)
    
def imprimir_seis():
    pin_a.value(0)
    pin_b.value(1)
    pin_f.value(0)
    pin_g.value(0)
    pin_c.value(0)
    pin_d.value(0)
    pin_e.value(0)
    
def imprimir_siete():
    pin_a.value(0)
    pin_b.value(0)
    pin_f.value(1)
    pin_g.value(1)
    pin_c.value(0)
    pin_d.value(1)
    pin_e.value(1)
    
def imprimir_ocho():
    pin_a.value(0)
    pin_b.value(0)
    pin_f.value(0)
    pin_g.value(0)
    pin_c.value(0)
    pin_d.value(0)
    pin_e.value(0)
    
def imprimir_nueve():
    pin_a.value(0)
    pin_b.value(0)
    pin_f.value(0)
    pin_g.value(0)
    pin_c.value(0)
    pin_d.value(1)
    pin_e.value(1)
    
#funcion para elegir el numero que se va a mostrar 
def mostrar_numero(numero):

    if numero == 0:
        imprimir_cero()

    elif numero == 1:
        imprimir_uno()

    elif numero == 2:
        imprimir_dos()

    elif numero == 3:
        imprimir_tres()

    elif numero == 4:
        imprimir_cuatro()

    elif numero == 5:
        imprimir_cinco()

    elif numero == 6:
        imprimir_seis()

    elif numero == 7:
        imprimir_siete()

    elif numero == 8:
        imprimir_ocho()

    elif numero == 9:
        imprimir_nueve()
        
        
# diccionario que almacena los productos y las cantidades que posee 
productos = {
    "papas": 0,
    "gaseosas": 7,
    "galletas": 5
}

# Mostrar cantidad de unidades que tiene un producto
variable = True

while variable == True:
    mostrar_numero(productos["papas"])

    # Esperar
    time.sleep(1)

    mostrar_numero(productos["gaseosas"])

    time.sleep(1)

    mostrar_numero(productos["galletas"])
    
    time.sleep(1)