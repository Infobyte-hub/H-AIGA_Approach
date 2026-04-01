import pandas as pd
import os

# =============================
# LOAD
# =============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")

df = pd.read_csv(os.path.join(RESULTS_DIR, "responses.csv"))

# =============================
# MÉTRICAS BASE
# =============================
acc_ia = df["acc_ia"].mean()
acc_h = df["acc_h"].mean()

IGA_ia = df["IGA_ia"].mean()
IGA_h = df["IGA_h"].mean()

gap = IGA_h - IGA_ia

P_ia = df["P_ia"].mean()

risk = df["risk_ia"].mean()
fairness = df["fairness_ia"].mean()

# =============================
# OVERCONFIDENCE
# =============================
df["overconfidence"] = df["trust_ia"] * (1 - df["acc_ia"])
overconfidence = df["overconfidence"].mean()

# versão em taxa (%)
overconfidence_rate = ((df["acc_ia"] < 1.0) & (df["trust_ia"] > 0.8)).mean()

# =============================
# TEMPO
# =============================
corr_tempo = df["tempo"].corr(df["acc_h"])

# =============================
# DECISÃO
# =============================
taxa_liberado = (df["acesso"] == 1).mean()
taxa_negado = (df["acesso"] == 0).mean()

# =============================
# PRINT FINAL
# =============================
print("\n===== RESULTADOS CONSOLIDADOS =====\n")

print(f"Acurácia IA: {acc_ia:.3f}")
print(f"Acurácia Humano: {acc_h:.3f}")

print(f"IGA IA: {IGA_ia:.3f}")
print(f"IGA Humano: {IGA_h:.3f}")

print(f"GAP (Humano - IA): {gap:.3f}")

print(f"Penalização média (P): {P_ia:.3f}")

print(f"Risk médio: {risk:.3f}")
print(f"Fairness médio: {fairness:.3f}")

print(f"Overconfidence (score): {overconfidence:.3f}")
print(f"Overconfidence (taxa): {overconfidence_rate:.2%}")

print(f"Correlação Tempo vs Acc Humano: {corr_tempo:.3f}")

print(f"Acesso Liberado: {taxa_liberado:.2%}")
print(f"Acesso Negado: {taxa_negado:.2%}")

print("\n==================================\n")
