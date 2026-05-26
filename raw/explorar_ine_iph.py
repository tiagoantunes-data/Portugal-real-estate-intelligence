import pandas as pd
import os

RAW = '/Users/tiagoantunes/Desktop/EMPRESA/03_DADOS/raw/2026-05_ine_iph_variacao_trimestral.csv'
PROCESSED = '/Users/tiagoantunes/Desktop/EMPRESA/03_DADOS/processed/2026-05_ine_iph_limpo.csv'

df = pd.read_csv(RAW, encoding='latin-1', sep=';', skiprows=3, header=None)
df.columns = ['periodo', 'categoria', 'variacao_pct']
df = df.dropna(subset=['variacao_pct'])
df = df[df['periodo'].str.contains('Trimestre', na=False)]
df = df.reset_index(drop=True)

df['ano'] = df['periodo'].str.extract(r'(\d{4})').astype(int)
df['trimestre_num'] = df['periodo'].str.extract(r'(\d)\.º Trimestre').astype(int)
df['periodo_ordem'] = df['ano'] * 10 + df['trimestre_num']

os.makedirs(os.path.dirname(PROCESSED), exist_ok=True)
df.to_csv(PROCESSED, index=False, encoding='utf-8')

print("Dataset processado:")
print(df.head(10))
print(f"\nShape: {df.shape}")
print(f"\nGuardado em: {PROCESSED}")
