import streamlit as st
from prompts import ai_intro_message_to_user
from agents import agent_executor, get_schema
from langchain_core.messages import AIMessage, HumanMessage

st.title("Meg: LLM Data Analyst")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.session_state["messages"] += [AIMessage(content = ai_intro_message_to_user)]


# Display chat messages from history on each rendering
for message in st.session_state.messages:

    with st.chat_message(message.type):
        st.markdown(message.content)


# Drive User Acceptance
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append(HumanMessage(content = prompt))

    # Display user message in chat message container
    with st.chat_message("human"):
        st.markdown(prompt)

    # Respond
    with st.chat_message("ai"):

        llm_result = agent_executor.invoke({"input": prompt,
                                            "chat_history": st.session_state.messages,
                                            "schema": get_schema()})
        
        response = st.write(llm_result['output'])
        st.session_state.messages.append(AIMessage(content = llm_result['output']))