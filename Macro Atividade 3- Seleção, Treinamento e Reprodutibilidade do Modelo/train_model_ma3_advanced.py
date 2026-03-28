#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Framework de Validação Normativa para IA (MA3 + MA4) - VERSÃO FINAL DEADLINE
Hardware: NVIDIA GTX 1650 4GB | Dataset: Subsampled (1/3)
"""

import os
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model, clone_model
from tensorflow.keras.optimizers import AdamW
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.metrics import confusion_matrix, matthews_corrcoef, classification_report

# ==========================
# 0. DETERMINISMO E HARDWARE
# ==========================
SEED = 42
os.environ['TF_DETERMINISTIC_OPS'] = '1'
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)

gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        tf.config.set_logical_device_configuration(
            gpus[0], [tf.config.LogicalDeviceConfiguration(memory_limit=3200)] 
        )
        print("✅ GPU GTX 1650 configurada (Limite 3.2GB).")
    except RuntimeError as e:
        print(f"❌ Erro GPU: {e}")

# ==========================
# 1. CONFIGURAÇÕES DE CAMINHO
# ==========================
BATCH_SIZE = 16 
IMG_SIZE = (256, 256) 
EPOCHS = 20

# --- AJUSTE ESTES CAMINHOS ABAIXO ---
BASE_DIR = "/home/igaog/captcha-trust-ai/dataset-subsampled/" 
TRAIN_DIR = os.path.join(BASE_DIR, "train")
VAL_DIR   = os.path.join(BASE_DIR, "valid") 
TEST_DIR  = os.path.join(BASE_DIR, "test")

METRICS_DIR = "experiments/ma3/metrics"
CHECKPOINT_DIR = "experiments/ma3/checkpoints"

os.makedirs(CHECKPOINT_DIR, exist_ok=True)
os.makedirs(METRICS_DIR, exist_ok=True)

# ==========================
# 2. ENGINES (MUTATION & GOVERNANCE)
# ==========================
class MutationEngine:
    def __init__(self, model):
        self.original_model = model

    def weight_shuffling(self, layer_index):
        mutant = clone_model(self.original_model)
        mutant.set_weights(self.original_model.get_weights())
        weights = mutant.layers[layer_index].get_weights()
        if weights:
            w_shape = weights[0].shape
            flat_w = weights[0].flatten()
            np.random.shuffle(flat_w)
            weights[0] = flat_w.reshape(w_shape)
            mutant.layers[layer_index].set_weights(weights)
        return mutant

class GovernanceEngine:
    def __init__(self, weights):
        self.w = weights

    def evaluate_governance(self, y_true, y_pred, trust_score=1.0):
        cm = confusion_matrix(y_true, y_pred)
        tn, fp, fn, tp = cm.ravel()
        perf = matthews_corrcoef(y_true, y_pred)
        risk = (2 * fn + fp) / (2 * (fn + tp) + (fp + tn))
        fairness = abs((fn/(fn+tp)) - (fp/(fp+tn)))

        Q_total = (self.w['wp']*perf) - (self.w['wr']*risk) - (self.w['wf']*fairness) - (self.w['wt']*(1-trust_score))
        P = (0.4 * fairness) + (0.6 * risk)
        IGA_final = Q_total - P

        return {
            "IGA_final": IGA_final, "Q_total": Q_total, "Penalty_P": P,
            "Performance_MCC": perf, "Risk_Score": risk, "Fairness_Gap": fairness,
            "Trust_Score": trust_score, "CM": cm
        }

# ==========================
# 3. PIPELINE DE DADOS
# ==========================
train_datagen = ImageDataGenerator(
    rescale=1./255, 
    rotation_range=10, 
    brightness_range=[0.8, 1.2], # Combate viés de iluminação
    horizontal_flip=True
)
val_test_datagen = ImageDataGenerator(rescale=1./255)

train_gen = train_datagen.flow_from_directory(
    TRAIN_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="binary")

val_gen = val_test_datagen.flow_from_directory(
    VAL_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="binary")

test_gen = val_test_datagen.flow_from_directory(
    TEST_DIR, target_size=IMG_SIZE, batch_size=BATCH_SIZE, class_mode="binary", shuffle=False)

# ==========================
# 4. ARQUITETURA E TREINAMENTO (MA3)
# ==========================
base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(256, 256, 3))
base_model.trainable = False

x = GlobalAveragePooling2D()(base_model.output)
x = BatchNormalization()(x)
x = Dense(512, activation="relu")(x)
x = Dropout(0.5)(x) # Evita Overconfidence
output = Dense(1, activation="sigmoid")(x)

model = Model(inputs=base_model.input, outputs=output)

model.compile(optimizer=AdamW(learning_rate=1e-3), loss="binary_crossentropy", metrics=["accuracy"])

callbacks = [
    EarlyStopping(monitor="val_loss", patience=3, restore_best_weights=True, verbose=1),
    ModelCheckpoint(os.path.join(CHECKPOINT_DIR, "best_model.keras"), save_best_only=True, verbose=1),
    ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=2, verbose=1)
]

print("\n🚀 Fase 1: Aquecimento das camadas densas...")
model.fit(train_gen, validation_data=val_gen, epochs=2, callbacks=callbacks)

# Fase 2: Fine-Tuning
base_model.trainable = True
for layer in base_model.layers[:143]: # Congela até os blocos finais
    layer.trainable = False

model.compile(optimizer=AdamW(learning_rate=1e-5), loss="binary_crossentropy", metrics=["accuracy"])

print("\n🚀 Fase 2: Fine-Tuning Estratégico...")
model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS, callbacks=callbacks)

# ==========================
# 5. EXECUÇÃO V&V E GOVERNANÇA (MA4)
# ==========================
print("\n--- Iniciando Macro Atividade 4: V&V ---")
y_prob = model.predict(test_gen)
y_pred = (y_prob > 0.5).astype(int)
y_true = test_gen.classes

# Teste de Mutação
mutator = MutationEngine(model)
mutant_ws = mutator.weight_shuffling(-2)
_, acc_orig = model.evaluate(test_gen, verbose=0)
_, acc_mut = mutant_ws.evaluate(test_gen, verbose=0)
mutation_score = 1.0 if abs(acc_orig - acc_mut) > 0.1 else 0.5

# Consolidação Governança
gov_weights = {'wp': 0.4, 'wr': 0.2, 'wf': 0.2, 'wt': 0.2}
engine = GovernanceEngine(gov_weights)
report = engine.evaluate_governance(y_true, y_pred, trust_score=mutation_score)

print(f"\n✅ IGA FINAL: {report['IGA_final']:.4f}")
print(classification_report(y_true, y_pred))

pd.DataFrame([report]).to_csv(os.path.join(METRICS_DIR, "final_governance_metrics.csv"), index=False)
print(f"🏁 Concluído. Resultados em {METRICS_DIR}")
