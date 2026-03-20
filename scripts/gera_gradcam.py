import tensorflow as tf
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image

# 1. Configurações de Caminho
MODEL_PATH = 'experiments/ma3/checkpoints/best_model.keras'
IMG_DIR = 'testes_ma3'
OUTPUT_DIR = 'testes_ma3/resultados_gradcam'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. Carregar Modelo
model = tf.keras.models.load_model(MODEL_PATH)

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_and_display_gradcam(img_path, heatmap, cam_path, alpha=0.4):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (224, 224))
    
    heatmap = cv2.resize(heatmap, (224, 224))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    superimposed_img = heatmap * alpha + img
    cv2.imwrite(cam_path, superimposed_img)

# Nome da última camada convolucional da ResNet50
# Se você usou a ResNet50 padrão do Keras, o nome é geralmente 'conv5_block3_out'
LAST_CONV_LAYER = 'conv5_block3_out'

print("--- Iniciando Geração de Grad-CAM ---")

for sub in ['real', 'fake']:
    pasta = os.path.join(IMG_DIR, sub)
    arquivos = [f for f in os.listdir(pasta) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    for arq in arquivos:
        path = os.path.join(pasta, arq)
        img = image.load_img(path, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        # Trata canal alpha de prints
        if img_array.shape[-1] == 4:
            img_array = img_array[:, :, :, :3]

        heatmap = make_gradcam_heatmap(img_array, model, LAST_CONV_LAYER)
        
        save_name = f"gradcam_{sub}_{arq}"
        save_path = os.path.join(OUTPUT_DIR, save_name)
        save_and_display_gradcam(path, heatmap, save_path)
        print(f"Salvo: {save_name}")

print(f"\n✅ Todos os mapas gerados em: {OUTPUT_DIR}")
