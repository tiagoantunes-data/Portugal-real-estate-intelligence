import pandas as pd
import os

RAW = '/Users/tiagoantunes/Desktop/EMPRESA/03_DADOS/raw/2026-05_ine_transacoes_alojamentos_familiares_nuts.csv'
PROCESSED = '/Users/tiagoantunes/Desktop/EMPRESA/03_DADOS/processed/2026-05_ine_transacoes_alojamentos_familiares_limpo.csv'

df = pd.read_csv(RAW, encoding='utf-8', sep=';', skiprows=12, header=None)
df.columns = ['periodo', 'localizacao', 'valor_milhares_eur', 'extra']
df = df[['periodo', 'localizacao', 'valor_milhares_eur']]

# Forward fill período
df['periodo'] = df['periodo'].ffill()

# Manter só linhas com valor numérico
df['valor_milhares_eur'] = pd.to_numeric(df['valor_milhares_eur'], errors='coerce')
df = df.dropna(subset=['valor_milhares_eur'])
df = df.dropna(subset=['localizacao'])
df = df.reset_index(drop=True)

# Guardar
os.makedirs(os.path.dirname(PROCESSED), exist_ok=True)
df.to_csv(PROCESSED, index=False, encoding='utf-8')

print("Dataset processado:")
print(df.head(20))
print(f"\nShape: {df.shape}")
print(f"\nPeríodos únicos: {df['periodo'].nunique()}")
print(f"Localizações únicas: {df['localizacao'].nunique()}")
print(f"\nGuardado em: {PROCESSED}")