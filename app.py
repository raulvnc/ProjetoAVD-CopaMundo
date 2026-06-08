import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats

# ── Configuração da página ──────────────────────────────────────────
st.set_page_config(
    page_title="Copa do Mundo — Dashboard",
    page_icon="⚽",
    layout="wide"
)

# ── Estilo global ───────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor": "#0d1117",
    "axes.facecolor":   "#0d1117",
    "axes.edgecolor":   "#30363d",
    "axes.labelcolor":  "#e6edf3",
    "xtick.color":      "#8b949e",
    "ytick.color":      "#8b949e",
    "text.color":       "#e6edf3",
    "grid.color":       "#21262d",
    "grid.linewidth":   0.8,
    "font.family":      "sans-serif",
})

# ── Carregamento dos dados ──────────────────────────────────────────
@st.cache_data
def load_data():
    cups        = pd.read_csv("cups_clean.csv")
    matches     = pd.read_csv("matches_clean.csv")
    players     = pd.read_csv("players_clean.csv")
    artilheiros = pd.read_csv("artilheiros_clean.csv")

    cups["Avg_Goals_Per_Match"] = (cups["GoalsScored"] / cups["MatchesPlayed"]).round(2)

    def resultado(row):
        if row["Home Team Goals"] > row["Away Team Goals"]:
            return "Home Win"
        elif row["Home Team Goals"] < row["Away Team Goals"]:
            return "Away Win"
        else:
            return "Draw"

    matches["Result"]      = matches.apply(resultado, axis=1)
    matches["Total_Goals"] = matches["Home Team Goals"] + matches["Away Team Goals"]

    def classificar_fase(stage):
        stage = str(stage).upper()
        if "GROUP" in stage:
            return "Fase de Grupos"
        elif "ROUND OF 16" in stage or "LAST 16" in stage or "FIRST ROUND" in stage:
            return "Oitavas de Final"
        elif "QUARTER" in stage:
            return "Quartas de Final"
        elif "SEMI" in stage:
            return "Semifinal"
        elif "FINAL" in stage:
            return "Final"
        else:
            return "Outros"

    matches["Stage_Clean"] = matches["Stage"].apply(classificar_fase)

    return cups, matches, players, artilheiros

cups, matches, players, artilheiros = load_data()

# ── Header ──────────────────────────────────────────────────────────
st.markdown("""
    <h1 style='text-align:center; color:#f0b429;'>⚽ Copa do Mundo — Dashboard Histórico</h1>
    <p style='text-align:center; color:#8b949e; font-size:16px;'>
        Análise exploratória de todas as edições de 1930 a 2014
    </p>
    <hr style='border-color:#30363d; margin-bottom:30px;'>
""", unsafe_allow_html=True)

# ── Sidebar — Filtros ───────────────────────────────────────────────
st.sidebar.header("🔎 Filtros")

anos = sorted(cups["Year"].unique())
ano_range = st.sidebar.select_slider(
    "Período da Copa",
    options=anos,
    value=(anos[0], anos[-1])
)

todas_selecoes = sorted(
    set(matches["Home Team Name"].unique()) |
    set(matches["Away Team Name"].unique())
)
selecao = st.sidebar.selectbox("Selecionar Seleção", ["Todas"] + todas_selecoes)

fases_disponiveis = ["Todas"] + sorted(matches["Stage_Clean"].unique())
fase_filtro = st.sidebar.selectbox("Fase do Torneio", fases_disponiveis)

st.sidebar.markdown("---")
st.sidebar.markdown("""
<small style='color:#8b949e;'>
📁 Fonte: Kaggle + Wikipedia (Web Scraping)<br>
🎓 CESAR School — Projeto AVD
</small>
""", unsafe_allow_html=True)

# ── Aplicar filtros ─────────────────────────────────────────────────
cups_f    = cups[(cups["Year"] >= ano_range[0]) & (cups["Year"] <= ano_range[1])]
matches_f = matches[(matches["Year"] >= ano_range[0]) & (matches["Year"] <= ano_range[1])]

if selecao != "Todas":
    matches_f = matches_f[
        (matches_f["Home Team Name"] == selecao) |
        (matches_f["Away Team Name"] == selecao)
    ]

if fase_filtro != "Todas":
    matches_f = matches_f[matches_f["Stage_Clean"] == fase_filtro]

# ── KPIs ────────────────────────────────────────────────────────────
st.subheader("📊 Visão Geral")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Edições", len(cups_f))
col2.metric("Partidas", len(matches_f))
col3.metric("Total de Gols", int(matches_f["Total_Goals"].sum()) if len(matches_f) > 0 else 0)
col4.metric("Média Gols/Jogo", round(matches_f["Total_Goals"].mean(), 2) if len(matches_f) > 0 else 0)

st.markdown("<hr style='border-color:#30363d;'>", unsafe_allow_html=True)

