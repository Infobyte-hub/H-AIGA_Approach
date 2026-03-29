# Relatório – Macro Atividade 6: Documentação, Governança e Monitoramento Contínuo

**Data:** 28/03/2026

---

## 1. Objetivo

Consolidar a documentação do processo de validação, garantir rastreabilidade completa dos artefatos produzidos e estabelecer um plano de monitoramento contínuo do modelo em produção, assegurando conformidade com princípios de Responsible AI e requisitos normativos.

---

## 2. Escopo da Atividade

A Macro Atividade 6 atua como camada final do pipeline, integrando:

- Resultados experimentais (MA5)
- Evidências técnicas de validação
- Métricas de desempenho e governança
- Documentação normativa e auditável

O foco principal é transformar resultados técnicos em **ativos de governança**, prontos para auditoria e uso em ambientes reais.

---

## 3. Artefatos Produzidos

### 3.1 Relatório de Avaliação de Impacto de IA

Documento consolidado contendo:

- Métricas de desempenho (IA e humano)
- Índice de Governança Algorítmica (IGA)
- Análise de risco e fairness
- Decisão final do sistema (liberação/negação)

---

### 3.2 Base de Dados de Auditoria

Arquivos gerados durante a execução do sistema:

- `responses.csv`

Esses dados garantem rastreabilidade completa das decisões.

---

### 3.3 Evidências Visuais

Gráficos gerados para suporte à análise:

- Comparação IA vs Humano  
- Relação tempo vs desempenho  
- Distribuição de decisões do sistema  

Esses artefatos suportam auditoria e interpretação dos resultados.

---

## 4. Análise de Governança

A integração entre decisões humanas e da IA, mediada pelo índice de governança algorítmica (IGA), demonstrou capacidade de controle sobre múltiplas dimensões da decisão.

Observou-se que:

- O IGA reduz o impacto de decisões com alto risco ou baixa equidade  
- O fator de penalização (P) atua diretamente na mitigação de cenários críticos  
- Decisões com alta confiança e baixo desempenho são penalizadas automaticamente  

Esse comportamento confirma que o modelo não depende exclusivamente de acurácia, mas incorpora critérios adicionais de governança, tornando o processo decisório mais robusto e auditável.

---

## 5. Análise de Padrões de Detecção (Real vs Fake)

A análise dos resultados indica que o modelo de IA opera com base em padrões estruturais e estatísticos das imagens.

Principais padrões identificados:

- Inconsistências de textura em imagens sintéticas  
- Artefatos visuais em regiões críticas (olhos, dentes, bordas)  
- Distribuição irregular de iluminação e cores  
- Assimetrias faciais sutis  

Observou-se que tanto a IA quanto os usuários humanos apresentam maior taxa de erro em casos limítrofes, onde as diferenças entre imagens reais e sintéticas são menos evidentes.

Essa análise reforça a necessidade de monitoramento contínuo, uma vez que melhorias em técnicas de geração sintética podem reduzir a eficácia desses padrões.

Esses padrões estão diretamente relacionados ao componente de risco (risk) do modelo, uma vez que erros em regiões críticas tendem a impactar negativamente a classificação.

A identificação desses padrões reforça a necessidade de monitoramento contínuo, especialmente diante da evolução de técnicas de geração sintética, que podem reduzir a eficácia dos sinais atualmente utilizados.

---
## 6. Plano de Monitoramento Contínuo

Para garantir a operação segura e auditável do sistema, define-se um plano baseado em métricas mensuráveis e ações corretivas.

### 6.1 Monitoramento de Performance e Governança

- Monitorar continuamente:
  - Acurácia da IA (acc_ia)
  - Índice de governança (IGA)
  - Penalização média (P)

- Critérios de alerta:
  - Queda de IGA abaixo de 0.5  
  - Aumento de P acima de 0.2  

- Ações:
  - Revisão do modelo  
  - Reavaliação dos pesos do GovernanceEngine  

---

### 6.2 Monitoramento de Risco e Fairness

- Monitorar:
  - Risk (risk_ia)
  - Fairness (fairness_ia)

- Critérios de alerta:
  - Risk > 0.10  
  - Fairness > 0.10  

- Ações:
  - Auditoria de erros por classe  
  - Ajuste de balanceamento do dataset  

---

### 6.3 Monitoramento de Confiança (Overconfidence)

- Monitorar:
  - Relação entre trust e acurácia  

- Critério de alerta:
  - Alta confiança com baixa acurácia  

- Ação:
  - Investigação de comportamento do modelo  
  - Ajuste de threshold ou calibração  

---

### 6.4 Monitoramento de Dados

- Verificar:
  - Mudança na distribuição das imagens  
  - Novos padrões de imagens sintéticas  

- Ação:
  - Atualização do dataset  
  - Re-treinamento do modelo  

---

### 6.5 Monitoramento de Usuários

- Monitorar:
  - Tempo de resposta  
  - Taxa de acerto  

- Critério:
  - Padrões inconsistentes ou anômalos  

- Ação:
  - Filtragem ou exclusão de dados  

---

### 6.6 Re-treinamento do Modelo

- Periodicidade:
  - Baseada em degradação de métricas  

- Critério:
  - Queda consistente de IGA  

- Ação:
  - Re-treinamento completo  
  - Revalidação via MA5  

---
## 7. Critérios de Aceitação

- Documentação completa e rastreável  
- Registro das métricas de governança (IGA, P, risk, fairness, trust)  
- Evidências quantitativas e visuais dos resultados  
- Definição clara de limites operacionais e critérios de alerta  
- Transparência no processo de decisão  
---
## 8. Riscos Identificados

- Documentação incompleta ou desatualizada  
- Ausência de monitoramento contínuo  
- Degradação do modelo devido a novos tipos de dados  
- Dependência excessiva de padrões específicos de detecção  

---

## 9. Conclusão da Macro Atividade

A Macro Atividade 6 consolida o sistema como uma solução governável, auditável e sustentável.

Os resultados demonstram que:

- O sistema produz evidências rastreáveis  
- A governança algorítmica é operacionalizável  
- O modelo pode ser monitorado e evoluído ao longo do tempo  

Dessa forma, o pipeline deixa de ser apenas experimental e passa a representar uma arquitetura de avaliação governável, com capacidade de monitoramento contínuo, detecção de falhas e adaptação a mudanças no ambiente.

O sistema demonstra viabilidade para aplicação em cenários reais que exigem controle, rastreabilidade e conformidade com princípios de Responsible AI.
