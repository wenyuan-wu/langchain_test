from dotenv import load_dotenv
from reason_finder import get_full_info, reason_extractor
from db_init import query_by_id, SQLiteUtility
import os
from util import chatgpt_wrapper
import json
import uuid
from datetime import datetime


def record_chat_db(db_path, chat_id, usr_id, chat_time, chat_type, language, chat_sum, chat_list):
    db = SQLiteUtility(db_path)
    data_list = [
        {
            "id": chat_id,
            "usr_id": usr_id,
            "time": chat_time,
            "type": chat_type,
            "language": language,
            "conversation_sum": chat_sum,
            "conversation_text": json.dumps(chat_list)
        },
    ]
    db.insert_rows("conversations", data_list)
    db.close_connection()


def update_chat_db(db_path, chat_id, chat_list):
    db = SQLiteUtility(db_path)
    data_list = [
        {
            "conversation_text": json.dumps(chat_list)
        },
    ]
    db.update_rows("conversations", data_list, f"id='{chat_id}'")
    db.close_connection()


database_folder = "database"
chat_db_path = os.path.join(database_folder, "conversation.db")
usr_id = 12
first_chat = []
second_chat = ['patient: Hi']
third_chat = ['patient: Hi', 'physician: Hello! How can I assist you today?']
forth_chat = ['patient: Hi', 'physician: Hello! How can I assist you today?', 'patient: I am not feeling well.']

chat_id = str(uuid.uuid4())  # Generates a unique ID
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

chat_type = "reason finder"
language = "en"
conversation_sum = f"reason finder at {now} with {usr_id}"

# record_chat_db(chat_db_path, chat_id, usr_id, now, chat_type, language, conversation_sum, first_chat)

update_chat_db(chat_db_path, "b8157233-82ba-4318-ad03-9b731bb2089c", forth_chat)



