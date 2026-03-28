import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESULTS_DIR = os.path.join(BASE_DIR, "results")
OUTPUT_DIR = os.path.join(RESULTS_DIR, "plots")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def safe_read_csv(filename):
    path = os.path.join(RESULTS_DIR, filename)
    if not os.path.exists(path):
        print(f"⚠️ Arquivo não encontrado: {filename}")
        return None

    for sep in [';', ',']:
        try:
            df = pd.read_csv(path, sep=sep)
            if len(df.columns) > 1:
                return df
        except:
            continue

    return None


def generate_plots():
    df = safe_read_csv("responses.csv")

    if df is None or df.empty:
        print("❌ Sem dados.")
        return

    print(f"📊 {len(df)} execuções carregadas")

    # =============================
    # PLOT 1 — IA vs HUMANO (BARRA LIMPA)
    # =============================
    plt.figure(figsize=(10, 6))

    labels = []
    values = []

    if "acc_h" in df.columns:
        labels.append("Humano")
        values.append(df["acc_h"].mean())

    if "acc_ia" in df.columns:
        labels.append("IA")
        values.append(df["acc_ia"].mean())

    if "iga_ia" in df.columns:
        labels.append("IGA (IA)")
        values.append(df["iga_ia"].mean())

    bars = plt.bar(labels, values)

    # rótulos no topo
    for bar in bars:
        y = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, y, f"{y:.2f}",
                 ha='center', va='bottom', fontsize=10)

    plt.title("Comparação de Performance e Governança")
    plt.ylabel("Score Médio")
    plt.ylim(0, 1)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "01_comparacao_geral.png"))
    plt.close()

    print("✅ Plot 1 OK")

    # =============================
    # PLOT 2 — TEMPO vs ACURÁCIA
    # =============================
    if "tempo" in df.columns:

        plt.figure(figsize=(10, 6))

        x = df["tempo"]
        y = df["acc_h"]

        plt.scatter(x, y)

        # linha de tendência
        if len(df) > 1:
            z = np.polyfit(x, y, 1)
            p = np.poly1d(z)
            plt.plot(x, p(x))

        plt.xlabel("Tempo de Resposta (s)")
        plt.ylabel("Acurácia Humana")
        plt.title("Relação entre Tempo e Performance Humana")

        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "02_tempo_vs_acuracia.png"))
        plt.close()

        print("✅ Plot 2 OK")

    # =============================
    # PLOT 3 — DECISÃO DO SISTEMA
    # =============================
    if "acesso" in df.columns:

        plt.figure(figsize=(6, 6))

        counts = df["acesso"].value_counts()

        labels = ["Negado", "Liberado"]
        values = [counts.get(0, 0), counts.get(1, 0)]

        plt.pie(values, labels=labels, autopct='%1.1f%%')

        plt.title("Distribuição de Decisão do Sistema")

        plt.tight_layout()
        plt.savefig(os.path.join(OUTPUT_DIR, "03_decisao_sistema.png"))
        plt.close()

        print("✅ Plot 3 OK")

    print(f"🏁 Tudo salvo em: {OUTPUT_DIR}")


if __name__ == "__main__":
    print("📊 Gerando plots (versão melhorada)...")
    generate_plots()
