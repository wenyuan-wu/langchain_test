
def create_db():
    patient_db = {
        12: {
            "name": "John",
            "BMI": "27",
            "plan": 27,
        }
    }

    plan_db = {
        27: {
            "plan": "Intervall-Fasten mit Essfenster morgens bis 13:00, Schwimmen 30 Minuten/500 Meter Mo/Do/Sa je "
                    "Abends"
        }
    }

    measure_db = {
        18: {
            "measure": "Am Do-Abend schwimmen gehen"
        },
        19: {
            "measure": "sich einer Aqua-Fit anschliessen, wo andere, übergewichtigeMenschen auch teilnehmen"
        }
    }

    return patient_db, plan_db, measure_db

