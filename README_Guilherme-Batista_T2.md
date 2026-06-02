# Mini-Projeto AED — Base Varejo
**Curso:** Análise de Dados com Python [T2]  
**Módulo:** 1 — Semana 07  
**Disciplina:** Tratamento de Dados / Análise Exploratória de Dados

---

## Como executar

### Pré-requisitos
- Python 3.8 ou superior instalado
- VSCode com a extensão Python

### Instalação das dependências
Abra o terminal do VSCode (`Ctrl + '`) e execute:
```bash
pip install pandas numpy
```

### Estrutura de pastas esperada
```
Miniprojeto_Guilherme-Batista_T2/
├── README_Guilherme-Batista_T2.md
├── dados/
│   ├── Base_Varejo.csv        ← baixar no Kaggle (link abaixo)
│   └── df_limpo.csv           ← gerado automaticamente ao rodar o script
└── codigo/
    └── Miniprojeto_Varejo_AED.py
```

### Passos
1. Baixe o arquivo `Base_Varejo.csv` no Kaggle:  
   https://www.kaggle.com/datasets/namespaiva/base-varejo/data

2. Coloque o `Base_Varejo.csv` dentro da pasta `dados/`

3. No terminal do VSCode, estando na **pasta raiz do projeto**, execute:
   ```bash
   python codigo/Miniprojeto_Varejo_AED.py
   ```

4. O arquivo `df_limpo.csv` será gerado automaticamente em `dados/`

> O script usa caminhos relativos automáticos — não é necessário alterar nenhum caminho no código.

---

## Sobre a base de dados

| Item | Valor |
|------|-------|
| Total de registros (raw) | 830.000 |
| Registros após limpeza | 733.447 |
| Duplicatas removidas | 96.553 (11,6%) |
| Colunas | 10 |
| Período | Jan/2019 a Dez/2022 |
| Clientes únicos | 1.000 |
| Produtos únicos | 229 |
| Categorias | ALIMENTOS, HIGIENE, LIMPEZA, BEBIDAS, PET, ACESSORIOS |

### Dicionário de colunas

| Coluna | Descrição |
|--------|-----------|
| DATA | Data da compra (convertida para datetime) |
| CO_ID | Identificador único da compra |
| CL_ID | Identificador do cliente |
| CL_GENERO | Gênero do cliente (M/F) |
| CL_EC | Estado civil (1 a 5) |
| CL_FHL | Número de filhos do cliente (0 a 4) |
| CL_SEG | Segmento do cliente (A/B/C) |
| PR_ID | Identificador do produto |
| PR_CAT | Categoria do produto |
| PR_NOME | Nome do produto |

---

## Estatísticas descritivas — CL_FHL (Número de Filhos)

| Parâmetro | Valor |
|-----------|-------|
| Contagem | 733.447 |
| Média | 1,1460 |
| Mediana | 0,0 |
| Desvio Padrão | 1,4169 |
| Moda | 0 |
| Mínimo | 0 |
| Máximo | 4 |
| Q1 (25%) | 0,0 |
| Q2 (50%) | 0,0 |
| Q3 (75%) | 2,0 |

**Distribuição:**

| Nº de Filhos | Registros | % |
|---|---|---|
| 0 | 384.986 | 52,5% |
| 1 | 90.845 | 12,4% |
| 2 | 94.168 | 12,8% |
| 3 | 92.407 | 12,6% |
| 4 | 71.041 | 9,7% |

---

## Principais Insights da Análise Exploratória

### 1. Volume de duplicatas expressivo
A base original continha **96.553 linhas duplicadas** — 11,6% do total. Sem esse tratamento, qualquer contagem de compras estaria inflada em quase 12%, comprometendo completamente a confiabilidade dos relatórios.

### 2. Categorias inválidas indicam falha de cadastro
A categoria `#N/D` apareceu em **3.228 registros** de `PR_CAT`, sinalizando uma falha no sistema de cadastro de produtos. Esses registros foram sinalizados como `'Sem Categoria'` via lógica `if/else`. Isso impacta análises de desempenho por categoria e deve ser corrigido na origem dos dados.

### 3. Perfil familiar dos clientes
A maioria dos clientes **não possui filhos**: moda e mediana são 0, com 52,5% dos registros em `CL_FHL = 0`. A média de 1,15 está distorcida pela presença de clientes com 3 e 4 filhos. O alto desvio padrão (1,42) sugere que a segmentação por faixa familiar seria mais informativa do que usar a média como referência.

### 4. Gênero Feminino lidera o volume de compras
O gênero **F (Feminino) realizou 382.427 compras (52,1%)** contra 351.020 do gênero M (47,9%). Considerando que a base tem 519 clientes femininos e 481 masculinos, a diferença proporcional de clientes é pequena, o que indica maior **frequência de compra per capita** entre as clientes femininas.

### 5. ALIMENTOS domina o volume de compras
A categoria **ALIMENTOS concentra 52,4% de todas as compras** (384.197 registros) com 120 produtos distintos. HIGIENE (18,8%) e LIMPEZA (17,5%) completam o top 3. A ausência de coluna de preço impede cálculo de receita — os agrupamentos refletem volume de compras, não faturamento.

### 6. Potencial para análises temporais e problemas remanescentes
A base cobre **quase 4 anos (Jan/2019 a Dez/2022)**, abrindo espaço para análises de sazonalidade e tendência — possíveis apenas após a conversão de `DATA` para `datetime`. Problema remanescente principal: a ausência de uma coluna de valor monetário impede cálculo de receita ou ticket médio.

---