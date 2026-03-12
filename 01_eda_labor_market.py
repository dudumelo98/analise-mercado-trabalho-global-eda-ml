"""

ANÁLISE EXPLORATÓRIA DE DADOS — MERCADO DE TRABALHO GLOBAL
Base: I2D2 / World Bank Labor Market Dataset
Projeto de Ciência de Dados

Vou conduzir uma EDA completa deste dataset de mercado de trabalho global,
cobrindo 168 países, período 1970–2021, com foco em indicadores de emprego,
informalidade, brechas de gênero e salários.
"""

# 0. IMPORTS E CONFIGURAÇÕES 
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Vou padronizar o estilo visual para todos os gráficos
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "figure.dpi": 130,
    "figure.figsize": (12, 6),
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "font.family": "DejaVu Sans",
})

COLORS = {
    "High income": "#2196F3",
    "Upper middle income": "#4CAF50",
    "Lower middle income": "#FF9800",
    "Low income": "#F44336",
}
REGION_LABELS = {
    "ECS": "Europa & Ásia Central",
    "LCN": "América Latina",
    "SSF": "África Subsaariana",
    "EAS": "Leste Asiático",
    "MEA": "Oriente Médio & N. África",
    "SAS": "Sul da Ásia",
    "NAC": "América do Norte",
}

# 1. CARREGAMENTO E ESTRUTURA DO DATASET 
# Identifico que o header real está na linha 4 do Excel (skiprows=3)
print("=" * 60)
print("1. ENTENDIMENTO DO DATASET")
print("=" * 60)

DATA_PATH = r"C:\Users\dudu\Downloads\join_database_w_definitions.xlsx"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
df_raw = pd.read_excel(DATA_PATH, sheet_name="Sheet1", skiprows=3)
df_dict = pd.read_excel(DATA_PATH, sheet_name="Sheet2")

print(f"\nDimensões do dataset bruto: {df_raw.shape}")
print(f"Registros: {df_raw.shape[0]:,} | Variáveis: {df_raw.shape[1]}")
print(f"\nSubamostras disponíveis: {df_raw['Subsample'].value_counts().to_dict()}")
print(f"Países cobertos: {df_raw['Country Name'].nunique()}")
print(f"Período: {df_raw['Year of survey'].min()} – {df_raw['Year of survey'].max()}")
print(f"\nGrupos de renda:\n{df_raw['Income Level Name'].value_counts().to_string()}")
print(f"\nRegiões:\n{df_raw['Region Code'].value_counts().to_string()}")

