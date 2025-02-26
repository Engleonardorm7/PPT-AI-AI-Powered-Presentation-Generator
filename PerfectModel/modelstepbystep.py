# GUI

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import gc
import psutil
import os
from API2 import PresentationAPI
import streamlit as st
from pptx import Presentation

print(f"CUDA disponible: {torch.cuda.is_available()}")
print(f"Versión de PyTorch: {torch.__version__}")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
       
@st.cache_resource  # Streamlit cache para recursos pesados como modelos
def load_model(model_path):
    # Limpiar memoria
    gc.collect()
    torch.cuda.empty_cache()
    
    print("Iniciando carga del modelo...")
        # Cargar el modelo con la configuración original
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        trust_remote_code=True,  # Usar la configuración original del modelo
        torch_dtype=torch.float32,#float16,#
        #low_cpu_mem_usage=True
    ).to(device)
    
    print("Cargando tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(
        model_path,
        trust_remote_code=True
    )
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        
    return model, tokenizer

   

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




def pptx_to_images(pptx_path, output_folder):
    """
    Convierte cada diapositiva de un archivo PowerPoint a imágenes PNG.

    Args:
        pptx_path (str): Ruta al archivo .pptx.
        output_folder (str): Carpeta donde se guardarán las imágenes.

    Returns:
        List[str]: Lista de rutas a las imágenes generadas.
    """
    presentation = Presentation(pptx_path)
    slide_images = []

    # Asegúrate de que la carpeta de salida exista
    os.makedirs(output_folder, exist_ok=True)

    for i, slide in enumerate(presentation.slides):
        # Crear una imagen en blanco para cada diapositiva
        img = Image.new("RGB", (1280, 720), color="white")
        draw = ImageDraw.Draw(img)
        text = f"Slide {i + 1}"  # Información básica para ejemplo
        draw.text((50, 50), text, fill="black")  # Agrega texto de ejemplo
        output_path = os.path.join(output_folder, f"slide_{i + 1}.png")
        img.save(output_path)
        slide_images.append(output_path)
    
    return slide_images

# Carpeta temporal para guardar las imágenes
output_folder = "slides_preview"





model_path = r"D:\Leo\AIR Master\2nd Sem\Workstudent\PerfectModel\Qwen2.5_Finetuned2.0"
loaded_model, loaded_tokenizer = load_model(model_path)
#if __name__ == "__main__":



api = PresentationAPI('presentation.pptx')

st.title("Chatbot Slide-Generator")
user_input = st.text_input("Type your prompt")

if st.button("Generate"):
    if user_input:
        print(user_input)
        with st.spinner("Generating response..."):
            try:
                response = generate_response(user_input, loaded_model, loaded_tokenizer)

                if "<|im_start|>assistant" in response:
                    # Obtener el contenido después de "assistant"
                    content = response.split("<|im_start|>assistant")[1]
                    # Eliminar todos los demás tags
                    content = content.split("<|im_end|>")[0]
                    content = content.split("<userStyle>")[0]
                    content = content.split("<tool_call>")[0]
                    content_before_tool_call = content.strip()
                else:
                    content_before_tool_call = response.strip()

                # Mostrar el contenido limpio
                st.write(content_before_tool_call)
            except Exception as e:
                print(f"\nError en la ejecución: {str(e)}")
                print_memory_status()

                if "<tool_call>" in response and "</tool_call>" in response:
                    tool_call_code = response.split("<tool_call>")[1].split("</tool_call>")[0].strip()
                    
                    st.write("Generated code for tool_call:")
                    st.code(tool_call_code)
                
                    try:
                        # Validar y ejecutar el código generado
                        exec(tool_call_code)
                
                        # Read the pptx generated file
                        with open("presentation.pptx", "rb") as ppt_file:
                            ppt_data = ppt_file.read()
                
                        # Download the file
                        st.success("Slide generated successfully!")
                        st.download_button(
                            label="Download Presentation",
                            data=ppt_data,
                            file_name="presentation.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        )
                    except SyntaxError as e:
                        st.error(f"Syntax error in tool_call code: {e}")
                    except Exception as e:
                        st.error(f"Error while executing tool call: {e}")
                        
                    else:
                        st.error("Please enter a text.")
        


            
            ####### preview if image slides (all white)
            try:
                # Generar imágenes de las diapositivas
                slide_images = pptx_to_images("presentation.pptx", output_folder)

                # Mostrar las imágenes generadas en Streamlit
                for slide_image in slide_images:
                    st.image(slide_image, caption=f"Slide {os.path.basename(slide_image)}", use_column_width=True)

            except Exception as e:
                st.error(f"Error al generar imágenes: {e}")
        

    # try:
       
        
    #     instruction = "create a slide talking about streams"
    #     print("\nGenerando respuesta...")
    #     response = generate_response(instruction, loaded_model, loaded_tokenizer)
        
    #     print("\nRespuesta generada:")
    #     #print(response)
    #     if "<tool_call>" in response and "</tool_call>" in response:
    #         tool_call_code = response.split("<tool_call>")[1].split("</tool_call>")[0].strip()
    #         print(tool_call_code)      
    #         exec(tool_call_code)




    #     print("\nEstado final de memoria:")
    #     print_memory_status()

    # except Exception as e:
    #     print(f"\nError en la ejecución: {str(e)}")
    #     print_memory_status()




