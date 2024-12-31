import json
from API_2 import PresentationAPI




class PresentationAPIExecutor:
    def __init__(self, api, instructions_file):
        """Initialize with the PresentationAPI instance and JSON instructions file."""
        self.api = api
        with open(instructions_file, 'r') as file:
            data = json.load(file)
            self.instructions = data.get('conversations', [])

    def execute_instruction(self, index):
        """Execute a specific instruction by index."""
        if index < 0 or index >= len(self.instructions):
            print(f"Error: Index {index} is out of range. Valid range is 0-{len(self.instructions)-1}")
            return

        conversation = self.instructions[index]
        text = conversation.get('text', '')
        
        print('*'*50)
        print(f"Executing instruction {index}")
        print(f"Conversation text:\n{text}\n")

        # Buscar el código entre los tokens tool_call
        tool_call_start = text.find("<tool_call>")
        tool_call_end = text.find("</tool_call>")
        
        if tool_call_start != -1 and tool_call_end != -1:
            # Extraer el código entre los tokens
            code_to_execute = text[tool_call_start + len("<tool_call>"):tool_call_end].strip()
            
            try:
                print(f"Executing code:\n{code_to_execute}")
                # Asegurarse de que 'api' esté disponible en el contexto de ejecución
                local_vars = {'api': self.api}
                exec(code_to_execute, globals(), local_vars)
            except Exception as e:
                print(f"Error executing code: {e}")
        else:
            print("No tool_call found in this conversation")

# Uso del código
api = PresentationAPI('presentation.pptx')

executor = PresentationAPIExecutor(api, 'formatted_data_new-2.json')
inst = 56


# #full
# executor = PresentationAPIExecutor(api, 'formatted_new_FULLex.json')
# inst = 4

executor.execute_instruction(inst)