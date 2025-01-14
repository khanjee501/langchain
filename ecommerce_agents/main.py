from tabnanny import verbose
from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
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
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(
            variable_name="agent_scratchpad",
        ),
    ]
)

tool = [
    run_query_tool,
    describe_tables_tool,
    write_report_tool,
]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tool,
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tool,
)

agent_executor("summarize top 5 products. Write the summary to a file?")
