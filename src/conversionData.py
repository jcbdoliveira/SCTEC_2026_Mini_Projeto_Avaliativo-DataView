import pandas as pd
import re
import numpy as np
import json
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==============================================================================
# RF03 – Limpar e Tratar os Dados
# ==============================================================================
def limpar_strings_regex(df, colunas):
    """
    Usa expressões regulares para normalizar colunas de texto:
    - Colapsa múltiplos espaços internos em um único espaço (re.sub)
    - Remove espaços nas pontas da string (.strip())
    - Preserva células nulas sem lançar erro (pd.notna)
    """
    df = df.copy()
    for col in colunas:
        df[col] = df[col].apply(
            lambda s: re.sub(r"\s+", " ", str(s)).strip() if pd.notna(s) else s
        )
    return df

def limpar_dados(df):
    """
    Limpa o DataFrame de vendas em quatro etapas:
    1. Normaliza strings com regex (espaços extras)
    2. Converte datas e remove registros com datas inválidas
    3. Remove linhas com valores nulos em colunas obrigatórias
    4. Garante os tipos numéricos corretos
    Retorna: (df_limpo, relatorio)
    """
    df = df.copy()
    n_inicial = len(df)
    relatorio = {}
    
    # --- Etapa 1: limpeza de strings com regex ---
    colunas_texto = df.select_dtypes(include="object").columns
    df = limpar_strings_regex(df, colunas_texto)
    
    # --- Etapa 2: conversão de datas ---
    df["data_venda"] = pd.to_datetime(df["data_venda"], errors="coerce")
    relatorio["datas_invalidas_removidas"] = int(df["data_venda"].isnull().sum())
    df = df.dropna(subset=["data_venda"])
    
    # --- Etapa 3: remoção de nulos em colunas obrigatórias ---
    n_antes = len(df)
    df = df.dropna(subset=["quantidade", "preco_unitario"])
    relatorio["linhas_nulas_removidas"] = n_antes - len(df)
    
    # --- Etapa 4: garantia de tipos numéricos ---
    df["quantidade"] = df["quantidade"].astype(int)
    df["preco_unitario"] = df["preco_unitario"].astype(float)
    
    # --- Relatório final ---
    relatorio["registros_iniciais"] = n_inicial
    relatorio["registros_finais"] = len(df)
    relatorio["registros_removidos_total"] = n_inicial - len(df)
    
    print("\n=== RELATORIO DE LIMPEZA ===")
    for k, v in relatorio.items():
        print(f"  {k}: {v}")
        
    return df, relatorio

# ==============================================================================
# RF04 – Detectar e Tratar Outliers (versões v1 e v2)
# ==============================================================================
def tratar_outliers(df, colunas, fator=1.5, metodo='remover'):
    """
    Trata outliers de colunas numéricas usando o Intervalo Interquartil (IQR).
    Parâmetros:
        colunas : lista de colunas numéricas a verificar
        fator : multiplicador do IQR para definir os limites (padrão=1.5)
        metodo : 'remover' exclui as linhas com outliers;
                'limitar' aplica winsorização (substitui pelo limite)
    """
    df = df.copy()
    for col in colunas:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lim_inf = q1 - fator * iqr
        lim_sup = q3 + fator * iqr
        
        n_out = ((df[col] < lim_inf) | (df[col] > lim_sup)).sum()
        print(f'  Outliers em {col}: {n_out} detectados (lim_inf={lim_inf:.2f}, lim_sup={lim_sup:.2f})')
        
        if metodo == 'remover':
            df = df[(df[col] >= lim_inf) & (df[col] <= lim_sup)]
        else:
            df[col] = df[col].clip(lower=lim_inf, upper=lim_sup)
            
    return df

# ==============================================================================
# RF05 – Criar Colunas Derivadas com Transformações
# ==============================================================================
def criar_colunas_derivadas(df):
    """
    Cria colunas calculadas a partir do dataset limpo:
    - receita_total : valor total da linha de venda (quantidade x preço)
    - mes / trimestre / ano : componentes extraídos da data
    - faixa_receita_item : classificação do valor de cada venda (np.select)
    """
    df = df.copy()
    
    # Receita por linha
    df["receita_total"] = df["quantidade"] * df["preco_unitario"]
    
    # Componentes de data
    df["mes"] = df["data_venda"].dt.month
    df["trimestre"] = df["data_venda"].dt.quarter.apply(lambda q: f"Q{q}")
    df["ano"] = df["data_venda"].dt.year
    
    # Classificação condicional usando np.select
    condicoes = [
        df["receita_total"] < 500,
        (df["receita_total"] >= 500) & (df["receita_total"] < 5000),
        df["receita_total"] >= 5000,
    ]
    rotulos = ["Baixo Valor", "Médio Valor", "Alto Valor"]
    df["faixa_receita_item"] = np.select(condicoes, rotulos, default="N/D")
    
    print("\nCOLUNAS DERIVADAS CRIADAS")
    print(df[["data_venda", "receita_total", "mes", "trimestre", "faixa_receita_item"]].head().to_string())
    return df

