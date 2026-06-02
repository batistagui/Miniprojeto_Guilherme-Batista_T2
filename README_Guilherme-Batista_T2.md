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
