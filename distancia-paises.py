import requests
import urllib.parse
import os

# URLs base de la API
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "4a4b6066-9eb0-4b53-9b2d-58ca88dc8bd9"

# Función para obtener coordenadas desde una ciudad
def obtener_coordenadas(ciudad):
    url = geocode_url + urllib.parse.urlencode({
        "q": ciudad, "limit": 1, "key": key
    })

    respuesta = requests.get(url).json()
    if len(respuesta["hits"]) > 0:
        lat = respuesta["hits"][0]["point"]["lat"]
        lng = respuesta["hits"][0]["point"]["lng"]
        nombre = respuesta["hits"][0]["name"]
        return lat, lng, nombre
    else:
        print("No se encontraron resultados para", ciudad)
        return None, None, ciudad

# Bucle principal
while True:
    os.system("cls" if os.name == "nt" else "clear")
    print("=============================================")
    print(" Calculador de distancia Chile - Argentina")
    print("=============================================")
    print("Ingrese 's' para salir.")
    print("Transporte: auto, bicicleta, pie")
    print("=============================================")

    vehiculo = input("Medio de transporte: ").lower()
    if vehiculo == "s":
        break
    if vehiculo not in ["auto", "bicicleta", "pie"]:
        print("Medio no valido. Se usara 'auto'.")
        vehiculo = "auto"

    # Traducir al formato de la API
    if vehiculo == "auto":
        perfil = "car"
    elif vehiculo == "bicicleta":
        perfil = "bike"
    else:
        perfil = "foot"

    origen = input("Ciudad de Origen (Chile): ")
    if origen == "s":
        break
    destino = input("Ciudad de Destino (Argentina): ")
    if destino == "s":
        break

    lat1, lon1, ciudad1 = obtener_coordenadas(origen)
    lat2, lon2, ciudad2 = obtener_coordenadas(destino)

    if lat1 is None or lat2 is None:
        input("Presione Enter para intentar de nuevo...")
        continue

    # Crear URL de ruta
    puntos = f"&point={lat1},{lon1}&point={lat2},{lon2}"
    ruta_url = route_url + urllib.parse.urlencode({
        "vehicle": perfil,
        "key": key
    }) + puntos

    respuesta = requests.get(ruta_url).json()

    if "paths" in respuesta:
        ruta = respuesta["paths"][0]
        distancia_km = ruta["distance"] / 1000
        distancia_millas = distancia_km * 0.621371
        duracion_seg = ruta["time"] / 1000
        horas = int(duracion_seg // 3600)
        minutos = int((duracion_seg % 3600) // 60)
        segundos = int(duracion_seg % 60)

        print("\n=============================================")
        print(f"Desde: {ciudad1}")
        print(f"Hasta: {ciudad2}")
        print(f"Distancia: {distancia_km:.1f} km / {distancia_millas:.1f} millas")
        print(f"Duración estimada: {horas}h {minutos}min {segundos}s")
        print(f"Narrativa: Viajar desde {ciudad1} hasta {ciudad2} en {vehiculo} tomará aproximadamente {horas} horas y {minutos} minutos.")
        print("=============================================")

        # Instrucciones paso a paso
        print("\nInstrucciones del viaje:")
        for paso in ruta["instructions"]:
            texto = paso["text"]
            dist = paso["distance"] / 1000
            print(f"- {texto} ({dist:.1f} km)")
    else:
        print("Error al calcular ruta:", respuesta.get("message", "Sin mensaje."))

    input("\nPresione Enter para continuar...")

