"""
LUXAR — Pipeline de processamento INE EPH (Estatísticas de Preços da Habitação ao Nível Local)
Foco: Península de Setúbal (NUTS 1B) e municípios

Fontes: INE EPH Q1–Q4 2025 (Excel, dados trimestrais desde Q1 2019)
Output: Parquet + CSV em processed/ine_eph/

Uso:
    python scripts/01_processar_ine_eph_setubal.py
"""

import re
from pathlib import Path

import duckdb
import pandas as pd

# ─── Configuração ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent

# Path explícito e verificado: o setup_dados_setubal.sh descarrega para ~/EMPRESA/,
# não para ~/Desktop/EMPRESA/ (onde vive este projecto). Resolvido com path absoluto.
RAW_INE = Path("/Users/tiagoantunes/EMPRESA/03_DADOS/raw/ine")
PROCESSED_DIR = BASE_DIR / "processed/ine_eph"

# Ficheiro de referência: Q4 2025 tem a série completa Q1 2019 → Q4 2025
XLSX_FILE = RAW_INE / "INE_EPH_NL_Q4_2025_Quadros.xlsx"

# Verificação de integridade ao arrancar
if not XLSX_FILE.exists():
    raise FileNotFoundError(
        f"Ficheiro INE não encontrado: {XLSX_FILE}\n"
        f"Executa primeiro: bash raw/setup_dados_setubal.sh"
    )
if XLSX_FILE.stat().st_size < 500_000:
    raise ValueError(
        f"Ficheiro suspeito — tamanho abaixo de 500 KB: {XLSX_FILE.stat().st_size} bytes"
    )

# Códigos NUTS a incluir: Península de Setúbal e seus municípios
SETUBAL_NUTS_PREFIX = "1B"

# Mapeamento de tipo de território para o dataset
TIPO_NUTS = {
    "1B": "sub-região",
    "1B0": "sub-região",
}


# ─── Utilitários ──────────────────────────────────────────────────────────────


def parse_trimestre(label: str) -> tuple[int, int]:
    """Converte '4ºT 2025' ou '3ºT2024' em (ano, trimestre)."""
    label = label.strip()
    m = re.search(r"(\d)º[Tt]\s*(\d{4})", label)
    if not m:
        raise ValueError(f"Formato de trimestre desconhecido: {label!r}")
    return int(m.group(2)), int(m.group(1))


def trimestre_para_data(ano: int, trimestre: int) -> str:
    """Converte (2025, 4) → '2025-10-01' (primeiro dia do trimestre)."""
    mes_inicio = {1: 1, 2: 4, 3: 7, 4: 10}
    return f"{ano}-{mes_inicio[trimestre]:02d}-01"


def extrair_bloco_wide(ws, sheet_name: str) -> pd.DataFrame:
    """
    Extrai o primeiro bloco de dados (valores absolutos) de uma sheet wide do EPH.
    Devolve DataFrame com colunas: cod, designacao, <trimestre_label>...
    """
    rows = list(ws.iter_rows(values_only=True))

    # Linha 2 (índice 1) tem os títulos das métricas; linha 3 (índice 2) tem os trimestres
    quarter_labels = rows[2]  # 3ª linha (0-indexed: 2)

    # Identificar colunas do bloco 1 (antes da primeira coluna vazia)
    data_cols = []
    for i, label in enumerate(quarter_labels):
        if i < 2:
            continue  # cols A e B são código e designação
        if label is None:
            break  # encontrou separador → fim do bloco 1
        data_cols.append((i, str(label)))

    records = []
    for row in rows[3:]:  # dados começam na linha 4
        if row[0] is None or str(row[0]).startswith("Fonte"):
            continue
        rec = {"cod": str(row[0]), "designacao": str(row[1]) if row[1] else ""}
        for col_idx, label in data_cols:
            rec[label] = row[col_idx]
        records.append(rec)

    df = pd.DataFrame(records)
    print(f"  [{sheet_name}] {len(df)} territórios × {len(data_cols)} trimestres")
    return df, data_cols


