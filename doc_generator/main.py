from pathlib import Path
import os, re, datetime, sys

"""
- Encontrar arquivos .py
- Filtrar excluindo os que estiverem em [libs./, __init__.py, env, venv, \.git]
- Filtrar main.py 
- pegar descrição do projeto em main.py
- pegar __authors__ do projeto em main.py
- pegar __stakeholder_infos__ do projeto em main.py
- pegar __po_infos__ do projeto em main.py
- pegar __date__ do projeto em main.py
- pegar classes e comentários de classe
- pegar funções, atributos e comentários de funções

- escrever o arquivo em um .md
- reciclar arquivo .md se ele já existir

- requerimentos:
    - precisa ser passado o diretório raiz do projeto
    - o nome da ação que deseja ser realizado (build, update)
"""

class DocGenerator:
    _list_dir_files: list = [0]
    _informations: list = []
    _database_type: str
    _schemas_db: list
    _tables_db: list
    
    def __init__(self, *, project_dir: str, command: str) -> None:
        for key, value in locals().items():
            if key not in ['self']:
                self.__setattr__(key, value)
    
    def get_and_filter_files_py(self, project_dir: str) -> None:
        """
            Search and get all paths with files .py and pass to list
        """
        for root, _, files in os.walk(Path(project_dir)):
            for file in files:
                if not re.search(r'\.git|env|venv|libs|__init__\.py|doc_generator', os.path.join(root, file)):
                    if re.search(r'main\.py', os.path.join(root, file)):
                        self._list_dir_files[0] = os.path.join(root, file)
                    elif re.search(r'\.py', os.path.join(root, file)):
                        self._list_dir_files.append(os.path.join(root, file))
    
    @staticmethod
    def _filter_infos_tuple(array):
        """
            Filter infos of function_name and commit contained in array attribute
            that is unordered in multiple tuples and union in one tuple
        """
        information = []
        for index in range(0,len(array)):
            if array[index] == '__index__':            
                del array[index]

        for index in range(0,len(array),2):
            function_name = [value for value in array[index] if value != '']
            commit = [value for value in array[index+1] if value != '']
            information.append((function_name[0], commit[0]))
        return information
    
    def extract_documentation_from_files_py(self):
        """
            Get:
            * class name
            * function name
            * function atributes
            * commits of class and functions
            
            Open files with "r" and search for:
            * name betwen "class" and ":"
            * name betwen "def" and "(".
            * commit betwen three quotation marks double or simple
        """
        for file_py in self._list_dir_files:
            with open(file_py, 'r') as file_reader_py:
                text_py = file_reader_py.read()
                information = re.findall(r'class (.+?)[:\(]|def (.+?)\(|:""" *(.+?) *"""|:\'\'\' *(.+?) *\'\'\'', text_py, re.IGNORECASE)
                if information != []:
                    self._informations.append(self._filter_infos_tuple(information))

    def extract_authors_from_main_py(self):
        pass
    
    def extract_stakeholdes_infos_from_main_py(self):
        pass
    
    def extract_po_infos_from_main_py(self):
        pass
    
    def extract_date_from_main_py(self):
        pass
    
    def extract_description_from_main_py(self):
        pass
    
    def extract_databases(self):
        """
            Search for databases names and atribute to instance class
        """
        pass
    
    def extract_tables(self):
        """
            Search for tables names and atribute to instance class
        """
        pass
    
    def get_Dockerfile(self):
        """
            Search and notate "has dockerfile" for .Dockerfile if has else ignore this function
        """
        pass
    
    def update(self):
        """
            If .md exists recycle title, author, date, description, environment_config,  else ignore this function.
        """
        pass
    
    def build(self):
        """
            Create file .md with configs default
        """

class CommandError(Exception):
    def __init__(self, command):
        super().__init__(__class__.__name__)
        self.errors = f'Not found command name {command}'
        print('Printing Errors:')
        print(f'Not found command name {command}')
        
class PathNotFound(Exception):
    def __init__(self, path):
        super().__init__(__class__.__name__)
        self.errors = f'Not found project path {path}'
        print('Printing Errors:')
        print(f'Not found project path {path}')

class ArgumentsExceeded(Exception):
    def __init__(self):
        super().__init__(__class__.__name__)
        self.errors = 'Number of args exceeded'
        print('Printing Errors:')
        print('Number of args exceeded')
    
if __name__ == '__main__':
    try:
        command = sys.argv[1]
        project_dir = sys.argv[2]
        
        if len(sys.argv) > 3:
            raise ArgumentsExceeded()
        elif command not in ['update', 'build']:
            raise CommandError(command)
        elif not Path(project_dir).is_dir():
            raise PathNotFound(project_dir)
        
        documentation = DocGenerator(
            command=command, project_dir=project_dir)
        
        documentation.get_files_py()
        documentation.extract_infos_from_files_py()
    except Exception as e:
        print(e)