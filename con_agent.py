from reason_finder import reason_finder
from measure_giver import measure_giver


def run_agent(event):
    reason = reason_finder(event)
    measure_giver(reason)


if __name__ == '__main__':

    event_json = {
        "patient": 12,
        "plan": 27,
        "measure": 18,
        "completed": False
    }

    run_agent(event_json)
