import sqlite3
from pydantic.v1 import BaseModel
from typing import List
from langchain.tools import Tool


conn = sqlite3.connect("db.sqlite")


def list_tables():
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    rows = c.fetchall()
    return "\n".join(row[0] for row in rows if row[0] is not None)


# table context containing list of the tables in the databases which will be used inside SystemMessage
# so chatgpt can know the tbales inisde the database.
def run_sqlite_query(query):
    c = conn.cursor()
    # handling sqlite3 errors so gpt can try again with anew query as it is running query against
    # wrong tables. It sometimes can correct itself with this fix but frequently doesn't.
    try:
        c.execute(query)
        return c.fetchall()
    except sqlite3.OperationalError as e:
        return f"The following error occurred: {str(e)}"


def describe_tables(table_names):
    c = conn.cursor()
    tables = ", ".join("'" + table + "'" for table in table_names)
    rows = c.execute(
        f"SELECT sql FROM sqlite_master WHERE type='table' and name IN ({tables});"
    )
    return "\n".join(row[0] for row in rows if row[0] is not None)


# this is used so that the function code has meaningful json objects instead of onjects like __arg1
# now it will show query and of type string. So thi way gpt can understand the context better
class RunQueryArgsSchema(BaseModel):
    query: str


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
    args_schema=RunQueryArgsSchema,
)


class DescribeTablesArgsSchema(BaseModel):
    table_names: List[str]


# describe tables tools to return the schema of the tables of the db
describe_tables_tool = Tool.from_function(
    name="describe_tables",
    description="Given a list of table names, return the schema of those tables",
    func=describe_tables,
    args_schema=DescribeTablesArgsSchema,
)
