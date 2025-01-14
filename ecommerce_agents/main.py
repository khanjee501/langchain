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

load_dotenv()

tables = list_tables()

chat = ChatOpenAI()

prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(
            content=f"You are an AI agent that has access to SQLite database which has the following tables. \n{tables}"
        ),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(
            variable_name="agent_scratchpad",
        ),
    ]
)

tool = [run_query_tool, describe_tables_tool]

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

agent_executor("How many users have provided a shipping address in table addresses?")
