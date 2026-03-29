# Macro Atividade 5 – Avaliação de Métricas e Análise de Resultados

## 1. Objetivo

Esta etapa tem como objetivo avaliar o desempenho do sistema proposto sob a perspectiva de governança, considerando a interação entre decisões humanas e da inteligência artificial.

A análise busca verificar não apenas a acurácia das decisões, mas também dimensões complementares como risco, equidade e confiança, permitindo uma avaliação mais robusta da qualidade das decisões.

---

## 2. Metodologia

O experimento foi conduzido por meio de uma interface interativa onde usuários anônimos participaram de rodadas de validação visual, classificando imagens como “real” ou “fake”.

Cada interação gerou dados estruturados contendo:

- Identificador anônimo do usuário  
- Tempo de resposta  
- Decisões humanas  
- Decisões da IA  
- Acurácia individual  
- Métricas derivadas (risk, fairness, trust)  
- Índices de governança (Q_total, P, IGA)  

O cálculo das métricas foi realizado programaticamente por meio de um motor de avaliação (`GovernanceEngine`), responsável por integrar múltiplas dimensões:

- **Performance (acc)**: proporção de acertos  
- **Risk (risk)**: penalização não linear associada ao erro, com maior peso para falsos negativos  
- **Fairness (fairness)**: diferença entre taxas de erro por classe  
- **Trust (trust)**: proxy de confiança baseada na acurácia da IA  

O escore agregado é definido como:
Q_total = w_p * performance - w_r * risk - w_f * fairness - w_t * (1 - trust)


A partir desse escore, aplica-se um fator de penalização normativa `P`, ativado quando limites de tolerância são excedidos (ex.: risk > 0.10, fairness > 0.10):

IGA = Q_total - P


Essa formulação permite que o sistema não apenas avalie desempenho, mas também incorpore critérios de governança.

Para avaliação comportamental, foram simulados diferentes perfis:

- Usuários buscando maximizar acertos  
- Usuários com erro deliberado  
- Usuários com comportamento natural  
- Usuários com maior tempo de resposta  

---

## 3. Resultados

### 3.1 Comparação entre desempenho humano e IA

- Acurácia média humana: **0.58**  
- Acurácia da IA: **0.79**

A IA apresentou maior consistência, enquanto o desempenho humano mostrou maior variabilidade.

---

### 3.2 Relação entre tempo de resposta e desempenho

A análise entre tempo e acurácia humana mostrou alta dispersão.

Observou-se que:

- Respostas rápidas podem apresentar alta acurácia  
- Maior tempo não garante melhor desempenho  

Isso indica que o tempo de resposta não é um indicador confiável de qualidade decisória.

---

### 3.3 Decisão do sistema

Distribuição das decisões:

- **60% Liberado**  
- **40% Negado**

O sistema apresenta comportamento equilibrado, evitando viés extremo de aceitação ou rejeição.

---

### 3.4 Métricas de Governança (IGA, P e Q_total)

A análise baseada nas métricas de governança evidenciou que o desempenho isolado não é suficiente para caracterizar a qualidade da decisão.

Observou-se que:

- O aumento da penalização (**P**) está diretamente associado à redução do IGA  
- O escore **Q_total** reflete o desempenho bruto, enquanto o IGA incorpora restrições normativas  
- O sistema responde de forma sensível a variações em risco, fairness e confiança  

O comportamento observado confirma que o mecanismo de penalização atua como elemento de controle, reduzindo a governança em cenários críticos.

---

### 3.5 Comparação de Governança: Humano vs IA

A análise comparativa entre IGA humano e IGA da IA mostrou distribuição dispersa.

Observou-se que:

- Em alguns cenários, o humano apresenta maior governança que a IA  
- Em outros, a IA supera o desempenho humano  
- Não há dominância absoluta entre os agentes  

Isso indica que a governança deve ser tratada como uma propriedade do sistema como um todo, e não de um único agente.

---

### 3.6 Detecção de Overconfidence

A análise da relação entre confiança (trust) e acurácia revelou a ocorrência de casos onde a IA apresenta alta confiança mesmo em decisões incorretas.

Esse comportamento caracteriza **overconfidence**, um tipo crítico de falha onde o modelo erra com elevada certeza.

Observou-se que:

- Existem pontos com confiança elevada e acurácia inferior  
- Esses casos não seriam identificados apenas com métricas tradicionais  

Esse resultado demonstra a importância da inclusão da dimensão de confiança na avaliação.

---

### 3.7 Trade-off entre Fairness e Risk

A análise conjunta de fairness e risk indicou que essas métricas não são independentes.

Observou-se que:

- Reduções em fairness nem sempre implicam redução de risco  
- Existe relação de trade-off entre essas dimensões  

Isso reforça a necessidade de abordagens multiobjetivo na avaliação de sistemas de IA.

---

## 4. Discussão

### 4.1 Variabilidade humana

O desempenho humano apresentou alta variabilidade, influenciado por estratégia, atenção e tempo de resposta.

Isso reforça a limitação de sistemas baseados exclusivamente em decisão humana.

---

### 4.2 Estabilidade da IA

A IA apresentou maior estabilidade em termos de acurácia.

No entanto, a análise de overconfidence mostra que alta performance não implica necessariamente confiabilidade, evidenciando a necessidade de métricas complementares.

---

### 4.3 Limitação do tempo como métrica

O tempo de resposta não demonstrou correlação consistente com qualidade decisória.

Isso indica que fatores cognitivos têm maior impacto que o tempo disponível.

---

### 4.4 Efetividade do modelo de governança

O sistema demonstrou capacidade de integrar múltiplas dimensões em um único índice.

A presença do fator de penalização permite:

- Reduzir impacto de decisões de alto risco  
- Controlar desvios de equidade  
- Penalizar excesso de confiança indevido  

Além disso, a combinação entre confiança e acurácia permite identificar falhas críticas que não seriam capturadas por métricas tradicionais.

---

## 5. Conclusão

Os resultados confirmam que o sistema é capaz de avaliar decisões utilizando múltiplas dimensões além da acurácia, incluindo risco, equidade e confiança.

O índice de governança algorítmica (IGA) demonstrou ser eficaz para consolidar essas dimensões em um único escore, permitindo análise comparativa entre decisões humanas e da IA.

A introdução do fator de penalização possibilita capturar desvios críticos, aumentando a robustez da avaliação.

Adicionalmente, a detecção de comportamentos de overconfidence evidencia a capacidade do sistema em identificar falhas relevantes não observáveis por métricas tradicionais.

Dessa forma, o modelo implementado atende ao objetivo de fornecer uma avaliação estruturada da qualidade das decisões em um cenário de interação humano-IA.