def wide_para_long(df_wide, data_cols, metric_name: str) -> pd.DataFrame:
    """Converte formato wide → long e cria coluna de data padronizada."""
    id_cols = ["cod", "designacao"]
    value_cols = [label for _, label in data_cols]

    df_long = df_wide.melt(
        id_vars=id_cols,
        value_vars=value_cols,
        var_name="trimestre_label",
        value_name=metric_name,
    )

    parsed = df_long["trimestre_label"].map(lambda x: parse_trimestre(x))
    df_long["ano"] = parsed.map(lambda x: x[0])
    df_long["trimestre"] = parsed.map(lambda x: x[1])
    df_long["data"] = df_long.apply(
        lambda r: trimestre_para_data(r["ano"], r["trimestre"]), axis=1
    )

    # Converter para numérico; '//' significa confidencial → NaN
    df_long[metric_name] = pd.to_numeric(df_long[metric_name], errors="coerce")

    return df_long[["cod", "designacao", "data", "ano", "trimestre", metric_name]]


# ─── Extracção e processamento ────────────────────────────────────────────────


def processar_eph(xlsx_path: Path) -> pd.DataFrame:
    print(f"\nA ler: {xlsx_path.name}")
    import openpyxl

    wb = openpyxl.load_workbook(xlsx_path, data_only=True)

    # Sheet 1: preço mediano por m²
    ws_preco = wb["Trimestral1_N2024"]
    df_preco_wide, cols_preco = extrair_bloco_wide(ws_preco, "Trimestral1_N2024")
    df_preco = wide_para_long(df_preco_wide, cols_preco, "preco_mediano_m2")

    # Sheet 2: número de transações
    ws_transacoes = wb["Nº transações alojamentos_N2024"]
    df_trans_wide, cols_trans = extrair_bloco_wide(
        ws_transacoes, "Nº transações alojamentos_N2024"
    )
    df_trans = wide_para_long(df_trans_wide, cols_trans, "n_transacoes")

    # Merge por código territorial + data
    df = pd.merge(
        df_preco,
        df_trans[["cod", "data", "n_transacoes"]],
        on=["cod", "data"],
        how="left",
    )

    return df


def filtrar_setubal(df: pd.DataFrame) -> pd.DataFrame:
    """Filtra territórios da Península de Setúbal e sub-regiões."""
    mask = df["cod"].str.startswith(SETUBAL_NUTS_PREFIX)
    df_set = df[mask].copy()

    # Classificar tipo de território
    df_set["tipo_territorio"] = df_set["cod"].apply(
        lambda c: "município" if len(c) > 3 else "sub-região"
    )

    # Ordenar: mais recente primeiro
    df_set = df_set.sort_values(["cod", "data"], ascending=[True, False])

    print(f"\nTerritórios encontrados na Península de Setúbal:")
    for cod, nome in (
        df_set[["cod", "designacao"]].drop_duplicates().values
    ):
        print(f"  {cod}: {nome}")

    return df_set


