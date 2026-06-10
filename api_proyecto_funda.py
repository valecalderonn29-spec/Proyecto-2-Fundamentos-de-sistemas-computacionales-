import requests

def colon_a_dolar(colones):
    #pide el tipo de cambio a la API
    res = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    
    #convierte la respuesta del get en un diccionario .json
    datos = res.json()
    
    #saca  el tipo de cambio del dólar a colones
    tipo_cambio = datos["rates"]["CRC"]
    
    #hace la conversion y redondea a 2 decimales
    return round(colones / tipo_cambio, 2)


#prueba
print(colon_a_dolar(250),"$")