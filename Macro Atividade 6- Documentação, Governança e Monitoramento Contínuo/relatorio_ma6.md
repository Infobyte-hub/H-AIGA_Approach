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

- `participants.csv` → registro de usuários anônimos  
- `responses_raw.csv` → respostas individuais  
- `ma5_audit_report.csv` → métricas consolidadas por execução  

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

A integração entre decisões humanas e da IA, mediada pelo IGA, demonstrou:

- Capacidade de filtrar comportamentos inconsistentes  
- Redução do impacto de erros humanos  
- Estabilidade na decisão final do sistema  

O modelo de governança operou como mecanismo de controle, evitando decisões baseadas exclusivamente em um único agente.

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

---

## 6. Plano de Monitoramento Contínuo

Para garantir a sustentabilidade do sistema, define-se o seguinte plano:

### 6.1 Monitoramento de Performance

- Acompanhamento contínuo da acurácia da IA  
- Avaliação da variação do IGA ao longo do tempo  

---

### 6.2 Monitoramento de Dados

- Verificação de mudanças na distribuição dos dados  
- Detecção de novos padrões de imagens sintéticas  

---

### 6.3 Monitoramento de Usuários

- Análise de comportamento (tempo de resposta, acertos)  
- Identificação de padrões anômalos  

---

### 6.4 Re-treinamento do Modelo

- Atualização periódica com novos dados  
- Reavaliação das métricas de fairness e robustez  

---

## 7. Critérios de Aceitação

- Documentação completa e rastreável  
- Evidências suficientes para auditoria externa  
- Métricas alinhadas com requisitos definidos  
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

Dessa forma, o pipeline deixa de ser apenas experimental e passa a representar uma base viável para aplicações reais em contextos sensíveis.
