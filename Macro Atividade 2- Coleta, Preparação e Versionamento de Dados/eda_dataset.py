# scripts/eda_dataset.py
import os
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import random

# Configurações
dataset_path = Path("/mnt/d/datasets/real_vs_fake")  # ajuste conforme seu dataset
output_dir = Path("outputs/eda")
output_dir.mkdir(parents=True, exist_ok=True)

splits = ["train", "valid", "test"]
classes = ["real", "fake"]

def count_images(split_path):
    counts = {}
    for cls in classes:
        cls_path = split_path / cls
        counts[cls] = len(list(cls_path.glob("*.*")))
    return counts

def get_image_sizes(paths):
    sizes = []
    for p in paths:
        with Image.open(p) as img:
            sizes.append(img.size)
    return sizes

def plot_image_sizes_hist(sizes, split_name="all"):
    if not sizes:
        print(f"Nenhuma imagem encontrada para {split_name}. Pulando gráfico.")
        return
    widths, heights = zip(*sizes)
    plt.figure(figsize=(8,5))
    plt.hist(widths, bins=30, alpha=0.5, label="width")
    plt.hist(heights, bins=30, alpha=0.5, label="height")
    plt.title(f"Tamanhos de Imagem ({split_name})")
    plt.xlabel("Pixels")
    plt.ylabel("Quantidade")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / f"image_sizes_hist_{split_name}.png")
    plt.close()
    print(f"Histograma de tamanhos ({split_name}) salvo em '{output_dir / f'image_sizes_hist_{split_name}.png'}'")

def show_sample_images(split_path, n=6):
    for cls in classes:
        cls_path = split_path / cls
        paths = list(cls_path.glob("*.*"))
        sample = random.sample(paths, min(n, len(paths)))
        fig, axes = plt.subplots(1, len(sample), figsize=(12,3))
        for ax, p in zip(axes, sample):
            img = Image.open(p)
            ax.imshow(img)
            ax.set_title(cls)
            ax.axis("off")
        plt.tight_layout()
        plt.savefig(output_dir / f"sample_{cls}_{split_path.name}.png")
        plt.close()
        print(f"Amostras de {cls} ({split_path.name}) salvas em '{output_dir / f'sample_{cls}_{split_path.name}.png'}'")

# === DISTRIBUIÇÃO ===
total_counts = {cls:0 for cls in classes}

for split in splits:
    split_path = dataset_path / split
    counts = count_images(split_path)
    print(f"{split.upper()}:")
    for cls in classes:
        print(f"  {cls}: {counts[cls]}")
        total_counts[cls] += counts[cls]
    print()
    
print("TOTAL:", sum(total_counts.values()), "\n")

# Histograma geral
all_paths = []
for split in splits:
    for cls in classes:
        all_paths.extend((dataset_path / split / cls).glob("*.*"))

sizes = get_image_sizes(all_paths)
plot_image_sizes_hist(sizes, split_name="all")

# Histograma e amostras por split
for split in splits:
    split_paths = []
    split_path = dataset_path / split
    for cls in classes:
        split_paths.extend((split_path / cls).glob("*.*"))
    sizes = get_image_sizes(split_paths)
    plot_image_sizes_hist(sizes, split_name=split)
    show_sample_images(split_path, n=6)
