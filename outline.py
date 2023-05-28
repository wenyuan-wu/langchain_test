import json




def reason_finder():
    raise NotImplementedError


def measure_giver():
    raise NotImplementedError


if __name__ == '__main__':
    event_str = """
    {
    patient: 12,
    plan: 27,
    measure: 18,
    if_completed: false
    }
    """
    event_json = ""

    patient_db = {
        12: {
            "Name": "John",
            "BMI": 27,
            "Plan": 27,
        }
    }
