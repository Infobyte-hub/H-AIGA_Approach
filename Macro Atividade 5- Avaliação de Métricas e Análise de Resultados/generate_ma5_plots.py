import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# =============================
# CONFIG
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
OUTPUT_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(RESULTS_DIR, "responses.csv"))

# =============================
# PADRÃO VISUAL (PROFISSIONAL)
# =============================
plt.rcParams.update({
    "font.size": 11,
    "axes.titlesize": 13,
    "axes.labelsize": 11
})

# =============================
# SANITY CHECK
# =============================
required_cols = ["IGA_h", "IGA_ia", "acc_ia", "trust_ia"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Coluna ausente no CSV: {col}")

# =============================
# PLOT 00 — RESUMO GERAL
# =============================
plt.figure()

labels = ["IA", "Humano"]
acc_values = [df["acc_ia"].mean(), df["acc_h"].mean()]
iga_values = [df["IGA_ia"].mean(), df["IGA_h"].mean()]

x = np.arange(len(labels))

plt.bar(x - 0.2, acc_values, width=0.4, label="Acurácia")
plt.bar(x + 0.2, iga_values, width=0.4, label="IGA")

plt.xticks(x, labels)
plt.ylabel("Score")
plt.title("Resumo Geral: Acurácia vs Governança")
plt.legend()
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "00_resumo_geral.png"))
plt.close()

# =============================
# PLOT 01 — IGA IA vs HUMANO
# =============================
plt.figure()
plt.scatter(df["IGA_h"], df["IGA_ia"])

plt.xlabel("IGA Humano")
plt.ylabel("IGA IA")
plt.title("Comparação de Governança: Humano vs IA")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "01_iga_vs_ia.png"))
plt.close()

# =============================
# PLOT 02 — OVERCONFIDENCE
# =============================
plt.figure()

erro = df["acc_ia"] < 1.0
overconf = (df["trust_ia"] > 0.8) & erro

plt.scatter(df["trust_ia"], df["acc_ia"], alpha=0.3, label="Geral")
plt.scatter(df["trust_ia"][overconf], df["acc_ia"][overconf], label="Overconfidence crítico")

plt.xlabel("Confiança da IA (Trust)")
plt.ylabel("Acurácia da IA")
plt.title("Detecção de Overconfidence")
plt.legend()
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "02_overconfidence.png"))
plt.close()

# =============================
# PLOT 03 — TEMPO vs IGA HUMANO
# =============================
plt.figure()
plt.scatter(df["tempo"], df["IGA_h"])

plt.xlabel("Tempo de Resposta (s)")
plt.ylabel("IGA Humano")
plt.title("Impacto do Tempo na Governança Humana")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "03_tempo_vs_iga.png"))
plt.close()

# =============================
# PLOT 04 — PENALIZAÇÃO vs IGA
# =============================
plt.figure()
plt.scatter(df["P_ia"], df["IGA_ia"])

plt.xlabel("Penalização (P)")
plt.ylabel("IGA IA")
plt.title("Impacto da Penalização Técnica")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "04_penalizacao_vs_iga.png"))
plt.close()

# =============================
# PLOT 05 — FAIRNESS vs RISK
# =============================
plt.figure()
plt.scatter(df["fairness_ia"], df["risk_ia"])

plt.xlabel("Fairness (disparidade)")
plt.ylabel("Risk (erro ponderado)")
plt.title("Trade-off entre Equidade e Risco")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "05_fairness_vs_risk.png"))
plt.close()

# =============================
# PLOT 06 — DISTRIBUIÇÃO IGA
# =============================
plt.figure()

plt.hist(df["IGA_ia"], bins=10, alpha=0.5, label="IA")
plt.hist(df["IGA_h"], bins=10, alpha=0.5, label="Humano")

plt.xlabel("IGA")
plt.ylabel("Frequência")
plt.title("Distribuição do IGA")
plt.legend()
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "06_distribuicao_iga.png"))
plt.close()

# =============================
# PLOT 07 — GAP IA vs HUMANO
# =============================
plt.figure()

gap = df["IGA_h"] - df["IGA_ia"]
plt.hist(gap, bins=10)

plt.xlabel("Diferença de Governança (Humano - IA)")
plt.ylabel("Frequência")
plt.title("Distribuição do Gap de Governança")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "07_gap_ia_humano.png"))
plt.close()

# =============================
# PLOT 08 — DISTRIBUIÇÃO PENALIZAÇÃO
# =============================
plt.figure()

plt.hist(df["P_ia"], bins=10)

plt.xlabel("Penalização (P)")
plt.ylabel("Frequência")
plt.title("Distribuição das Penalizações")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "08_distribuicao_penalizacao.png"))
plt.close()

# =============================
# PLOT 09 — PERFORMANCE vs GOVERNANÇA
# =============================
plt.figure()

plt.scatter(df["acc_ia"], df["IGA_ia"])

plt.xlabel("Acurácia IA")
plt.ylabel("IGA IA")
plt.title("Acurácia vs Governança")
plt.grid(True)

plt.savefig(os.path.join(OUTPUT_DIR, "09_perf_vs_governance.png"))
plt.close()

print("✅ Todos os 10 plots gerados com sucesso.")
