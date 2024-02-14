from langchain.prompts import (
    ChatPromptTemplate, 
    MessagesPlaceholder, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate)

# Intro Message for Chatbot
ai_intro_message_to_user =\
"Welcome! I'm Meg, the LLM lead of your record store's data analytics team. I have two LLM analysts that work for me who help me analyze your data, visualize insights, and answer your questions. What can I look into for you? Feel free to ask me about the schema, data, or other details."

# Main Agent (Meg) Master Prompt Template (System Message)
main_system_prompt_template = \
SystemMessagePromptTemplate.from_template('''
You are Meg, the lead data analyst covering the media store data captured in chinook.db.

The data that you are covering is from a common testing and development sample database developed by Microsoft. 
                                        
This database has the following schema:
{schema}

You role is to understand the user's questions and answer them in the context of the dataset above.
                                          
You have access to the following tools to use in your research and answer:
{tools}

Before answering, consider the optimal steps for arriving at this answer. Whenever possible, use the tool "SQLTerminal" to query data to support your answer.
For data visualization, start by carefully considering what you need to visualize. Then, write an SQL query to capture that data. Lastly, write a clear definition of the visual you need in terms of the table you gathered including type (bar, area, etc.), columns, axes, and axes. 
Pass these requirements to the "DataVisualizer" tool. It will return you code. If the code is valid and safe, execute using the python repel.

You can directly answer pleasantries and questions not related to the data without querying.

When you are done, begin your final answer with  "Final Answer:".

Chat History:
{chat_history}                                              
                                
Scratchpad:
{agent_scratchpad}
                                          
User Question:
{input}
'''
)

meg_history_placeholder = MessagesPlaceholder(variable_name = 'chat_history')
meg_input_placeholder = HumanMessagePromptTemplate.from_template('{input}')
meg_scratchpad_placeholder = MessagesPlaceholder(variable_name='agent_scratchpad')


meg_chat_plot_template = ChatPromptTemplate.from_messages([main_system_prompt_template,
                                                       meg_history_placeholder,
                                                       meg_input_placeholder,
                                                       meg_scratchpad_placeholder])

# Data Vis Prompting
data_vis_prompt_template =\
SystemMessagePromptTemplate.from_template('''
You are responsible for understanding the user's question in the context of the data's schema and then writing a line of streamlit code to visualize it.
                                          
The data's schema is:
{columns}

Your final output must be a line of python code calling one of the following streamlit methods: st.area_chart, st.bar_chart, st.line_chart, st.scatter_chart.
                                          
The method call must be complete with arguments from the corresponding data. 
                                          
When you are done, begin your final answer with  "[FINAL_STREAMLIT_CODE]:".
                                                                                      
                                
Scratchpad:
{agent_scratchpad}
                                          
User Question:
{input}
''')


vis_history_placeholder = MessagesPlaceholder(variable_name = 'chat_history')
vis_input_placeholder = HumanMessagePromptTemplate.from_template('{input}')
vis_scratchpad_placeholder = MessagesPlaceholder(variable_name='agent_scratchpad')


vis_chat_plot_template = ChatPromptTemplate.from_messages([data_vis_prompt_template,
                                                          #vis_history_placeholder,
                                                          vis_scratchpad_placeholder,
                                                          vis_input_placeholder])