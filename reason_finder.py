from db_test import create_db


def reason_finder(event):
    patient_db, plan_db, measure_db = create_db()
    print(event)



if __name__ == '__main__':
    event_json = {
        "patient": 12,
        "plan": 27,
        "measure": 18,
        "completed": False
    }
    reason_finder(event_json)