# setup.py
import subprocess
import sys

def install_requirements():
    """
    Instala todas las dependencias necesarias en el orden correcto,
    incluyendo PyTorch con soporte CUDA.
    """
    # Primero instalamos PyTorch con CUDA
    pytorch_cuda_command = [
        "pip3", "install", 
        "torch", "torchvision", "torchaudio", 
        "--index-url", "https://download.pytorch.org/whl/cu118"
    ]
    
    # Luego las demás dependencias
    requirements = [
        "reportlab",
        "pillow",
        "pdf2image",
        "unsloth",
        "huggingface_hub",
        "diffusers",
        "transformers",
        "accelerate",
        "streamlit",
        "ipython",
        "python-pptx",
        "pyngrok"
    ]
    
    print("Instalando PyTorch con soporte CUDA...")
    subprocess.check_call(pytorch_cuda_command)
    
    print("Instalando otras dependencias...")
    for package in requirements:
        print(f"Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("Actualizando packages específicos...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install", 
        "--upgrade", "--no-cache-dir", "--no-deps",
        "git+https://github.com/unslothai/unsloth.git"
    ])
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "--upgrade", "diffusers", "transformers", "accelerate"
    ])

if __name__ == "__main__":
    install_requirements()