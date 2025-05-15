import os
import dotenv
import pandas as pd
import prompts as prompts
from sqlalchemy import create_engine
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.tools import PythonREPLTool
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.agents import AgentExecutor, create_openai_functions_agent


dotenv.load_dotenv()

# Setup Database Connection and Utilities
db_file = "sqlite:///data/chinook.db"
db = SQLDatabase.from_uri(db_file)
engine = create_engine(db_file)

def get_schema():
    '''
    Get schema from database.
    '''
    return db.get_table_info()


def run_query(query):
    '''
    Execute query against database.
    '''
    return db.run(query)


def run_query_df(query):
    '''
    Execute and return database
    '''
    
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)

    return result


# Define Tools
@tool
def SQLTerminal(query):
    '''
    Run SQL Query.
    '''

    return run_query(query)


# Setup LLM
llm = ChatOpenAI(model="gpt-3.5-turbo-1106", 
                 temperature=os.environ['DEFAULT_TEMPATURE'])

vis_tools = [PythonREPLTool()]
vis_agent = create_openai_functions_agent(llm, 
                                          tools = vis_tools, 
                                          prompt = prompts.vis_chat_plot_template)

vis_executor = AgentExecutor(agent = vis_agent, 
                             tools = vis_tools)


@tool
def DataVisualizer(prompt, query):
    '''
    Visualize results of query.
    '''
    result_df =  run_query_df(query)

    result_text = vis_executor.invoke({"input": prompt,
                                       "columns": result_df.columns})['output']

    final_code = result_text.split('[FINAL_STREAMLIT_CODE]:')[-1].strip().strip('`').strip().strip('python')
    query_concat = ' '.join(query.split("\n"))

    with open('temp_vis_script.py', 'w') as outfile:
        python_lines = ['import pandas as pd',
                        'from sqlalchemy import create_engine',
                        f'engine = create_engine("{db_file}")',
                        'connection = engine.connect()',
                        f'result_df = pd.read_sql("{query_concat}", connection)',
                        'connection.close()',
                        final_code
                        ]
        
        for line in python_lines:
            outfile.write(line)
            outfile.write('\n\n')

    return final_code



agent_tools = [SQLTerminal, DataVisualizer, PythonREPLTool()]
tool_list = "\n".join([f"{tool.name}: {tool.description}" for tool in agent_tools])
agent = create_openai_functions_agent(llm, 
                                      tools=agent_tools, 
                                      prompt = prompts.meg_chat_plot_template.partial(tools = tool_list),
                                      )

main_agent_executor = AgentExecutor(agent = agent, 
                                    tools = agent_tools)        