def enriquecer(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona colunas de período e variação YoY calculada."""
    df = df.copy()

    # Coluna período legível
    df["periodo"] = df["ano"].astype(str) + " Q" + df["trimestre"].astype(str)

    # Ordem cronológica para cálculos
    df = df.sort_values(["cod", "data"])

    # Variação YoY do preço mediano por município
    df["preco_yoy_pct"] = df.groupby("cod")["preco_mediano_m2"].transform(
        lambda s: s.pct_change(4) * 100
    )

    # Variação QoQ do preço mediano
    df["preco_qoq_pct"] = df.groupby("cod")["preco_mediano_m2"].transform(
        lambda s: s.pct_change(1) * 100
    )

    # Variação YoY do número de transações
    df["transacoes_yoy_pct"] = df.groupby("cod")["n_transacoes"].transform(
        lambda s: s.pct_change(4) * 100
    )

    # Tipologia: não disponível por tipologia nesta fonte → "Total"
    df["tipologia"] = "Total"

    # Arredondar a 2 casas decimais
    for col in ["preco_mediano_m2", "preco_yoy_pct", "preco_qoq_pct", "transacoes_yoy_pct"]:
        df[col] = df[col].round(2)

    return df


# ─── Gravação ─────────────────────────────────────────────────────────────────


def guardar(df: pd.DataFrame, nome_base: str) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    parquet_path = PROCESSED_DIR / f"{nome_base}.parquet"
    csv_path = PROCESSED_DIR / f"{nome_base}.csv"

    df.to_parquet(parquet_path, index=False)
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    print(f"\nGuardado:")
    print(f"  Parquet: {parquet_path}")
    print(f"  CSV:     {csv_path}")
    print(f"  Linhas:  {len(df)}")
    print(f"  Colunas: {list(df.columns)}")


# ─── Análises DuckDB ──────────────────────────────────────────────────────────


def analises_duckdb(df: pd.DataFrame) -> None:
    con = duckdb.connect()
    con.register("eph", df)

    print("\n" + "=" * 60)
    print("ANÁLISES BASE — Península de Setúbal")
    print("=" * 60)

    # 1. Último trimestre disponível
    print("\n📊 PREÇO MEDIANO/m² por MUNICÍPIO — Último trimestre (Q4 2025)")
    print("-" * 55)
    q = """
    SELECT designacao AS concelho, preco_mediano_m2,
           preco_yoy_pct AS var_yoy_pct,
           n_transacoes
    FROM eph
    WHERE tipo_territorio = 'município'
      AND data = (SELECT MAX(data) FROM eph WHERE tipo_territorio = 'município')
    ORDER BY preco_mediano_m2 DESC NULLS LAST
    """
    print(con.execute(q).df().to_string(index=False))

    # 2. Evolução da sub-região (1B)
    print("\n📈 EVOLUÇÃO — Península de Setúbal (NUTS 1B) — 2022→2025")
    print("-" * 55)
    q = """
    SELECT periodo, preco_mediano_m2, preco_yoy_pct, n_transacoes
    FROM eph
    WHERE cod = '1B' AND ano >= 2022
    ORDER BY data
    """
    print(con.execute(q).df().to_string(index=False))

    # 3. Ranking de preços — todos os períodos disponíveis
    print("\n🏆 RANKING MÉDIO de PREÇO/m² (média 2023–2025, municípios)")
    print("-" * 55)
    q = """
    SELECT designacao AS concelho,
           ROUND(AVG(preco_mediano_m2), 0) AS preco_medio,
           ROUND(AVG(preco_yoy_pct), 1)   AS var_yoy_media,
           SUM(n_transacoes)               AS total_transacoes
    FROM eph
    WHERE tipo_territorio = 'município' AND ano >= 2023
    GROUP BY designacao
    ORDER BY preco_medio DESC NULLS LAST
    """
    print(con.execute(q).df().to_string(index=False))

    con.close()


# ─── Main ─────────────────────────────────────────────────────────────────────


def main() -> None:
    # Processamento
    df_raw = processar_eph(XLSX_FILE)
    df_setubal = filtrar_setubal(df_raw)
    df_final = enriquecer(df_setubal)

    # Dataset completo (todos territórios Setúbal)
    guardar(df_final, "ine_eph_setubal_trimestral")

    # Dataset só municípios
    df_municipios = df_final[df_final["tipo_territorio"] == "município"].copy()
    guardar(df_municipios, "ine_eph_setubal_municipios_trimestral")

    # Análises rápidas
    analises_duckdb(df_final)

    print("\n✅ Pipeline concluído.")


if __name__ == "__main__":
    main()
