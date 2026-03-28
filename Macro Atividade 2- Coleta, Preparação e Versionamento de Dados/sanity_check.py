import os
import random
import matplotlib.pyplot as plt
from PIL import Image

DATASET_PATH = "data/raw/real_vs_fake"

def get_random_images(split="train", n=6):
    images = []
    labels = []

    for label in ["real", "fake"]:
        path = os.path.join(DATASET_PATH, split, label)
        files = os.listdir(path)
        sampled = random.sample(files, n)

        for f in sampled:
            images.append(os.path.join(path, f))
            labels.append(label)

    return images, labels


def plot_images(images, labels):
    plt.figure(figsize=(10, 5))

    for i, (img_path, label) in enumerate(zip(images, labels)):
        img = Image.open(img_path)

        plt.subplot(2, 6, i + 1)
        plt.imshow(img)
        plt.title(label)
        plt.axis("off")

    plt.tight_layout()
    plt.savefig("sanity_check.png")
print("Imagem salva como sanity_check.png")


if __name__ == "__main__":
    imgs, lbls = get_random_images()
    plot_images(imgs, lbls)
