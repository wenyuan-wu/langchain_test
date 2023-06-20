import sqlite3
from sqlite3 import Error
import json
import os
import logging


class SQLiteUtility:
    """
    A helper class to interact with an SQLite database.
    """

    def __init__(self, db_name):
        self.conn = None
        self.create_connection(db_name)

    def create_connection(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            logging.info(f'Successful connection with {db_name}')
        except Error as e:
            logging.error(e)

    def close_connection(self):
        if self.conn:
            self.conn.close()
            logging.info('Connection closed')

    def create_table(self, table_name, table_col):
        create_table_sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({table_col});'
        try:
            c = self.conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            logging.error(e)

    def drop_table(self, table_name):
        drop_table_sql = f'DROP TABLE IF EXISTS {table_name};'
        try:
            c = self.conn.cursor()
            c.execute(drop_table_sql)
            self.conn.commit()
            logging.info(f'Dropped table {table_name} successfully.')
        except Error as e:
            logging.error(e)

    def insert_rows(self, table_name, data_dict_list):
        for data_dict in data_dict_list:
            columns = ', '.join(data_dict.keys())
            placeholders = ', '.join('?' * len(data_dict))
            insert_sql = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders});'
            try:
                c = self.conn.cursor()
                c.execute(insert_sql, tuple(data_dict.values()))
                self.conn.commit()
            except Error as e:
                logging.error(e)

    def update_rows(self, table_name, data_dict_list, condition):
        for data_dict in data_dict_list:
            set_clause = ', '.join([f'{key} = ?' for key in data_dict])
            update_sql = f'UPDATE {table_name} SET {set_clause} WHERE {condition}'
            try:
                c = self.conn.cursor()
                c.execute(update_sql, tuple(data_dict.values()))
                self.conn.commit()
            except Error as e:
                logging.error(e)

    def delete_rows(self, table_name, condition):
        delete_sql = f'DELETE FROM {table_name} WHERE {condition};'
        try:
            c = self.conn.cursor()
            c.execute(delete_sql)
            self.conn.commit()
            logging.info('Rows deleted successfully.')
        except Error as e:
            logging.error(e)

    def select_rows(self, table_name, condition=None, if_json=False):
        select_sql = f"SELECT * FROM {table_name}"
        if condition:
            select_sql = f"SELECT * FROM {table_name} WHERE {condition}"
        cur = self.conn.cursor()
        cur.execute(select_sql)
        rows = cur.fetchall()
        if if_json:
            col_names = [description[0] for description in cur.description]
            res_data = [dict(zip(col_names, row)) for row in rows]
            # json_data = json.dumps(res_data, indent=4)
            return res_data
        else:
            return rows

    def execute_query(self, query):
        cur = self.conn.cursor()
        cur.execute(query)
        self.conn.commit()

    def list_table(self):
        cur = self.conn.cursor()
        res = cur.execute("SELECT name FROM sqlite_master")
        print(res.fetchall())


def create_db(db_folder, db_name, table_name, table_col, data_list):
    db_path = os.path.join(db_folder, db_name)
    db = SQLiteUtility(db_path)
    db.create_table(table_name, table_col)
    db.insert_rows(table_name, data_list)
    db.close_connection()


def query_by_id(db_path, table_name, key_id):
    db = SQLiteUtility(db_path)
    res_json = db.select_rows(table_name, condition=f"id={key_id}", if_json=True)
    db.close_connection()
    return res_json


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


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO,
                        # datefmt='%d-%b-%y %H:%M:%S'
                        )
    database_folder = "database"

    # create patient database
    patient_db_name = "patient.db"
    patient_table_name = "patients"
    patient_table_col = """
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    BMI INTEGER NOT NULL,
    plan INTEGER NOT NULL
    """
    patient_data_list = [
        {
            "id": 12,
            "name": "Daniel",
            "age": 34,
            "BMI": 27,
            "plan": 27
        },
        {
            "id": 13,
            "name": "Emma",
            "age": 45,
            "BMI": 28,
            "plan": 28
        },
    ]
    # create_db(database_folder, patient_db_name, patient_table_name, patient_table_col, patient_data_list)

    # create plan database
    plan_db_name = "plan.db"
    plan_table_name = "plans"
    plan_table_col = """
    id INTEGER PRIMARY KEY,
    plan_sum TEXT NOT NULL,
    plan_text TEXT NOT NULL
    """
    plan_data_list = [
        {
            "id": 27,
            "plan_sum": "Intervallfasten und Schwimmen planen",
            "plan_text": "Intervall-Fasten mit Essfenster morgens bis 13:00, Schwimmen 30 Minuten/500 Meter Mo/Do/Sa "
                         "je Abends"
        },
        {
            "id": 28,
            "plan_sum": "Periodisches Fasten und Laufen planen",
            "plan_text": "Periodisches Fasten mit Essperiode bis 14:00 Uhr, Laufen 45 Minuten/5 Kilometer Di/Fr/So "
                         "jeweils am Abend"
        },
    ]
    # create_db(database_folder, plan_db_name, plan_table_name, plan_table_col, plan_data_list)

    # create measure database
    measure_db_name = "measure.db"
    measure_table_name = "measures"
    measure_table_col = """
    id INTEGER PRIMARY KEY,
    measure_sum TEXT NOT NULL,
    measure_text TEXT NOT NULL
    """
    measure_data_list = [
        {
            "id": 18,
            "measure_sum": "Do-Abend schwimmen",
            "measure_text": "Am Do-Abend schwimmen gehen"
        },
        {
            "id": 19,
            "measure_sum": "Aqua-Fit anschliessen",
            "measure_text": "sich einer Aqua-Fit anschliessen, wo andere, übergewichtigeMenschen auch teilnehmen"
        },
    ]
    # create_db(database_folder, measure_db_name, measure_table_name, measure_table_col, measure_data_list)

    # create prompt database
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
    # create_db(database_folder, prompt_db_name, prompt_table_name, prompt_table_col, prompt_data_list)

    # create conversation database
    conversation_db_name = "conversation.db"
    conversation_table_name = "conversations"
    conversation_table_col = """
    id TEXT PRIMARY KEY,
    usr_id INTEGER NOT NULL,
    time TEXT NOT NULL,
    type TEXT,
    language TEXT NOT NULL,
    conversation_sum TEXT NOT NULL,
    conversation_text TEXT NOT NULL
    """
    chat_history = ['patient: Hi', 'physician: Hello! How can I assist you today?', 'patient: I am not feeling well.']
    chat_history_json = json.dumps(chat_history)
    conversation_data_list = [
        {
            "id": "6a9dafea-d77a-404a-a00b-69e3cb0bc274",
            "usr_id": 12,
            "time": "2023-06-19 18:57:08",
            "type": "reason finder",
            "language": "en",
            "conversation_sum": "test conversation history",
            "conversation_text": chat_history_json
        },
    ]
    # create_db(database_folder,
    #           conversation_db_name,
    #           conversation_table_name,
    #           conversation_table_col,
    #           conversation_data_list
    #           )
