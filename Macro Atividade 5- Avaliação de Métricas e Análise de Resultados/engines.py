import numpy as np
from sklearn.metrics import confusion_matrix

# =========================
# PERFORMANCE ENGINE
# =========================
class MeasurementEngine:
    def performance(self, y_true, y_pred):
        acc = np.mean(np.array(y_true) == np.array(y_pred))
        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
        return acc, cm


# =========================
# FAIRNESS ENGINE
# =========================
class FairnessEngine:
    def fairness_gap(self, y_true, y_pred):
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

        FP = cm[0][1]
        FN = cm[1][0]

        total_fake = np.sum(y_true == 0) + 1e-6
        total_real = np.sum(y_true == 1) + 1e-6

        rate_fp = FP / total_fake
        rate_fn = FN / total_real

        fairness = abs(rate_fn - rate_fp)

        return fairness


# =========================
# RISK ENGINE
# =========================
class RiskEngine:
    def compute(self, y_true, y_pred):
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)

        cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

        FP = cm[0][1]
        FN = cm[1][0]

        total_fake = np.sum(y_true == 0) + 1e-6
        total_real = np.sum(y_true == 1) + 1e-6

        rate_fp = FP / total_fake
        rate_fn = FN / total_real

        risk = (0.7 * rate_fn) + (0.3 * rate_fp)

        # não linearidade
        risk = np.power(risk, 2)

        return risk


# =========================
# COMPLIANCE ENGINE (NOVO)
# =========================
class ComplianceEngine:
    def evaluate(self, acc, fairness, risk):
        """
        Avaliação simples baseada na sua tabela ISO-like
        """

        results = {}

        # Desempenho (proxy de GAR/EER)
        results["performance_ok"] = acc >= 0.95

        # Fairness (<= 3%)
        results["fairness_ok"] = fairness <= 0.03

        # Risco (proxy)
        results["risk_ok"] = risk <= 0.10

        # Score geral
        score = sum(results.values()) / len(results)

        return results, score


# =========================
# GOVERNANCE ENGINE
# =========================
class GovernanceEngine:
    def __init__(self, wp, wr, wf, wt, alpha, beta, gamma):
        self.wp = wp
        self.wr = wr
        self.wf = wf
        self.wt = wt

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        self.compliance_engine = ComplianceEngine()

    def compute(self, performance, risk, fairness, trust):
        # =========================
        # QUALIDADE BASE
        # =========================
        Q_total = (
            self.wp * performance
            - self.wr * risk
            - self.wf * fairness
            - self.wt * (1 - trust)
        )

        # =========================
        # PENALIZAÇÃO
        # =========================
        bias_excess = max(0, fairness - 0.10)
        trust_excess = max(0, (1 - trust) - 0.10)
        risk_excess = max(0, risk - 0.10)

        P = (
            self.alpha * bias_excess +
            self.beta * trust_excess +
            self.gamma * risk_excess
        )

        # =========================
        # COMPLIANCE (NOVO)
        # =========================
        compliance_results, compliance_score = self.compliance_engine.evaluate(
            performance, fairness, risk
        )

        # penalização extra se não cumprir norma
        compliance_penalty = (1 - compliance_score) * 0.2

        # =========================
        # SCORE FINAL
        # =========================
        IGA_final = Q_total - P - compliance_penalty

        IGA_final = max(-1.0, min(1.0, IGA_final))

        return Q_total, P, compliance_penalty, IGA_final, compliance_results
