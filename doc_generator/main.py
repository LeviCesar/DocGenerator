from pathlib import Path
import os, re, sys

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
    # constrollers
    _list_dir_files: list = [0]
    _doc: list = []
    _main_text_py: str
    
    # infos
    _title: str
    _authors: str
    _date: str
    _stakeholdes_infos: list
    _po_infos: list
    _project_description: str
    
    def __init__(self, *, project_path: str, command: str) -> None:
        path_parts = Path(project_path).parts
        self._title = path_parts[len(path_parts)-1]
        for key, value in locals().items():
            if key not in ['self']:
                self.__setattr__(key, value)
    
    def get_and_filter_files_py(self) -> None:
        """
            Search and get all paths with files .py and pass to list
        """
        for root, _, files in os.walk(Path(self.project_path)):
            for file in files:
                if not re.search(r'\.git|env|venv|libs|__init__\.py|doc_generator', os.path.join(root, file)):
                    if re.search(r'main\.py', os.path.join(root, file)):
                        self._list_dir_files[0] = os.path.join(root, file)
                    elif re.search(r'\.py', os.path.join(root, file)):
                        self._list_dir_files.append(os.path.join(root, file))
    
    def _read_py_file(self) -> None:
        """
            Read files and get text
        """
        for index in range(0, self._list_dir_files):
            with open(self._list_dir_files[index], 'r') as file:
                if index == 0:
                    self._main_text_py = file.read()
                    self._extract_documentation_from_files_py(self._main_text_py)
                else:
                    text_py = file.read()
                    self._extract_documentation_from_files_py(text_py)

    def _extract_documentation_from_files_py(self, text_py) -> None:
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
        information = re.findall(
            r'([classdef]{1,5} .+? *:)\n *["""\'\'\']{1,3}\n *(.+?)\n *["""\'\'\']{1,3}', 
            text_py, re.IGNORECASE)
        if information != []:
            self._doc.append(information)
                

    def _extract_authors_from_main_py(self) -> None:
        """
            Get list of authors from main.py
        """
        self._authors = list(re.search(r'__authors__ *= *\[(.+?)\]', self._main_text_py, re.IGNORECASE))
    
    def _extract_stakeholdes_infos_from_main_py(self) -> None:
        """
            Get infos of stakeholders from main.py
        """
        self._stakeholdes_infos = list(re.search(r'__stakeholder_infos__ *= *\[(.+?)\]', self._main_text_py, re.IGNORECASE))
    
    def _extract_po_infos_from_main_py(self) -> None:
        """
            Get infos of PO from main.py
        """
        self._po_infos = list(re.search(r'__po_infos__ *= *\[(.+?)\]', self._main_text_py, re.IGNORECASE))
    
    def _extract_date_from_main_py(self) -> None:
        """
            Get date from main.py
        """
        self._date = re.search(r'__date__ *= *\[(.+?)\]', self._main_text_py, re.IGNORECASE)
    
    def _extract_description_from_main_py(self) -> None:
        """
            Get description of project from main.py
        """
        self._description = re.search(r'["""\'\'\']{1,3}\n *(.+?) *["""\'\'\']{1,3}\n', self._main_text_py, re.IGNORECASE)
    
    def _extract_databases(self):
        """
            Search for databases names and atribute to instance class
        """
        pass
    
    def _extract_tables(self):
        """
            Search for tables names and atribute to instance class
        """
        pass
    
    def _get_Dockerfile(self):
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
            Start process and Create file .md with configs default
        """
        pass

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
        project_path = sys.argv[2]
        
        if len(sys.argv) > 3:
            raise ArgumentsExceeded()
        elif command not in ['update', 'build']:
            raise CommandError(command)
        elif not Path(project_path).is_dir():
            raise PathNotFound(project_path)
        
        documentation = DocGenerator(
            command=command, project_path=project_path)
        
        documentation.get_files_py()
        documentation.extract_infos_from_files_py()
    except Exception as e:
        print(e)