from tabnanny import verbose
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain.memory import ConversationBufferMemory
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import run_query_tool, list_tables, describe_tables_tool
from tools.report import write_report_tool

load_dotenv()

tables = list_tables()

chat = ChatOpenAI()

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(
            content=f"You are an AI agent that has access to SQLite database which has the following tables. \n{tables}. \n"
            "Do not make assumptions about what tables exists or what columns exists. "
            "Instead use the 'describe_tables' and 'run_sqlite_query functions"
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(
            variable_name="agent_scratchpad",
        ),
    ]
)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
tools = [
    run_query_tool,
    describe_tables_tool,
    write_report_tool,
]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools,
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools,
    memory=memory,
)

agent_executor("How many orders are there? Write the summary to a file?")

agent_executor("repeat the exact same process for every user")
