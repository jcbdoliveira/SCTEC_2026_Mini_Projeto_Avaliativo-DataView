# ==============================================================================
# RF02 – Inspecionar e Descrever os Dados
# ==============================================================================
def inspecionar_dados(df):
    """Exibe informações básicas do DataFrame."""
    print("\n=== INSPEÇÃO INICIAL DO DATASET ===")
    print(f"\nShape: {df.shape} (linhas: {df.shape[0]} X colunas: {df.shape[1]})")
    print(f"\nColunas: {list(df.columns)}")
    print(f"\nTipos de dados:\n{df.dtypes}")
    print(f"\nValores nulos por coluna:\n{df.isnull().sum()}")
    print(f"\nPrimeiros 10 registros:\n{df.head(10).to_string()}")
    print(f"\nUltimos 10 registros:\n{df.tail(10).to_string()}")
    print("\nEstatísticas descritivas:")
    desc = df.describe(include="all")
    print(desc.to_string())
    return desc
