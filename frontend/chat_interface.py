# check for retriever and search types "mmr" maximum marginal retriever
# check techniques like stuffing of documenst

import streamlit as st
from backend.analysis import llm
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory


def render_chat_interface():
    st.header("Let me answer your question. Hit me up")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "vector_store" in st.session_state:
        retriever = st.session_state.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={"k": 3},  # top 3 chunks
        )

        # chat logic setup for contextualizing user questions
        contextualize_q_system_prompt = (
            "Given a chat history and the latest user question "
            "which might reference context in the chat history, "
            "formulate a standalone question which can be understood "
            "without the chat history. DO NOT answer the question, "
            "just reformulate it if needed and otherwise return it as is."
        )
        # creating a prompt template for contextualizing questions
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        # creating a history-aware retriever with the lang model
        history_aware_retriever = create_history_aware_retriever(
            llm, retriever, contextualize_q_prompt
        )

        # system prompt for answering questions
        system_prompt = (
            "You are an assistant for question-answering tasks."
            "Use the following pieces of retrieved context to answer "
            "the question. If you don't know the answer, sa that you don't know"
            "Use three sentences maximum and keep the answer concise"
            "\n\n"
            "{context}"
        )
        # creating a prompt template for question-answering
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # setting up the question-answering chain
        question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
        retriever_chain = create_retrieval_chain(
            history_aware_retriever, question_answer_chain
        )

        # chat history management using a dictionary
        store = {}
        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            """
            Maintaining session of each chain with session id
            """
            if session_id not in store:
                store[session_id] = ChatMessageHistory()
            return store[session_id]

        # create a runnable chain with message history
        conversational_retriever_chain = RunnableWithMessageHistory(
            retriever_chain,
            get_session_history=get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer",
        )
        # create a container for messages with input space
        chat_container = st.container()

        # # Add space at the bottom to prevent messages from being hidden behind input
        # st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)

        # input box
        prompt = st.chat_input("Ask about the resume")
        print(f"prompt:{prompt}")

        # display messages in the container
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with chat_container:
                with st.chat_message("user"):
                    st.markdown(prompt)  # display user imput

                with st.chat_message("assistant"):
                    # prepare input data for the convesational chain
                    input_data = {
                        "input": prompt,
                        "chat_history": st.session_state.messages,
                    }

                    response = conversational_retriever_chain.invoke(
                        input_data,
                        config={
                            "configurable": {"session_id": "abc123"},
                        },
                    )
                    print(f"response from llm:{response}")
                    answer_text = response["answer"]  # extracting assistant response
                    st.markdown(answer_text)

            st.session_state.messages.append(
                {"role": "assistant", "content": answer_text}
            )

            # force a rerun to update the chat immediately
            st.rerun()

        else:
            st.info("Please upload a resume and analyze it to start chatting.")

