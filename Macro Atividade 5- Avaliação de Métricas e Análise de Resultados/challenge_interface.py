import os
import time
import uuid
import random
import shutil
import numpy as np
import tensorflow as tf
import gradio as gr
import pandas as pd
from PIL import Image
from engines import GovernanceEngine

# =============================
# CONFIG
# =============================
BASE_DIR = os.getcwd()
TMP_DIR = "/tmp/gradio_images"
os.makedirs(TMP_DIR, exist_ok=True)

DATASET_PATH = "/home/igaog/captcha-trust-ai/dataset-subsampled/test"
MODEL_PATH = "/home/igaog/captcha-trust-ai/Macro Atividade 3- Seleção, Treinamento e Reprodutibilidade do Modelo/best_model.keras"

RESULTS_DIR = os.path.join(BASE_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

RESPONSES_FILE = os.path.join(RESULTS_DIR, "responses.csv")

IMG_SIZE = 256

# =============================
# MODEL + GOVERNANCE
# =============================
model = tf.keras.models.load_model(MODEL_PATH, compile=False)

gov_engine = GovernanceEngine(
    wp=0.4, wr=0.2, wf=0.2, wt=0.2,
    alpha=0.4, beta=0.3, gamma=0.3
)

# =============================
# USER ID
# =============================
def new_user():
    return f"user_{uuid.uuid4().hex[:8]}"

# =============================
# XAI
# =============================
class XAI:
    def explain(self, label, prob):
        conf = prob if label == "REAL" else (1 - prob)

        if conf > 0.85:
            regiao = "região facial"
            padrao = "alta consistência estrutural"
        elif conf > 0.65:
            regiao = "bordas e fundo"
            padrao = "possíveis artefatos sutis"
        else:
            regiao = "múltiplas regiões"
            padrao = "inconsistência visual global"

        return f"Modelo identifica com {conf:.2f} de confiança padrões em {regiao}, indicando {padrao}, classificando como {label}."

xai = XAI()

# =============================
# LOAD IMAGES
# =============================
def load_images():
    real = [os.path.join(DATASET_PATH, "real", f) for f in os.listdir(os.path.join(DATASET_PATH, "real"))]
    fake = [os.path.join(DATASET_PATH, "fake", f) for f in os.listdir(os.path.join(DATASET_PATH, "fake"))]

    paths = random.sample(real, 3) + random.sample(fake, 3)
    random.shuffle(paths)

    tmp_paths = []
    for p in paths:
        new_path = os.path.join(TMP_DIR, f"{uuid.uuid4().hex}.png")
        shutil.copy(p, new_path)
        tmp_paths.append(new_path)

    labels = [1 if "real" in p else 0 for p in paths]

    return tmp_paths, labels

# =============================
# PROCESS
# =============================
def process(selected, paths, labels, user_id, start_time):

    if not selected:
        return "⚠️ Selecione pelo menos 1 imagem", "", ""

    rows = []

    y_true = []
    y_pred_ia = []
    y_pred_h = []

    for i, path in enumerate(paths):
        img = Image.open(path).resize((IMG_SIZE, IMG_SIZE))
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, 0)

        prob = float(model.predict(arr, verbose=0)[0][0])
        pred_ia = 1 if prob > 0.5 else 0
        pred_h = 1 if i in selected else 0
        gt = labels[i]

        y_true.append(gt)
        y_pred_ia.append(pred_ia)
        y_pred_h.append(pred_h)

        label_txt = "REAL" if pred_ia == 1 else "FAKE"
        expl = xai.explain(label_txt, prob)

        rows.append({
            "img": i,
            "gt": gt,
            "human": pred_h,
            "ia": pred_ia,
            "prob": prob,
            "explanation": expl
        })

    # =============================
    # IA METRICS
    # =============================
    acc_ia = np.mean(np.array(y_true) == np.array(y_pred_ia))
    risk_ia = (1 - acc_ia) ** 2
    fairness_ia = abs(sum(y_true) - sum(y_pred_ia)) / len(y_true)
    trust_ia = acc_ia

    Q_ia, P_ia, Pcomp_ia, IGA_ia, comp_ia = gov_engine.compute(
        acc_ia, risk_ia, fairness_ia, trust_ia
    )

    # =============================
    # HUMAN METRICS
    # =============================
    acc_h = np.mean(np.array(y_true) == np.array(y_pred_h))
    risk_h = (1 - acc_h) ** 2
    fairness_h = abs(sum(y_true) - sum(y_pred_h)) / len(y_true)
    trust_h = acc_h

    Q_h, P_h, Pcomp_h, IGA_h, comp_h = gov_engine.compute(
        acc_h, risk_h, fairness_h, trust_h
    )

    # =============================
    # ACCESS RULE
    # =============================
    acesso = acc_h >= 0.66
    tempo = time.time() - start_time

    # =============================
    # CSV LOG (COMPLETO)
    # =============================
    df = pd.DataFrame([{
        "user_id": user_id,

        "acc_h": acc_h,
        "risk_h": risk_h,
        "fairness_h": fairness_h,
        "trust_h": trust_h,
        "Q_h": Q_h,
        "P_h": P_h,
        "Pcomp_h": Pcomp_h,
        "IGA_h": IGA_h,

        "acc_ia": acc_ia,
        "risk_ia": risk_ia,
        "fairness_ia": fairness_ia,
        "trust_ia": trust_ia,
        "Q_ia": Q_ia,
        "P_ia": P_ia,
        "Pcomp_ia": Pcomp_ia,
        "IGA_ia": IGA_ia,

        "acesso": int(acesso),
        "tempo": tempo
    }])

    df.to_csv(RESPONSES_FILE, mode="a", index=False, header=not os.path.exists(RESPONSES_FILE))

    # =============================
    # TABELA VISUAL
    # =============================
    tabela = """
    <table style="width:100%; border-collapse:collapse;">
    <tr>
    <th>Foto</th>
    <th>Classe</th>
    <th>Humano</th>
    <th>IA</th>
    <th>Conf</th>
    <th>Explicação</th>
    </tr>
    """

    for r in rows:
        classe_icon = "🟢 REAL" if r["gt"] == 1 else "🔴 FAKE"

        humano_icon = "✅" if r["human"] == r["gt"] else "❌"
        ia_icon = "🤖✅" if r["ia"] == r["gt"] else "🤖❌"

        tabela += f"""
        <tr>
            <td>{r['img']+1}</td>
            <td>{classe_icon}</td>
            <td>{humano_icon}</td>
            <td>{ia_icon}</td>
            <td>{r['prob']:.2f}</td>
            <td>{r['explanation']}</td>
        </tr>
        """

    tabela += "</table>"

    # =============================
    # RESUMO EXECUTIVO
    # =============================
    resumo = f"""
    ### RESULTADO

    🔐 Acesso: {"LIBERADO" if acesso else "NEGADO"}

    👤 HUMANO  
    Acc={acc_h:.2f} | IGA={IGA_h:.2f} | P={P_h:.2f} | Pcomp={Pcomp_h:.2f}

    🤖 IA  
    Acc={acc_ia:.2f} | IGA={IGA_ia:.2f} | P={P_ia:.2f} | Pcomp={Pcomp_ia:.2f}

    ⏱ Tempo: {tempo:.2f}s
    """

    return resumo, tabela, df.to_html(index=False)

# =============================
# UI
# =============================
with gr.Blocks() as demo:

    user_id = gr.State(new_user())
    start_time = gr.State(time.time())

    gallery = gr.Gallery(columns=3)
    labels = gr.State()
    paths = gr.State()
    selected = gr.State([])

    output = gr.Markdown()
    table = gr.HTML()
    metrics = gr.HTML()

    def new_round():
        uid = new_user()
        imgs, labs = load_images()
        return imgs, labs, imgs, [], uid, time.time()

    def select(evt: gr.SelectData, sel):
        if evt.index in sel:
            sel.remove(evt.index)
        else:
            sel.append(evt.index)
        return sel

    demo.load(new_round, outputs=[gallery, labels, paths, selected, user_id, start_time])
    gallery.select(select, inputs=selected, outputs=selected)

    gr.Button("Validar").click(
        process,
        inputs=[selected, paths, labels, user_id, start_time],
        outputs=[output, table, metrics]
    )

    gr.Button("Nova Rodada").click(
        new_round,
        outputs=[gallery, labels, paths, selected, user_id, start_time]
    )

demo.launch(share=True, allowed_paths=[DATASET_PATH])
