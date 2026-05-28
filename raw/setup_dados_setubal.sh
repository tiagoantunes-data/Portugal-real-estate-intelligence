#!/bin/bash
# ============================================================
# LUXAR — Dossier de Mercado v1 | Distrito de Setúbal
# Script de download e organização de dados brutos
# Fonte: INE (Estatísticas de Preços da Habitação ao Nível Local)
# Gerado automaticamente em 2026-05-28
# ============================================================

set -e

# --- Diretórios ---
RAW_INE="$HOME/EMPRESA/03_DADOS/raw/ine"
RAW_IMPIC="$HOME/EMPRESA/03_DADOS/raw/impic"

echo "📁 A criar estrutura de pastas..."
mkdir -p "$RAW_INE"
mkdir -p "$RAW_IMPIC"
echo "✅ Pastas criadas em $HOME/EMPRESA/03_DADOS/raw/"

# --- Headers para simular browser ---
HEADERS='-H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36" -H "Referer: https://www.ine.pt/"'

echo ""
echo "📥 A descarregar ficheiros INE — Estatísticas de Preços da Habitação ao Nível Local..."
echo "   (4 trimestres mais recentes: Q1 2025 a Q4 2025)"
echo ""

# -----------------------------------------------------------------
# INE — Quadros Excel (dados por município/sub-região NUTS III)
# Publicação: Estatísticas de Preços da Habitação ao Nível Local
# -----------------------------------------------------------------

# Q1 2025 (publicado 16/07/2025)
echo "  → Q1 2025 Excel..."
curl -L -o "$RAW_INE/INE_EPH_NL_Q1_2025_Quadros.xlsx" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.ine.pt/" \
  "https://www.ine.pt/ngt_server/attachfileu.jsp?look_parentBoui=737543765&att_display=n&att_download=y"

# Q1 2025 CSV
echo "  → Q1 2025 CSV..."
curl -L -o "$RAW_INE/INE_EPH_NL_Q1_2025_Quadros.csv" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.ine.pt/" \
  "https://www.ine.pt/ngt_server/attachfileu.jsp?look_parentBoui=737543956&att_display=n&att_download=y"

# Q2 2025 (publicado 22/10/2025)
echo "  → Q2 2025 Excel..."
curl -L -o "$RAW_INE/INE_EPH_NL_Q2_2025_Quadros.xlsx" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.ine.pt/" \
  "https://www.ine.pt/ngt_server/attachfileu.jsp?look_parentBoui=757132386&att_display=n&att_download=y"

# Q2 2025 CSV
echo "  → Q2 2025 CSV..."
curl -L -o "$RAW_INE/INE_EPH_NL_Q2_2025_Quadros.csv" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.ine.pt/" \
  "https://www.ine.pt/ngt_server/attachfileu.jsp?look_parentBoui=757132589&att_display=n&att_download=y"

# Q3 2025 (publicado 02/02/2026)
echo "  → Q3 2025 Excel..."
curl -L -o "$RAW_INE/INE_EPH_NL_Q3_2025_Quadros.xlsx" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.ine.pt/" \
  "https://www.ine.pt/ngt_server/attachfileu.jsp?look_parentBoui=774718738&att_display=n&att_download=y"

# Q3 2025 CSV
echo "  → Q3 2025 CSV..."
curl -L -o "$RAW_INE/INE_EPH_NL_Q3_2025_Quadros.csv" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.ine.pt/" \
  "https://www.ine.pt/ngt_server/attachfileu.jsp?look_parentBoui=774719385&att_display=n&att_download=y"

# Q4 2025 (publicado 24/04/2026) — MAIS RECENTE
echo "  → Q4 2025 Excel..."
curl -L -o "$RAW_INE/INE_EPH_NL_Q4_2025_Quadros.xlsx" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.ine.pt/" \
  "https://www.ine.pt/ngt_server/attachfileu.jsp?look_parentBoui=789055751&att_display=n&att_download=y"

# Q4 2025 CSV
echo "  → Q4 2025 CSV..."
curl -L -o "$RAW_INE/INE_EPH_NL_Q4_2025_Quadros.csv" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
  -H "Referer: https://www.ine.pt/" \
  "https://www.ine.pt/ngt_server/attachfileu.jsp?look_parentBoui=789056085&att_display=n&att_download=y"

echo ""
echo "📊 IMPIC: Não dispõe de dados de transações por município para download."
echo "   Apenas relatórios PDF de análise de empresas de mediação."
echo "   Consultar: https://www.impic.pt/impic/pt-pt/relatorios-e-dados-estatisticos/relatorios-de-imobiliario"
echo ""

# --- Verificação ---
echo "✅ Download concluído. A verificar ficheiros..."
echo ""
echo "=== Ficheiros em $RAW_INE ==="
ls -lh "$RAW_INE/"

echo ""
echo "=== Verificação de integridade (tamanho mínimo esperado: 50 KB) ==="
for f in "$RAW_INE"/*.xlsx "$RAW_INE"/*.csv; do
  size=$(du -k "$f" | cut -f1)
  if [ "$size" -lt 10 ]; then
    echo "  ⚠️  ATENÇÃO: $f parece vazio ou corrompido ($size KB)"
  else
    echo "  ✅ $f ($size KB)"
  fi
done

echo ""
echo "🏁 Script concluído."
