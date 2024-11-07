# code to start the application

import streamlit as st
from frontend.main_app import render_main_app
# from frontend.main_app import clear_all_inputs
from frontend.chat_interface import render_chat_interface

st.set_page_config(layout="wide")

def main():
    st.title("Resume Analyzer")

    with st.sidebar:
        st.image("resume_analyzer_logo.png", width=150)

    # create two columns with a 3:2 ration for layout
    col1, col2 = st.columns([3,2])

    # if st.button("Clear all", key="clear_all"):
    #     clear_all_inputs()

    with col1:
        # Render the main app in the larger column
        render_main_app()

    with col2:
        # Render the chat interface in the smaller column
        render_chat_interface()


if __name__=="__main__":
    main()