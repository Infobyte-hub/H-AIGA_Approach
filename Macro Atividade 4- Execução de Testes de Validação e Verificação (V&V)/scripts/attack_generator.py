import tensorflow as tf
import numpy as np
import cv2
import os
import pandas as pd

class MA4_StressTester_Massive:
    def __init__(self, model_path, output_dir):
        self.model = tf.keras.models.load_model(model_path, compile=False)
        self.output_csv = os.path.join(output_dir, "stress_test_results.csv")
        self.results = []
        print(f"[*] Modelo carregado: {model_path}")

    def preprocess(self, image_path):
        # ResNet50 padrão usa 224x224, mas se seu treino foi 256x256, mude aqui
        img = tf.keras.utils.load_img(image_path, target_size=(256, 256))
        return tf.keras.utils.img_to_array(img) / 255.0

    def apply_compression(self, image, quality=5):
        img_255 = (image * 255).astype(np.uint8)
        _, encimg = cv2.imencode('.jpg', img_255, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
        return cv2.imdecode(encimg, 1).astype(np.float32) / 255.0

    def fgsm_attack(self, image_tensor, label, epsilon=0.03):
        image_tensor = tf.cast(image_tensor, tf.float32)
        with tf.GradientTape() as tape:
            tape.watch(image_tensor)
            prediction = self.model(image_tensor)
            loss = tf.keras.losses.BinaryCrossentropy()(tf.constant([[label]], dtype=tf.float32), prediction)
        gradient = tape.gradient(loss, image_tensor)
        return tf.clip_by_value(image_tensor + epsilon * tf.sign(gradient), 0, 1)

    def run_mass_attack(self, base_path, class_name, true_label):
        if not os.path.exists(base_path):
            print(f"[-] Erro: Pasta {base_path} não encontrada.")
            return

        print(f"\n🚀 Atacando Classe: {class_name.upper()}")
        arquivos = [f for f in os.listdir(base_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for arq in arquivos:
            path = os.path.join(base_path, arq)
            try:
                img_arr = self.preprocess(path)
                img_tensor = np.expand_dims(img_arr, axis=0)

                # 1. Original
                orig_pred = float(self.model.predict(img_tensor, verbose=0)[0][0])
                
                # 2. Adversário (Matemático)
                adv_tensor = self.fgsm_attack(img_tensor, true_label)
                adv_pred = float(self.model.predict(adv_tensor, verbose=0)[0][0])
                
                # 3. Híbrido (Adversário + Compressão Física)
                hybrid_img = self.apply_compression(adv_tensor.numpy()[0], quality=15)
                hybrid_pred = float(self.model.predict(np.expand_dims(hybrid_img, axis=0), verbose=0)[0][0])

                self.results.append({
                    "arquivo": arq,
                    "classe": class_name,
                    "original": orig_pred,
                    "adversarial": adv_pred,
                    "hybrid": hybrid_pred,
                    "vulneravel": abs(orig_pred - adv_pred) > 0.4
                })
                status = "💀" if abs(orig_pred - adv_pred) > 0.4 else "🛡️"
                print(f"{status} {arq[:15]:<15} | Orig: {orig_pred:.2f} | Adv: {adv_pred:.2f}")
            except Exception as e:
                print(f"❌ Erro em {arq}: {e}")

    def save(self):
        df = pd.DataFrame(self.results)
        df.to_csv(self.output_csv, index=False)
        print(f"\n✅ Relatório de Stress-Test salvo em: {self.output_csv}")

if __name__ == "__main__":
    # CAMINHOS CORRIGIDOS (RAIZ DA MA3)
    BASE_MA3 = "/home/igaog/captcha-trust-ai/Macro Atividade 3- Seleção, Treinamento e Reprodutibilidade do Modelo"
    BASE_MA4 = "/home/igaog/captcha-trust-ai/Macro Atividade 4- Execução de Testes de Validação e Verificação (V&V)"
    
    MODEL = os.path.join(BASE_MA3, "best_model.keras")
    OUT_DIR = os.path.join(BASE_MA4, "results")
    os.makedirs(OUT_DIR, exist_ok=True)

    tester = MA4_StressTester_Massive(MODEL, OUT_DIR)
    
    # Ataca as amostras da MA3 (Ajuste os nomes das pastas se forem diferentes)
    tester.run_mass_attack(os.path.join(BASE_MA3, "amostras_real"), "real", 1)
    tester.run_mass_attack(os.path.join(BASE_MA3, "amostras_fake"), "fake", 0)
    
    tester.save()
