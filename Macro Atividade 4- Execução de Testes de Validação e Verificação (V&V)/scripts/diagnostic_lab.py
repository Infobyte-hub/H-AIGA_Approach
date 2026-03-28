import os
import numpy as np
import tensorflow as tf
import cv2
import pandas as pd
import matplotlib.pyplot as plt

class MA4_Perito_Digital:
    def __init__(self, model_path, output_dir):
        self.model = tf.keras.models.load_model(model_path, compile=False)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        print(f"[*] Perito pronto. Analisando em: {output_dir}")

    def get_integrated_gradients(self, img_input, target_label, steps=50):
        """Calcula a atribuição de pixels para o diagnóstico."""
        baseline = tf.zeros_like(img_input)
        alphas = tf.linspace(0.0, 1.0, steps+1)
        grads = []

        for alpha in alphas:
            interpolated = baseline + alpha * (img_input - baseline)
            with tf.GradientTape() as tape:
                tape.watch(interpolated)
                pred = self.model(interpolated)
                loss = pred[:, 0] if target_label == 1 else (1.0 - pred[:, 0])
            grads.append(tape.gradient(loss, interpolated))

        avg_grads = tf.reduce_mean(grads, axis=0)
        return (img_input - baseline) * avg_grads

    def gerar_laudo_texto(self, label, score, ig_map):
        """A 'Voz da IA' adaptada para diagnóstico de ataque."""
        mask = np.sum(np.abs(ig_map), axis=-1)
        threshold = np.percentile(mask, 97)
        y_idx, x_idx = np.where(mask > threshold)
        dispersao = (np.std(y_idx) + np.std(x_idx)) / 2
        
        conf = score * 100 if label == "REAL" else (1.0 - score) * 100
        
        if dispersao < 40:
            msg = f"A IA manteve foco cirúrgico (Conf: {conf:.1f}%). O ataque não desestabilizou a extração de bordas."
        else:
            msg = f"A IA entrou em colapso cognitivo (Conf: {conf:.1f}%). O ataque espalhou a atenção para o ruído de fundo."
        
        return msg

    def run_diagnosis(self, csv_path, base_img_path):
        if not os.path.exists(csv_path):
            print("[-] Erro: CSV de resultados não encontrado. Rode o attack_generator primeiro.")
            return

        df = pd.DataFrame(pd.read_csv(csv_path))
        # Focamos nos casos onde o modelo foi 'Vulnerável' ou 'Híbrido' deu errado
        targets = df[df['vulneravel'] == True].head(10) # Analisar os 10 piores

        print(f"\n🕵️ Iniciando Perícia em {len(targets)} casos críticos...")

        for _, row in targets.iterrows():
            img_name = row['arquivo']
            classe_original = row['classe']
            
            # Tentar achar a imagem na pasta real ou fake
            path = os.path.join(base_img_path, f"amostras_{classe_original}", img_name)
            if not os.path.exists(path): continue

            # Preproc
            img = tf.keras.utils.load_img(path, target_size=(256, 256))
            img_arr = tf.keras.utils.img_to_array(img) / 255.0
            img_tensor = np.expand_dims(img_arr, axis=0)

            # IG para o estado Original
            ig_map = self.get_integrated_gradients(img_tensor, 1 if classe_original == 'real' else 0).numpy()[0]
            laudo = self.gerar_laudo_texto("REAL" if classe_original == 'real' else "FAKE", row['original'], ig_map)

            # Plot de Diagnóstico
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
            ax1.imshow(img_arr)
            ax1.set_title(f"Original: {img_name}\nPred: {row['original']:.4f}")
            
            # Heatmap de IG
            mask_viz = np.sum(np.abs(ig_map), axis=-1)
            ax2.imshow(img_arr, alpha=0.6)
            ax2.imshow(mask_viz, cmap='hot', alpha=0.5)
            ax2.set_title(f"Mapa de Calor (IG)\n{laudo}")

            plt.tight_layout()
            save_path = os.path.join(self.output_dir, f"pericia_{img_name}.png")
            plt.savefig(save_path)
            plt.close()
            print(f"[+] Laudo gerado para {img_name}")

if __name__ == "__main__":
    BASE_MA3 = "/home/igaog/captcha-trust-ai/Macro Atividade 3- Seleção, Treinamento e Reprodutibilidade do Modelo"
    BASE_MA4 = "/home/igaog/captcha-trust-ai/Macro Atividade 4- Execução de Testes de Validação e Verificação (V&V)"
    
    MODEL = os.path.join(BASE_MA3, "best_model.keras")
    CSV = os.path.join(BASE_MA4, "results/stress_test_results.csv")
    OUT = os.path.join(BASE_MA4, "results/pericia_visual")

    perito = MA4_Perito_Digital(MODEL, OUT)
    perito.run_diagnosis(CSV, BASE_MA3)
