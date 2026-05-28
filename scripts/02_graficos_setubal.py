"""
LUXAR — Gráficos para Dossier de Mercado — Península de Setúbal
Gera PNG de alta resolução prontos para inclusão em PDF.

Uso:
    python scripts/02_graficos_setubal.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# ─── Configuração ─────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent
PROCESSED_DIR = BASE_DIR / "processed/ine_eph"
OUTPUT_DIR = BASE_DIR / "outputs/graficos_setubal"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Paleta LUXAR
CORES_MUNICIPIOS = {
    "Almada":     "#1A3E5C",
    "Seixal":     "#2E6DA4",
    "Sesimbra":   "#3D9BE9",
    "Alcochete":  "#F4A020",
    "Setúbal":    "#E87B1E",
    "Montijo":    "#C45A15",
    "Barreiro":   "#6BAF92",
    "Palmela":    "#4A8A73",
    "Moita":      "#D9534F",
}

COR_SETUBAL_NUTS = "#1A3E5C"
COR_MEDIA_PT     = "#AAAAAA"

FONTE = "Source Sans Pro"
plt.rcParams.update({
    "font.family": "sans-serif",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 150,
})


def salvar(fig: plt.Figure, nome: str) -> None:
    path = OUTPUT_DIR / f"{nome}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✅ {path.name}")


# ─── Carregamento ─────────────────────────────────────────────────────────────

df_todos = pd.read_parquet(PROCESSED_DIR / "ine_eph_setubal_trimestral.parquet")
df_municipios = pd.read_parquet(PROCESSED_DIR / "ine_eph_setubal_municipios_trimestral.parquet")
df_nuts = df_todos[df_todos["cod"] == "1B"].copy()

df_todos["data_dt"] = pd.to_datetime(df_todos["data"])
df_municipios["data_dt"] = pd.to_datetime(df_municipios["data"])
df_nuts["data_dt"] = pd.to_datetime(df_nuts["data"])


# ─── Gráfico 1: Evolução preço mediano/m² — sub-região Setúbal ───────────────

def grafico_evolucao_subreigiao() -> None:
    fig, ax = plt.subplots(figsize=(10, 5))

    ax.plot(
        df_nuts["data_dt"],
        df_nuts["preco_mediano_m2"],
        color=COR_SETUBAL_NUTS,
        linewidth=2.5,
        marker="o",
        markersize=5,
        label="Península de Setúbal",
    )

    # Anotar último valor
    ultimo = df_nuts.dropna(subset=["preco_mediano_m2"]).iloc[-1]
    ax.annotate(
        f"  {int(ultimo['preco_mediano_m2'])} €/m²",
        xy=(ultimo["data_dt"], ultimo["preco_mediano_m2"]),
        fontsize=10,
        color=COR_SETUBAL_NUTS,
        fontweight="bold",
    )

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,} €"))
    ax.set_title(
        "Evolução do Preço Mediano de Habitação por m²\nPenínsula de Setúbal — Q1 2019 a Q4 2025",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.set_xlabel("")
    ax.set_ylabel("€/m²", fontsize=10)

    # Shading por ano
    anos = df_nuts["ano"].unique()
    for i, ano in enumerate(sorted(anos)):
        df_ano = df_nuts[df_nuts["ano"] == ano]
        if len(df_ano) == 0:
            continue
        ax.axvspan(
            df_ano["data_dt"].min(), df_ano["data_dt"].max(),
            alpha=0.04 if i % 2 == 0 else 0,
            color="grey",
        )

    ax.legend(fontsize=9)
    ax.set_xlim(df_nuts["data_dt"].min(), df_nuts["data_dt"].max())
    fig.text(
        0.01, -0.02,
        "Fonte: INE, Estatísticas de Preços da Habitação ao Nível Local (EPH)",
        fontsize=7, color="grey",
    )
    salvar(fig, "01_evolucao_preco_subreigiao")


# ─── Gráfico 2: Evolução preço por município — linhas ────────────────────────

def grafico_evolucao_municipios() -> None:
    # Últimos 4 anos para legibilidade
    df_plot = df_municipios[df_municipios["ano"] >= 2022].dropna(subset=["preco_mediano_m2"])

    fig, ax = plt.subplots(figsize=(12, 6))

    for concelho, df_c in df_plot.groupby("designacao"):
        df_c = df_c.sort_values("data_dt")
        cor = CORES_MUNICIPIOS.get(concelho, "#999999")
        ax.plot(
            df_c["data_dt"], df_c["preco_mediano_m2"],
            color=cor, linewidth=2, marker=".", markersize=6, label=concelho,
        )
        # Anotar último ponto
        ultimo = df_c.dropna(subset=["preco_mediano_m2"]).iloc[-1]
        ax.annotate(
            f" {int(ultimo['preco_mediano_m2'])}",
            xy=(ultimo["data_dt"], ultimo["preco_mediano_m2"]),
            fontsize=8, color=cor, va="center",
        )

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,} €"))
    ax.set_title(
        "Preço Mediano por m² por Município\nPenínsula de Setúbal — 2022 a 2025",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.set_ylabel("€/m²", fontsize=10)
    ax.legend(fontsize=8, ncol=3, loc="upper left")
    ax.set_xlim(df_plot["data_dt"].min(), df_plot["data_dt"].max())
    fig.text(
        0.01, -0.02,
        "Fonte: INE, EPH — Nota: // indica dado confidencial (não disponível)",
        fontsize=7, color="grey",
    )
    salvar(fig, "02_evolucao_preco_municipios")


# ─── Gráfico 3: Ranking preço mediano Q4 2025 ────────────────────────────────

def grafico_ranking_preco() -> None:
    ultimo_trimestre = df_municipios["data"].max()
    df_rank = (
        df_municipios[df_municipios["data"] == ultimo_trimestre]
        .dropna(subset=["preco_mediano_m2"])
        .sort_values("preco_mediano_m2", ascending=True)
    )

    fig, ax = plt.subplots(figsize=(9, 5.5))

    bars = ax.barh(
        df_rank["designacao"],
        df_rank["preco_mediano_m2"],
        color=[CORES_MUNICIPIOS.get(c, "#AAAAAA") for c in df_rank["designacao"]],
        edgecolor="white",
        height=0.65,
    )

    # Anotações
    for bar, (_, row) in zip(bars, df_rank.iterrows()):
        yoy = row["preco_yoy_pct"]
        seta = "▲" if pd.notna(yoy) and yoy > 0 else "▼"
        cor_seta = "#27AE60" if pd.notna(yoy) and yoy > 0 else "#E74C3C"
        label_yoy = f" {seta}{abs(yoy):.1f}% YoY" if pd.notna(yoy) else ""
        ax.text(
            bar.get_width() + 30,
            bar.get_y() + bar.get_height() / 2,
            f"{int(row['preco_mediano_m2']):,} €/m²{label_yoy}",
            va="center", fontsize=8.5,
        )

    ax.set_xlim(0, df_rank["preco_mediano_m2"].max() * 1.25)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_xlabel("€/m²", fontsize=10)
    ax.set_title(
        f"Ranking de Preço Mediano por m² — Q4 2025\nPenínsula de Setúbal",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.grid(axis="y", alpha=0)
    fig.text(
        0.01, -0.02,
        "Fonte: INE, EPH Q4 2025",
        fontsize=7, color="grey",
    )
    salvar(fig, "03_ranking_preco_q4_2025")


# ─── Gráfico 4: Volume de transações por trimestre ───────────────────────────

def grafico_volume_transacoes() -> None:
    df_plot = df_nuts.dropna(subset=["n_transacoes"]).sort_values("data_dt")

    fig, ax = plt.subplots(figsize=(11, 5))

    # Barras por ano com cor gradiente
    cores_anos = {
        2019: "#D0E4F5", 2020: "#A9CCEB", 2021: "#7FB3E0",
        2022: "#559AD5", 2023: "#2B81CA", 2024: "#1E5F99",
        2025: "#1A3E5C",
    }

    for _, row in df_plot.iterrows():
        cor = cores_anos.get(row["ano"], "#AAAAAA")
        ax.bar(row["data_dt"], row["n_transacoes"], width=60, color=cor, edgecolor="white")

    # Linha de tendência (média móvel 4 trimestres)
    df_plot = df_plot.copy()
    df_plot["media_movel"] = df_plot["n_transacoes"].rolling(4, center=True).mean()
    ax.plot(
        df_plot["data_dt"], df_plot["media_movel"],
        color="#E87B1E", linewidth=2, linestyle="--", label="Média móvel 4T",
    )

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.set_title(
        "Volume de Transações Trimestrais\nPenínsula de Setúbal — Q1 2019 a Q4 2025",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.set_ylabel("Nº de transações", fontsize=10)
    ax.legend(fontsize=9)

    # Legenda de anos por cor
    from matplotlib.patches import Patch
    patches = [Patch(facecolor=c, label=str(a)) for a, c in cores_anos.items()]
    ax.legend(handles=patches + [
        plt.Line2D([0], [0], color="#E87B1E", linewidth=2, linestyle="--", label="Média móvel 4T")
    ], fontsize=8, ncol=4, loc="upper left")

    fig.text(
        0.01, -0.02,
        "Fonte: INE, EPH",
        fontsize=7, color="grey",
    )
    salvar(fig, "04_volume_transacoes_trimestral")


# ─── Gráfico 5: Variação YoY por município (heatmap) ─────────────────────────

def grafico_yoy_heatmap() -> None:
    df_plot = df_municipios[df_municipios["ano"] >= 2021].dropna(subset=["preco_yoy_pct"])
    pivot = df_plot.pivot_table(
        index="designacao", columns="periodo", values="preco_yoy_pct"
    )
    # Ordenar colunas cronologicamente
    cols_sorted = sorted(pivot.columns, key=lambda x: (int(x[:4]), int(x[6])))
    pivot = pivot[cols_sorted]
    # Ordenar municípios pelo preço médio
    ordem_concelhos = ["Almada", "Sesimbra", "Seixal", "Alcochete", "Setúbal",
                       "Montijo", "Barreiro", "Palmela", "Moita"]
    pivot = pivot.reindex([c for c in ordem_concelhos if c in pivot.index])

    fig, ax = plt.subplots(figsize=(16, 5))
    im = ax.imshow(pivot.values, cmap="RdYlGn", aspect="auto", vmin=-20, vmax=40)

    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=45, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index, fontsize=9)

    # Anotações de valor
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            if pd.notna(val):
                ax.text(j, i, f"{val:.1f}%", ha="center", va="center",
                        fontsize=6.5, color="black" if abs(val) < 30 else "white")

    plt.colorbar(im, ax=ax, label="Variação YoY (%)", shrink=0.8)
    ax.set_title(
        "Variação Homóloga do Preço Mediano/m² por Município\nPenínsula de Setúbal — 2021 a 2025",
        fontsize=13, fontweight="bold", pad=15,
    )
    ax.grid(False)
    fig.text(
        0.01, -0.04,
        "Fonte: INE, EPH — Vermelho: queda; Amarelo: estável; Verde: subida",
        fontsize=7, color="grey",
    )
    salvar(fig, "05_heatmap_yoy_municipios")


# ─── Gráfico 6: Distribuição de preços — últimos 4 trimestres ────────────────

def grafico_distribuicao_precos_recentes() -> None:
    df_plot = (
        df_municipios[df_municipios["ano"] == 2025]
        .dropna(subset=["preco_mediano_m2"])
        .sort_values(["designacao", "data"])
    )

    # Agrupar por concelho, mostrar 4 trimestres 2025 como "dot plot"
    concelhos = sorted(df_plot["designacao"].unique(),
                       key=lambda c: df_plot[df_plot["designacao"] == c]["preco_mediano_m2"].mean(),
                       reverse=True)

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, concelho in enumerate(concelhos):
        df_c = df_plot[df_plot["designacao"] == concelho].sort_values("trimestre")
        cor = CORES_MUNICIPIOS.get(concelho, "#AAAAAA")
        ax.scatter(df_c["preco_mediano_m2"], [i] * len(df_c),
                   color=cor, s=60, zorder=3)
        ax.plot(df_c["preco_mediano_m2"], [i] * len(df_c),
                color=cor, linewidth=1.5, alpha=0.6)
        # Anotar Q4
        q4 = df_c[df_c["trimestre"] == 4]
        if len(q4):
            ax.annotate(
                f" {int(q4.iloc[-1]['preco_mediano_m2']):,}",
                xy=(q4.iloc[-1]["preco_mediano_m2"], i),
                fontsize=8, va="center", color=cor,
            )

    ax.set_yticks(range(len(concelhos)))
    ax.set_yticklabels(concelhos, fontsize=9)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,} €"))
    ax.set_xlabel("Preço Mediano/m²", fontsize=10)
    ax.set_title(
        "Preços Medianos/m² — Q1 a Q4 de 2025 por Município\nPenínsula de Setúbal",
        fontsize=13, fontweight="bold", pad=15,
    )
    fig.text(
        0.01, -0.02,
        "Fonte: INE, EPH — Cada ponto = um trimestre de 2025",
        fontsize=7, color="grey",
    )
    salvar(fig, "06_distribuicao_precos_2025")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print("A gerar gráficos para o Dossier de Mercado — Setúbal...\n")
    grafico_evolucao_subreigiao()
    grafico_evolucao_municipios()
    grafico_ranking_preco()
    grafico_volume_transacoes()
    grafico_yoy_heatmap()
    grafico_distribuicao_precos_recentes()
    print(f"\n🎨 6 gráficos guardados em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