# ── Gráfico 1 — Evolução de gols ────────────────────────────────────
st.subheader("📈 Evolução da Média de Gols por Edição")
st.caption("Princípios Gestalt: Continuidade (linha do tempo) + Figura-fundo (linha dourada sobre fundo escuro)")

if len(cups_f) > 1:
    fig1, ax1 = plt.subplots(figsize=(13, 5))
    ax1.plot(cups_f["Year"], cups_f["Avg_Goals_Per_Match"],
             color="#f0b429", linewidth=2.5, zorder=3)
    ax1.scatter(cups_f["Year"], cups_f["Avg_Goals_Per_Match"],
                color="#f0b429", s=70, zorder=4)
    ax1.fill_between(cups_f["Year"], cups_f["Avg_Goals_Per_Match"],
                     alpha=0.15, color="#f0b429")

    idx_max = cups_f["Avg_Goals_Per_Match"].idxmax()
    idx_min = cups_f["Avg_Goals_Per_Match"].idxmin()
    ax1.annotate(f'Máximo\n{cups_f.loc[idx_max, "Avg_Goals_Per_Match"]} gols/jogo',
                 xy=(cups_f.loc[idx_max, "Year"], cups_f.loc[idx_max, "Avg_Goals_Per_Match"]),
                 xytext=(cups_f.loc[idx_max, "Year"] + 2, cups_f.loc[idx_max, "Avg_Goals_Per_Match"] + 0.3),
                 color="#f0b429", fontsize=9,
                 arrowprops=dict(arrowstyle="->", color="#f0b429"))
    ax1.annotate(f'Mínimo\n{cups_f.loc[idx_min, "Avg_Goals_Per_Match"]} gols/jogo',
                 xy=(cups_f.loc[idx_min, "Year"], cups_f.loc[idx_min, "Avg_Goals_Per_Match"]),
                 xytext=(cups_f.loc[idx_min, "Year"] - 10, cups_f.loc[idx_min, "Avg_Goals_Per_Match"] - 0.4),
                 color="#8b949e", fontsize=9,
                 arrowprops=dict(arrowstyle="->", color="#8b949e"))

    ax1.set_xlabel("Ano")
    ax1.set_ylabel("Média de Gols/Jogo")
    ax1.set_xticks(cups_f["Year"])
    ax1.set_xticklabels(cups_f["Year"], rotation=45, ha="right", fontsize=8)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)
    ax1.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig1)
    plt.close(fig1)
else:
    st.info("Selecione mais edições para exibir o gráfico de evolução.")

# ── Gráfico 2 — Top 10 vitórias ─────────────────────────────────────
st.subheader("🏆 Top 10 Seleções com Mais Vitórias")
st.caption("Princípios Gestalt: Similaridade (gradiente de cor no ranking) + Figura-fundo (líder em dourado)")

if len(matches_f) > 0:
    home_wins  = matches_f[matches_f["Result"] == "Home Win"]["Home Team Name"].value_counts()
    away_wins  = matches_f[matches_f["Result"] == "Away Win"]["Away Team Name"].value_counts()
    total_wins = (home_wins.add(away_wins, fill_value=0)).astype(int)
    top10      = total_wins.sort_values(ascending=True).tail(10)

    if len(top10) > 0:
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        colors = ["#f0b429" if c == top10.index[-1] else "#1f6feb" for c in top10.index]
        bars = ax2.barh(top10.index, top10.values, color=colors,
                        edgecolor="none", height=0.65)
        for bar, val in zip(bars, top10.values):
            ax2.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
                     str(val), va="center", fontsize=10,
                     color="#e6edf3", fontweight="bold")
        ax2.set_xlabel("Total de Vitórias")
        ax2.set_xlim(0, top10.max() + 8)
        ax2.grid(axis="x", linestyle="--", alpha=0.3)
        ax2.spines[["top", "right", "left"]].set_visible(False)
        st.pyplot(fig2)
        plt.close(fig2)
else:
    st.info("Sem dados para exibir com os filtros selecionados.")

# ── Gráfico 3 — Distribuição de gols ────────────────────────────────
st.subheader("📊 Distribuição de Gols por Partida")
st.caption("Princípios Gestalt: Figura-fundo (outliers em vermelho) + Continuidade (linha de corte)")

if len(matches_f) > 0:
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    limite  = 8.5
    normal  = matches_f[matches_f["Total_Goals"] <= limite]["Total_Goals"]
    outlier = matches_f[matches_f["Total_Goals"] >  limite]["Total_Goals"]
    ax3.hist(normal,  bins=range(0, 14), color="#1f6feb", alpha=0.85,
             edgecolor="#0d1117", linewidth=0.5, label="Partidas normais")
    ax3.hist(outlier, bins=range(0, 14), color="#f85149", alpha=0.9,
             edgecolor="#0d1117", linewidth=0.5, label="Outliers (> 8.5 gols)")
    ax3.axvline(x=limite, color="#f0b429", linewidth=1.8, linestyle="--",
                label=f"Limite outlier: {limite}")
    ax3.set_xlabel("Gols na Partida")
    ax3.set_ylabel("Nº de Partidas")
    ax3.set_xticks(range(0, 14))
    ax3.legend(framealpha=0.2, fontsize=10)
    ax3.grid(axis="y", linestyle="--", alpha=0.3)
    ax3.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig3)
    plt.close(fig3)
