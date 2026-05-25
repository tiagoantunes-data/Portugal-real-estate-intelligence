import pandas as pd
import os

RAW = '/Users/tiagoantunes/EMPRESA/03_DADOS/raw/2026-05_ine_iph_variacao_trimestral.csv'
PROCESSED = '/Users/tiagoantunes/EMPRESA/03_DADOS/processed/2026-05_ine_iph_limpo.csv'

df = pd.read_csv(RAW, encoding='latin-1', sep=';', skiprows=3)

df.columns = ['periodo', 'categoria', 'variacao_pct', 'localizacao']
df = df.dropna(subset=['periodo', 'variacao_pct'])
df = df[df['periodo'].str.contains('Trimestre', na=False)]
df = df[['periodo', 'categoria', 'variacao_pct']].reset_index(drop=True)

os.makedirs(os.path.dirname(PROCESSED), exist_ok=True)
df.to_csv(PROCESSED, index=False, encoding='utf-8')

print("Dataset processado:")
print(df)
print(f"\nGuardado em: {PROCESSED}")