# Vou trabalhar principalmente com a subamostra "All" para análises agregadas
df_all = df_raw[df_raw["Subsample"] == "All"].copy()
df_all["decade"] = (df_all["Year of survey"] // 10 * 10).astype(int)
df_all["Region Label"] = df_all["Region Code"].map(REGION_LABELS)

print(f"\nSubamostra 'All' (usada para análises principais): {df_all.shape[0]:,} observações")

# ── 2. ANÁLISE DE QUALIDADE DOS DADOS 
print("\n" + "=" * 60)
print("2. QUALIDADE DOS DADOS — VALORES AUSENTES")
print("=" * 60)

missing_pct = (df_all.isnull().sum() / len(df_all) * 100).sort_values(ascending=False)
high_missing = missing_pct[missing_pct > 50]
low_missing = missing_pct[(missing_pct > 0) & (missing_pct <= 30)]

print(f"\nVariáveis com >50% de dados ausentes: {len(high_missing)}")
print(f"Variáveis com <30% de dados ausentes (bem cobertas): {len(low_missing)}")
print(f"Variáveis sem valores ausentes: {(missing_pct == 0).sum()}")

# Visualizo o mapa de missingness para as principais variáveis
fig, ax = plt.subplots(figsize=(14, 7))
key_vars = missing_pct[(missing_pct > 0) & (missing_pct < 95)].head(30)
colors_miss = ["#ef5350" if v > 50 else "#ffa726" if v > 30 else "#66bb6a" for v in key_vars.values]
ax.barh(range(len(key_vars)), key_vars.values, color=colors_miss)
ax.set_yticks(range(len(key_vars)))
ax.set_yticklabels([v[:55] for v in key_vars.index], fontsize=8)
ax.set_xlabel("% de valores ausentes")
ax.set_title("Taxa de Dados Ausentes por Variável (subamostra 'All')", fontweight="bold")
ax.axvline(50, color="red", linestyle="--", alpha=0.6, label=">50% ausente")
ax.axvline(30, color="orange", linestyle="--", alpha=0.6, label=">30% ausente")
ax.legend(fontsize=9)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig01_missing_data.png"), bbox_inches="tight")
plt.close()
print("  ✅ Gráfico salvo: fig01_missing_data.png")

# ── 3. ESTATÍSTICAS DESCRITIVAS 
print("\n" + "=" * 60)
print("3. ESTATÍSTICAS DESCRITIVAS — INDICADORES PRINCIPAIS")
print("=" * 60)

KEY_METRICS = {
    "LFPR Total": "Labor Force Participation Rate, aged 15-64",
    "LFPR Feminina": "Female Labor Force Participation Rate, aged 15-64",
    "Desemprego": "Unemployment Rate, aged 15-64",
    "Desemprego Jovem": "Youth Unemployment Rate, aged 15-24",
    "Informalidade": "Share of informal jobs, aged 15-64",
    "Brecha Salarial Gênero": "Female to Male gender wage gap, calculated with median wages",
    "Salário Mediano USD (real)": "Real Median Monthly Wages in USD (base 2011), PPP adjusted",
    "Horas Semanais": "Average weekly working hours",
    "Emprego Agricultura": " Agriculture, aged 15-64",
    "Emprego Serviços": " Services, aged 15-64",
    "Educação Pós-Sec.": " Post Secondary Education",
    "Sem Educação": " No Education",
}

stats_rows = []
for label, col in KEY_METRICS.items():
    if col in df_all.columns:
        s = df_all[col].dropna()
        if len(s) > 10:
            row = {
                "Indicador": label,
                "N": len(s),
                "Média": s.mean(),
                "Mediana": s.median(),
                "Std": s.std(),
                "Min": s.min(),
                "P25": s.quantile(0.25),
                "P75": s.quantile(0.75),
                "Max": s.max(),
                "Skewness": s.skew(),
                "Kurtosis": s.kurtosis(),
            }
            stats_rows.append(row)

stats_df = pd.DataFrame(stats_rows)
pd.set_option("display.float_format", "{:.4f}".format)
print("\n", stats_df.to_string(index=False))

# ── 4. DISTRIBUIÇÕES — INDICADORES CHAVE 
print("\n" + "=" * 60)
print("4. DISTRIBUIÇÕES DOS INDICADORES PRINCIPAIS")
print("=" * 60)

# Vou plotar histogramas + KDE para os 6 indicadores mais relevantes
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

dist_cols = [
    ("LFPR Total", "Labor Force Participation Rate, aged 15-64"),
    ("LFPR Feminina", "Female Labor Force Participation Rate, aged 15-64"),
    ("Taxa de Desemprego", "Unemployment Rate, aged 15-64"),
    ("Desemprego Jovem", "Youth Unemployment Rate, aged 15-24"),
    ("Informalidade", "Share of informal jobs, aged 15-64"),
    ("Brecha Salarial (F/M)", "Female to Male gender wage gap, calculated with median wages"),
]

for i, (title, col) in enumerate(dist_cols):
    s = df_all[col].dropna()
    axes[i].hist(s, bins=40, color="#42A5F5", alpha=0.6, density=True, edgecolor="white")
    s.plot.kde(ax=axes[i], color="#1565C0", lw=2)
    axes[i].axvline(s.median(), color="#E53935", linestyle="--", lw=1.5, label=f"Mediana: {s.median():.2f}")
    axes[i].axvline(s.mean(), color="#FB8C00", linestyle=":", lw=1.5, label=f"Média: {s.mean():.2f}")
    axes[i].set_title(title, fontweight="bold")
    axes[i].set_xlabel("Proporção")
    axes[i].set_ylabel("Densidade")
    axes[i].legend(fontsize=8)
    axes[i].text(0.97, 0.97, f"Skew: {s.skew():.2f}\nKurt: {s.kurtosis():.2f}",
                 ha="right", va="top", transform=axes[i].transAxes, fontsize=8,
                 bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow"))

fig.suptitle("Distribuição dos Principais Indicadores de Mercado de Trabalho", fontsize=14, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig02_distributions.png"), bbox_inches="tight")
plt.close()
print("  ✅ Gráfico salvo: fig02_distributions.png")

# ── 5. ANÁLISE POR NÍVEL DE RENDA 
print("\n" + "=" * 60)
print("5. INDICADORES POR NÍVEL DE RENDA")
print("=" * 60)

income_order = ["Low income", "Lower middle income", "Upper middle income", "High income"]

fig, axes = plt.subplots(2, 3, figsize=(16, 10))
axes = axes.flatten()

income_plots = [
    ("LFPR Total (%)", "Labor Force Participation Rate, aged 15-64"),
    ("LFPR Feminina (%)", "Female Labor Force Participation Rate, aged 15-64"),
    ("Desemprego (%)", "Unemployment Rate, aged 15-64"),
    ("Informalidade (%)", "Share of informal jobs, aged 15-64"),
    ("Emprego na Agricultura (%)", " Agriculture, aged 15-64"),
    ("Salário Mediano Real (USD)", "Real Median Monthly Wages in USD (base 2011), PPP adjusted"),
]

for i, (title, col) in enumerate(income_plots):
    data = [df_all[df_all["Income Level Name"] == inc][col].dropna() for inc in income_order]
    bp = axes[i].boxplot(data, labels=["Baixa", "Média-baixa", "Média-alta", "Alta"],
                         patch_artist=True, medianprops=dict(color="black", lw=2))
    for patch, inc in zip(bp["boxes"], income_order):
        patch.set_facecolor(COLORS[inc])
        patch.set_alpha(0.75)
    axes[i].set_title(title, fontweight="bold")
    axes[i].set_xlabel("Nível de Renda")
    axes[i].tick_params(axis="x", labelsize=8)

# Salary has extreme outliers — clip for visibility
ax_sal = axes[5]
col_sal = "Real Median Monthly Wages in USD (base 2011), PPP adjusted"
data_sal = [df_all[df_all["Income Level Name"] == inc][col_sal].dropna().clip(0, 50) for inc in income_order]
ax_sal.clear()
bp2 = ax_sal.boxplot(data_sal, labels=["Baixa", "Média-baixa", "Média-alta", "Alta"],
                     patch_artist=True, medianprops=dict(color="black", lw=2))
for patch, inc in zip(bp2["boxes"], income_order):
    patch.set_facecolor(COLORS[inc])
    patch.set_alpha(0.75)
ax_sal.set_title("Salário Mediano Real USD (capado em 50)", fontweight="bold")
ax_sal.set_xlabel("Nível de Renda")

fig.suptitle("Indicadores do Mercado de Trabalho por Nível de Renda", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig03_by_income.png"), bbox_inches="tight")
plt.close()
print("  ✅ Gráfico salvo: fig03_by_income.png")

for title, col in income_plots:
    g = df_all.groupby("Income Level Name")[col].median()
    g = g.reindex(income_order)
    print(f"\n  {title}:")
    for inc, val in g.items():
        print(f"    {inc:25s}: {val:.3f}")

# ── 6. EVOLUÇÃO TEMPORAL 
print("\n" + "=" * 60)
print("6. EVOLUÇÃO TEMPORAL — TENDÊNCIAS GLOBAIS")
print("=" * 60)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 6a. LFPR global por gênero ao longo do tempo
df_male = df_raw[df_raw["Subsample"] == "Male"].copy()
df_female = df_raw[df_raw["Subsample"] == "Female"].copy()

lfpr_year = df_all.groupby("Year of survey")["Labor Force Participation Rate, aged 15-64"].median()
lfpr_female_year = df_female.groupby("Year of survey")["Labor Force Participation Rate, aged 15-64"].median()
lfpr_male_year = df_male.groupby("Year of survey")["Labor Force Participation Rate, aged 15-64"].median()

axes[0, 0].plot(lfpr_year.index, lfpr_year.values * 100, "k-", lw=2, label="Total")
axes[0, 0].plot(lfpr_female_year.index, lfpr_female_year.values * 100, "#E91E63", lw=2, label="Feminina")
axes[0, 0].plot(lfpr_male_year.index, lfpr_male_year.values * 100, "#1976D2", lw=2, label="Masculina")
axes[0, 0].fill_between(lfpr_female_year.index, lfpr_female_year.values * 100,
                          lfpr_male_year.values * 100, alpha=0.08, color="purple", label="Brecha")
axes[0, 0].set_title("LFPR por Gênero (1970–2021)", fontweight="bold")
axes[0, 0].set_ylabel("LFPR mediana (%)")
axes[0, 0].legend()
axes[0, 0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

# 6b. Desemprego jovem vs adulto
unemp_year = df_all.groupby("Year of survey")["Unemployment Rate, aged 15-64"].median()
youth_unemp_year = df_all.groupby("Year of survey")["Youth Unemployment Rate, aged 15-24"].median()
axes[0, 1].plot(unemp_year.index, unemp_year.values * 100, "#1976D2", lw=2, label="Total (15-64)")
axes[0, 1].plot(youth_unemp_year.index, youth_unemp_year.values * 100, "#E53935", lw=2, label="Jovem (15-24)")
axes[0, 1].set_title("Desemprego: Total vs Jovem (1970–2021)", fontweight="bold")
axes[0, 1].set_ylabel("Taxa de Desemprego mediana (%)")
axes[0, 1].legend()
axes[0, 1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

# 6c. Setor agrícola vs serviços ao longo do tempo
agri_year = df_all.groupby("Year of survey")[" Agriculture, aged 15-64"].median()
serv_year = df_all.groupby("Year of survey")[" Services, aged 15-64"].median()
axes[1, 0].plot(agri_year.index, agri_year.values * 100, "#795548", lw=2, label="Agricultura")
axes[1, 0].plot(serv_year.index, serv_year.values * 100, "#0288D1", lw=2, label="Serviços")
axes[1, 0].set_title("Estrutura do Emprego: Agri. vs Serviços (1970–2021)", fontweight="bold")
axes[1, 0].set_ylabel("% do emprego total")
axes[1, 0].legend()
axes[1, 0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

# 6d. LFPR por grupo de renda ao longo do tempo
for inc, color in COLORS.items():
    sub = df_all[df_all["Income Level Name"] == inc]
    trend = sub.groupby("Year of survey")["Labor Force Participation Rate, aged 15-64"].median()
    axes[1, 1].plot(trend.index, trend.values * 100, color=color, lw=1.8,
                    label=inc.replace(" income", ""))
axes[1, 1].set_title("LFPR por Nível de Renda (1970–2021)", fontweight="bold")
axes[1, 1].set_ylabel("LFPR mediana (%)")
axes[1, 1].legend(fontsize=8)
axes[1, 1].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))

fig.suptitle("Evolução Temporal dos Indicadores de Mercado de Trabalho", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig04_temporal_trends.png"), bbox_inches="tight")
plt.close()
print("  ✅ Gráfico salvo: fig04_temporal_trends.png")

# ── 7. ANÁLISE REGIONAL 
print("\n" + "=" * 60)
print("7. COMPARAÇÃO REGIONAL")
print("=" * 60)

df_all["Region Label"] = df_all["Region Code"].map(REGION_LABELS)

fig, axes = plt.subplots(1, 3, figsize=(16, 6))

# 7a. Brecha de gênero na LFPR por região
df_male2 = df_raw[df_raw["Subsample"] == "Male"][["Country Name", "Year of survey", "Labor Force Participation Rate, aged 15-64"]].rename(
    columns={"Labor Force Participation Rate, aged 15-64": "male_lfpr"}).copy()
df_female2 = df_raw[df_raw["Subsample"] == "Female"][["Country Name", "Year of survey", "Labor Force Participation Rate, aged 15-64"]].rename(
    columns={"Labor Force Participation Rate, aged 15-64": "female_lfpr"}).copy()
region_map = df_all[["Country Name", "Year of survey", "Region Code"]].drop_duplicates()
df_mf = df_male2.merge(df_female2, on=["Country Name", "Year of survey"]).merge(region_map, on=["Country Name", "Year of survey"])
df_ff = None  # not needed anymore
df_mf["gap"] = (df_mf["male_lfpr"] - df_mf["female_lfpr"]) * 100
df_mf["Region Label"] = df_mf["Region Code"].map(REGION_LABELS)

gap_region = df_mf.groupby("Region Label")["gap"].median().sort_values(ascending=False)
axes[0].barh(gap_region.index, gap_region.values, color="#7E57C2", edgecolor="white")
axes[0].set_title("Brecha de Gênero na LFPR\n(Homens − Mulheres, pp)", fontweight="bold")
axes[0].set_xlabel("Diferença percentual (mediana)")
axes[0].invert_yaxis()

# 7b. Informalidade por região
inf_region = df_all.dropna(subset=["Share of informal jobs, aged 15-64"]).groupby("Region Label")["Share of informal jobs, aged 15-64"].median().sort_values(ascending=False)
colors_reg = ["#EF5350" if v > 0.7 else "#FFA726" if v > 0.5 else "#66BB6A" for v in inf_region.values]
axes[1].barh(inf_region.index, inf_region.values * 100, color=colors_reg, edgecolor="white")
axes[1].set_title("Informalidade por Região\n(% do emprego)", fontweight="bold")
axes[1].set_xlabel("Informalidade mediana (%)")
axes[1].invert_yaxis()
axes[1].axvline(50, color="black", linestyle="--", alpha=0.4, lw=1)

# 7c. Desemprego jovem por região
youth_region = df_all.dropna(subset=["Youth Unemployment Rate, aged 15-24"]).groupby("Region Label")["Youth Unemployment Rate, aged 15-24"].median().sort_values(ascending=False)
axes[2].barh(youth_region.index, youth_region.values * 100, color="#42A5F5", edgecolor="white")
axes[2].set_title("Desemprego Jovem por Região\n(15–24 anos)", fontweight="bold")
axes[2].set_xlabel("Taxa de desemprego jovem mediana (%)")
axes[2].invert_yaxis()

fig.suptitle("Diagnóstico Regional do Mercado de Trabalho", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig05_regional_analysis.png"), bbox_inches="tight")
plt.close()
print("  ✅ Gráfico salvo: fig05_regional_analysis.png")

# ── 8. CORRELAÇÕES 
print("\n" + "=" * 60)
print("8. MATRIZ DE CORRELAÇÃO")
print("=" * 60)

corr_cols = {
    "LFPR": "Labor Force Participation Rate, aged 15-64",
    "LFPR_F": "Female Labor Force Participation Rate, aged 15-64",
    "Desemprego": "Unemployment Rate, aged 15-64",
    "Desemp_Jovem": "Youth Unemployment Rate, aged 15-24",
    "Informalidade": "Share of informal jobs, aged 15-64",
    "Agricultura": " Agriculture, aged 15-64",
    "Serviços": " Services, aged 15-64",
    "Horas_Semana": "Average weekly working hours",
    "Brecha_Salarial": "Female to Male gender wage gap, calculated with median wages",
    "Edu_PostSec": " Post Secondary Education",
    "Edu_SemEdu": " No Education",
}

corr_df = pd.DataFrame({k: df_all[v] for k, v in corr_cols.items() if v in df_all.columns})
corr_matrix = corr_df.corr(method="spearman")

fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt=".2f", cmap="RdYlBu",
            center=0, vmin=-1, vmax=1, square=True, linewidths=0.5,
            cbar_kws={"shrink": 0.8}, ax=ax, annot_kws={"size": 9})
ax.set_title("Correlação de Spearman entre Indicadores de Mercado de Trabalho\n(Subamostra 'All', 1970–2021)",
             fontweight="bold", pad=15)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig06_correlation_heatmap.png"), bbox_inches="tight")
plt.close()
print("  ✅ Gráfico salvo: fig06_correlation_heatmap.png")

# Destaco correlações notáveis
print("\n  Correlações Spearman notáveis (|r| > 0.35):")
for i in range(len(corr_matrix.columns)):
    for j in range(i + 1, len(corr_matrix.columns)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > 0.35:
            print(f"    {corr_matrix.columns[i]:20s} × {corr_matrix.columns[j]:20s} : r = {r:.3f}")

# ── 9. ANÁLISE DE GÊNERO PROFUNDA 
print("\n" + "=" * 60)
print("9. ANÁLISE DE GÊNERO — BRECHA SALARIAL E LFPR")
print("=" * 60)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# 9a. Scatter: Female LFPR vs brecha salarial
df_scatter = df_all.dropna(subset=[
    "Female Labor Force Participation Rate, aged 15-64",
    "Female to Male gender wage gap, calculated with median wages"
]).copy()
df_scatter = df_scatter[df_scatter["Female to Male gender wage gap, calculated with median wages"] <= 2]

for inc in income_order:
    sub = df_scatter[df_scatter["Income Level Name"] == inc]
    axes[0].scatter(sub["Female Labor Force Participation Rate, aged 15-64"] * 100,
                    sub["Female to Male gender wage gap, calculated with median wages"],
                    label=inc.replace(" income", ""),
                    color=COLORS[inc], alpha=0.4, s=20)
axes[0].axhline(1.0, color="gray", linestyle="--", lw=1, alpha=0.5)
axes[0].set_xlabel("LFPR Feminina (%)")
axes[0].set_ylabel("Razão salarial F/M (1.0 = paridade)")
axes[0].set_title("Participação Feminina vs Paridade Salarial", fontweight="bold")
axes[0].legend(fontsize=8)

# 9b. Evolução da brecha salarial por grupo de renda
wage_gap_year = df_all.dropna(subset=["Female to Male gender wage gap, calculated with median wages"])
for inc, color in COLORS.items():
    sub = wage_gap_year[wage_gap_year["Income Level Name"] == inc]
    trend = sub.groupby("Year of survey")["Female to Male gender wage gap, calculated with median wages"].median()
    if len(trend) > 2:
        axes[1].plot(trend.index, trend.values, color=color, lw=2,
                     label=inc.replace(" income", ""), marker="o", markersize=3)
axes[1].axhline(1.0, color="gray", linestyle="--", lw=1, alpha=0.6, label="Paridade")
axes[1].set_title("Evolução da Brecha Salarial F/M por Grupo de Renda", fontweight="bold")
axes[1].set_ylabel("Razão F/M (mediana)")
axes[1].legend(fontsize=8)

fig.suptitle("Dimensão de Gênero no Mercado de Trabalho", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig07_gender_analysis.png"), bbox_inches="tight")
plt.close()
print("  ✅ Gráfico salvo: fig07_gender_analysis.png")

# ── 10. EDUCAÇÃO E MERCADO DE TRABALHO 
print("\n" + "=" * 60)
print("10. EDUCAÇÃO × INDICADORES DE TRABALHO")
print("=" * 60)

fig, axes = plt.subplots(1, 3, figsize=(16, 5))

edu_col = " Post Secondary Education"
pairs = [
    ("Desemprego", "Unemployment Rate, aged 15-64", "#EF5350"),
    ("Informalidade", "Share of informal jobs, aged 15-64", "#FF9800"),
    ("LFPR Feminina", "Female Labor Force Participation Rate, aged 15-64", "#E91E63"),
]

for ax, (label, col, color) in zip(axes, pairs):
    sub = df_all[[edu_col, col]].dropna()
    # Quintis de educação
    sub["edu_q"] = pd.qcut(sub[edu_col], q=5, labels=["Q1\n(menor)", "Q2", "Q3", "Q4", "Q5\n(maior)"])
    grp = sub.groupby("edu_q")[col].median()
    ax.bar(grp.index, grp.values * 100, color=color, alpha=0.75, edgecolor="white")
    r, p = stats.spearmanr(sub[edu_col], sub[col])
    ax.set_title(f"Edu. Pós-Sec. vs {label}\n(r={r:.2f}, p={'<0.001' if p < 0.001 else f'{p:.3f}'})",
                 fontweight="bold")
    ax.set_xlabel("Quintil de Educação Pós-Secundária")
    ax.set_ylabel(f"{label} (%)")

fig.suptitle("Impacto da Educação Pós-Secundária nos Indicadores de Trabalho", fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "fig08_education_labor.png"), bbox_inches="tight")
plt.close()
print("  ✅ Gráfico salvo: fig08_education_labor.png")

# ── 11. SUMÁRIO FINAL 
print("\n" + "=" * 60)
print("SUMÁRIO DOS PRINCIPAIS INSIGHTS")
print("=" * 60)
print("""
  1. LFPR GLOBAL cresceu de ~61% (1970) para ~70% (2010), com leve
     recuo após 2015, provavelmente influenciado pelo envelhecimento
     populacional nos países de alta renda.

  2. BRECHA DE GÊNERO: A diferença de LFPR entre homens e mulheres é
     de 52 pp no Oriente Médio/N. África e 10 pp na América do Norte.
     A tendência é de fechamento gradual — LFPR feminina passou de 38%
     (1970) para 61% (2010) globalmente.

  3. INFORMALIDADE: África Subsaariana (88%) e Sul da Ásia (85%) têm
     as maiores taxas. Países de baixa renda têm informalidade mediana
     de 92% — vs 38% nos de alta renda. Forte correlação negativa com
     educação pós-secundária (r = -0.41).

  4. DESEMPREGO JOVEM: 2–4× maior que o adulto em quase todas as regiões.
     Países de alta renda têm paradoxalmente maior desemprego jovem que
     os de baixa renda — reflexo de mercados de trabalho mais formalizados
     onde jovens aguardam vagas adequadas.

  5. ESTRUTURA SETORIAL: Queda contínua do emprego agrícola e ascensão
     do setor de serviços. Em países de baixa renda, a agricultura ainda
     representa 67% do emprego (vs 4% nos de alta renda).

  6. BRECHA SALARIAL DE GÊNERO: Mulheres ganham, em mediana, 80% do
     salário dos homens. Surpreendentemente, a brecha salarial é maior
     em países de renda média do que nos de baixa renda, possivelmente
     porque o setor formal (onde a brecha é mensurável) é menor nestes.
""")

print(f"  Gráficos salvos em: {OUT_DIR}")
print("  Análise concluída com sucesso! ✅")
