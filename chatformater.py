import json

# Leer el archivo JSON original
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Formatear una conversación individual
def format_conversation(item):
    # Extraer la parte del código (entre ### CODE y ### END_CODE)
    code_content = item["output"].split('### CODE\n')[1].split('\n### END_CODE')[0].strip()
    
    # Crear el texto formateado con los tokens de control
    formatted_text = (
        f"<|im_start|>human\n{item['instruction']}<|im_end|>\n"
        f"<|im_start|>assistant\nI'll help you with that.\n\n"
        f"<tool_call>\n{code_content}\n</tool_call><|im_end|>"
    )
    
    return {"text": formatted_text}

# Procesar todo el dataset
def process_dataset(input_file, output_file):
    try:
        # Leer el dataset original
        original_data = read_json_file(input_file)
        
        # Formatear el dataset
        formatted_dataset = {
            "conversations": [
                format_conversation(item)
                for item in original_data
            ]
        }
        
        # Guardar el dataset formateado
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(formatted_dataset, f, indent=2, ensure_ascii=False)
            
        print(f"Dataset procesado exitosamente y guardado en {output_file}")
        
    except Exception as e:
        print(f"Error procesando el dataset: {str(e)}")

# Ejecutar la conversión
if __name__ == "__main__":
    input_file = "data.json"
    output_file = "formatted_data.json"
    process_dataset(input_file, output_file)