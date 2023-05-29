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
                   "The 'completed': False indicates that the patient did not take the measure as intended. " \
                   "The purpose of the output is to put it into a prompt for another large language model. " \
                   "The output should only be the conversation in natural language, nothing else. "
    result = chatgpt_wrapper(sys_template, json_str)
    return result


def reason_extractor(prompt_context, history):
    # sys_template = "You are a reason finder that try to find out the extract reason about the patient who " \
    #                "did not take the measure as intended based on the conversation history of the patient " \
    #                "and the physician. " \
    #                "You need to find the real reason hidden inside the patient's words, not just some common excuses." \
    #                "If you don't find out the reason based on the conversation history, provide a negative answer " \
    #                "and the your thought. " \
    #                "If you find out the reason based on the conversation history, return a true value " \
    #                "and extract the reason of the patient into one sentence, " \
    #                "but remove the patient's personal information. " \
    #                "The user input will be the conversation history. " \
    #                "Here is the context information: "
    # sys_template = sys_template + prompt_context
    # response_schemas = [
    #     ResponseSchema(name="reason_found", description="true or false value to indicate if the model find the reason"),
    #     ResponseSchema(name="reason", description="patient's reason, should be a sentence.")
    # ]
    # output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    # format_instructions = output_parser.get_format_instructions()
    # llm = ChatOpenAI(
    #     model_name="gpt-3.5-turbo",
    #     temperature=0,
    # )
    # system_message_prompt = SystemMessagePromptTemplate.from_template(sys_template)
    # human_template = "{text}"
    # human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    # chat_prompt = ChatPromptTemplate(
    #     messages=[system_message_prompt, human_message_prompt],
    #     input_variables=["text"],
    #     partial_variables={"format_instructions": format_instructions}
    # )
    # history_str = "\n".join(history[1:])
    # # get a chat completion from the formatted messages
    # messages = chat_prompt.format_prompt(text=history_str).to_messages()
    # result = llm(messages)
    # return output_parser.parse(result.content)
    sys_template = "You are a reason finder that try to find out the extract reason about the patient who " \
                   "did not take the measure as intended based on the conversation history of the patient " \
                   "and the physician. " \
                   "You need to find the real reason hidden inside the patient's words, " \
                   "not just some common excuses. " \
                   "Your output should be strictly in JSON format, " \
                   "CAPITALIZED WORD is placeholder, here is the JSON schema:\n" \
                   "'reason_found': TRUE_OR_FALSE, 'reason': REASON \n" \
                   "If you don't find out the reason based on the conversation history, " \
                   "or the conversation history is not provided, " \
                   "the 'reason_found' value should be false, and 'reason' should be 'null'. " \
                   "If you find out the reason based on the conversation history, " \
                   "the 'reason_found' value should be true, " \
                   "and 'reason' should be one-sentence summary patient's reason " \
                   "without patient's personal information " \
                   "The user input will be the conversation history. " \
                   "Here is the context information: "
    sys_template = sys_template + prompt_context
    history_str = "\n".join(history)
    result = chatgpt_wrapper(sys_template, history_str)

    sys_template_new = "You take plain text as input and only JSON format string as output. " \
                       "Your output should be strictly in JSON format, " \
                       "here is the JSON schema:\n" \
                       "'reason_found': TRUE_OR_FALSE, 'reason': REASON \n" \
                       "If the input shows the reason is not find,  " \
                       "or the conversation history is not provided, " \
                       "the 'reason_found' value should be false, and 'reason' should be 'null'. " \
                       "If the reason is found out, " \
                       "the 'reason_found' value should be true, " \
                       "and 'reason' should be one-sentence summary patient's reason " \
                       "without patient's personal information. "
    result_new = chatgpt_wrapper(sys_template_new, result)
    return result_new
    # # print(result)
    # reason = {
    #     "reason_found": False,
    #     "reason": "null"
    # }
    # return reason


def reason_finder(event):
    event = get_full_info(event)
    prompt_context = create_context_template(event)
    sys_template = "The following is a friendly conversation between a physician and a patient. " \
                   "The physician is talkative and provides lots of specific details from its context." \
                   "The physician is trying to find out why the patient did not complete the planned measure. " \
                   "The first message from user input will be 'Hi', " \
                   "ignore this message and create a short greeting to get the conversation started. " \
                   "Here is the context information: "
    sys_template = sys_template + prompt_context
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(sys_template),
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
        print(history)
        reason = reason_extractor(prompt_context, history)
        print(reason)
        if not reason["reason_found"]:
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
