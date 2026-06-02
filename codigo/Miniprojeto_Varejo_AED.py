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

# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 4 — ESTATÍSTICAS DESCRITIVAS
# Coluna CL_FHL — Número de filhos do cliente
# Parâmetros: média, mediana, desvio padrão, moda, mín, máx, contagem, quartis
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  SPRINT 4 — ESTATÍSTICAS DESCRITIVAS — CL_FHL (Nº de Filhos)")
print("=" * 65)

serie = df_limpo['CL_FHL']

print(f"\n  Coluna      : CL_FHL — Número de Filhos do Cliente")
print(f"  Contagem    : {serie.count():,}")
print(f"  Média       : {serie.mean():.4f}")
print(f"  Mediana     : {serie.median()}")
print(f"  Desvio Pad  : {serie.std():.4f}")
print(f"  Moda        : {serie.mode().tolist()}")
print(f"  Mínimo      : {serie.min()}")
print(f"  Máximo      : {serie.max()}")
print(f"  Q1 (25%)    : {serie.quantile(0.25)}")
print(f"  Q2 (50%)    : {serie.quantile(0.50)}")
print(f"  Q3 (75%)    : {serie.quantile(0.75)}")

print("\n  Distribuição de frequência:")
dist = serie.value_counts().sort_index()
for val, qtd in dist.items():
    pct = qtd / serie.count() * 100
    print(f"    {val} filho(s): {qtd:>7,} registros ({pct:.1f}%)")

# ─────────────────────────────────────────────────────────────────────────────
# SPRINT 5 — PADRÕES DE AGRUPAMENTO
# groupby 1: volume de compras por gênero (CL_GENERO)
# groupby 2: volume de compras por categoria (PR_CAT)
# bônus: pivot_table gênero × categoria
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("  SPRINT 5 — PADRÕES DE AGRUPAMENTO")
print("=" * 65)

# Agrupamento 1 — por gênero
print("\n[Agrupamento 1] Compras por Gênero (CL_GENERO):")
agg_genero = df_limpo.groupby('CL_GENERO').agg(
    Qtd_Compras     = ('CO_ID', 'count'),
    Clientes_Unicos = ('CL_ID', 'nunique')
).sort_values('Qtd_Compras', ascending=False)
agg_genero['Pct_Compras'] = (
    agg_genero['Qtd_Compras'] / agg_genero['Qtd_Compras'].sum() * 100
).round(2)
print(agg_genero.to_string())
genero_top = agg_genero.index[0]
print(f"\n  → Gênero com mais compras: '{genero_top}' "
      f"({agg_genero.loc[genero_top, 'Qtd_Compras']:,} compras — "
      f"{agg_genero.loc[genero_top, 'Pct_Compras']}%)")

# Agrupamento 2 — por categoria
print("\n[Agrupamento 2] Compras por Categoria de Produto (PR_CAT):")
agg_cat = df_limpo.groupby('PR_CAT').agg(
    Qtd_Compras     = ('CO_ID', 'count'),
    Produtos_Unicos = ('PR_ID', 'nunique')
).sort_values('Qtd_Compras', ascending=False)
agg_cat['Pct_Compras'] = (
    agg_cat['Qtd_Compras'] / agg_cat['Qtd_Compras'].sum() * 100
).round(2)
print(agg_cat.to_string())
cat_top = agg_cat.index[0]
print(f"\n  → Categoria líder: '{cat_top}' "
      f"({agg_cat.loc[cat_top, 'Qtd_Compras']:,} compras — "
      f"{agg_cat.loc[cat_top, 'Pct_Compras']}%)")

# Bônus — pivot_table
print("\n[Agrupamento 3 — Bônus] Pivot: Gênero × Categoria (nº de compras):")
pivot = pd.pivot_table(
    df_limpo,
    values='CO_ID',
    index='CL_GENERO',
    columns='PR_CAT',
    aggfunc='count',
    fill_value=0
)
print(pivot.to_string())