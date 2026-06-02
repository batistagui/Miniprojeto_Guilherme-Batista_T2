# =============================================================================
# MINI-PROJETO AVALIATIVO - MÓDULO 1 - SEMANA 07
# Análise Exploratória de Dados (AED) - Base Varejo
# Curso: Análise de Dados com Python [T2]
# Aluno: Guilherme Batista

import csv
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Caminhos relativos à raiz do projeto
# O script fica em codigo/ e lê/grava em dados/
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQUIVO     = os.path.join(BASE_DIR, "dados", "Base_Varejo.csv")
SAIDA_LIMPO = os.path.join(BASE_DIR, "dados", "df_limpo.csv")

print("=" * 65)
print("  MINI-PROJETO AED — BASE VAREJO")
print("=" * 65)

# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 1 — IMPORTAÇÃO DOS DADOS
# Leitura estruturada com csv.DictReader e pandas.
# ─────────────────────────────────────────────────────────────────────────────

print("\n[SPRINT 1] Carregando dados com csv.DictReader...")

registros_brutos = []
with open(ARQUIVO, encoding="utf-8", newline="") as f:
    leitor = csv.DictReader(f, delimiter=";")
    colunas_csv = leitor.fieldnames
    for linha in leitor:
        registros_brutos.append(linha)

print(f"  → {len(registros_brutos):,} registros lidos via csv.DictReader")
print(f"  → Colunas: {colunas_csv}")

# Carrega com pandas para análise completa
df = pd.read_csv(ARQUIVO, sep=";", encoding="utf-8")

# Remove colunas completamente vazias (exportação gerou colunas extras)
colunas_vazias = [c for c in df.columns if df[c].isnull().all() or c.strip() == '']
df.drop(columns=colunas_vazias, inplace=True)
df.columns = df.columns.str.strip()

print(f"\n  Dimensões : {df.shape[0]:,} linhas × {df.shape[1]} colunas")
print(f"  Colunas   : {df.columns.tolist()}")
print("\n  Tipos de dados por coluna:")
print(df.dtypes.to_string())
print("\n  Primeiras 5 linhas:")
print(df.head(5).to_string())
