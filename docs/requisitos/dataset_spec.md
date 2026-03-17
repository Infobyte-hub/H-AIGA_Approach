## 1. Dataset Selecionado

Nome: 140k Real and Fake Faces
Origem: Kaggle (xhlulu)

Tipo:
Dataset de classificação binária para detecção de faces reais vs sintéticas.

Justificativa:
Adequado ao problema de CAPTCHA, permitindo distinguir humanos reais de imagens geradas artificialmente.

## 2. Divisão dos Dados

Treino: 70%
Validação: 15%
Teste: 15%

Critério:
Divisão estratificada por grupos demográficos para evitar viés estatístico.

## 3. Definição de Labels

Label: "Real"
Critério:
- Imagens de rostos humanos autênticos
- Presença de características naturais (textura de pele, assimetria, imperfeições)

Label: "Fake"
Critério:
- Imagens geradas artificialmente (GANs)
- Presença de artefatos visuais (bordas inconsistentes, padrões irreais)

Justificativa:
Os labels refletem diretamente o objetivo do sistema de diferenciar humanos reais de entidades sintéticas.

## Riscos Específicos do Dataset

R04: Overfitting a artefatos de geração
Impacto: Alto
Probabilidade: Alta

R05: Falta de diversidade demográfica explícita
Impacto: Alto
Probabilidade: Média

R06: Dataset desbalanceado entre real e fake
Impacto: Médio
Probabilidade: Média

## 5. Estratégia de Expansão e Contração

Expansão:
- Augmentation em imagens reais e fake separadamente

Contração:
- Balanceamento entre classes

Objetivo:
Evitar viés do modelo em reconhecer padrões específicos de geração artificial.

Métricas:
- Acurácia por classe
- Precision/Recall por classe

## 6. Ética e Uso

- Dataset contém imagens reais e sintéticas, podendo envolver direitos de imagem
- Uso restrito à pesquisa
- Proibição de uso para vigilância ou identificação de indivíduos

Risco ético:
Possível uso indevido para detecção invasiva de identidade
