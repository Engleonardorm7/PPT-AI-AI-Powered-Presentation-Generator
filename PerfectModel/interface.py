

######################################### WORKING KODE


from API2 import PresentationAPI
import streamlit as st
from pptx import Presentation
from pptx.util import Inches


# Importar las funciones del modelo
from transformers import AutoModelForCausalLM, AutoTokenizer
import io
import torch
import gc

import aspose.slides as slides
import os
from PIL import Image
from win32com import client
import shutil
import stat

#device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

device = torch.device('cuda')     

# Función para cargar el modelo
@st.cache_resource
def load_model(model_path):
    # Limpiar memoria
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    
    try:
        print("Iniciando carga del modelo...")
        # Cargar el modelo con la configuración original
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            trust_remote_code=True,  # Usar la configuración original del modelo
            torch_dtype=torch.float16,#float16,#32
            #low_cpu_mem_usage=True
        )#.to(device)
        
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

# Función para generar una respuesta
def generate_response(instruction, model, tokenizer, max_length=512):
    try:
        prompt = f"<|im_start|>human\n{instruction}<|im_end|>\n<|im_start|>assistant\n"
        
        # Procesar input
        #inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

        inputs = tokenizer(prompt, return_tensors="pt")#.to(device)
        
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


def pptx_to_images(pptx_path, output_folder):
    """
    Exporta cada diapositiva de un archivo PowerPoint como una imagen.

    Args:
        pptx_path (str): Ruta al archivo .pptx.
        output_folder (str): Carpeta donde se guardarán las imágenes.

    Returns:
        List[str]: Lista de rutas a las imágenes generadas.
    """
    # Crear la carpeta de salida si no existe
    os.makedirs(output_folder, exist_ok=True)
    image_paths = []

    # Inicializar PowerPoint
    powerpoint = client.Dispatch("PowerPoint.Application")
    powerpoint.Visible = 1  # Mostrar PowerPoint

    # Abrir la presentación
    presentation = powerpoint.Presentations.Open(pptx_path, WithWindow=False)

    # Exportar cada diapositiva como imagen
    for i, slide in enumerate(presentation.Slides):
        image_path = os.path.abspath(os.path.join(output_folder, f"slide_{i + 1}.png"))
        slide.Export(image_path, "PNG")
        image_paths.append(image_path)
        print(f"Slide {i + 1} exportada a {image_path}")

    # Cerrar PowerPoint
    presentation.Close()
    powerpoint.Quit()

    return image_paths


def clean_up_generated_files():
    def on_rm_error(func, path, exc_info):
        """
        Función auxiliar para manejar archivos bloqueados al eliminar.
        """
        # Cambia los permisos y vuelve a intentar
        os.chmod(path, stat.S_IWRITE)
        func(path)

    try:
        # Eliminar archivo de presentación si existe
        if os.path.exists("presentation.pptx"):
            os.remove("presentation.pptx")
            print("Deleted presentation.pptx")
        
        # Eliminar carpeta de imágenes (forzando permisos si es necesario)
        if os.path.exists("slide_images") and os.path.isdir("slide_images"):
            shutil.rmtree("slide_images", onerror=on_rm_error)
            print("Deleted slide_images folder")
        
        st.success("Temporary files cleaned up successfully!")
    except Exception as e:
        st.error(f"Error while cleaning up files: {e}")





# Carpeta temporal para guardar las imágenes
output_folder = "slide_images"
pptx_path = os.path.abspath("presentation.pptx")


# API y funciones necesarias
api = PresentationAPI('presentation.pptx')

# Cargar el modelo
#model_path = "/home/jovyan/2nd semester/PP Model/PerfectModel/Qwen2.5_Finetuned2.0"#for the notebook 
model_path = "Qwen2.5_Finetuned2.0"
model, tokenizer = load_model(model_path)

# Área de entrada de texto




################################### User Interface ###########################################################################
       

st.title("Chatbot Slide-Generator")
user_input = st.text_input("Type your prompt")
if st.button("Generate"):
    if user_input:
        with st.spinner("Generating response..."):
            # Obtener la respuesta del modelo
            response = generate_response(user_input, model, tokenizer)
            
            # Procesar la respuesta para extraer contenido limpio
            if "<|im_start|>assistant" in response:
                content = response.split("<|im_start|>assistant")[1]
                content = content.split("<|im_end|>")[0]
                content = content.split("<userStyle>")[0]
                content = content.split("<tool_call>")[0]
                content_before_tool_call = content.strip()
            else:
                content_before_tool_call = response.strip()

            # Mostrar la respuesta limpia
            st.write(content_before_tool_call)

            # Si hay un <tool_call>, ejecutarlo
            if "<tool_call>" in response and "</tool_call>" in response:
                tool_call_code = response.split("<tool_call>")[1].split("</tool_call>")[0].strip()
                
                st.write("Generated code for tool_call:")
                st.code(tool_call_code)
                
                try:
                    # Validar y ejecutar el código generado
                    exec(tool_call_code)
                    
                    # Leer la presentación generada
                    with open("presentation.pptx", "rb") as ppt_file:
                        ppt_data = ppt_file.read()
                    
                    # Mostrar el botón para descargar la presentación
                    st.success("Slide generated successfully!")
                    st.session_state.ppt_data = ppt_data  # Guardar los datos de la presentación en el estado de la sesión
                    st.session_state.generated = True  # Indicador de que la presentación fue generada
                    
                except SyntaxError as e:
                    st.error(f"Syntax error in tool_call code: {e}")
                
            
            # Generar las imágenes de las diapositivas
            try:
                output_folder = "slide_images"
                #st.info("Generating slide images...")
                images = pptx_to_images(pptx_path, output_folder)
                st.success("Slide images generated successfully!")

                # Mostrar las imágenes en Streamlit
                st.subheader("Slide Previews:")
                image_width = 300
                for image_path in images:
                    st.image(image_path, caption=os.path.basename(image_path), width=image_width)

            except FileNotFoundError:
                st.error("Image not found.")
     

if st.session_state.get("generated", False):
    st.write("Your presentation is ready to download.")
    download_clicked = st.download_button(
        label="Download Presentation",
        data=st.session_state.ppt_data,
        file_name="presentation.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
    )
    
    # Botón manual para limpiar los archivos después de la descarga
    if st.button("Clean Up Files"):
        clean_up_generated_files()
        st.session_state.generated = False

        
