from db_init import create_db
import logging

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        # datefmt='%d-%b-%y %H:%M:%S'
                        )
    database_folder = "database"

    # create measure database
    prompt_db_name = "prompt.db"
    prompt_table_name = "prompts"
    prompt_table_col = """
    id INTEGER PRIMARY KEY,
    type TEXT NOT NULL,
    language TEXT NOT NULL,
    prompt_sum TEXT NOT NULL,
    variable TEXT,
    prompt_text TEXT NOT NULL
    """
    prompt_data_list = [
        {
            "id": 1,
            "type": "full",
            "language": "en",
            "prompt_sum": "JSON to natural language",
            "prompt_text": "You are a helpful assistant that convert the JSON format input into natural language. "
                           "The 'completed': false indicates that the patient did not take the measure as intended. "
                           "The purpose of the output is to put it into a prompt for another large language model. "
                           "The output should only be the conversation in natural language, nothing else. "
        },
        {
            "id": 2,
            "type": "full",
            "language": "en",
            "prompt_sum": "JSON to natural language v2",
            "prompt_text": "You are a helpful assistant that convert the JSON format input into natural language. "
                           "The 'completed' property indicates if the patient did take the measure as intended or did "
                           "not. "
                           "The purpose of the output is to put it into a prompt for another large language model. "
                           "The output should only be the conversation in natural language, nothing else. "
        },
        {
            "id": 3,
            "type": "full",
            "language": "en",
            "prompt_sum": "reason extractor",
            "variable": "prompt_context",
            "prompt_text": "I would like you to analyze a conversation history between a patient and a physician in "
                           "order to identify the clearly described reason "
                           "why the patient did not follow the prescribed measures. "
                           "Remember, you are doing qualitative research "
                           "the common excuses or vague answers shouldn't be considered as the real reason. "
                           "For example, an over-weight person who would not want to go swimming in public pools "
                           "is afraid that his body would be judged by others in public pools, "
                           "but he might not express this clearly at first. "
                           "Here is the context information of the conversation: {prompt_context}"
                           "You will ONLY provide the output in JSON format, "
                           "with a boolean indicating whether a reason was found and a 'reason' field containing a "
                           "one-sentence summary of the patient's reason without any personal information, "
                           "like name or age. "
                           "Additionally, a 'confidence_score' from 0-100 indicates "
                           "how confident you are with your answer. "
                           "If no reason can be determined or the conversation history is not provided, "
                           "the 'reason_found' value will be False and the 'reason' will be 'null', "
                           "the 'confidence_score' will be 0"
        },
        {
            "id": 4,
            "type": "full",
            "language": "en",
            "prompt_sum": "reason finder conversation holder",
            "variable": "prompt_context",
            "prompt_text": "The following is a friendly conversation between a physician and a patient. "
                           "The physician is talkative and provides lots of specific details from its context."
                           "The physician is trying to find out why the patient did not complete the planned measure. "
                           "The first message from user input will be 'Hi', "
                           "ignore this message and create a short greeting to get the conversation started. "
                           "Here is the context information: {prompt_context}"
        },
    ]
    create_db(database_folder, prompt_db_name, prompt_table_name, prompt_table_col, prompt_data_list)
