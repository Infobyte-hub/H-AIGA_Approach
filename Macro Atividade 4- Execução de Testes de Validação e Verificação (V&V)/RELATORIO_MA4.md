# MA4 – Relatório de Execução de Testes de Validação e Verificação (V&V)

**Data:** 25 de Março de 2026  
**Status:** Concluído  
**Modelo Auditado:** ResNet50 (`best_model.keras`)  
**Responsável:** igaog

---

### 1. Resumo da Atividade
Esta etapa consistiu no "Red Teaming" do modelo desenvolvido na MA3. O objetivo foi submeter a rede a condições extremas de estresse (Ataques Adversários e Degradação Física) para medir a real confiabilidade do sistema em ambiente de produção.

---

### 2. Metodologia de Auditoria
Foram aplicados três protocolos de ataque automatizados via script `attack_generator_v2.py`:
1.  **FGSM (Fast Gradient Sign Method):** Ataque matemático que explora o gradiente do modelo com $\epsilon=0.03$.
2.  **Compressão JPEG (Qualidade 5-15):** Simulação de perda de pacotes e baixa largura de banda.
3.  **Ataque Híbrido:** Combinação de ruído matemático com degradação visual para testar o colapso total.

A análise qualitativa foi realizada via **Integrated Gradients (IG)**, gerando mapas de atribuição de pixels para identificar "pontos cegos".

---

### 3. Resultados Quantitativos (Métricas de Stress)

| Classe | Acurácia (Limpo) | Acurácia (Sob Ataque) | Status de Robustez |
| :--- | :--- | :--- | :--- |
| **REAL** | 100% | 0% | 💀 **Vulnerabilidade Crítica** |
| **FAKE** | 30% | 70% (Inversão) | 🛡️ **Mimetismo Persistente** |

**Observação:** O modelo apresentou um decaimento de performance catastrófico na classe Real. Amostras com 1.00 de predição (ex: `122448.png`) caíram para valores próximos a 0.00 após manipulações invisíveis ao olho humano.

---

### 4. Diagnóstico por Explicabilidade (XAI)

Através da perícia visual (scripts de auditoria v6/v2), identificamos três padrões de falha:

* **Dispersão Cognitiva:** Em imagens reais com fundos complexos (ex: `122448.png`), o modelo foca no ruído do cenário em vez do objeto principal. O ataque FGSM "suja" o fundo e desorienta a predição.
* **Foco Cirúrgico em Bordas:** O modelo valida imagens baseando-se em contornos geométricos (olhos, nariz, boca). Como as Fakes (ex: `3.jpg`, `4.jpg`) possuem geometria perfeita, o modelo as classifica como Reais com 99% de confiança.
* **Fragilidade de Gradiente:** A ResNet50 demonstrou ser um "classificador de vidro": extremamente precisa em condições ideais, mas instável sob qualquer ruído de alta frequência.

---

### 5. Evidências Fotográficas (Amostras de Perícia)

As imagens abaixo (geradas pelo `diagnostic_lab_v2.py`) comprovam que o foco da IA é desviado durante o ataque:

* **Amostra 122448 (REAL):** Colapso total; o mapa de calor mostra foco na parede de fundo.
* **Amostra 152248 (REAL):** Foco excessivo em contornos faciais, ignorando a textura da pele.
* **Amostra 3 (FAKE):** Aceita como real devido ao alinhamento geométrico dos olhos.

---

### 6. Conclusão e Recomendações
O modelo **não possui robustez adversária** suficiente para deploy seguro. Para a próxima etapa (MA5), recomenda-se:
1.  **Adversarial Training:** Treinar o modelo expondo-o a imagens atacadas por FGSM.
2.  **Filtros de Frequência:** Implementar filtros passa-baixa para remover ruídos antes da inferência.
3.  **Regularização:** Aplicar Dropout e Weight Decay mais agressivos para evitar que a rede decore ruídos de fundo.

---
