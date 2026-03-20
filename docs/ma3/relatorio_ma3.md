Relatório de Validação e Generalização - MA3
Projeto: Detecção de Deepfakes com ResNet50 e Explainable AI (XAI)
Data: 20 de Março de 2026
Status: Concluído (Fase de Inferência Externa)

1. Resumo Executivo

Este documento detalha os testes de generalização realizados no modelo de rede neural ResNet50, submetido a um processo de Fine-Tuning para a classificação de imagens entre as classes REAL e FAKE. O objetivo da MA3 foi validar o comportamento do modelo fora do dataset de treinamento, utilizando amostras de controle e amostras de estresse (ambientes não controlados).

2. Metodologia de Teste

Foram utilizadas 15 amostras inéditas, divididas em dois grupos:
Grupo Real (n=8): Capturas de tela (prints) e fotografias nativas com variações de textura orgânica.
Grupo Fake (n=7): Imagens geradas por redes adversárias generativas (GANs) e modelos de difusão, incluindo casos de alta fidelidade e iluminação complexa.
A técnica de Grad-CAM (Gradient-weighted Class Activation Mapping) foi aplicada para auditar as decisões do modelo e mitigar o efeito "Caixa Preta".

3. Resultados Quantitativos

Métrica                  Resultado
Acurácia Global          80% (12/15)
Acurácia Classe REAL     100% (8/8)
Acurácia Classe FAKE     57,1% (4/7)
Confiança Média (Acertos)82.4%
Confiança Média (Erros)  90.8%

Destaques da Inferência:
Melhor acerto (REAL): Amostra 152325.png com 98.34% de confiança.
Pior erro (FAKE): Amostra 7.png classificada como REAL com 98.53% de confiança.

4. Análise de Explicabilidade (Grad-CAM)

4.1. O "Detetive de Texturas" (Sucessos)
A análise visual confirmou que, em amostras reais, o modelo foca em entropia biológica.
Evidência: O mapa de calor concentrou-se em irregularidades cutâneas (espinhas, machucados e porosidade).
Conclusão: O Fine-Tuning foi bem-sucedido em identificar que a ausência de micro-imperfeições é um forte indicativo de geração sintética.

4.2. O "Viés Estético" (Falhas Críticas)
Identificou-se um fenômeno de Overconfidence nos erros.
Evidência: Nas amostras 6.jpeg e 7.png, o modelo ignorou a face e focou na transição de iluminação do pescoço e na textura da vestimenta.
Diagnóstico: O modelo correlacionou indevidamente "alta nitidez" e "iluminação de estúdio (Chiaroscuro)" com a classe REAL. A complexidade matemática das sombras em geradores de última geração mimetizou a assinatura de sensores CMOS reais, induzindo o erro.

5. Conclusão da MA3

O modelo atingiu o objetivo de separar classes em ambientes controlados, demonstrando 100% de eficácia em não barrar usuários legítimos. No entanto, a vulnerabilidade a Deepfakes de alta fidelidade com iluminação dramática define o limite operacional da versão atual. O modelo passou nos critérios de validação, mas requer ajustes de robustez.

6. Proposta para MA4 (Robustez e Verificação)

Com base nos dados coletados, a próxima fase focará em:
Aumentação Adversária: Treinamento focado em variações de brilho e contraste para quebrar a dependência de "iluminação de estúdio".
Ataque de Mutantes: Testar a persistência das ativações biométricas sob oclusão e ruído.
Redução de Viés: Implementação de normalização de histograma para neutralizar o viés de nitidez identificado nos erros de 98%.
