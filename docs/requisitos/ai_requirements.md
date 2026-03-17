# AI REQUIREMENTS DOCUMENT — CAPTCHA TRUST AI

## 1. Contexto

Sistema de reconhecimento facial aplicado à validação de identidade humana em desafios do tipo CAPTCHA, com foco em segurança, robustez e mitigação de vieses.

Objetivo: Garantir que o modelo distinga humanos reais de tentativas automatizadas, mantendo conformidade com princípios de IA responsável.

## 2. Requisitos Funcionais

RF01: O sistema deve classificar imagens faciais como "humano válido" ou "não válido".
RF02: O sistema deve processar imagens em tempo inferior a 500ms.
RF03: O sistema deve operar com imagens em diferentes condições (iluminação, pose, oclusão).

## 3. Requisitos Não Funcionais

RNF01 (Acurácia):
O modelo deve atingir acurácia mínima de 95% no conjunto de teste.

RNF02 (FAR - False Acceptance Rate):
Taxa máxima de aceitação indevida: <= 1%.

RNF03 (FRR - False Rejection Rate):
Taxa máxima de rejeição indevida: <= 3%.

RNF04 (Latência):
Tempo máximo de inferência: 500ms por requisição.

RNF05 (Robustez):
Desempenho não deve cair mais que 10% sob variações de iluminação e pose.

RNF06 (Fairness - Equidade):
Diferença máxima de desempenho entre grupos demográficos <= 5%.

## 4. Requisitos de IA Responsável

RAI01 (Transparência):
O modelo deve possuir Model Card documentado.

RAI02 (Rastreabilidade):
Todos os experimentos devem ser versionados (dados, código e modelo).

RAI03 (Auditabilidade):
Logs de inferência e treinamento devem ser armazenados.

RAI04 (Gestão de Risco):
Cada versão do modelo deve possuir avaliação de risco documentada.

RAI05 (Explicabilidade):
Devem ser gerados mapas de ativação (CAM) para análise do modelo.

## 5. Critérios de Aceitação

- Todos os RNFs devem ser validados por métricas quantitativas.
- Testes devem ser reproduzíveis.
- Resultados devem ser documentados e versionados.
- Evidências devem estar disponíveis para auditoria.

## 6. Riscos

R01: Viés demográfico não detectado.
Impacto: Alto
Probabilidade: Média

R02: Dados de baixa qualidade.
Impacto: Alto
Probabilidade: Alta

R03: Requisitos ambíguos.
Impacto: Médio
Probabilidade: Alta

## 7. Checkpoint

Revisão técnica obrigatória garantindo:
- Clareza dos requisitos
- Métricas bem definidas
- Alinhamento com objetivos do sistema

## 8. Matriz de Rastreabilidade

| ID | Requisito | Métrica | Método de Validação | Risco Associado |
|----|----------|--------|---------------------|----------------|
| RNF01 | Acurácia >= 95% | Accuracy | Teste em dataset validado | R02 |
| RNF02 | FAR <= 1% | False Acceptance Rate | Matriz de confusão | R01 |
| RNF03 | FRR <= 3% | False Rejection Rate | Matriz de confusão | R01 |
| RNF05 | Robustez | Δ desempenho <= 10% | Testes com mutação de dados | R02 |
| RNF06 | Fairness | Gap <= 5% entre grupos | Análise de sensibilidade | R01 |
| RAI02 | Rastreabilidade | Versionamento ativo | Git + logs | R03 |

## 9. Matriz de Risco

| ID | Descrição | Impacto | Probabilidade | Severidade | Mitigação |
|----|----------|--------|--------------|-----------|----------|
| R01 | Viés demográfico | Alto | Médio | Alto | Sensitive Loss + Fairness SA |
| R02 | Baixa qualidade dos dados | Alto | Alto | Crítico | Filtro biométrico (ISO 29794-5) |
| R03 | Falta de rastreabilidade | Médio | Alto | Alto | Versionamento obrigatório |

## 10. Evidências de Auditoria

- Logs de treinamento e inferência armazenados
- Versões de datasets documentadas
- Model Cards disponíveis
- Resultados de testes registrados
- Relatórios de risco atualizados por versão
## 11. Estratégia de Validação (Pseudo-Oráculo)

Devido à ausência de oráculo perfeito, serão utilizados:

- Testes metamórficos (invariância a iluminação, rotação)
- Testes de mutação:
  - Dados (ruído, distorção)
  - Programa (alteração pipeline)
  - Modelo (arquitetura)
- Neuron Coverage para análise estrutural

Objetivo: detectar comportamentos inconsistentes do modelo sem depender de saída esperada explícita.


## 12. Conflitos entre Requisitos

C01: Acurácia vs Fairness  
- Descrição: Aumento de acurácia pode amplificar viés entre grupos  
- Decisão: Priorizar fairness quando diferença > 5%  
- Ação: Aplicação de Sensitive Loss + monitoramento contínuo  

C02: Segurança (FAR baixo) vs Usabilidade (FRR baixo)  
- Descrição: Reduzir FAR aumenta rejeição de usuários legítimos  
- Decisão: Balanceamento com threshold adaptativo  
- Ação: Ajuste dinâmico baseado em contexto de risco  

C03: Robustez vs Latência  
- Descrição: Modelos mais robustos tendem a ser mais pesados  
- Decisão: Limite rígido de 500ms mantido  
- Ação: Otimização de inferência (quantização/pruning)

## 13. Priorização de Requisitos

| Requisito | Criticidade | Justificativa |
|----------|------------|--------------|
| RNF02 (FAR) | Crítico | Impacto direto em segurança |
| RNF06 (Fairness) | Alto | Risco ético e regulatório |
| RNF01 (Acurácia) | Alto | Performance geral do sistema |
| RNF04 (Latência) | Médio | Impacto na experiência |
| RAI02 (Rastreabilidade) | Crítico | Base da auditoria |