# ==============================================================================
# RF10 – Organizar o Código em Funções Reutilizáveis & Ordem Superior
# ==============================================================================
def aplicar_transformacao(df, coluna, funcao):
    """
    Função de ordem superior: aplica qualquer função (incluindo lambdas)
    a uma coluna do DataFrame, criando uma coluna '_transformado'.
    Retorna uma cópia do DataFrame com a nova coluna; não modifica o original.
    """
    df = df.copy()
    df[f"{coluna}_transformado"] = df[coluna].apply(funcao)
    return df

# ==============================================================================
# RF06 – Calcular Métricas Agregadas (groupby)
# ==============================================================================
def calcular_metricas(df):
    """
    Calcula e retorna um dicionário com métricas agregadas por quatro dimensões:
    mês, produto, categoria e região.
    """
    metricas = {}
    
    # Receita e volume por mês
    metricas["por_mes"] = (
        df.groupby("mes")
        .agg(
            receita_total=("receita_total", "sum"),
            quantidade=("quantidade", "sum"),
            n_vendas=("id_venda", "count"),
        )
        .reset_index()
        .sort_values("mes")
    )
    
    # Top 5 produtos por receita total
    metricas["top_produtos"] = (
        df.groupby("produto")["receita_total"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )
    
    # Receita por categoria
    metricas["por_categoria"] = (
        df.groupby("categoria")["receita_total"]
        .sum()
        .reset_index()
        .sort_values("receita_total", ascending=False)
    )
    
    # Receita e ticket médio por região
    metricas["por_regiao"] = (
        df.groupby("regiao")
        .agg(
            receita_total=("receita_total", "sum"),
            media_ticket=("receita_total", "mean"),
        )
        .reset_index()
        .sort_values("receita_total", ascending=False)
    )
    
    # Exbição resumida para conferência no console
    for nome, tabela in metricas.items():
        print(f"\n=== {nome.upper().replace('_', ' ')} ===")
        print(tabela.to_string(index=False))
        
    return metricas

# ==============================================================================
# RF07 – Segmentar Clientes por Nível de Gasto
# ==============================================================================
def segmentar_clientes(df):
    """
    Agrupa os dados por cliente, calcula o total gasto por cada um
    e classifica em Bronze / Prata / Ouro conforme os limites abaixo:
    - Abaixo de R$ 5.000 -> Bronze
    - R$ 5.000 a R$ 15.000 -> Prata
    - Acima de R$ 15.000 -> Ouro
    Utiliza função lambda com condicional encadeado.
    """
    clientes_df = (
        df.groupby("cliente")["receita_total"]
        .sum()
        .reset_index()
    )
    clientes_df.columns = ["cliente", "total_gasto"]
    
    # Lambda com ternário aninhado
    clientes_df["segmento"] = clientes_df["total_gasto"].apply(
        lambda g: "Ouro" if g > 15000 else ("Prata" if g >= 5000 else "Bronze")
    )
    
    clientes_df = clientes_df.sort_values("total_gasto", ascending=False)
    
    print("\n=== SEGMENTAÇÃO DE CLIENTES (Top 10) ===")
    print(clientes_df.head(10).to_string(index=False))
    print(f"\nDistribuição de segmentos:\n{clientes_df['segmento'].value_counts().to_string()}")
    
    return clientes_df

# ==============================================================================
# RF08 – Calcular Estatísticas com NumPy
# ==============================================================================
def calcular_estatisticas_numpy(df):
    """
    Usa NumPy diretamente sobre arrays para calcular estatísticas de receita.
    Demonstra três conceitos:
    1. Operações vetorizadas
    2. Broadcasting (divisão de array por escalar)
    3. Boolean indexing (filtragem rápida com máscara)
    """
    receitas = df["receita_total"].to_numpy()
    
    stats = {
        "media": float(np.mean(receitas)),
        "mediana": float(np.median(receitas)),
        "desvio_padrao": float(np.std(receitas)),
        "total": float(np.sum(receitas)),
        "p25": float(np.percentile(receitas, 25)),
        "p75": float(np.percentile(receitas, 75)),
    }
    
    # Broadcasting: participação percentual de cada venda
    receitas_pct = (receitas / receitas.sum()) * 100
    print("\n=== ESTATÍSTICAS COM NUMPY ===")
    print(f"Participação das 5 maiores vendas no total: {np.sort(receitas_pct)[-5:].round(2)}%")
    
    # Boolean indexing (filtro vetorizado)
    acima_da_media = int((receitas > stats["media"]).sum())
    stats["acima_da_media"] = acima_da_media
    
    for k, v in stats.items():
        if k == "acima_da_media":
            print(f"  {k}: {v} vendas")
        else:
            print(f"  {k}: R$ {v:.2f}")
            
    return stats


# ==============================================================================
# RF09 – Criar Visualizações com Matplotlib e Seaborn
# ==============================================================================
def gerar_visualizacoes(df, metricas, output_dir="outputs/graficos"):
    """
    Gera e exporta 3 gráficos informativos em PNG:
    1. Linha — receita total por mês (tendência ao longo do tempo)
    2. Barras — top 5 produtos por receita (ranking)
    3. Boxplot — distribuição de receita por região (dispensar/outliers)
    """
    os.makedirs(output_dir, exist_ok=True)
    sns.set_theme(style="whitegrid", palette="muted")
    
    meses_abrev = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]
    
    # Gráfico 1: Linha — Receita por Mês
    fig, ax = plt.subplots(figsize=(10, 5))
    pm = metricas["por_mes"]
    
    # Criar mapeamento para garantir que todos os meses estejam presentes de 1 a 12
    meses_disponiveis = pm["mes"].values
    receitas_mapeadas = []
    for m in range(1, 13):
        if m in meses_disponiveis:
            receitas_mapeadas.append(pm[pm["mes"] == m]["receita_total"].values[0])
        else:
            receitas_mapeadas.append(0)
            
    ax.plot(range(1, 13), receitas_mapeadas, marker="o", color="#3b82f6", linewidth=2.5, label="Receita")
    ax.set_title("Receita Total por Mês (2024)", fontsize=14, pad=15, fontweight='bold')
    ax.set_xlabel("Mês")
    ax.set_ylabel("Receita (R$)")
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(meses_abrev)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/receita_por_mes.png", dpi=120)
    plt.close()
    
    # Gráfico 2: Barras Horizontais — Top 5 Produtos
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=metricas["top_produtos"], y="produto", x="receita_total", ax=ax, hue="produto", legend=False)
    ax.set_title("Top 5 Produtos em Receita Total", fontsize=14, pad=15, fontweight='bold')
    ax.set_xlabel("Receita Total (R$)")
    ax.set_ylabel("Produto")
    fig.tight_layout()
    fig.savefig(f"{output_dir}/top_produtos.png", dpi=120)
    plt.close()
    
    # Gráfico 3: Boxplot — Distribuição de Receita por Região
    fig, ax = plt.subplots(figsize=(10, 5))
    # Ordenar as regioes por valor de mediana ou total para ficar mais harmonioso
    sns.boxplot(data=df, x="regiao", y="receita_total", ax=ax, hue="regiao", legend=False)
    ax.set_title("Distribuição de Receita por Região", fontsize=14, pad=15, fontweight='bold')
    ax.set_xlabel("Região")
    ax.set_ylabel("Receita por Venda (R$)")
    plt.xticks(rotation=20)
    fig.tight_layout()
    fig.savefig(f"{output_dir}/dist_regiao.png", dpi=120)
    plt.close()
    
    print(f"3 gráficos salvos em: {output_dir}")


