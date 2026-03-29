import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
OUTPUT_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(RESULTS_DIR, "responses.csv"))

# =============================
# SANITY CHECK
# =============================
required_cols = ["IGA_h", "IGA_ia", "acc_ia", "trust_ia"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Coluna ausente no CSV: {col}")

# =============================
# PLOT 1 — IGA IA vs HUMANO
# =============================
plt.figure()
plt.scatter(df["IGA_h"], df["IGA_ia"])
plt.xlabel("IGA Humano")
plt.ylabel("IGA IA")
plt.title("Comparação de Governança: Humano vs IA")
plt.savefig(os.path.join(OUTPUT_DIR, "01_iga_vs_ia.png"))
plt.close()

# =============================
# PLOT 2 — OVERCONFIDENCE REAL
# =============================
plt.figure()

erro = df["acc_ia"] < 1.0
overconf = (df["trust_ia"] > 0.8) & erro

plt.scatter(df["trust_ia"], df["acc_ia"], alpha=0.3, label="Geral")
plt.scatter(df["trust_ia"][overconf], df["acc_ia"][overconf], label="Overconfidence crítico")

plt.xlabel("Confiança (Trust IA)")
plt.ylabel("Acurácia IA")
plt.title("Overconfidence Detection")

plt.legend()
plt.savefig(os.path.join(OUTPUT_DIR, "02_overconfidence.png"))
plt.close()

# =============================
# PLOT 3 — TEMPO vs IGA HUMANO
# =============================
plt.figure()
plt.scatter(df["tempo"], df["IGA_h"])
plt.xlabel("Tempo")
plt.ylabel("IGA Humano")
plt.title("Tempo vs Governança Humana")
plt.savefig(os.path.join(OUTPUT_DIR, "03_tempo_vs_iga.png"))
plt.close()

# =============================
# PLOT 4 — PENALIZAÇÃO vs IGA
# =============================
plt.figure()
plt.scatter(df["P_ia"], df["IGA_ia"])
plt.xlabel("Penalização (P IA)")
plt.ylabel("IGA IA")
plt.title("Impacto da Penalização Técnica")
plt.savefig(os.path.join(OUTPUT_DIR, "04_penalizacao_vs_iga.png"))
plt.close()

# =============================
# PLOT 5 — FAIRNESS vs RISK
# =============================
plt.figure()
plt.scatter(df["fairness_ia"], df["risk_ia"])
plt.xlabel("Fairness")
plt.ylabel("Risk")
plt.title("Trade-off entre Equidade e Risco")
plt.savefig(os.path.join(OUTPUT_DIR, "05_fairness_vs_risk.png"))
plt.close()

# =============================
# PLOT 6 — DISTRIBUIÇÃO IGA
# =============================
plt.figure()
plt.hist(df["IGA_ia"], bins=10, alpha=0.5, label="IA")
plt.hist(df["IGA_h"], bins=10, alpha=0.5, label="Humano")
plt.xlabel("IGA")
plt.ylabel("Frequência")
plt.title("Distribuição de Governança")
plt.legend()
plt.savefig(os.path.join(OUTPUT_DIR, "06_distribuicao_iga.png"))
plt.close()

# =============================
# PLOT 7 — GAP IA vs HUMANO
# =============================
plt.figure()
gap = df["IGA_h"] - df["IGA_ia"]
plt.hist(gap, bins=10)
plt.xlabel("Diferença (Humano - IA)")
plt.title("Gap de Governança")
plt.savefig(os.path.join(OUTPUT_DIR, "07_gap_ia_humano.png"))
plt.close()

# =============================
# PLOT 8 — COMPLIANCE (SE EXISTIR)
# =============================
if "Pcomp_ia" in df.columns:
    plt.figure()
    plt.scatter(df["Pcomp_ia"], df["IGA_ia"])
    plt.xlabel("Penalização Normativa (Pcomp IA)")
    plt.ylabel("IGA IA")
    plt.title("Impacto da Não Conformidade Normativa")
    plt.savefig(os.path.join(OUTPUT_DIR, "08_compliance_vs_iga.png"))
    plt.close()

print("✅ Todos os plots gerados com sucesso.")
