

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import gc
import psutil
import os

print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"Versión de PyTorch: {torch.__version__}")
#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cuda")
       
def load_model(model_path):
    # Limpiar memoria
    gc.collect()
    torch.cuda.empty_cache()
    
    try:
        print("Iniciando carga del modelo...")
         # Cargar el modelo con la configuración original
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,  # Usar la configuración original del modelo
            torch_dtype=torch.float16,#float32
            low_cpu_mem_usage=True
        ).to(device)
        
        print("Cargando tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True
        )
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            
        return model, tokenizer
    
    except Exception as e:
        print(f"Error detallado al cargar el modelo: {str(e)}")
        raise

def generate_response(instruction, model, tokenizer, max_length=512):
    try:
        prompt = f"<|im_start|>human\n{instruction}<|im_end|>\n<|im_start|>assistant\n"
        
        # Procesar input
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        
        print("Iniciando generación...")
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_length=max_length,
                pad_token_id=tokenizer.pad_token_id,
                temperature=0.7,
                do_sample=True,
                top_p=0.95,
                num_return_sequences=1,
                use_cache=True
            )
            print("Generación completada.")
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=False)
        return response
    
    except Exception as e:
        print(f"Error en la generación: {str(e)}")
        raise

def print_memory_status():
    print("\nEstado de la memoria:")
    print(f"CPU - Uso de memoria: {psutil.Process().memory_info().rss / 1024**3:.2f} GB")
    print(f"CPU - Memoria total disponible: {psutil.virtual_memory().total / 1024**3:.2f} GB")
    print(f"CPU - Memoria disponible: {psutil.virtual_memory().available / 1024**3:.2f} GB")
from API2 import PresentationAPI

if __name__ == "__main__":
    api = PresentationAPI('presentation.pptx')
    model_path = r"D:\Leo\AIR Master\2nd Sem\Workstudent\PerfectModel\Qwen2.5_Finetuned2.0"

    try:
        print("\nEstado inicial de memoria:")
        print_memory_status()
        
        print("\nCargando modelo...")
        loaded_model, loaded_tokenizer = load_model(model_path)
        
        print("\nModelo cargado. Estado de memoria:")
        print_memory_status()
        
        instruction = "create am image slide with an image of dragonball"
        print("\nGenerando respuesta...")
        response = generate_response(instruction, loaded_model, loaded_tokenizer)
        
        print("\nRespuesta generada:")
        #print(response)
        if "<tool_call>" in response and "</tool_call>" in response:
            tool_call_code = response.split("<tool_call>")[1].split("</tool_call>")[0].strip()
            print(tool_call_code)      
            exec(tool_call_code)




        print("\nEstado final de memoria:")
        print_memory_status()

    except Exception as e:
        print(f"\nError en la ejecución: {str(e)}")
        print_memory_status()




