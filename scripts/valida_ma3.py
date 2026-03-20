import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

def carregar_modelo(caminho):
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo do modelo não encontrado em: {caminho}")
    print(f"--- Carregando o 'Cérebro' da MA3: {caminho} ---")
    return tf.keras.models.load_model(caminho)

def realizar_testes(model, pasta_raiz):
    # Subpastas onde você colocará os 4 prints (real) e os 4 downloads (fake)
    subpastas = ['real', 'fake'] 

    for sub in subpastas:
        caminho_completo = os.path.join(pasta_raiz, sub)
        if not os.path.exists(caminho_completo):
            print(f"⚠️ Pasta {caminho_completo} não encontrada. Pulando...")
            continue

        print(f"\n🔍 ANALISANDO CLASSE: {sub.upper()}")
        print("="*60)

        arquivos = [f for f in os.listdir(caminho_completo) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for arq in arquivos:
            caminho_img = os.path.join(caminho_completo, arq)

            # 1. PRÉ-PROCESSAMENTO (Padronização para a ResNet50)
            img = image.load_img(caminho_img, target_size=(224, 224))
            img_array = image.img_to_array(img)

            # 2. TRATAMENTO DE PRINT SCREENS (Remove transparência Alpha se houver)
            if img_array.shape[-1] == 4:
                img_array = img_array[:, :, :3]

            # 3. NORMALIZAÇÃO (Escala de 0 a 1 usada no seu treinamento)
            img_array = img_array / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # 4. INFERÊNCIA
            predicao = model.predict(img_array, verbose=0)
            score = predicao[0][0]

            # DEFINIÇÃO DE LABELS:
            # Threshold de 0.5: Acima de 0.5 = REAL, Abaixo = FAKE
            is_real = score > 0.5
            veredito = "REAL" if is_real else "FAKE"
            confianca = score if is_real else (1 - score)

            # Compara o veredito com o nome da pasta para dar o check de acerto
            status = "✅" if veredito.lower() == sub.lower() else "❌"

            print(f"{status} Arquivo: {arq[:15]:<15} | Veredito: {veredito} ({confianca:.2%})")
            print(f"   [Análise Técnica: Valor bruto de ativação: {score:.4f}]")

# --- CONFIGURAÇÃO DE CAMINHOS (AJUSTADOS PARA SEU WSL) ---
# Caminho exato que você me passou via terminal
CAMINHO_DO_MODELO = 'experiments/ma3/checkpoints/best_model.keras'
# Pasta que contém as subpastas 'real' e 'fake'
CAMINHO_DAS_FOTOS = 'testes_ma3' 

try:
    resnet_ma3 = carregar_modelo(CAMINHO_DO_MODELO)
    realizar_testes(resnet_ma3, CAMINHO_DAS_FOTOS)
    print("\n✅ Teste de Generalização concluído. Pronto para o relatório!")
except Exception as e:
    print(f"\n❌ Erro na execução: {e}")
