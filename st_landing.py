import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="AI Toolkit @ IfI",
    page_icon="🖥",
)

st.write("# Welcome to AI Toolkit @ IfI 🖥")

st.sidebar.success("Select a tool above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
"""
)

html_string = """<script type="text/javascript" src="https://ssl.gstatic.com/trends_nrtr/3349_RC01/embed_loader.js
"></script> <script type="text/javascript"> trends.embed.renderExploreWidget( "TIMESERIES", {"comparisonItem":[{
"keyword":"prompt engineering","geo":"","time":"today 12-m"}],"category":0,"property":""}, 
{"exploreQuery":"q=prompt%20engineering&hl=en&date=today 12-m",
"guestPath":"https://trends.google.com:443/trends/embed/"}); </script>"""

components.html(html_string, height=500)
