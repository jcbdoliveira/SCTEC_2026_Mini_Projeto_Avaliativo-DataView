import pandas as pd
import numpy as np
import random
import os
from datetime import datetime, timedelta

# ==============================================================================
# RF01 – Criar ou Carregar o Dataset de Vendas
# gerarDatasetVendas: gear os dados de vendas sintéticos
# getDatasetVendas: carregar o dataset de vendas a partir de um arquivo CSV.
# ==============================================================================

def gerarDatasetVendas(n_registros=150, seed=42):
    """
    Gera um dataset sintético de vendas com dados propositalmente sujos,
    incluindo valores nulos, strings sujas, datas inválidas e outliers.
    """
    random.seed(seed)
    np.random.seed(seed)
    
    produtos = ['Notebook', 'Smartphone', 'Tablet', 'Monitor', 'Teclado', 'Mouse']
    precos = { 
        'Notebook': 3500, 'Smartphone': 2200, 'Tablet': 1800,
        'Monitor': 1200, 'Teclado': 250, 'Mouse': 120 
    }
    categorias = { 
        "Notebook": "Computadores", "Smartphone": "Celulares",
        "Tablet": "Celulares", "Monitor": "Computadores", "Teclado": "Perifericos",
        "Mouse": "Perifericos" 
    }
    regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]
    clientes = [f"Cliente_{i:03d}" for i in range(1, 31)]
    
    data_inicio = datetime(2024, 1, 1)
    dados = []
    
    for i in range(n_registros):
        produto = random.choice(produtos)
        quantidade = random.randint(1, 10)
        preco = precos[produto]
        data = data_inicio + timedelta(days=random.randint(0, 364))
        
        # Inserindo dados intencionalmente sujos para limpeza
        if random.random() < 0.05:
            quantidade = None  # valor nulo
        if random.random() < 0.04:
            preco = None       # valor nulo
        if random.random() < 0.03:
            produto = "  " + produto + " "  # espaço extra (string suja)
            
        data_str = data.strftime("%Y-%m-%d") if random.random() > 0.02 else "DATA INVALIDA"
        
        # Gerar outliers (valores exorbitantes ou quantidades atípicas para teste)
        if random.random() < 0.04 and quantidade is not None:
            quantidade = quantidade * 12  # Outlier de quantidade
        if random.random() < 0.03 and preco is not None:
            preco = preco * 6             # Outlier de preco

        dados.append({
            "id_venda": i + 1,
            "data_venda": data_str,
            "cliente": random.choice(clientes),
            "produto": produto,
            "categoria": categorias.get(produto.strip() if pd.notna(produto) else "", "Outros"),
            "regiao": random.choice(regioes),
            "quantidade": quantidade,
            "preco_unitario": preco
        })
    salvarDatasetVendas(pd.DataFrame(dados))
    return pd.DataFrame(dados) 

def getDatasetVendas():   
    caminho="https://raw.githubusercontent.com/jcbdoliveira/SCTEC_2026_Mini_Projeto_Avaliativo-DataView/main/data/raw/sales.csv"
    dados = pd.read_csv(caminho)
    print(f"{len(dados)} linhas carregadas.")  
    salvarDatasetVendas(pd.DataFrame(dados))
    return dados

def salvarDatasetVendas(df_bruto):
    arquivo = 'data/raw/vendas.csv'
    if os.path.exists(arquivo):
        os.remove(arquivo)
        print(f"Arquivo existente removido: {arquivo}")

    df_bruto.to_csv(arquivo, index=False)

    print(f"Dataset gerado e salvo com {len(df_bruto)} registros.")
    print(df_bruto.head())