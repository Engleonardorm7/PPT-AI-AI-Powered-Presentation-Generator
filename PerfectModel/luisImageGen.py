import requests
import time
import json
import base64
# URL de la API
base_url = "https://stable-diffusion-1.ki-awz.iisys.de/sdapi/v1/txt2img"

# Cookies de autenticación
cookies = {
    "_oauth2_proxy": "djIuWDI5aGRYUm9NbDl3Y205NGVTMHhOV1ZoTUdGbFpUQXlOalZtTlRZeE1XRXlPV05qTVRKak1XSTJNVFEzTXcuWmtpY1hfdzZRTVBMWFZLMVNKRjVtUQ==|1735628788|pipupY3wTQRbXhU1cUcJWKkDVi0aOfT8AJawUANUDws="
}

# Crear la tarea
payload = {
    "prompt": "A futuristic robot walkin over the see",  # Tu descripción de la imagen
    "negative_prompt": "",  # Si deseas especificar lo que NO quieres en la imagen
    "width": 512,  # Ancho de la imagen
    "height": 512,  # Altura de la imagen
    "samples": 1,  # Número de imágenes a generar
    "seed": 4175255287,  # Semilla para la generación aleatoria (opcional)
    "cfg_scale": 7.0,  # Controla la fidelidad del modelo al prompt
    "steps": 50  # Número de pasos de generación
}


response = requests.post(base_url, json=payload, cookies=cookies)

if response.status_code == 200:
    # Obtener los datos de la respuesta
    response_data = response.json()
    
    # Imprimir la respuesta para ver qué contiene
    print(json.dumps(response_data, indent=4))

    # Acceder a la imagen generada (generalmente en el campo "images")
    if "images" in response_data:
        image_base64 = response_data["images"][0]  # La primera imagen en la lista
        # Decodificar la imagen de base64
        image_data = base64.b64decode(image_base64)
        
        # Guardar la imagen generada
        with open("generated_image.png", "wb") as img_file:
            img_file.write(image_data)
        print("Imagen generada con éxito.")
    else:
        print("No se encontró el campo 'images' en la respuesta.")
else:
    print(f"Error al generar la imagen: {response.status_code}")
    print(response.text)