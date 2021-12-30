from pathlib import Path
import os, re, sys

"""
- Encontrar arquivos .py OK
- Filtrar excluindo os que estiverem em [libs./, __init__.py, env, venv, \.git] OK
- Filtrar main.py:
- pegar descrição do projeto em main.py OK
- pegar __authors__ do projeto em main.py OK
- pegar __stakeholder_infos__ do projeto em main.py OK
- pegar __po_infos__ do projeto em main.py OK
- pegar __date__ do projeto em main.py OK
- pegar classes e comentários de classe OK
- pegar funções, atributos e comentários de funções OK

- escrever o arquivo em um .md
- reciclar arquivo .md se ele já existir

- requerimentos:
    - precisa ser passado o diretório raiz do projeto
    - o nome da ação que deseja ser realizado (build, update)
"""

class DocGenerator:
    # constrollers
    _list_dir_files: list = [0]
    _documentation: list = []
    _main_text_py: str
    
    # infos
    _title: str
    _authors: str
    _date: str
    _stakeholdes_infos: list
    _po_infos: list
    _project_description: str
    
    # utils
    _databases_mysql: list
    _databases_mongo: list
    _rabbit_infos: list
    _dockerfile_infos: dict = {}
    
    def __init__(self, *, project_path: str, command: str) -> None:
        super().__init__()
        path_parts = Path(project_path).parts
        self._title = path_parts[len(path_parts)-1]
        self.project_path = project_path
        self.__getattribute__(command)()
    
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
            self._documentation.append(information)                

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
    
    def _extract_url_docker_from_main_py(self) -> None:
        """
            Get url docker of project from main.py
        """
        self._dockerfile_infos['urls_docker'] = re.search(r'__url_docker__ *= *\[(.+?)\]', self._main_text_py, re.IGNORECASE)
    
    def _extract_databases(self, text_py: str):
        """
            Search for databases names and atribute to instance class
        """
        pass
    
    def _extract_tables(self, text_py: str):
        """
            Search for tables names and atribute to instance class
        """
        pass
    
    def _extract_infos_rabbit(self, text_py: str):
        """
            Search and get infos about rabbit
        """
        self._rabbit_infos = re.findall(r'RabbitMQ\((.*?)\)', text_py)
        
    
    def _extract_infos_dockerfile(self):
        """
            Search and notate "has dockerfile" for .Dockerfile if has else ignore this function
        """
        with open(Path(self.project_path).joinpath('Dockerfile'), 'r') as file:
            text_docker = file.read()
            self._dockerfile_infos['docker_distro'] = re.search(r'from .*?\n', text_docker, re.IGNORECASE)
            self._dockerfile_infos['code_location'] = re.search(r'workdir .*?\n', text_docker, re.IGNORECASE)
    
    def write_readme(self):
        """
            Write an README.md file to documentation
        """
        
        text_readme = f'''
        # {self._title}
        
        ## Autores
        
        -
        
        ## Stakeholder
        
        -
        
        ## PO
        
        -
        
        ## Data de Criação
        
        - **{self._date}**
        
        ## Descrição do Projeto
        
        {self._description}
        
        
        ## Documentação Técnica
        
        -
        
        ## Utils
        
        ### Rabbit
        
        - 
        
        ### Docker
        
        ### Banco de dados
        
        - Mysql
            - Database
                - Tabelas
        
        - MongoDB
            - Database
                - Collections

        ## Configurações de ambiente

        - python 3.8
        - git
        - .env

        ```bash
        # Clone o repositório
        $ git clone <nome do repositorio>

        # Instale as libs python
        $ python3 -m pip install -r req.txt

        # Em caso de alterações ou acrescimo de libs
        $ python3 -m pip freeze > req.txt

        ````
        
        '''
        
    # executors
    def update(self):
        """
            If .md exists recycle title, author, date, description, environment_config,  else ignore this function.
        """
        pass
    
    def build(self):
        """
            Start process and Create file .md with configs default
        """
        self._read_py_file()

class CommandError(Exception):
    def __init__(self, command):
        super().__init__(f'Not found command name {command}')
        self.errors = __class__.__name__
        print(__class__.__name__)
        
class PathNotFound(Exception):
    def __init__(self, path):
        super().__init__(f'Not found project path {path}')
        self.errors = __class__.__name__
        print(__class__.__name__)

class ArgumentsExceeded(Exception):
    def __init__(self):
        super().__init__('Number of args exceeded')
        self.errors = __class__.__name__
        print(__class__.__name__)
    
class ArgumentsNecessary(Exception):
    def __init__(self):
        super().__init__('Need command and project_path')
        self.errors = __class__.__name__
        print(__class__.__name__)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        raise ArgumentsNecessary()
    
    command = sys.argv[1]
    project_path = sys.argv[2].replace('\\', '/')
    
    if len(sys.argv) > 3:
        raise ArgumentsExceeded()
    elif command not in ['update', 'build']:
        raise CommandError(command)
    elif not Path(project_path).is_dir():
        raise PathNotFound(project_path)
    
    documentation = DocGenerator(
        command=command, project_path=project_path)