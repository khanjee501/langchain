import sqlite3
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


run_query_tool = Tool.from_function(
    name="run_sqlite_query",
    description="Run a sqlite query.",
    func=run_sqlite_query,
)
