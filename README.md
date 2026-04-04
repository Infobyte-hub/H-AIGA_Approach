# Integrated Responsible AI Assurance Framework (IRAAF)

Este repositório contém a implementação e os resultados do framework de avaliação normativa para componentes de IA, com foco em reconhecimento facial e detecção de faces sintéticas.

## 🚀 Visão Geral
O projeto operacionaliza seis macro atividades de governança, integrando métricas técnicas (Acurácia, EER) com indicadores de responsabilidade (IGA - Índice de Governança Algorítmica).

## 📊 Principais Resultados
O framework utiliza um modelo de penalização por risco:
$IGA_{final} = Q_{total} - (\alpha B + \beta C + \gamma T)$

- **Acurácia Nominal:** ~0.82
- **IGA Médio:** ~0.10
- **Taxa de Rejeição Normativa:** 40% (Modelos com alta acurácia, mas baixo IGA).

## 🛠 Tecnologias e Normas
- **Linguagem:** Python (Pandas, Matplotlib, Scikit-learn)
- **Normas Referenciadas:** ISO/IEC 42001, ISO/IEC 23894, IEEE Std 2945.
- **Técnicas de Teste:** Teste de Mutação, Teste Metamórfico e Fair SA.

## 📁 Estrutura do Pipeline
1. MA1: Requisitos e Riscos
2. MA2: Preparação de Dados (140k faces)
3. MA3: Treinamento Reprodutível (ArcFace/ResNet)
4. MA4: Execução de Testes (V&V)
5. MA5: Avaliação de Métricas e IGA
6. MA6: Governança e Monitoramento
