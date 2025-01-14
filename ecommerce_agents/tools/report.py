from fileinput import filename
from langchain.tools import StructuredTool
from pydantic.v1 import BaseModel


# write report tool function to write the response of the gpt into any kind of file (html, pdf, .txt etx)
def write_report(filename, html):
    with open(filename, "w") as f:
        f.write(html)


class WriteReportArgsSchema(BaseModel):
    filename: str
    html: str


write_report_tool = StructuredTool.from_function(
    name="write_report",
    description="write an HTML file to disk. Use this tool to write a report when someone asks for it",
    func=write_report,
    args_schema=WriteReportArgsSchema,
)
