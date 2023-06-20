from db_init import create_db, SQLiteUtility
import logging
import os
import json

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        # datefmt='%d-%b-%y %H:%M:%S'
                        )
    database_folder = "database"
    prompt_db_path = os.path.join(database_folder, "prompt.db")
    prompt_db = SQLiteUtility(prompt_db_path)

    # add new prompts
    # new_data_list = [
    #     {
    #         "id": 5,
    #         "type": "full",
    #         "language": "en",
    #         "prompt_sum": "test prompt",
    #         "prompt_text": "Answer the question based on the context below. If the "
    #                        "question cannot be answered using the information provided answer "
    #                        "with 'I don't know'."
    #     },
    # ]
    #

    # prompt_db.insert_rows("prompts", new_data_list)
    update_data_list = [
        {
            "type": "full",
            "language": "en",
            "prompt_sum": "measure giver conversation holder",
            "variable": "prompt_context",
            "prompt_text": "The following is a friendly conversation between a physician and a patient. The physician "
                           "is talkative and provides lots of specific details from its context.The physician is "
                           "trying to give the patient a new measure based on the reason that the patient "
                           "does not conduct the current reason. "
                           "Here is the context information: {prompt_context}\n"
                           "The first input will be the previous conversation history. "
                           "Continue the conversation based on the provided conversation history "
                           "and only output what the physician would say next."
        },
    ]
    prompt_db.update_rows("prompts", update_data_list, "id=5")
    prompt_db.close_connection()
