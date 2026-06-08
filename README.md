# ⚽ Copa do Mundo — Dashboard Histórico

Dashboard interativo com análise exploratória de todas as edições da Copa do Mundo FIFA (1930–2014).

Projeto Final da disciplina de **Análise e Visualização de Dados com Python** — CESAR School.

---

## 📁 Estrutura do Projeto

| Arquivo | Descrição |
|---|---|
| `app.py` | Dashboard interativo em Streamlit |
| `cups_clean.csv` | Histórico de edições da Copa (limpo) |
| `matches_clean.csv` | Partidas jogadas (limpo) |
| `players_clean.csv` | Jogadores por partida (limpo) |
| `artilheiros_clean.csv` | Artilheiros por edição — via Web Scraping |

---

## 🚀 Como Executar

```bash
pip install streamlit pandas matplotlib seaborn scipy
streamlit run app.py
```

---

## 📊 Fases do Projeto

- **Fase 1 — Web Scraping:** Raspagem da Wikipedia com `requests` + `BeautifulSoup`
- **Fase 2 — ETL:** Limpeza e transformação dos dados com `Pandas`
- **Fase 3 — Análise Estatística:** Pearson, ANOVA, quartis e outliers com `SciPy`
- **Fase 4 — Visualizações:** 6 gráficos com princípios de Gestalt via `Matplotlib`
- **Fase 5 — Dashboard:** Aplicação interativa com filtros dinâmicos em `Streamlit`

---

## 🔎 Filtros Disponíveis

- Período da Copa (1930–2014)
- Seleção específica
- Fase do torneio

---

## 📈 Principais Insights

- A média de gols caiu de 5,38 (1954) para 2,21 (1990) — futebol mais defensivo ao longo das décadas
- Brasil lidera o histórico de vitórias em Copas do Mundo
- Semifinais e finais concentram mais gols que a fase de grupos (ANOVA p = 0,0375)
- Público presente não influencia o número de gols (r = -0,114)

---

**Fonte dos dados:** Kaggle + Wikipedia (Web Scraping)