else:
    st.info("Sem dados para exibir com os filtros selecionados.")

# ── Gráfico 4 — Boxplot por fase ────────────────────────────────────
st.subheader("🎯 Gols por Fase do Torneio")
st.caption("Princípios Gestalt: Similaridade (cores por fase) + Proximidade (fases em ordem de progressão)")

ordem = ["Fase de Grupos", "Oitavas de Final", "Quartas de Final", "Semifinal", "Final"]
cores = ["#1f6feb", "#388bfd", "#f0b429", "#e3b341", "#f85149"]
dados_fase    = [matches_f[matches_f["Stage_Clean"] == f]["Total_Goals"].dropna() for f in ordem]
dados_validos = [(d, c, o) for d, c, o in zip(dados_fase, cores, ordem) if len(d) > 0]

if dados_validos:
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    bp = ax4.boxplot(
        [d for d, _, _ in dados_validos],
        patch_artist=True,
        medianprops=dict(color="white", linewidth=2),
        whiskerprops=dict(color="#8b949e"),
        capprops=dict(color="#8b949e"),
        flierprops=dict(marker="o", color="#f85149", alpha=0.5, markersize=5)
    )
    for patch, (_, cor, _) in zip(bp["boxes"], dados_validos):
        patch.set_facecolor(cor)
        patch.set_alpha(0.8)
    ax4.set_xticklabels([o for _, _, o in dados_validos], fontsize=10)
    ax4.set_ylabel("Gols por Partida")
    ax4.set_xlabel("Fase do Torneio")
    ax4.grid(axis="y", linestyle="--", alpha=0.3)
    ax4.spines[["top", "right"]].set_visible(False)
    ax4.text(0.98, 0.97, "ANOVA: p = 0.0375 (p < 0.05)",
             transform=ax4.transAxes, ha="right", va="top", fontsize=9,
             color="#8b949e",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#21262d", alpha=0.8))
    st.pyplot(fig4)
    plt.close(fig4)
else:
    st.info("Sem dados suficientes para o boxplot com os filtros selecionados.")

# ── Gráfico 5 — Scatter público vs gols ─────────────────────────────
st.subheader("👥 Público vs Gols por Partida")
st.caption("Princípios Gestalt: Continuidade (linha de regressão) + Figura-fundo (tendência destacada)")

m_plot = matches_f[matches_f["Attendance"] > 0]
if len(m_plot) > 1:
    fig5, ax5 = plt.subplots(figsize=(12, 5))
    ax5.scatter(m_plot["Attendance"], m_plot["Total_Goals"],
                alpha=0.25, color="#1f6feb", s=30, zorder=2)
    z      = np.polyfit(m_plot["Attendance"], m_plot["Total_Goals"], 1)
    p_line = np.poly1d(z)
    x_line = np.linspace(m_plot["Attendance"].min(), m_plot["Attendance"].max(), 200)
    ax5.plot(x_line, p_line(x_line), color="#f0b429",
             linewidth=2, linestyle="--", zorder=3, label="Linha de tendência")
    corr, pval = stats.pearsonr(m_plot["Attendance"], m_plot["Total_Goals"])
    ax5.text(0.97, 0.92, f"r = {corr:.3f}  |  p = {pval:.4f}",
             transform=ax5.transAxes, ha="right", va="top", fontsize=10,
             color="#8b949e",
             bbox=dict(boxstyle="round,pad=0.4", facecolor="#21262d", alpha=0.8))
    ax5.set_xlabel("Público (Attendance)")
    ax5.set_ylabel("Gols na Partida")
    ax5.legend(framealpha=0.2, fontsize=10)
    ax5.grid(linestyle="--", alpha=0.3)
    ax5.spines[["top", "right"]].set_visible(False)
    st.pyplot(fig5)
    plt.close(fig5)
else:
    st.info("Dados insuficientes para o gráfico de dispersão com os filtros selecionados.")

# ── Footer ───────────────────────────────────────────────────────────
st.markdown("""
    <hr style='border-color:#30363d; margin-top:40px;'>
    <p style='text-align:center; color:#8b949e; font-size:13px;'>
        Projeto AVD — CESAR School &nbsp;|&nbsp;
        Dados: Kaggle + Wikipedia (Web Scraping) &nbsp;|&nbsp;
        Desenvolvido com Streamlit
    </p>
""", unsafe_allow_html=True)
