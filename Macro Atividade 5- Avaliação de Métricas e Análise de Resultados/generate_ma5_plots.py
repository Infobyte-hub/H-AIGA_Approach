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
# PLOT 00 — RESUMO GERAL
# =============================
plt.figure()
labels = ["Acc IA", "Acc Humano", "IGA IA", "IGA Humano"]
values = [
    df["acc_ia"].mean(),
    df["acc_h"].mean(),
    df["IGA_ia"].mean(),
    df["IGA_h"].mean()
]
plt.bar(labels, values)
plt.title("Resumo Geral do Sistema")
plt.savefig(os.path.join(OUTPUT_DIR, "00_resumo_geral.png"))
plt.close()

# =============================
# PLOT 01 — IGA IA vs HUMANO
# =============================
plt.figure()
plt.scatter(df["IGA_h"], df["IGA_ia"])
plt.xlabel("IGA Humano")
plt.ylabel("IGA IA")
plt.savefig(os.path.join(OUTPUT_DIR, "01_iga_vs_ia.png"))
plt.close()

# =============================
# PLOT 02 — OVERCONFIDENCE
# =============================
plt.figure()
erro = df["acc_ia"] < 1.0
overconf = (df["trust_ia"] > 0.8) & erro
plt.scatter(df["trust_ia"], df["acc_ia"], alpha=0.3)
plt.scatter(df["trust_ia"][overconf], df["acc_ia"][overconf])
plt.savefig(os.path.join(OUTPUT_DIR, "02_overconfidence.png"))
plt.close()

# =============================
# PLOT 03 — TEMPO vs IGA
# =============================
plt.figure()
plt.scatter(df["tempo"], df["IGA_h"])
plt.savefig(os.path.join(OUTPUT_DIR, "03_tempo_vs_iga.png"))
plt.close()

# =============================
# PLOT 04 — PENALIZAÇÃO vs IGA
# =============================
plt.figure()
plt.scatter(df["P_ia"], df["IGA_ia"])
plt.savefig(os.path.join(OUTPUT_DIR, "04_penalizacao_vs_iga.png"))
plt.close()

# =============================
# PLOT 05 — FAIRNESS vs RISK
# =============================
plt.figure()
plt.scatter(df["fairness_ia"], df["risk_ia"])
plt.savefig(os.path.join(OUTPUT_DIR, "05_fairness_vs_risk.png"))
plt.close()

# =============================
# PLOT 06 — DISTRIBUIÇÃO IGA
# =============================
plt.figure()
plt.hist(df["IGA_ia"], bins=10, alpha=0.5)
plt.hist(df["IGA_h"], bins=10, alpha=0.5)
plt.savefig(os.path.join(OUTPUT_DIR, "06_distribuicao_iga.png"))
plt.close()

# =============================
# PLOT 07 — GAP IA vs HUMANO
# =============================
plt.figure()
gap = df["IGA_h"] - df["IGA_ia"]
plt.hist(gap, bins=10)
plt.savefig(os.path.join(OUTPUT_DIR, "07_gap_ia_humano.png"))
plt.close()

# =============================
# PLOT 08 — COMPLIANCE (SE EXISTIR)
# =============================
if "Pcomp_ia" in df.columns:
    plt.figure()
    plt.scatter(df["Pcomp_ia"], df["IGA_ia"])
    plt.savefig(os.path.join(OUTPUT_DIR, "08_compliance_vs_iga.png"))
    plt.close()

# =============================
# PLOT 09 — DECISÃO
# =============================
plt.figure()
counts = df["acesso"].value_counts()
plt.pie([counts.get(1,0), counts.get(0,0)], labels=["Liberado","Negado"], autopct='%1.1f%%')
plt.savefig(os.path.join(OUTPUT_DIR, "09_decisao.png"))
plt.close()

# =============================
# PLOT 10 — PERFORMANCE vs GOVERNANÇA
# =============================
plt.figure()
plt.scatter(df["acc_ia"], df["IGA_ia"])
plt.xlabel("Performance IA")
plt.ylabel("IGA IA")
plt.savefig(os.path.join(OUTPUT_DIR, "10_perf_vs_governance.png"))
plt.close()

print("✅ 10 plots gerados com sucesso.")
