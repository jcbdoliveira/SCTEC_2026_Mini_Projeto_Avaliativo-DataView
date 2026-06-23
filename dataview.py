from src.install import instalar_pacotes, criar_pastas
# Garantir que as dependências estejam instaladas
instalar_pacotes()

# Importação de bibliotecas
import sys
import os
import json
import pandas as pd
#------------------------------------------------------

from src.generateData import getDatasetVendas, gerarDatasetVendas
from src.inspectData import inspecionar_dados
#from conversionData import limpar_dados, 
#                           tratar_outliers, 
#                           criar_colunas_derivadas, 
#                           aplicar_transformacao
#como ficou muito grnade a importação, usei *
from src.conversionData import *

def main():
    print("Iniciando Pipeline de ETL DataView...")
    #------------------------------------------------------
    # 0. Preparação do ambiente (instalação de pacotes e criação de pastas)    
    # Garantir que as dependências estejam instaladas
    instalar_pacotes()
    # Garantir que os diretórios principais existam
    criar_pastas()
    #------------------------------------------------------
    
    #------------------------------------------------------
    # 1. Geração de dados sintéticos em um novo dataset ou carregando de um CSV existente.
    # Se passado argumento "--csv", carrega o dataset existente.
    # Caso contrário, gera um novo dataset.
    mostra_grafico = False
    vem_CSV = False
    if len(sys.argv) > 1 and sys.argv[1].lower() in ('--csv', 'csv', 'carregar'):
        vem_CSV = True
        print("Carregando dataset de vendas...")
        dataset_vendas = getDatasetVendas()
        
        if len(sys.argv) > 2 and sys.argv[2].lower() in ('--show'):
            mostra_grafico = True

    else:
        print("Gerando novo dataset de vendas...")
        dataset_vendas = gerarDatasetVendas()
        
        if len(sys.argv) > 1 and sys.argv[1].lower() in ('--show'):
            mostra_grafico = True
    #------------------------------------------------------

    #------------------------------------------------------
    # 2. Inspeção Inicial dos Dados
    # Exibe informações básicas, estatísticas e amostras do dataset 
    # para entender sua estrutura e qualidade.
    # head, tail, shape, dtypes, nulos, estatísticas descritivas, etc.
    inspecionar_dados(dataset_vendas)
    #------------------------------------------------------

    #------------------------------------------------------
    # 3. Limpeza Geral dos Dados
    # Aplica as cinco etapas de limpeza: 
    # --- Etapa 1: limpeza de strings com regex ---   
    # --- Etapa 2: conversão de datas ---
    # --- Etapa 3: remoção de nulos em colunas obrigatórias ---
    # --- Etapa 4: garantia de tipos numéricos ---
    # --- Relatório final ---
    df_v1, relatorio = limpar_dados(dataset_vendas)
    #os.makedirs("data/processed/v1_com_outliers", exist_ok=True)
    df_v1.to_csv("data/processed/v1_com_outliers/vendas_v1.csv", index=False)
    with open("data/processed/v1_com_outliers/relatorio_limpeza_v1.json", 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, indent=2, ensure_ascii=False)
    print("\n2. Dataset limpo (com outliers) salvo em data/processed/v1_com_outliers/vendas_v1.csv")
    #------------------------------------------------------

    #------------------------------------------------------
    # 4. Tratamento de Outliers
    # Cópia temporária para detecção de outliers em quantidade e receita_total
    df_v1_tmp = df_v1.copy()
    df_v1_tmp["receita_total"] = df_v1_tmp["quantidade"] * df_v1_tmp["preco_unitario"]

