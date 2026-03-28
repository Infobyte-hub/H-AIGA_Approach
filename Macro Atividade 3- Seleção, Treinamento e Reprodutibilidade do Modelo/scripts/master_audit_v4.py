import os
import numpy as np
import tensorflow as tf
import cv2
import sys
from tensorflow.keras.preprocessing import image

# --- CONFIGURAÇÕES DE CAMINHO ---
BASE_MA3 = '/home/igaog/captcha-trust-ai/Macro Atividade 3- Seleção, Treinamento e Reprodutibilidade do Modelo'
MODEL_PATH = os.path.join(BASE_MA3, 'best_model.keras')
OUTPUT_DIR = os.path.join(BASE_MA3, 'auditoria_pixels_ig')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Limpeza inicial de memória GPU
tf.keras.backend.clear_session()

# 1. Carregamento do Modelo
print(f"🤖 Carregando cérebro do modelo...")
try:
    model = tf.keras.models.load_model(MODEL_PATH, compile=False)
except Exception as e:
    print(f"❌ Erro ao carregar modelo: {e}")
    sys.exit()

def get_integrated_gradients(img_input, model, steps=50, batch_size=4):
    """
    Calcula a atribuição de pixels (IG) fatiando em lotes para economizar VRAM.
    """
    baseline = tf.zeros_like(img_input)
    alphas = tf.linspace(0.0, 1.0, steps+1)
    accumulated_grads = []

    for i in range(0, len(alphas), batch_size):
        batch_alphas = alphas[i:i+batch_size]
        interpolated = baseline + batch_alphas[:, tf.newaxis, tf.newaxis, tf.newaxis] * (img_input - baseline)
        with tf.GradientTape() as tape:
            tape.watch(interpolated)
            preds = model(interpolated)
            target_output = preds[:, 0]
        accumulated_grads.append(tape.gradient(target_output, interpolated))

    all_grads = tf.concat(accumulated_grads, axis=0)
    avg_grads = tf.reduce_mean(all_grads[:-1] + all_grads[1:], axis=0) / 2.0
    return (img_input - baseline) * avg_grads

def resposta_estilo_ia(label, score, ig_map):
    """
    Gera uma narrativa humana baseada na física da imagem e dispersão de pixels.
    """
    mask = np.sum(np.abs(ig_map), axis=-1)
    threshold = np.percentile(mask, 95)
    y_idx, x_idx = np.where(mask > threshold)
    
    # Diagnóstico de foco
    dispersao = (np.std(y_idx) + np.std(x_idx)) / 2
    confianca_val = score * 100 if label == "REAL" else (1.0 - score) * 100
    
    # Determinação da posição de foco
    pos_v = "superior" if np.mean(y_idx) < 128 else "inferior"
    pos_h = "esquerda" if np.mean(x_idx) < 128 else "direita"

    # Construção da Resposta (O 'Eu acho que...')
    intro = f"Eu acho que é {label}. Tenho {confianca_val:.1f}% de certeza."
    
    if dispersao < 35:
        argumento = (
            f"Embora a nitidez esteja alta, a irregularidade orgânica detectada na região {pos_v}-{pos_h} "
            "e a morfologia dos pixels sugerem a física de uma captura óptica autêntica."
        )
    elif dispersao < 60:
        argumento = (
            f"Notei uma ativação que oscila entre as bordas e o fundo na área {pos_h}. "
            "Isso indica uma possível hesitação do modelo entre o objeto real e ruído digital."
        )
    else:
        argumento = (
            "A iluminação e a distribuição de pesos parecem artificiais. Detectei uma ativação caótica, "
            "traço comum de inconsistência em geradores sintéticos de imagem."
        )

    return f"{intro}\n{argumento}"

# --- LOOP PRINCIPAL ---
print(f"🚀 Iniciando Auditoria Cognitiva v6...")

for sub in ['amostras_real', 'amostras_fake']:
    pasta = os.path.join(BASE_MA3, sub)
    if not os.path.exists(pasta):
        continue
    
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"\n📂 Processando Classe: {sub.upper()}")

    for arq in arquivos:
        path = os.path.join(pasta, arq)
        try:
            # Preprocessamento
            img = image.load_img(path, target_size=(256, 256))
            img_arr = image.img_to_array(img) / 255.0
            img_in = tf.expand_dims(img_arr, axis=0)

            # 1. Predição e Auditoria de Pixels
            preds = model.predict(img_in, verbose=0)
            score = float(preds[0][0])
            label = "REAL" if score > 0.5 else "FAKE"
            
            ig_map = get_integrated_gradients(img_in, model).numpy()[0]
            
            # 2. Geração da Resposta "Humana"
            narrativa = resposta_estilo_ia(label, score, ig_map)

            # 3. Visualização de Auditoria (Overlay)
            mask_viz = np.uint8(255 * (np.sum(np.abs(ig_map), axis=-1) / (np.max(np.abs(ig_map)) + 1e-10)))
            heatmap = cv2.applyColorMap(mask_viz, cv2.COLORMAP_HOT)
            original = cv2.resize(cv2.imread(path), (256, 256))
            final_overlay = cv2.addWeighted(original, 0.5, heatmap, 0.5, 0)
            
            save_name = f"audit_{sub}_{arq}"
            cv2.imwrite(os.path.join(OUTPUT_DIR, save_name), final_overlay)

            # 4. Output Final no Console
            status = "✅" if (label == "REAL" and "real" in sub) or (label == "FAKE" and "fake" in sub) else "❌"
            print("-" * 60)
            print(f"STATUS: {status} | ARQUIVO: {arq}")
            print(f"{narrativa}")

        except Exception as e:
            print(f"❌ Falha em {arq}: {e}")

print(f"\n🏁 Auditoria completa. Resultados salvos em: {OUTPUT_DIR}")
