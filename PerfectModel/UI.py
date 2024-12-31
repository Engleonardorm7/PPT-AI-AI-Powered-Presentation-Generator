import os
import streamlit as st
from pyngrok import ngrok
import warnings
warnings.filterwarnings("ignore")  # Para ignorar las advertencias que vemos en el notebook

# Instalar dependencias necesarias (ejecutar esto primero desde la terminal)
"""
pip install reportlab pillow
pip install pdf2image
pip install unsloth
pip install --upgrade --no-cache-dir --no-deps git+https://github.com/unslothai/unsloth.git
pip install huggingface_hub diffusers transformers
pip install --upgrade diffusers transformers accelerate
pip install streamlit ipython python-pptx pyngrok
"""

def main():
    # Configurar el directorio de trabajo
    # Ajusta esta ruta a tu estructura de directorios local
    working_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(working_directory)
    
    # Configurar Streamlit
    st.set_page_config(page_title="Interfaz Gráfica Sencilla")
    st.write("Loading app...")
    
    # Si quieres usar ngrok para acceso remoto (opcional)
    # Necesitarás configurar tu token de ngrok primero
    try:
        public_url = ngrok.connect(7860)
        print(f"La API es accesible públicamente en: {public_url}")
    except Exception as e:
        print(f"No se pudo establecer conexión con ngrok: {e}")
    
    # Ejecutar la interfaz principal
    # Asegúrate de que interface.py esté en el mismo directorio
    with open("interface.py", "r", encoding='utf-8') as file:
        exec(file.read())

if __name__ == "__main__":
    main()

# import torch
# print(f"CUDA disponible: {torch.cuda.is_available()}")
# print(f"Versión de PyTorch: {torch.__version__}")