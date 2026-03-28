import os
import shutil
import random

# CONFIGURAÇÃO DE CAMINHOS (Ajuste conforme seu WSL)
ORIGINAL_DATASET = "/home/igaog/captcha-trust-ai/data/raw/real_vs_fake/"
NEW_DATASET = "/home/igaog/captcha-trust-ai/dataset-subsampled/"
FRACTION = 0.33  # Reduzindo para ~1/3

def subsample():
    # Verifica se a pasta de destino existe, se não, cria
    if not os.path.exists(NEW_DATASET):
        os.makedirs(NEW_DATASET)
        print(f"Diretório {NEW_DATASET} criado.")

    for split in ['train', 'valid', 'test']:
        for category in ['real', 'fake']:
            src_dir = os.path.join(ORIGINAL_DATASET, split, category)
            dst_dir = os.path.join(NEW_DATASET, split, category)
            
            if not os.path.exists(src_dir):
                print(f"⚠️ Aviso: Diretorio {src_dir} não encontrado. Pulando...")
                continue
                
            os.makedirs(dst_dir, exist_ok=True)

            files = os.listdir(src_dir)
            # Filtra apenas arquivos de imagem comuns
            files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            num_to_keep = int(len(files) * FRACTION)
            selected_files = random.sample(files, num_to_keep)

            print(f"📂 Processando {split}/{category}: Copiando {num_to_keep} de {len(files)} imagens...")
            
            for f in selected_files:
                shutil.copy(os.path.join(src_dir, f), os.path.join(dst_dir, f))

if __name__ == "__main__":
    print("🚀 Iniciando redução estratégica do dataset...")
    subsample()
    print("\n✅ Redução concluída! Use o novo caminho para o treino da MA3.")
