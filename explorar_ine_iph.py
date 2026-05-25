import pandas as pd

df = pd.read_csv(
    '/Users/tiagoantunes/EMPRESA/03_DADOS/raw/2026-05_ine_iph_variacao_trimestral.csv',
    encoding='latin-1',
    sep=';',
    skiprows=3
)

print(df.head(10))
print(f"\nShape: {df.shape}")
print(f"\nColunas: {list(df.columns)}")
