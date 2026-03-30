class RiskModel:
    def __init__(self, data):
        self.data = data

    def clasificar_riesgo(self, promedio, asistencia):
        if promedio < 3.0 or asistencia < 80:
            return "Alto"
        elif promedio <= 3.5 and asistencia >= 80:
            return "Medio"
        else:
            return "Bajo"

    def aplicar_clasificacion(self):
        self.data["riesgo"] = self.data.apply(
            lambda row: self.clasificar_riesgo(
                row["promedio"], row["asistencia"]
            ),
            axis=1
        )
        return self.data