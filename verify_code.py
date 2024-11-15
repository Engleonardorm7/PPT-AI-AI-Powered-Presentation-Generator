import json
from API_2 import PresentationAPI


class PresentationAPIExecutor:
    def __init__(self, api, instructions_file):
        """Initialize with the PresentationAPI instance and JSON instructions file."""
        self.api = api
        with open(instructions_file, 'r') as file:
            self.instructions = json.load(file)

    def execute_instructions(self):
        """Execute each code block from the JSON instructions."""
        inst=250#ya se termino, el siguiente es el nuevo
        
        
        print('*'*50)
        print(self.instructions[inst]['instruction'])
        # print(f"\nExecuting Instruction {idx+1}: {instruction['instruction']}")
        instructions=self.instructions[inst]
        # Extraer el código entre los delimitadores ###code y ###endcode
        code_block = instructions.get('output', '')
        code_start = code_block.find("### CODE") + len("### CODE")
        code_end = code_block.find("### END_CODE")
        code_to_execute = code_block[code_start:code_end].strip()
        #print(code_to_execute)
        # Ejecutar el código extraído
       
        exec(code_to_execute)
        print(f"Executed code:\n{code_to_execute}")
    

api = PresentationAPI('presentation.pptx')
executor = PresentationAPIExecutor(api, 'data.json')
executor.execute_instructions()


######################################################
#creemos ahora una slide de visial respresentation y q la imagen se incluya ahi en e
# add an image (to the slide)
#create an slide with an image talking about .....