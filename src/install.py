import sys
import os
import subprocess

#Modulo criado para garantir que todas as bilbiotecas necessárias estejam instaladas 
#para o projeto, mesmo que o usuário não tenha um ambiente virtual configurado.

#se precisar de mais alguma biblioteca, basta adicionar o nome dela na lista abaixo. 
required_packages = ["pandas", "numpy", "matplotlib", "seaborn"]

def instalar_pacotes():
    for pkg in required_packages:
        try:
            __import__(pkg)
        except ImportError:
            print(f"Instalando dependência de Python em tempo de execução: {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])    
    
    print("Todas as dependências estão instaladas. O ambiente está pronto para execução do mini-projeto.")

def criar_pastas():
    raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    pastas = [
        os.path.join(raiz, 'data'),
        os.path.join(raiz, 'data', 'raw'),
        os.path.join(raiz, 'data', 'processed'),
        os.path.join(raiz, 'data', 'final'),
        os.path.join(raiz, 'outputs'),
        os.path.join(raiz, 'outputs', 'graficos')
    ]

    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)

    print('Diretórios iniciais criados ou já existentes:')
    for pasta in pastas:
        print(f' - {os.path.relpath(pasta, raiz)}')
