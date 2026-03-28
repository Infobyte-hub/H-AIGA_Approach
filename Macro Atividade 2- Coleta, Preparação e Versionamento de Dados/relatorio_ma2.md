# MA2 – Relatório Experimental: Governança, Ética e Preparação de Dados

## 1. Introdução
Este documento descreve a configuração experimental e os fundamentos éticos do framework de auditoria. O cenário utiliza o dataset **140k Real and Fake Face**, focado na distinção entre faces humanas reais e faces sintéticas geradas por redes adversárias generativas (GANs).

A arquitetura de dados segue o método **holdout**, garantindo a separação rigorosa para evitar vazamento de dados (*data leakage*):
- **Treinamento:** 70% (Base de aprendizado)
- **Validação:** 15% (Ajuste de hiperparâmetros)
- **Teste:** 15% (Avaliação final de performance)

---

## 2. Conformidade Ética e Governança de Dados
A condução desta pesquisa prioriza a transparência e a proteção de dados, seguindo as diretrizes da LGPD e os princípios de *Responsible AI*:

* **Licenciamento:** As imagens reais provêm do conjunto **FFHQ (NVIDIA)**, coletadas sob licenças **Creative Commons (BY-NC-SA 4.0)**. O uso é estritamente acadêmico e não-comercial.
* **Privacidade (Privacy by Design):** Metadados de identificação pessoal (EXIF) foram removidos. O uso de 50% de faces sintéticas (StyleGAN) atua como medida de mitigação de risco, pois estas não possuem correspondentes biológicos reais.
* **Pesquisa com Humanos (MA5):** A validação com voluntários implementa um **TCLE (Termo de Consentimento Livre e Esclarecido)** digital. Os logs de auditoria são anonimizados via IDs aleatórios, garantindo que nenhum dado sensível dos participantes seja armazenado.
* **Integridade:** O dataset passou por curadoria humana (NVIDIA e curadores originais) para garantir a precisão das etiquetas (*labels*).

---

## 3. Distribuição e Amostragem Estratégica
Para viabilizar a execução do treinamento e auditoria dentro do cronograma estabelecido (**Deadline: 06/04**), aplicou-se uma redução proporcional do volume de dados.

### 3.1 Tabela de Distribuição Original
| Split | Real | Fake | Total |
|-------|------|------|-------|
| Train | 50.000 | 50.000 | 100.000 |
| Valid | 10.000 | 10.000 | 20.000 |
| Test  | 10.000 | 10.000 | 20.000 |
| **Total** | **70.000** | **70.000** | **140.000** |

### 3.2 Estratégia de Subsampling (1/3)
Utilizou-se o método de sorteio aleatório simples para reduzir o dataset a **33% de sua capacidade original** (aprox. 46.666 imagens). Esta decisão estratégica visa:
1.  **Convergência Acelerada:** Permitir múltiplos ciclos de treino (MA3) no ambiente WSL.
2.  **Eficiência de Auditoria:** Facilitar a geração de mapas de calor (Grad-CAM) em tempo real.
3.  **Manutenção Estatística:** Preservar o balanceamento 50/50 entre as classes para evitar vieses.

---

## 4. Teste de Sanidade e Observações Visuais
A análise preliminar indicou que:
- **Imagens Reais:** Apresentam ruído de sensor térmico natural e texturas orgânicas complexas.
- **Imagens Fake:** Exibem artefatos típicos de GANs, como fundos amorfos ("líquidos"), dentes frontais desalinhados e assimetria em acessórios (brincos/óculos).
- **Desafio Humano:** Algumas instâncias sintéticas de alta fidelidade demonstram potencial para enganar observadores humanos, justificando a necessidade do framework de governança.

---

## 5. Próximos Passos
1.  Execução do treinamento da ResNet50 com o dataset reduzido (MA3).
2.  Implementação do módulo de explicabilidade textual (XAI).
3.  Coleta de dados psicofísicos com voluntários humanos (MA5).

---

## Referências
- NVIDIA (2019). *Flickr-Faces-HQ Dataset (FFHQ)*.
- Karras, T., et al. (2019). *A Style-Based Generator Architecture for GANs*.
- Lei Geral de Proteção de Dados Pessoais (LGPD) - Lei nº 13.709/2018.
