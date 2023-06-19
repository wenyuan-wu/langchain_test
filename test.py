from dotenv import load_dotenv
from reason_finder import get_full_info, reason_extractor
from db_init import query_by_id
import os
from util import chatgpt_wrapper
import json

# history = ['patient: Hi', 'physician: Hello! How can I assist you today?']
# contex = """The patient's name is Daniel and he is 34 years old with a BMI of 27. His plan includes intermittent
# fasting with an eating window until 1 pm and swimming for 30 minutes or 500 meters on Monday, Thursday, and Saturday
# evenings. The measure he was supposed to take was to go swimming on Thursday evening, but the {'completed': false}
# indicates that he did not do it as intended."""
#
# reason = reason_extractor(contex, history)
# print(reason)

event_json = {
    "patient": 12,
    "plan": 27,
    "measure": 18,
    "completed": False
}

database_folder = "database"
patient_db_path = os.path.join(database_folder, "patient.db")
res_json = query_by_id(patient_db_path, "patients", event_json["patient"])
print(res_json)

out_json = get_full_info(event_json)
print(out_json)


def create_context_template(event):
    json_str = json.dumps(event)
    # print(json_str)
    sys_template = "You are a helpful assistant that convert the JSON format input into natural language. " \
                   "The 'completed': false indicates that the patient did not take the measure as intended. " \
                   "The purpose of the output is to put it into a prompt for another large language model. " \
                   "The output should only be the conversation in natural language, nothing else. "
    result = chatgpt_wrapper(sys_template, json_str)
    return result


# sys_template = "You are a helpful assistant that convert the JSON format input into natural language. " \
#                "The 'completed' status indicates if the patient did take the measure as intended or did not. " \
#                "The purpose of the output is to put it into a prompt for another large language model. " \
#                "The output should only be the conversation in natural language, nothing else. "

prompt_db_path = os.path.join(database_folder, "prompt.db")
sys_temp = query_by_id(prompt_db_path, "prompts", 2)[0]["prompt_text"]


# gpt_result = chatgpt_wrapper(sys_temp, out_json)
# print(gpt_result)

