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

# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 2 — DIAGNÓSTICO DE QUALIDADE
# Identificar problemas ANTES de limpar
# Problemas encontrados: 96.553 duplicatas, '#N/D' em PR_CAT, DATA como string.
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  SPRINT 2 — DIAGNÓSTICO DE QUALIDADE DOS DADOS")
print("=" * 65)

print("\n[Problema 1] Valores nulos reais (NaN) por coluna:")
nulos = df.isnull().sum()
if nulos.sum() == 0:
    print("  → Nenhum NaN detectado.")
else:
    print(nulos[nulos > 0].to_string())

print("\n[Problema 2] Strings disfarçadas de nulo:")
strings_invalidas = ['NULL', 'null', 'N/A', 'n/a', '', ' ', '#N/D', 'nan']
for col in df.select_dtypes(include=['object', 'str']).columns:
    n = df[col].isin(strings_invalidas).sum()
    if n > 0:
        print(f"  → '{col}': {n:,} ocorrências de valor inválido")

print(f"\n[Problema 3] Linhas completamente duplicadas: {df.duplicated().sum():,}")

print("\n[Problema 4] Coluna DATA está como string — precisa ser datetime:")
print(f"  → Tipo atual: {df['DATA'].dtype}  |  Exemplo: {df['DATA'].iloc[0]}")

# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 3 — LIMPEZA MÍNIMA NECESSÁRIA
# Etapa 1: '#N/D' em PR_CAT → 'Sem Categoria' (lógica if/else)
# Etapa 2: remover duplicatas + reindexar
# Etapa 3: converter DATA para datetime com errors='coerce'
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  SPRINT 3 — LIMPEZA DOS DADOS")
print("=" * 65)

df_limpo = df.copy()

# Etapa 1 — categorias inválidas: if/else (critério avaliativo)
# Justificativa: '#N/D' é erro de cadastro no sistema de origem.
# Mantemos os registros sinalizando com 'Sem Categoria' para não perder dados.
print("\n[Limpeza 1] Substituindo '#N/D' em PR_CAT por 'Sem Categoria' (if/else)...")
antes_nd = df_limpo['PR_CAT'].isin(['#N/D']).sum()
df_limpo['PR_CAT'] = df_limpo['PR_CAT'].apply(
    lambda x: 'Sem Categoria' if x == '#N/D' else x
)
print(f"  → {antes_nd:,} registros '#N/D' convertidos para 'Sem Categoria'")

# Etapa 2 — duplicatas
print("\n[Limpeza 2] Removendo duplicatas...")
antes = len(df_limpo)
df_limpo.drop_duplicates(inplace=True)
df_limpo.reset_index(drop=True, inplace=True)   # reindexação obrigatória
depois = len(df_limpo)
print(f"  → Antes: {antes:,} | Depois: {depois:,} | Removidas: {antes - depois:,}")

# Etapa 3 — conversão de data
# Justificativa: data como string bloqueia análises temporais.
# errors='coerce' garante que datas inválidas virem NaT sem travar o pipeline.
print("\n[Limpeza 3] Convertendo DATA para datetime (DD/MM/YYYY)...")
df_limpo['DATA'] = pd.to_datetime(df_limpo['DATA'], dayfirst=True, errors='coerce')
nulos_data = df_limpo['DATA'].isnull().sum()
print(f"  → Tipo convertido : {df_limpo['DATA'].dtype}")
print(f"  → Datas inválidas : {nulos_data}")
print(f"  → Período da base : {df_limpo['DATA'].min().date()} a {df_limpo['DATA'].max().date()}")
print(f"\n  Nulos totais após limpeza: {df_limpo.isnull().sum().sum()}")

df_limpo.to_csv(SAIDA_LIMPO, index=False, encoding="utf-8")
print(f"  → df_limpo.csv salvo em: {SAIDA_LIMPO}")