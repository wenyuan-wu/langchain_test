import streamlit as st
from dotenv import load_dotenv
import os


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


def prompt_test():



def main():
    page_init()


if __name__ == "__main__":
    main()
