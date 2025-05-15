import streamlit as st
from prompts import ai_intro_message_to_user
from agents import main_agent_executor, get_schema
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.callbacks import StreamlitCallbackHandler
import hashlib

def file_hash(file_path):
    """
    Calculates the SHA-256 hash of a file.

    :param file_path: Path to the file whose hash is to be calculated.
    :return: The SHA-256 hash of the file's content.
    """
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print("File not found.")
        return None


last_py_hash = file_hash('temp_vis_script.py')

st.title("Meg: LLM Data Analyst")

def execute_python_file(file_path):
   try:
      with open(file_path, 'r') as file:
         python_code = file.read()
         exec(python_code)
   except FileNotFoundError:
      print(f"Error: The file '{file_path}' does not exist.")

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
        st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        llm_result = main_agent_executor.invoke({"input": prompt,
                                                 "chat_history": st.session_state.messages,
                                                 "schema": get_schema()},
                                                 {"callbacks": [st_callback]})
        
        response = st.write(llm_result['output'])

        if file_hash('temp_vis_script.py') != last_py_hash:
            last_py_hash = file_hash('temp_vis_script.py')
            execute_python_file('temp_vis_script.py')

        st.session_state.messages.append(AIMessage(content = llm_result['output']))