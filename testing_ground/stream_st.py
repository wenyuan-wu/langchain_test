# import streamlit as st
# from dotenv import load_dotenv
# from util import dummy_chatbot
#
#
# def page_init():
#     st.set_page_config(
#         page_title="Testing Ground",
#         page_icon="🤖"
#     )
#     st.write("# Testing Ground 🤖")
#     st.markdown("Caution. Construction Site")
#
#     # if 'usr_input' not in st.session_state:
#     #     st.session_state.usr_input = 'value'
#     history = []
#     st.text_input("Your name", key="name")
#     while True:
#         # st.write(st.session_state.usr_input)
#
#         history.append(st.session_state.name)
#         # This exists now:
#         st.write(st.session_state.name)
#         st.write(history)
#
#
# if __name__ == '__main__':
#     page_init()

from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text="", display_method='markdown'):
        self.container = container
        self.text = initial_text
        self.display_method = display_method

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token + "/"
        display_function = getattr(self.container, self.display_method, None)
        if display_function is not None:
            display_function(self.text)
        else:
            raise ValueError(f"Invalid display_method: {self.display_method}")

query = st.text_input("input your query", value="Tell me a joke")
ask_button = st.button("ask")

st.markdown("### streaming box")
chat_box = st.empty()
stream_handler = StreamHandler(chat_box, display_method='write')
chat = ChatOpenAI(max_tokens=25, streaming=True, callbacks=[stream_handler])

st.markdown("### together box")

if query and ask_button:
    response = chat([HumanMessage(content=query)])
    llm_response = response.content
    st.markdown(llm_response)