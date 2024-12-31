import os
from comtypes.client import CreateObject

def convert_pptx_to_pdf(input_path, output_path):
    try:
        # Crear una instancia de PowerPoint
        powerpoint = CreateObject("PowerPoint.Application")
        powerpoint.Visible = 1  # Para abrir en modo visible, opcional
        
        # Abrir la presentación
        presentation = powerpoint.Presentations.Open(input_path)
        
        # Exportar como PDF
        presentation.SaveAs(output_path, 32)  # 32 es el formato para PDF
        
        # Cerrar la presentación y PowerPoint
        presentation.Close()
        powerpoint.Quit()
        print(f"Archivo convertido exitosamente a: {output_path}")
    except Exception as e:
        print(f"Error durante la conversión: {e}")

# Ruta del archivo de entrada y salida
input_file = "presentation.pptx"
output_file = "presentation.pdf"

# Asegurarse de que las rutas sean absolutas
input_path = os.path.abspath(input_file)
output_path = os.path.abspath(output_file)

convert_pptx_to_pdf(input_path, output_path)
