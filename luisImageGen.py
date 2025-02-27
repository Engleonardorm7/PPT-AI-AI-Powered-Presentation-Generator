import requests
import time
import json
import base64
# URL - API
base_url = "https://stable-diffusion-1.ki-awz.iisys.de/sdapi/v1/txt2img"

# Auth cookie 
cookies = {
    "_oauth2_proxy": "djIuWDI5aGRYUm9NbDl3Y205NGVTMWlNRGxrWm1NeE1qUmxZbUUzWmpBeE1qUXlOV016TUdSaU1qQTROalZsTUEuczFqYy1jbll6cGZqdWs4V05td3V3Zw==|1736516098|zEg1JVRUW8662qvJ8phvq_LlAC2TUkA3n1g5pGV6WqM="
}



def generate_image(prompt):
    # Crear la tarea
    payload = {
        "prompt": prompt,   
        "negative_prompt": "",   
        "width": 512,   
        "height": 512,   
        "samples": 1,   
        "seed": 4175255287,   
        "cfg_scale": 7.0,   
        "steps": 100  
    }


    response = requests.post(base_url, json=payload, cookies=cookies)

    if response.status_code == 200:
        # get answer data
        response_data = response.json()
        
        # print answer
        #print(json.dumps(response_data, indent=4))

        if "images" in response_data:
            image_base64 = response_data["images"][0]   
            # decode image base64
            image_data = base64.b64decode(image_base64)
            
            # save image
            with open("generated_image.png", "wb") as img_file:
                img_file.write(image_data)
            print("Imagen generada con éxito.")
        else:
            print("The 'images' field was not found in the response.")
    else:
        print(f"Error generating image: {response.status_code}")
        print(response.text)
    return True

# generate_image("image of a rock band")