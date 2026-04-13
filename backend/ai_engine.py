import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

class AIEngine:
    def __init__(self):
        self.scaler = StandardScaler()
        self.model = IsolationForest(
            contamination=0.05,
            n_estimators=200,
            random_state=42
        )
        self.total = 0
        self.anomalies = 0
        self.blocked = set()
        self._train()

    def _train(self):
        print("Entraînement du modèle IA...")
        normal = []
        np.random.seed(42)
        for _ in range(1000):
            normal.append([
                np.random.randint(5, 150),    # req_rate : trafic humain normal
                np.random.randint(300, 4000), # bytes : pages web normales
                np.random.choice([80, 443]),  # ports web uniquement
                np.random.randint(80, 500),   # durée : requête normale
            ])
        X = np.array(normal)
        self.scaler.fit(X)
        self.model.fit(self.scaler.transform(X))
        print("Modèle prêt !")

    def _extract_features(self, log: dict) -> list:
        return [
            log.get("req_rate", 0),
            log.get("bytes", 0),
            log.get("port", 80),
            log.get("duration_ms", 100),
        ]

    def analyze(self, log: dict) -> tuple:
        self.total += 1
        features = self._extract_features(log)
        X = self.scaler.transform([features])

        raw = self.model.decision_function(X)[0]
        score = float(1 / (1 + np.exp(raw * 3)))

        is_anomaly = score > 0.50

        if is_anomaly:
            self.anomalies += 1
            self.blocked.add(log.get("ip", "unknown"))

        return score, is_anomaly

    def security_score(self) -> int:
        if self.total == 0:
            return 100
        rate = self.anomalies / self.total
        return max(0, round(100 - rate * 200))
