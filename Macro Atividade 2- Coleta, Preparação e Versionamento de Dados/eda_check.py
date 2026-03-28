import os
from collections import Counter
from PIL import Image

DATASET_PATH = "data/raw/real_vs_fake"

def count_images(base_path):
    counts = {}
    total = 0

    for split in ["train", "valid", "test"]:
        split_path = os.path.join(base_path, split)
        if not os.path.exists(split_path):
            continue

        counts[split] = {}
        for label in ["real", "fake"]:
            label_path = os.path.join(split_path, label)
            n = len(os.listdir(label_path))
            counts[split][label] = n
            total += n

    return counts, total


def check_image_sizes(base_path, sample_size=100):
    sizes = Counter()
    checked = 0

    for root, _, files in os.walk(base_path):
        for f in files:
            if f.endswith(".png") or f.endswith(".jpg"):
                path = os.path.join(root, f)
                try:
                    with Image.open(path) as img:
                        sizes[img.size] += 1
                        checked += 1
                        if checked >= sample_size:
                            return sizes
                except:
                    continue
    return sizes


if __name__ == "__main__":
    counts, total = count_images(DATASET_PATH)

    print("\n=== DISTRIBUIÇÃO ===")
    for split, data in counts.items():
        print(f"\n{split.upper()}:")
        for label, n in data.items():
            print(f"  {label}: {n}")
    
    print(f"\nTOTAL: {total}")

    print("\n=== TAMANHO DAS IMAGENS (amostra) ===")
    sizes = check_image_sizes(DATASET_PATH)
    for size, n in sizes.items():
        print(f"{size}: {n}")
