import pandas as pd
import os

RAW = '/Users/tiagoantunes/Desktop/EMPRESA/03_DADOS/raw/2026-05_ine_transacoes_numero_alojamentos_familiares_nuts.csv'
PROCESSED = '/Users/tiagoantunes/Desktop/EMPRESA/03_DADOS/processed/2026-05_ine_transacoes_numero_alojamentos_familiares_limpo.csv'

df = pd.read_csv(RAW, encoding='latin-1', sep=';', skiprows=12, header=None)
df.columns = ['periodo', 'localizacao', 'numero_transacoes', 'extra']
df = df[['periodo', 'localizacao', 'numero_transacoes']]

df['periodo'] = df['periodo'].ffill()
df['numero_transacoes'] = pd.to_numeric(df['numero_transacoes'], errors='coerce')
df = df.dropna(subset=['numero_transacoes'])
df = df.dropna(subset=['localizacao'])
df = df.reset_index(drop=True)

df['ano'] = df['periodo'].str.extract(r'(\d{4})').astype(int)
df['trimestre_num'] = df['periodo'].str.extract(r'(\d)\.º Trimestre').astype(int)
df['periodo_ordem'] = df['ano'] * 10 + df['trimestre_num']
df['data_trimestre'] = df['ano'].astype(str) + '-Q' + df['trimestre_num'].astype(str)

os.makedirs(os.path.dirname(PROCESSED), exist_ok=True)
df.to_csv(PROCESSED, index=False, encoding='utf-8')

print("Dataset processado:")
print(df.head(10))
print(f"\nShape: {df.shape}")
print(f"\nGuardado em: {PROCESSED}")
