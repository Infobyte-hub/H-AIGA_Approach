# MA3 – Relatório de Treino, Validação e Generalização (Versão Final)

**Data:** 25 de Março de 2026  
**Status:** Concluído / Auditoria de XAI Finalizada  
**Responsável:** igaog  
**Objetivo:** Validar a generalização da ResNet50 e diagnosticar falhas de percepção em imagens sintéticas de alta fidelidade.

---

### 1. Resumo Executivo
Este documento detalha o Fine-Tuning e os testes de estresse da ResNet50. Identificou-se que, embora o modelo possua 100% de acurácia em amostras orgânicas, ele apresenta uma **vulnerabilidade crítica de mimetismo** em imagens sintéticas de alta fidelidade. Para mitigar o *overfitting* e garantir a entrega técnica em 06/04, consolidou-se um pipeline de auditoria via **Integrated Gradients (IG)**.

---

### 2. Metodologia de Teste e Auditoria
O modelo foi submetido a um ciclo de validação com 18 amostras inéditas (Dataset Customizado):
* **Grupo Real (n=8):** Capturas nativas com texturas biológicas e ruído de sensor óptico.
* **Grupo Fake (n=10):** Imagens geradas por modelos de difusão com alta complexidade estrutural.
* **Auditoria de Pixels (XAI):** Substituição do Grad-CAM pelo **Integrated Gradients (IG)**. O método axiomático foi utilizado para gerar uma "narrativa cognitiva", traduzindo atribuições de pixels em diagnósticos textuais de confiança.

---

### 3. Resultados Quantitativos (Finais da MA3)
Os testes com o motor de auditoria revelaram os seguintes índices:

| Métrica | Resultado |
| :--- | :--- |
| **Acurácia Global** | 61.1% (11/18) |
| **Acurácia Classe REAL** | 100% (8/8) |
| **Acurácia Classe FAKE** | 30% (3/10) |
| **Confiança Média (Acertos)** | 99.1% |
| **Confiança Média (Erros)** | 88.5% |

> **Nota Técnica:** O fenômeno de *Overconfidence* foi extremo nas falhas. O modelo classificou fakes como reais com até **100% de certeza**, indicando que as características sintéticas mimetizaram perfeitamente os pesos aprendidos para a classe real.

---

### 4. Análise de Explicabilidade (XAI)

#### 4.1 O "Foco Estrutural" (Sucessos)
Nas amostras reais, o IG confirmou que a ResNet50 foca em **irregularidades orgânicas** e morfologia de pixels não-linear. O modelo identifica corretamente a "assinatura física" da captura óptica, mantendo 100% de precisão nesta classe.

#### 4.2 O "Mimetismo de Textura" (Falhas Críticas)
A auditoria revelou que as falhas (ex: **Amostra 7.png**, **Amostra 6.jpeg**) não ocorreram por erro de localização, mas por **interpretação errônea de textura**. 
* **Evidência:** O modelo justificou erros de 100% de confiança alegando "irregularidade orgânica detectada". 
* **Diagnóstico:** A qualidade da geração sintética superou o filtro de texturas da ResNet50. O modelo interpretou sombras complexas (Chiaroscuro) e nitidez de bordas como evidências de realidade, ignorando a natureza artificial da imagem.

---

### 5. Decisões Estratégicas para o Deadline (06/04)
Para corrigir os desvios sem comprometer o cronograma, foram executadas as seguintes ações:
1.  **Subsampling Estratégico (1/3):** Dataset reduzido para ~33k imagens para acelerar o re-treinamento e ajuste de hiperparâmetros.
2.  **Ajuste de Atribuição:** Implementação do script de auditoria v6 com "Voz de IA" para monitorar a hesitação do modelo entre bordas e fundo.
3.  **Normalização Dinâmica:** Pré-processamento focado em reduzir a dependência da rede em relação à nitidez excessiva das imagens sintéticas.

---

### 6. Próximos Passos (MA4)
* **MA4:** Consolidação do módulo de explicabilidade e análise de **Frequência de Fourier** para detectar artefatos de grade invisíveis ao olho humano e à ResNet convencional.

---
**Referências:**
* Sundararajan, M. et al. (2017) – Axiomatic Attribution for Deep Networks (Integrated Gradients).
* Karras, T., et al. (2019) – StyleGAN.
