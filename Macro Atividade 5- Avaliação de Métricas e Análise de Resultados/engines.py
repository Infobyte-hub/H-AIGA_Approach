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

        # Classe 0 = fake | Classe 1 = real
        FP = cm[0][1]  # marcou real em fake
        FN = cm[1][0]  # marcou fake em real

        # Normalização por classe (evita distorção)
        total_fake = np.sum(y_true == 0) + 1e-6
        total_real = np.sum(y_true == 1) + 1e-6

        rate_fp = FP / total_fake
        rate_fn = FN / total_real

        # Gap de equidade
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

        # 🔥 Penalização maior para erro em REAL (FN)
        rate_fp = FP / total_fake
        rate_fn = FN / total_real

        # Peso maior para erro crítico (real class)
        risk = (0.7 * rate_fn) + (0.3 * rate_fp)

        # 🔥 Não linearidade (tolerância a erro pequeno)
        risk = np.power(risk, 2)

        return risk


# =========================
# GOVERNANCE ENGINE
# =========================
class GovernanceEngine:
    def __init__(self, wp, wr, wf, wt, alpha, beta, gamma):
        self.wp = wp  # peso performance
        self.wr = wr  # peso risco
        self.wf = wf  # peso fairness
        self.wt = wt  # peso trust

        self.alpha = alpha  # penalização bias
        self.beta = beta    # penalização compliance
        self.gamma = gamma  # penalização trust

    def compute(self, performance, risk, fairness, trust):
        # =========================
        # QUALIDADE BASE (MAUT)
        # =========================
        Q_total = (
            self.wp * performance
            - self.wr * risk
            - self.wf * fairness
            - self.wt * (1 - trust)
        )

        # =========================
        # PENALIZAÇÃO COM THRESHOLD
        # =========================
        # tolerância inicial (zona segura)
        bias_excess = max(0, fairness - 0.10)
        trust_excess = max(0, (1 - trust) - 0.10)
        risk_excess = max(0, risk - 0.10)

        P = (
            self.alpha * bias_excess +
            self.beta * trust_excess +
            self.gamma * risk_excess
        )

        # =========================
        # SCORE FINAL
        # =========================
        IGA_final = Q_total - P

        # clamp
        IGA_final = max(-1.0, min(1.0, IGA_final))

        return Q_total, P, IGA_final
