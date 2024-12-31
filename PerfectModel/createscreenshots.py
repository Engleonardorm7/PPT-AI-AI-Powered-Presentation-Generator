import os
from win32com import client

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


# Ruta al archivo PPTX
pptx_path = os.path.abspath("presentation.pptx")

# Carpeta de salida para las imágenes
output_folder = "slide_images"

# Generar imágenes de las diapositivas
print("Generando imágenes de las diapositivas...")
images = pptx_to_images(pptx_path, output_folder)
print("Imágenes generadas con éxito:")
print(images)
