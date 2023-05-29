from db_test import create_db
import json
from util import chatgpt_wrapper
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    # datefmt='%d-%b-%y %H:%M:%S'
                    )


def get_full_info(event):
    patient_db, plan_db, measure_db = create_db()
    event["patient"] = {k: patient_db[event["patient"]][k] for k in ["name", "age", "BMI"]}
    event["plan"] = plan_db[event["plan"]]["plan"]
    event["measure"] = measure_db[event["measure"]]["measure"]
    return event


def create_context_template(event):
    json_str = json.dumps(event)
    # print(json_str)
    sys_template = "You are a helpful assistant that convert the JSON format input into natural language. " \
                   "The {{'completed': false}} indicates that the patient did not take the measure as intended. " \
                   "The purpose of the output is to put it into a prompt for another large language model. " \
                   "The output should only be the conversation in natural language, nothing else. "
    result = chatgpt_wrapper(sys_template, json_str)
    return result


def reason_extractor(prompt_context, history):
    sys_template = f"I would like you to analyze a conversation history between a patient and a physician in order to " \
                   "identify the clearly described reason why the patient did not follow the prescribed measures. Remember, " \
                   "you are doing qualitative research, the common excuses or vague answers shouldn't be considered as " \
                   "the real reason. For example, an over-weight person who would not want to go swimming " \
                   "in public pools " \
                   "is afraid that his body would be judged by others in public pools, but he might not express this " \
                   f"clearly at first. Here is the context information of the conversation: {prompt_context}" \
                   "You will ONLY provide the output in JSON format, " \
                   "with a boolean indicating whether a reason was found and a 'reason' field containing a " \
                   "one-sentence summary of the patient's reason without any personal information, like name or age. " \
                   "Additionally, a 'confidence_score' from 0-100 indicates how confident you are with your answer. " \
                   "If no reason can " \
                   "be determined or the conversation history is not provided, " \
                   "the 'reason_found' value will be False and the 'reason' will be 'null', " \
                   "the 'confidence_score' will be 0"
    sys_template = sys_template + prompt_context
    history_str = "\n".join(history)
    result = chatgpt_wrapper(sys_template, history_str)
    try:
        output = json.loads(result)
    except json.JSONDecodeError:
        logging.info("The response was not valid JSON.")
        non_reason = """
        {
        "reason_found": false,
        "reason": null,
        "confidence_score": 0
        }
        """
        output = json.loads(non_reason)
    return output


def reason_finder(event):
    event = get_full_info(event)
    prompt_context = create_context_template(event)
    # print(prompt_context)
    sys_template = "The following is a friendly conversation between a physician and a patient. " \
                   "The physician is talkative and provides lots of specific details from its context." \
                   "The physician is trying to find out why the patient did not complete the planned measure. " \
                   "The first message from user input will be 'Hi', " \
                   "ignore this message and create a short greeting to get the conversation started. " \
                   "Here is the context information: "
    sys_template = sys_template + prompt_context
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(sys_template, validate_template=False),
        MessagesPlaceholder(variable_name="history"),
        HumanMessagePromptTemplate.from_template("{input}")
    ])
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
        streaming=True,
        callbacks=[StreamingStdOutCallbackHandler()]
    )
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(memory=memory, prompt=prompt, llm=llm)
    history = []
    while True:
        usr_prompt = input("\ntype input here: \n")
        history.append(f"patient: {usr_prompt}")
        logging.info(history)
        reason = reason_extractor(prompt_context, history)
        logging.info(reason)
        if reason["confidence_score"] < 95:
            resp = conversation(usr_prompt)
            history.append(f"physician: {resp['response']}")
        else:
            print(memory.json())
            return reason


if __name__ == '__main__':
    load_dotenv()
    event_json = {
        "patient": 12,
        "plan": 27,
        "measure": 18,
        "completed": False
    }
    reason_stat = reason_finder(event_json)
    print(reason_stat)
