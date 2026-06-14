# Importação de bibliotecas
import sys
import os
import pandas as pd
from install import instalar_pacotes, criar_pastas
from generateData import getDatasetVendas, gerarDatasetVendas
from inspectData import inspecionar_dados
#from conversionData import limpar_dados, 
#                           tratar_outliers, 
#                           criar_colunas_derivadas, 
#                           aplicar_transformacao
#como ficou muito grnade a importação, usei *
from conversionData import *

def main():
    print("Iniciando Pipeline de ETL DataView...")
    #------------------------------------------------------
    # 0. Preparação do ambiente (instalação de pacotes e criação de pastas)    
    # Garantir que as dependências estejam instaladas
    instalar_pacotes()
    # Garantir que os diretórios necessários existam
    criar_pastas()
    #------------------------------------------------------

    #------------------------------------------------------
    # 1. Geração de Dados ou Carregamento do Dataset
    # Se passado argumento "--get", carrega o dataset existente.
    # Caso contrário, gera um novo dataset.
    if len(sys.argv) > 1 and sys.argv[1].lower() in ('--get', 'get', 'carregar'):
        print("Carregando dataset de vendas...")
        dataset_vendas = getDatasetVendas()
    else:
        print("Gerando novo dataset de vendas...")
        dataset_vendas = gerarDatasetVendas()
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
    os.makedirs("data/processed/v1_com_outliers", exist_ok=True)
    df_v1.to_csv("data/processed/v1_com_outliers/vendas_v1.csv", index=False)
    relatorio.to_json("data/processed/v1_com_outliers/relatorio_limpeza_v1.csv", orient="records")
    print("\n2. Dataset limpo (com outliers) salvo em data/processed/v1_com_outliers/vendas_v1.csv")
    #------------------------------------------------------

    #------------------------------------------------------
    # 4. Tratamento de Outliers
    # Cópia temporária para detecção de outliers em quantidade e receita_total
    df_v1_tmp = df_v1.copy()
    df_v1_tmp["receita_total"] = df_v1_tmp["quantidade"] * df_v1_tmp["preco_unitario"]
    
    print("\n=== DETECÇÃO DE OUTLIERS (IQR) ===")
    df_v2 = tratar_outliers(
        df_v1_tmp,
        colunas=["quantidade", "receita_total"],
        metodo='remover'
    )
    df_v2 = df_v2.drop(columns=["receita_total"])    

    # Exibir diferença
    print(f"\nv1 = {len(df_v1)} linhas (com outliers)")
    print(f"v2 = {len(df_v2)} linhas (outliers removidos)")
    print(f"Diferença = {len(df_v1) - len(df_v2)} linhas removidas pelo IQR")
    
    os.makedirs("data/processed/v2_outliers_tratado", exist_ok=True)
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
    gerar_visualizacoes(df_final, metricas)
    
    # 10. Exportação dos Resultados
    print("\nExportando CSVs e JSON...")
    exportar_resultados(metricas, clientes, stats)
    
    # 11. Consolidar e Salvar Dataset Final
    os.makedirs("data/final", exist_ok=True)
    df_final.to_csv("data/final/vendas_final.csv", index=False)
    print("\nETL CONCLUÍDO COM SUCESSO! Dataset final gravado em data/final/vendas_final.csv")


if __name__ == "__main__":
    main()