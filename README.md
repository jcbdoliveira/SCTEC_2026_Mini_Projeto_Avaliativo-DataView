# 📊 SCTEC 2026 Mini Projeto Avaliativo: DataView

## 🔍 Sobre o projeto
O **DataView** é um projeto de análise exploratória de dados focado em vendas. Ele utiliza um notebook Python para:

- ler dados de vendas
- limpar e tratar outliers
- transformar e analisar informações
- gerar relatórios e gráficos
- exportar resultados para CSV e JSON

## 📌 O que o projeto analisa

- Receita total e volume de vendas por mês e trimestre
- Produtos e categorias mais lucrativos
- Desempenho regional de vendas
- Segmentação de clientes por nível de gasto: Bronze, Prata e Ouro
- Comparação entre versões de dados sem e com tratamento de outliers (v1 e v2)
- Geração de gráficos (PNG)
- Geração de relatórios em CSV e JSON


## 🎯 Objetivos do projeto

Praticar e demonstrar conceitos de programação e análise de dados em Python, aprendidos durante o curso, incluindo:

- lógica de programação
- variáveis, tipos e operadores
- condicionais (`if`, `elif`, `else`) e laços (`for`, `while`)
- funções, parâmetros, retorno e `lambda`
- leitura e escrita de arquivos CSV e JSON
- manipulação de datas com `datetime`
- uso de expressões regulares com `re`
- análise de dados com `pandas`
- operações numéricas com `NumPy`
- detecção e tratamento de outliers (IQR)
- visualização com `matplotlib` e `seaborn`
- versionamento com GitHub

## 🚀 Como executar

### 💻 Localmente com VS Code

1. Instale Python 3.10+ e o VS Code
2. Abra a pasta do projeto no VS Code
3. Abra o arquivo `dataview.py` e execute o script.

### 💻 Localmente com DOS
1. Esxecute o pronpt MS-Dos
2. Navegue até a pasta do projeto
3. Execute o script (python dataview.py, para ler o dataset sintético ou python dataview.py --csv, para ler o dataset armazendo no github) e com --show para mostrar os gráficos.``

   **python dataview.py** ou 
   **python dataview.py --show** ou
   **python dataview.py --csv --show**


## 📁 Estrutura do projeto

```
SCTEC_2026_Mini_Projeto_Avaliativo-DataView/
├── data/
│   ├── raw/
│   │   └── vendas.csv
│   ├── processed/
│   │   ├── v1_com_outliers/
│   │   │   ├── relatorio_limpeza_v1.json
│   │   │   └── vendas_v1.csv
│   │   └── v2_outliers_tratado/
│   │       └── vendas_v2.csv
│   └── final/
│       └── vendas_final.csv
├── notebooks/
│   └── dataview.ipynb
├── outputs/
│   ├── estatisticas_gerais.json
│   ├── metricas_por_mes.csv
│   ├── segmentacao_clientes.csv
│   └── graficos/
│           ├── categorias.png
│           ├── dist_regiao.png
│           ├── receita_por_mes.png
│           └── top_produtos.png
├── pdf/
│   └── Desenvolvedor(a) em IA para Análise Preditiva [T2] - M1S08 - Mini-Projeto Avaliativo.pdf
├── src/
│   ├── conversionData.py
│   ├── generateData.py
│   ├── inspectData.py
│   └── install.py
├── dataview.py
└── README.md
```

## 🛠️ Ferramentas utilizadas

- Python **3.10+**
- pandas **v_2.3.3**
- numpy **v_2.2.6**
- matplotlib **v_3.10.9**
- seaborn **v_0.13.2**
- re **v_2.2.1**
- datetime **v_3.10+**
- Git / GitHub
- Copilot
- Gemini
- aistudio.google.com
- VSCode **v_1.125.1**
- Windows 10 x64 **v_10.0.19045**

## 🎥 Demonstração

- [Inserir link do Google Drive ou YouTube aqui]

## ✅ Resultado esperado

Ao finalizar, o projeto entrega:

- instala as dependencias de biblioteca de forma automatica e silenciosa
- cria as pastas de tarabalho de forma centralizada e transparente.
- análise de vendas e métricas por período
- segmentação de clientes por comportamento de compra
- relatórios exportados em CSV e JSON
- relatorio de limpeza exportado em JSON na pasta **data/processed/v1_com_outliers/relatorio_limpeza_v1.json**
- gráficos e visualizações para apoiar decisões

## 📌 Conclusões
- todo o mini projeto foi basedo no arquivo **Desenvolvedor(a) em IA para Análise Preditiva [T2] - M1S08 - Mini-Projeto Avaliativo.pdf**, que esta na pasta pdf deste repositório.
- neste arquivo encontramos um esqueleto/roteiro completo para o desenvolvimento.
- apesar de existir o arquivo **notebooks/dataview.ipynb**, resolvi fazer o projeto no VSCode, sendo o arquivo .ipynb gerado por IA com base no .py
- está decisão foi uma forma de me testar e entregar um produto mais proximo da realidade comercial.
- distribui o código em varios arquivos dentro da pasta src, isto me fez aprender como referenciar módulos de outros arquivos (**from src.MODULO import**)
- na limpeza de dados optei por **remover** os outliers por querer dados mais confiáveis e representativos, e também por achar esta abordagem mais utilizada e clássica.

Mafra, 21 de junho de 2.026.