# Utilizado remover outliers pois os dados foram imputados por geração sintetica, ou seja, são erros 
# claros de coleta ou inserção de dados (ex.: idade = 300 anos)..
    print("\n=== DETECÇÃO DE OUTLIERS (IQR) ===")
    df_v2 = tratar_outliers(
        df_v1_tmp,
        colunas=["quantidade", "receita_total"],
        fator=1.5 if vem_CSV == False else 1.0,  # fator mais alto para dados sintéticos, mais rigoroso para dados reais
        metodo='remover'
    )

    ## Histogramas + curva de densidade
    #fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    #
    #sns.histplot(df_v1_tmp["quantidade"], kde=True, ax=axes[0], bins=30, color="steelblue")
    #axes[0].set_title("Distribuição - Quantidade")
    #
    #sns.histplot(df_v1_tmp["receita_total"], kde=True, ax=axes[1], bins=30, color="darkorange")
    #axes[1].set_title("Distribuição - Receita Total")
    #
    #plt.tight_layout()
    #plt.show()

    #df_f15 = tratar_outliers(df_v1_tmp,["quantidade", "receita_total"], fator=1.5, metodo="media")
    #df_f25 = tratar_outliers(df_v1_tmp,["quantidade", "receita_total"], fator=1.5, metodo="remover")
    #df_f30 = tratar_outliers(df_v1_tmp, ["quantidade", "receita_total"], fator=1.0, metodo="remover")

    # Criar subplots
    #fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    # Original
    #sns.boxplot(data=df_v1_tmp, x="regiao", y="receita_total", ax=axes[0, 0])
    #axes[0, 0].set_title("Original")

    # Winsorização (fator=1.5)
    #sns.boxplot(data=df_f15, x="regiao", y="receita_total", ax=axes[0, 1])
    #axes[0, 1].set_title("Winsorização (fator=1.5)")

    # Outliers removidos (fator=2.5)
    #sns.boxplot(data=df_f25, x="regiao", y="receita_total", ax=axes[1, 0])
    #axes[1, 0].set_title("Outliers removidos (fator=1.5)")

    # Outliers removidos (fator=1.0)
    #sns.boxplot(data=df_f30, x="regiao", y="receita_total", ax=axes[1, 1])
    #axes[1, 1].set_title("Outliers removidos (fator=1.0)")

    #plt.tight_layout()
    #plt.show()

    df_v2 = df_v2.drop(columns=["receita_total"])    

    # Exibir diferença
    print(f"\nv1 = {len(df_v1)} linhas (com outliers)")
    print(f"v2 = {len(df_v2)} linhas (outliers removidos)")
    print(f"Diferença = {len(df_v1) - len(df_v2)} linhas removidas pelo IQR")
    
    #os.makedirs("data/processed/v2_outliers_tratado", exist_ok=True)
    df_v2.to_csv("data/processed/v2_outliers_tratado/vendas_v2.csv", index=False)
    print("Dataset tratado (v2) salvo em data/processed/v2_outliers_tratado/vendas_v2.csv")
    #------------------------------------------------------

    #------------------------------------------------------
    # 5. Criar Colunas Derivadas (Trabalhamos sobre df_v2 - versão final limpa e sem outliers)
    print("\nCriando colunas derivadas sobre v2...")
    df_final = criar_colunas_derivadas(df_v2)
    
    # Demostração opcional de Ordem Superior
    print("\n=== DEMO: FUNÇÃO DE ORDEM SUPERIOR ===")
    df_demo = aplicar_transformacao(df_final, "receita_total", lambda x: "Alto" if x > 5000 else "Normal")
    print(df_demo[["receita_total", "receita_total_transformado"]].head(3).to_string())

    # 6. Agregações e Métricas
    print("\nCalculando métricas agrupadas...")
    metricas = calcular_metricas(df_final)

    # 7. Segmentação de Clientes
    print("\nSegmentando clientes...")
    clientes = segmentar_clientes(df_final)
    
    # 8. Estatísticas NumPy
    print("\nEstatísticas NumPy...")
    stats = calcular_estatisticas_numpy(df_final)
    
    # 9. Geração de Gráficos
    print("\nGerando visualizações...")
    gerar_visualizacoes(df_final, metricas, mostra_grafico)

    # 10. Organizar o Código em Funções Reutilizáveis & Ordem Superior
    # df_demo e df_demo2 são apenas demonstrações — df principal não é alterado. 
    df_demo = aplicar_transformacao(df_final, "receita_total", lambda x: "Alto" if x > 5000 else "Normal") 
    print("=== EXEMPLO: classificação por ticket ===") 
    print(df_demo[["receita_total", "receita_total_transformado"]].head()) 

    df_demo2 = aplicar_transformacao(df_final, "receita_total", lambda x: round(x / 1000, 2)) 
    print("\n=== EXEMPLO: receita em milhares (R$ k) ===") 
    print(df_demo2[["receita_total", "receita_total_transformado"]].head())
    
    # 11. Exportação dos Resultados
    print("\nExportando CSVs e JSON...")
    exportar_resultados(metricas, clientes, stats)
    
    # 12. Consolidar e Salvar Dataset Final
    #os.makedirs("data/final", exist_ok=True)
    df_final.to_csv("data/final/vendas_final.csv", index=False)
    print("\nETL CONCLUÍDO COM SUCESSO! Dataset final gravado em data/final/vendas_final.csv")

if __name__ == "__main__":
    main()