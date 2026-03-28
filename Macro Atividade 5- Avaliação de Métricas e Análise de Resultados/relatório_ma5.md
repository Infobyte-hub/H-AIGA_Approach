# Macro Atividade 5 – Avaliação de Métricas e Análise de Resultados

## 1. Objetivo

Esta etapa tem como objetivo avaliar o desempenho do sistema proposto sob a perspectiva de governança, considerando a interação entre decisões humanas e da inteligência artificial. A análise busca verificar a confiabilidade do sistema, sua capacidade de filtragem e o impacto do comportamento do usuário no resultado final.

---

## 2. Metodologia

O experimento foi conduzido por meio de uma interface interativa onde usuários anônimos participaram de rodadas de validação visual, classificando imagens como “real” ou “fake”.

Cada interação gerou dados estruturados contendo:

- Identificador anônimo do usuário  
- Tempo de resposta  
- Número de seleções  
- Acertos e erros  
- Decisão da IA  
- Veredito final do sistema  

O cálculo do Índice de Governança Algorítmica (IGA), bem como os detalhes da arquitetura do sistema e da coleta de dados, seguem conforme definido nas seções anteriores do trabalho.

Para avaliação comportamental, foram simulados diferentes perfis de uso:

- Usuários tentando maximizar acertos  
- Usuários tentando errar deliberadamente  
- Usuários com comportamento natural  
- Usuários com tempo de resposta elevado  

Essa abordagem permitiu observar a robustez do sistema diante de diferentes estratégias humanas.

---

## 3. Resultados

### 3.1 Comparação entre desempenho humano e IA

Os resultados indicam que a IA apresentou desempenho superior em relação aos usuários humanos.

- Acurácia média humana: **0.58**  
- Acurácia da IA: **0.79**

Esse resultado evidencia maior consistência da IA, enquanto o desempenho humano apresentou maior variabilidade.

---

### 3.2 Relação entre tempo de resposta e desempenho

A análise da relação entre tempo de resposta e acurácia humana mostrou uma tendência levemente positiva, porém com alta dispersão.

Observou-se que:

- Alguns usuários obtiveram bons resultados com respostas rápidas  
- Outros apresentaram baixo desempenho mesmo com maior tempo de análise  

Isso indica que o tempo de resposta, isoladamente, não é um indicador confiável de qualidade da decisão.

---

### 3.3 Decisão do sistema (governança)

A distribuição das decisões finais do sistema foi:

- **60% Liberado**  
- **40% Negado**

Esse resultado demonstra que o sistema não apresenta comportamento extremo, mantendo um equilíbrio entre aceitação e rejeição.

---

## 4. Discussão

Os resultados evidenciam três pontos principais.

### 4.1 Variabilidade humana

O desempenho humano mostrou-se inconsistente, variando significativamente entre diferentes usuários e estratégias. Essa variabilidade reforça a necessidade de mecanismos de governança que não dependam exclusivamente da decisão humana.

---

### 4.2 Estabilidade da IA

A IA apresentou comportamento estável e previsível, com maior taxa de acerto. Isso confirma seu papel como elemento central na validação automatizada, reduzindo a incerteza associada ao fator humano.

---

### 4.3 Limitação do tempo como métrica de qualidade

Embora o tempo de resposta represente esforço, ele não se traduz diretamente em melhor desempenho. Isso indica que decisões humanas são influenciadas por fatores além do tempo disponível, como percepção, atenção e estratégia.

---

### 4.4 Efetividade do sistema de governança

O sistema demonstrou capacidade de:

- Identificar comportamentos inconsistentes  
- Filtrar respostas de baixa confiabilidade  
- Manter equilíbrio entre segurança e usabilidade  

A combinação entre avaliação humana, decisão da IA e métricas de governança mostrou-se eficaz na definição do veredito final.

---

## 5. Conclusão

A avaliação realizada nesta etapa confirma que o sistema proposto é funcional e capaz de operar como mecanismo de validação baseado em governança humano-IA.

Os principais resultados indicam que:

- A IA apresenta maior consistência decisória em comparação ao humano  
- O comportamento do usuário impacta diretamente a confiabilidade do sistema  
- O tempo de resposta não é um indicador suficiente de qualidade  
- O modelo de governança adotado consegue equilibrar segurança e acessibilidade  

Dessa forma, o sistema se mostra adequado para cenários que exigem validação robusta, especialmente em contextos onde decisões humanas isoladas podem ser inconsistentes.
