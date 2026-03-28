import os
import time
import uuid
import random
import shutil
import cv2
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
# XAI SIMPLES (TEXTO)
# =============================
class XAI:
    def explain(self, label, prob):
        conf = prob if label == "REAL" else (1 - prob)

        if conf > 0.85:
            return f"Alta confiança ({conf:.2f}) — padrões faciais consistentes."
        elif conf > 0.65:
            return f"Confiança moderada ({conf:.2f}) — possíveis artefatos sutis."
        else:
            return f"Baixa confiança ({conf:.2f}) — ruído ou inconsistência visual."

xai = XAI()

# =============================
# LOAD IMAGES (FIX GRADIO)
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

    acertos = 0
    acertos_reais = 0
    total = len(paths)

    rows = []

    for i, path in enumerate(paths):
        img = Image.open(path).resize((IMG_SIZE, IMG_SIZE))
        arr = np.array(img) / 255.0
        arr = np.expand_dims(arr, 0)

        prob = float(model.predict(arr, verbose=0)[0][0])
        pred = 1 if prob > 0.5 else 0

        human = 1 if i in selected else 0
        gt = labels[i]

        correct = (human == gt)

        if correct:
            acertos += 1
        if gt == 1 and correct:
            acertos_reais += 1

        label_txt = "REAL" if pred == 1 else "FAKE"
        expl = xai.explain(label_txt, prob)

        rows.append({
            "img": i,
            "gt": gt,
            "human": human,
            "ia": pred,
            "prob": prob,
            "correct": int(correct),
            "explanation": expl
        })

    # =============================
    # DECISÃO DE ACESSO
    # =============================
    acesso = (acertos_reais >= 2 and acertos >= 4)

    # =============================
    # MÉTRICAS
    # =============================
    acc_h = acertos / total
    acc_ia = np.mean([r["ia"] == r["gt"] for r in rows])

    risk = (1 - acc_ia) ** 2
    fairness = abs(sum([r["gt"] for r in rows]) - sum([r["ia"] for r in rows])) / total
    trust = acc_ia

    Q, P, IGA = gov_engine.compute(acc_ia, risk, fairness, trust)

    tempo = time.time() - start_time

    # =============================
    # LOG CSV
    # =============================
    df = pd.DataFrame([{
        "user_id": user_id,
        "acc_h": acc_h,
        "acc_ia": acc_ia,
        "risk": risk,
        "fairness": fairness,
        "trust": trust,
        "IGA": IGA,
        "acesso": int(acesso),
        "tempo": tempo
    }])

    df.to_csv(RESPONSES_FILE, mode="a", index=False, header=not os.path.exists(RESPONSES_FILE))

    # =============================
    # TABELA PROFISSIONAL
    # =============================
    tabela = """
    <style>
    .table-audit { width:100%; border-collapse:collapse; font-size:14px;}
    .table-audit th, .table-audit td {border:1px solid #444; padding:8px; text-align:center;}
    .table-audit th {background:#111; color:#fff;}
    .ok {color:#00c853; font-weight:bold;}
    .erro {color:#ff1744; font-weight:bold;}
    .real {color:#00e676; font-weight:bold;}
    .fake {color:#ff5252; font-weight:bold;}
    </style>

    <table class="table-audit">
    <tr>
    <th>Foto</th>
    <th>Classe Real</th>
    <th>Seu Status</th>
    <th>Status IA</th>
    <th>Confiança</th>
    <th>Justificativa</th>
    </tr>
    """

    for r in rows:
        classe = "REAL" if r["gt"] == 1 else "FAKE"
        classe_class = "real" if r["gt"] == 1 else "fake"

        humano_ok = "OK" if r["human"] == r["gt"] else "ERRO"
        humano_class = "ok" if humano_ok == "OK" else "erro"

        ia_ok = "OK" if r["ia"] == r["gt"] else "ERRO"
        ia_class = "ok" if ia_ok == "OK" else "erro"

        tabela += f"""
        <tr>
            <td>{r['img']+1}</td>
            <td class="{classe_class}">{"✅" if classe=='REAL' else "🚫"} {classe}</td>
            <td class="{humano_class}">{"✅" if humano_ok=='OK' else "❌"} {humano_ok}</td>
            <td class="{ia_class}">{"✅" if ia_ok=='OK' else "❌"} {ia_ok}</td>
            <td>{r['prob']:.2f}</td>
            <td>{r['explanation']}</td>
        </tr>
        """

    tabela += "</table>"

    status = "🔓 ACESSO LIBERADO" if acesso else "🔒 ACESSO NEGADO"

    resumo = f"""
    ## {status}

    Acc Humano: {acc_h:.2f}  
    Acc IA: {acc_ia:.2f}  
    Risk: {risk:.2f}  
    Fairness: {fairness:.2f}  
    Trust: {trust:.2f}  
    IGA: {IGA:.2f}  
    Tempo: {tempo:.2f}s
    """

    return resumo, tabela, df.to_html(index=False)

# =============================
# DASHBOARD
# =============================
def dashboard():
    if not os.path.exists(RESPONSES_FILE):
        return "Sem dados ainda"

    df = pd.read_csv(RESPONSES_FILE)
    return df.describe().to_html()

# =============================
# UI
# =============================
with gr.Blocks(title="AI Governance CAPTCHA") as demo:

    user_id = gr.State(new_user())
    start_time = gr.State(time.time())

    gr.Markdown("# 🏦 Sistema de Validação com Governança IA")

    gallery = gr.Gallery(columns=3, height=400)
    labels = gr.State()
    paths = gr.State()
    selected = gr.State([])

    output = gr.Markdown()
    table = gr.HTML()
    metrics = gr.HTML()
    dash = gr.HTML()

    btn_submit = gr.Button("Validar")
    btn_new = gr.Button("Nova Rodada")
    btn_dash = gr.Button("Atualizar Dashboard")

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

    btn_submit.click(process,
        inputs=[selected, paths, labels, user_id, start_time],
        outputs=[output, table, metrics]
    )

    btn_new.click(new_round,
        outputs=[gallery, labels, paths, selected, user_id, start_time]
    )

    btn_dash.click(dashboard, outputs=dash)

demo.launch(share=True, allowed_paths=[DATASET_PATH])