# ==============================================================================
# RF10 – Organizar o Código em Funções Reutilizáveis & Ordem Superior
# ==============================================================================
def aplicar_transformacao(df, coluna, funcao):
    """
    Função de ordem superior: aplica qualquer função (incluindo lambdas)
    a uma coluna do DataFrame, criando uma coluna '_transformado'.
    Retorna uma cópia do DataFrame com a nova coluna; não modifica o original.
    """
    df = df.copy()
    df[f"{coluna}_transformado"] = df[coluna].apply(funcao)
    return df


# ==============================================================================
# RF11 – Ler e Escrever Arquivos (CSV e JSON)
# ==============================================================================
def exportar_resultados(metricas, clientes, stats):
    """
    Exporta os resultados da análise em dois formatos:
    - CSV : métricas mensais e segmentação de clientes (excel compatibility)
    - JSON: estatísticas gerais calculadas com NumPy
    Lê o JSON de volta para confirmar.
    """
    os.makedirs("outputs", exist_ok=True)
    
    # --- Exportação CSV ---
    # encoding="utf-8-sig" garante compatibilidade com MS Excel
    metricas["por_mes"].to_csv(
        "outputs/metricas_por_mes.csv", index=False, encoding="utf-8-sig"
    )
    print("CSV exportado: outputs/metricas_por_mes.csv")
    
    clientes.to_csv(
        "outputs/segmentacao_clientes.csv", index=False, encoding="utf-8-sig"
    )
    print("CSV exportado: outputs/segmentacao_clientes.csv")
    
    # --- Exportação JSON ---
    stats_serializaveis = {k: round(float(v), 2) for k, v in stats.items()}
    caminho_json = "outputs/estatisticas_gerais.json"
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(stats_serializaveis, f, indent=2, ensure_ascii=False)
    print(f"JSON exportado: {caminho_json}")
    
    # --- Leitura de volta para confirmar ---
    with open(caminho_json, "r", encoding="utf-8") as f:
        lido = json.load(f)
    print("\nJSON lido de volta para confirmação:")
    print(json.dumps(lido, indent=2, ensure_ascii=False))