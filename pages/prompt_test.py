import streamlit as st
from dotenv import load_dotenv
import os
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)


def page_init():
    # Load the OpenAI API key from the environment variable
    load_dotenv()
    # test that the API key exists
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")
    # setup streamlit page
    st.set_page_config(
        page_title="Prompt Engineering Playground",
        page_icon="🤖"
    )
    st.write("# Prompt Engineering Playground 🤖")
    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
    """
    )

def chat_sum(text):
    chat = ChatOpenAI(temperature=0)
    template = "You are a helpful assistant that summarize the content to around 15% of it's original size. The " \
               "original content is from transcript of lectures, the summarization should be descriptive, instead of " \
               "like speech."
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)
    human_template = "{text}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)
    chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

    # get a chat completion from the formatted messages
    messages = chat_prompt.format_prompt(text=text).to_messages()
    # print(messages)
    result = chat(messages)
    return result.content


def prompt_test():
    # Create Text Area Widget to enable user to enter texts
    article_text = st.text_area(":blue[Enter your scientific texts to summarize]")

    # Create Radio Buttons
    # output_size = st.radio(label=":blue[What kind of output do you want?]",
    #                        options=["To-The-Point", "Concise", "Detailed"]
    #                        )

    if st.button("Generate Summary", type='primary'):

        # Use GPT-3 to generate a summary of the article
        res = chat_sum(article_text)
        st.success(res)
        # Give user the option to download result
        st.download_button('Download result', res)
    else:
        st.warning("Not enough words to summarize!")


def main():
    page_init()
    prompt_test()


if __name__ == "__main__":
    main()
